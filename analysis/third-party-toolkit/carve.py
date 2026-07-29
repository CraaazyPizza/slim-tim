#!/usr/bin/env python3.12
"""Carve a truncated (no EOCD) ZIP by walking local file headers sequentially."""
import os, sys, struct, json, zlib, hashlib

ZIP = "/home/user/new-skinny-bob/community/2026-05-25_Confidential leaked ufo-ebe footage continuation of disclosure.zip"
OUT = "/home/user/new-skinny-bob/analysis/third-party-toolkit/extracted"
MAN = "/home/user/new-skinny-bob/analysis/third-party-toolkit/manifest.json"

LFH = b"PK\x03\x04"
CDH = b"PK\x01\x02"
DD  = b"PK\x07\x08"

def dosdt(t, d):
    sec = (t & 0x1f) * 2
    mnt = (t >> 5) & 0x3f
    hr  = (t >> 11) & 0x1f
    day = d & 0x1f
    mon = (d >> 5) & 0xf
    yr  = ((d >> 9) & 0x7f) + 1980
    return f"{yr:04d}-{mon:02d}-{day:02d} {hr:02d}:{mnt:02d}:{sec:02d}"

def main(extract=True):
    size = os.path.getsize(ZIP)
    print(f"file size at start: {size}", file=sys.stderr)
    f = open(ZIP, "rb")
    off = 0
    entries = []
    truncated_at = None
    while off + 30 <= size:
        f.seek(off)
        hdr = f.read(30)
        if len(hdr) < 30:
            truncated_at = off; break
        if hdr[:4] == CDH:
            print(f"reached central directory at {off}", file=sys.stderr); break
        if hdr[:4] != LFH:
            # resync: scan forward for next LFH
            print(f"desync at {off}, scanning...", file=sys.stderr)
            f.seek(off)
            found = None
            chunk_off = off
            while True:
                buf = f.read(1 << 22)
                if not buf: break
                i = buf.find(LFH)
                if i >= 0:
                    found = chunk_off + i; break
                chunk_off += len(buf) - 3
                f.seek(chunk_off)
            if found is None:
                truncated_at = off; break
            off = found; continue
        (ver, flags, comp, mtime, mdate, crc, csize, usize,
         nlen, elen) = struct.unpack("<HHHHHIIIHH", hdr[4:30])
        name_b = f.read(nlen)
        extra = f.read(elen)
        if len(name_b) < nlen or len(extra) < elen:
            truncated_at = off; break
        try:
            name = name_b.decode("utf-8")
        except UnicodeDecodeError:
            name = name_b.decode("cp437")
        # zip64 extra
        z64 = False
        i = 0
        while i + 4 <= len(extra):
            hid, hsz = struct.unpack("<HH", extra[i:i+4])
            body = extra[i+4:i+4+hsz]
            if hid == 0x0001:
                z64 = True
                j = 0
                if usize == 0xFFFFFFFF and j+8 <= len(body):
                    usize = struct.unpack("<Q", body[j:j+8])[0]; j += 8
                if csize == 0xFFFFFFFF and j+8 <= len(body):
                    csize = struct.unpack("<Q", body[j:j+8])[0]; j += 8
            i += 4 + hsz
        data_off = off + 30 + nlen + elen
        streaming = bool(flags & 0x08) and csize == 0
        if streaming:
            # scan for data descriptor / next LFH
            print(f"streaming entry (no size in LFH): {name}", file=sys.stderr)
            f.seek(data_off)
            probe_start = data_off
            end = None
            cur = data_off
            while True:
                buf = f.read(1 << 22)
                if not buf: break
                k = 0
                while True:
                    k = buf.find(DD, k)
                    if k < 0: break
                    cand = cur + k
                    csz = cand - data_off
                    f2 = open(ZIP, "rb"); f2.seek(cand+4); dd = f2.read(12); f2.close()
                    if len(dd) == 12:
                        dcrc, dcs, dus = struct.unpack("<III", dd)
                        if dcs == csz:
                            end = cand; break
                    k += 4
                if end is not None: break
                cur += len(buf) - 3
                f.seek(cur)
            if end is None:
                truncated_at = data_off; entries.append(dict(
                    path=name, offset=off, data_offset=data_off, method=comp,
                    flags=flags, usize=None, csize=None, crc=None, dos=dosdt(mtime, mdate),
                    dos_raw=[mtime, mdate], zip64=z64, extra_len=elen,
                    extra_ids=[], complete=False, note="streaming, no descriptor found (truncated)"))
                break
            csize = end - data_off
            usize = csize if comp == 0 else None
            next_off = end + 16
        else:
            next_off = data_off + csize
        complete = (data_off + csize) <= size
        extra_ids = []
        i = 0
        while i + 4 <= len(extra):
            hid, hsz = struct.unpack("<HH", extra[i:i+4])
            extra_ids.append((hex(hid), hsz, extra[i+4:i+4+hsz].hex()[:64]))
            i += 4 + hsz
        e = dict(path=name, offset=off, data_offset=data_off, method=comp, flags=flags,
                 usize=usize, csize=csize, crc=crc, dos=dosdt(mtime, mdate),
                 dos_raw=[mtime, mdate], zip64=z64, extra_len=elen, extra_ids=extra_ids,
                 complete=complete)
        if extract and complete and not name.endswith("/"):
            dst = os.path.join(OUT, name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            f.seek(data_off)
            remaining = csize
            h = hashlib.sha256(); crc_run = 0
            with open(dst, "wb") as o:
                if comp == 0:
                    while remaining > 0:
                        b = f.read(min(1 << 22, remaining))
                        if not b: break
                        o.write(b); h.update(b); crc_run = zlib.crc32(b, crc_run)
                        remaining -= len(b)
                elif comp == 8:
                    d = zlib.decompressobj(-15)
                    while remaining > 0:
                        b = f.read(min(1 << 22, remaining))
                        if not b: break
                        db = d.decompress(b)
                        o.write(db); h.update(db); crc_run = zlib.crc32(db, crc_run)
                        remaining -= len(b)
                    db = d.flush(); o.write(db); h.update(db); crc_run = zlib.crc32(db, crc_run)
            e["sha256"] = h.hexdigest()
            e["crc_ok"] = (crc_run == crc) if crc else None
        elif not complete and not name.endswith("/"):
            e["note"] = f"truncated: needs {data_off+csize} > {size}"
            truncated_at = off
            entries.append(e)
            break
        entries.append(e)
        off = next_off
        if len(entries) % 500 == 0:
            print(f"  {len(entries)} entries, off={off}", file=sys.stderr)
    f.close()
    out = dict(zip_size_at_start=size, zip_size_at_end=os.path.getsize(ZIP),
               n_entries=len(entries), truncated_at=truncated_at, entries=entries)
    with open(MAN, "w") as o:
        json.dump(out, o, indent=1)
    print(f"entries: {len(entries)}  truncated_at={truncated_at}", file=sys.stderr)

if __name__ == "__main__":
    main(extract="--list" not in sys.argv)
