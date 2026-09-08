#!/usr/bin/env python3.12
"""Bounded public-puzzle key probes, not a claim of exhaustive cryptanalysis.

Run in /home/user/tools/devpc-python (PyCryptodome 3.23.0).
Only candidate plaintext passing UTF-8 and >=95% printable-character checks is
retained. Padding alone is deliberately not accepted as a successful decryption.
"""
import argparse
import base64
import hashlib
import json
from collections import Counter
from pathlib import Path

from Crypto.Cipher import AES, ARC4, Blowfish, DES
from Crypto.Util.Padding import pad, unpad

PASSWORDS = ['qtecqot', 'Qtecqot', 'QTECQOT', 'quetzalcoatl', 'Quetzalcoatl',
             'QUETZALCOATL', 'Quetzalcóatl', 'Quetzalcōātl', 'quetzalcouatl',
             'quetzalcohuatl', 'ivan0135', 'Ivan0135', '0135', 'serpo', 'SERPO',
             'skinnybob', 'Skinny Bob', 'slimtim', 'Slim Tim', 'mantis',
             'red pill', 'redpill', 'blue pill', 'bluepill', 'disclosure',
             'deadmansswitch', "Deadman's Switch", '¯\\_(ツ)_/¯',
             'QTE C QOT', 'qtecqot.com']


def key_variants(p):
    variants = {'md5': hashlib.md5(p).digest(), 'sha256': hashlib.sha256(p).digest(),
                'md5-hex': hashlib.md5(p).hexdigest().encode()}
    for n in [16, 24, 32]:
        variants[f'zero-pad-{n}'] = p[:n].ljust(n, b'\0')
        variants[f'repeat-{n}'] = (p * (n // len(p) + 1))[:n]
        variants[f'sha512-first-{n}'] = hashlib.sha512(p).digest()[:n]
    variants['sha1-first16'] = hashlib.sha1(p).digest()[:16]
    variants['sha256-first16'] = hashlib.sha256(p).digest()[:16]
    return variants


def evp(p, digest, salt=b'', length=48):
    result = last = b''
    while len(result) < length:
        last = hashlib.new(digest, last + p + salt).digest()
        result += last
    return result[:length]


def readable(data):
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return False
    return (len(text) >= 16 and sum(c.isprintable() or c in '\n\r\t' for c in text)
            / len(text) >= .95)


def scan(blob, passwords, include_pbkdf=True):
    counts = Counter()
    hits = []

    def check(label, password, data, authenticated=False):
        counts['plaintext_candidates'] += 1
        variants = [data]
        for size in [8, 16]:
            try:
                variants.append(unpad(data, size))
                counts['padding_valid'] += 1
            except ValueError:
                pass
        if authenticated or any(readable(v) for v in variants):
            hits.append({'recipe': label, 'password': password, 'authenticated': authenticated,
                         'plaintext_hex': data.hex()})

    for password in passwords:
        p = password.encode('utf-8')
        check('repeating-XOR', password, bytes(x ^ p[i % len(p)] for i, x in enumerate(blob)))
        for kn, key in key_variants(p).items():
            check('RC4/' + kn, password, ARC4.new(key).decrypt(blob))
            check('AES-ECB/' + kn, password, AES.new(key, AES.MODE_ECB).decrypt(blob))
            for ivn, iv, ct in [('zero', bytes(16), blob), ('key-first16', key[:16], blob),
                                ('prefix16', blob[:16], blob[16:])]:
                for mn, mode, kwargs in [('CBC', AES.MODE_CBC, {}), ('CFB8', AES.MODE_CFB, {}),
                                         ('CFB128', AES.MODE_CFB, {'segment_size': 128}),
                                         ('OFB', AES.MODE_OFB, {})]:
                    out = AES.new(key, mode, iv=iv, **kwargs).decrypt(ct)
                    check(f'AES-{mn}/{kn}/iv={ivn}', password, out)
            for nn in [12, 16]:
                for tag_position in ['last', 'after-nonce']:
                    nonce = blob[:nn]
                    ct, tag = ((blob[nn:-16], blob[-16:]) if tag_position == 'last'
                               else (blob[nn+16:], blob[nn:nn+16]))
                    for mn, mode in [('GCM', AES.MODE_GCM), ('EAX', AES.MODE_EAX)]:
                        counts['authenticated_attempts'] += 1
                        try:
                            out = AES.new(key, mode, nonce=nonce).decrypt_and_verify(ct, tag)
                        except ValueError:
                            continue
                        check(f'AES-{mn}/{kn}/nonce{nn}/tag={tag_position}', password, out, True)
        check('RC4/raw-UTF8', password, ARC4.new(p).decrypt(blob))
        for cn, cipher, key in [('DES', DES, p[:8].ljust(8, b'\0')),
                                ('Blowfish', Blowfish, p.ljust(4, b'\0'))]:
            check(cn + '-ECB/raw-pad', password, cipher.new(key, cipher.MODE_ECB).decrypt(blob))
            for ivn, iv, ct in [('zero', bytes(8), blob), ('prefix8', blob[:8], blob[8:])]:
                check(cn + '-CBC/raw-pad/' + ivn, password,
                      cipher.new(key, cipher.MODE_CBC, iv).decrypt(ct))
        for digest in ['md5', 'sha256']:
            for n in [16, 24, 32]:
                material = evp(p, digest, length=n+16)
                check(f'OpenSSL-EVP-{digest}-nosalt-AES{n*8}-CBC', password,
                      AES.new(material[:n], AES.MODE_CBC, material[n:]).decrypt(blob))
        if include_pbkdf:
            # Hypothesized raw layouts, not an identified serialization format.
            for digest in ['sha1', 'sha256']:
                for it in [1000, 10000, 100000]:
                    for sn in [0, 16]:
                        material = hashlib.pbkdf2_hmac(digest, p, blob[:sn], it, 48)
                        check(f'PBKDF2-{digest}-{it}/salt{sn}/derived-IV/CBC', password,
                              AES.new(material[:32], AES.MODE_CBC, material[32:]).decrypt(blob[sn:]))
                        if sn:
                            check(f'PBKDF2-{digest}-{it}/salt16/IV16/CBC', password,
                                  AES.new(material[:32], AES.MODE_CBC, blob[16:32]).decrypt(blob[32:]))
    return {'counts': dict(counts), 'hits': hits}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video_details', type=Path)
    args = ap.parse_args()
    d = json.loads(args.video_details.read_text())
    if d['channelId'] != 'UCw1EA-KJud9OmMA5p7_MWgw' or d['videoId'] != 'bg1BmaF6AJA':
        raise ValueError('Unexpected source channel/video')
    encoded = ''.join(d['shortDescription'].split('red pill:\n', 1)[1].split())
    blob = base64.b64decode(encoded, validate=True)
    if len(blob) != 96:
        raise ValueError('Public block has changed; re-assess the candidate layouts')
    # Positive controls use independently constructed known ciphertexts.
    plaintext = b'Synthetic control: a known message with enough text to detect.'
    key = hashlib.sha256(b'qtecqot').digest()
    iv = bytes(range(16))
    padded = pad(plaintext, 16)
    synthetic_cbc = iv + AES.new(key, AES.MODE_CBC, iv).encrypt(padded)
    # scan assumes full block multiples; the synthetic CBC blob is 80 bytes.
    assert any(h['plaintext_hex'] == padded.hex() for h in scan(synthetic_cbc, ['qtecqot'], False)['hits'])
    gcm = AES.new(key, AES.MODE_GCM, nonce=bytes(range(16)))
    ct, tag = gcm.encrypt_and_digest(bytes(64))
    synthetic_gcm = bytes(range(16)) + ct + tag
    assert any(h['authenticated'] for h in scan(synthetic_gcm, ['qtecqot'], False)['hits'])
    print(json.dumps({
        'source_url': 'https://www.youtube.com/watch?v=bg1BmaF6AJA',
        'source_channel_id': d['channelId'],
        'source_description_sha256': hashlib.sha256(d['shortDescription'].encode()).hexdigest(),
        'base64_chars': len(encoded), 'decoded_bytes': len(blob),
        'decoded_sha256': hashlib.sha256(blob).hexdigest(),
        'decoded_hex': blob.hex(), 'openssl_salted_header': blob.startswith(b'Salted__'),
        'passwords': PASSWORDS, 'positive_controls': ['SHA256-key/AES-CBC/prefix-IV',
                                                   'SHA256-key/AES-GCM/prefix-nonce/tag-last'],
        'recognition_floor': 'UTF-8 text >=16 characters with >=95% printable characters, or valid authentication tag. Short, binary, compressed, or damaged plaintext can fail this filter.',
        'results': scan(blob, PASSWORDS),
        'limits': 'No algorithm, KDF, salt, IV, authentication layout or plaintext type is established. These finite failed recipes do not exclude any password in an untested recipe.',
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
