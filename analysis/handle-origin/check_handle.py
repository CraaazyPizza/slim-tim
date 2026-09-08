#!/usr/bin/env python3.12
"""Finite handle tests. Standard library only; dictionary bytes are hash-pinned."""
import argparse
import base64
import hashlib
import json
import math
import re
from pathlib import Path

HANDLE = 'qtecqot'
DICTIONARY_URL = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
DICTIONARY_SHA256 = '3ed0c94610d8bcf7c11bbb49c56aa49c7234d32b66824df91f554169e572da48'
KEYS = ['ivan', 'serpo', 'skinnybob', 'slimtim', 'disclosure', 'deadmansswitch',
        'mantis', 'quetzalcoatl', 'kgb', 'tape', 'seven', 'eight']
DIGIT_KEYS = ['0135', '135', '2011', '2026', '20260421', '20260422',
              '20260428', '20260525', '1234567', '5678']


def pattern(s):
    return [s.index(c) for c in s]


def affine(s, a, b):
    return ''.join(chr((a * (ord(c) - 97) + b) % 26 + 97) for c in s)


def affine_candidates(s):
    return {f'reversed={rev},a={a},b={b}': affine(t, a, b)
            for rev, t in [(False, s), (True, s[::-1])]
            for a in range(26) if math.gcd(a, 26) == 1 for b in range(26)}


def phone(s):
    table = {c: str(n) for n, group in enumerate(
        ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz'], 2) for c in group}
    return ''.join(table[c] for c in s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dictionary', type=Path)
    ap.add_argument('--timeline', type=Path)
    args = ap.parse_args()
    raw = args.dictionary.read_bytes()
    if hashlib.sha256(raw).hexdigest() != DICTIONARY_SHA256:
        raise ValueError('Dictionary differs from the recorded experiment')
    words = set(raw.decode().splitlines())
    seven = {w for w in words if len(w) == 7}
    candidates = affine_candidates(HANDLE)
    keyed = {}
    for key in KEYS:
        k = [ord(c) - 97 for c in key]
        c = [ord(x) - 97 for x in HANDLE]
        keyed[key] = {name: ''.join(chr(v % 26 + 97) for v in values) for name, values in [
            ('vigenere-decrypt', [x-k[i % len(k)] for i, x in enumerate(c)]),
            ('vigenere-encrypt', [x+k[i % len(k)] for i, x in enumerate(c)]),
            ('beaufort', [k[i % len(k)]-x for i, x in enumerate(c)])]}
    digits = {k: {str(sign): ''.join(chr((ord(c)-97+sign*int(k[i % len(k)])) % 26+97)
                                    for i, c in enumerate(HANDLE)) for sign in [-1, 1]}
              for k in DIGIT_KEYS}
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    qwerty = 'qwertyuiopasdfghjklzxcvbnm'
    rows = ['qwertyuiop[]', "asdfghjkl;'", 'zxcvbnm,./']
    layouts = {
        'qwerty-to-russian': HANDLE.translate(str.maketrans(
            'qwertyuiopasdfghjklzxcvbnm', 'йцукенгшщзфывапролдячсмить')),
        'qwerty-ordinal-to-alphabet': HANDLE.translate(str.maketrans(qwerty, alphabet)),
        'alphabet-to-qwerty-ordinal': HANDLE.translate(str.maketrans(alphabet, qwerty)),
        'qwerty-to-dvorak': HANDLE.translate(str.maketrans(
            'qwertyuiopasdfghjklzxcvbnm', "',.pyfgcrlaoeuidhtn;qjkxbm")),
        'qwerty-to-colemak': HANDLE.translate(str.maketrans(
            'qwertyuiopasdfghjklzxcvbnm', 'qwfpgjluy;arstdhneizxcvbkm')),
    }
    for step in [-1, 1]:
        table = {c: row[i+step] if 0 <= i+step < len(row) else '?'
                 for row in rows for i, c in enumerate(row)}
        layouts[f'qwerty-horizontal-{step}'] = ''.join(table[c] for c in HANDLE)
    controls = {}
    for name, text in [('caesar', affine('contact', 1, 7)),
                       ('affine', affine('contact', 5, 8)),
                       ('reversed-affine', affine('contact', 5, 8)[::-1])]:
        controls[name] = 'contact' in affine_candidates(text).values()
    controls['T9-contact'] = phone('contact') == '2668228' and 'contact' in words
    assert all(controls.values())
    # Recovering an exact dictionary word does not measure recognition of typos,
    # abbreviations, missing characters, other languages, or arbitrary ciphers.
    result = {
        'handle': HANDLE, 'dictionary_url': DICTIONARY_URL,
        'dictionary_sha256': DICTIONARY_SHA256, 'dictionary_entries': len(words),
        'seven_letter_entries': len(seven), 'pattern_first_indices': pattern(HANDLE),
        'same_pattern_candidates': sorted(w for w in seven if pattern(w) == pattern(HANDLE)),
        'affine_candidate_count': len(candidates),
        'affine_dictionary_hits': {k: v for k, v in candidates.items() if v in words},
        'caesar': {str(i): affine(HANDLE, 1, i) for i in range(26)},
        'atbash': affine(HANDLE, 25, 25), 'reversal': HANDLE[::-1],
        'anagrams': sorted(w for w in seven if sorted(w) == sorted(HANDLE)),
        'phone_digits': phone(HANDLE),
        'phone_dictionary_hits': sorted(w for w in seven if phone(w) == phone(HANDLE)),
        'layouts': layouts, 'keyed': keyed, 'digit_keyed': digits,
        'keyed_dictionary_hits': [(k, mode, v) for k, values in {**keyed, **digits}.items()
                                  for mode, v in values.items() if v in words],
        'base64_hex': base64.b64decode(HANDLE + '=').hex(),
        'base32_hex': base64.b32decode(HANDLE.upper() + '=').hex(),
        'positive_controls': controls,
        'detection_scope': 'Exact dictionary matches in the enumerated finite families only.',
    }
    if args.timeline:
        raw = args.timeline.read_bytes()
        data = json.loads(raw)
        entries = [e for e in data['entries'] if e['kind'] != 'repost' and e['id'].isdigit()
                   and e['author'].get('handle', '').lower() == HANDLE]
        terms = r'\b(?:quetzal\w*|aztec\w*|nahua\w*|kukul\w*|serpent\w*|feather\w*|qte|qot|qtc|radio\w*|bearing\w*|callsign\w*)\b'
        acrostics = []
        for e in entries:
            clean = re.sub(r'https?://\S+|@\w+', '', e['text'])
            initials = ''.join(w[0].lower() for w in re.findall(r'[A-Za-z]+', clean))
            if HANDLE in initials:
                acrostics.append(e['id'])
        result['corpus'] = {
            'timeline_sha256': hashlib.sha256(raw).hexdigest(),
            'generated_at': data['generated_at'], 'entry_count': len(data['entries']),
            'authored_x_count': len(entries), 'authored_x_ids': sorted(e['id'] for e in entries),
            'whitespace_word_count': sum(len(e['text'].split()) for e in entries),
            'literal_term_pattern': terms,
            'literal_term_hit_ids': [e['id'] for e in entries if re.search(terms, e['text'], re.I)],
            'within_post_word_initial_hit_ids': acrostics,
            'scope': 'Held text only; excludes media, uncaptured deletions, reposts and manual entries.',
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
