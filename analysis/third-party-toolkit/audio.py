#!/usr/bin/env python3.12
import os, subprocess, wave, numpy as np
BASE = "/home/user/new-skinny-bob/analysis/third-party-toolkit/extracted/2026-05-25_Confidential leaked ufo-ebe footage continuation of disclosure"
SCR = "/tmp/claude-1001/-home-user-new-skinny-bob/6c2508df-43ca-4f35-aaa6-0d27ef73c55d/scratchpad"
SD = f"{BASE}/SOUND"
SEG = f"{SD}/05 - Tape 06 - Case 31 - Mk.5 virgin"

def rd(p, sr=None):
    """decode any audio to float32 mono+stereo numpy via ffmpeg"""
    cmd = ["ffmpeg","-v","error","-i",p,"-f","f32le","-acodec","pcm_f32le"]
    if sr: cmd += ["-ar",str(sr)]
    cmd += ["-ac","2","-"]
    b = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(b, dtype=np.float32).reshape(-1,2)

full = rd(f"{SD}/Confidential leaked ufo-ebe footage continuation of disclosure (1080p).wav")
print(f"LC full WAV: {full.shape[0]} samples @44100 = {full.shape[0]/44100:.4f}s  peak={np.abs(full).max():.6f} rms={np.sqrt((full**2).mean()):.6f}")

# 1. is it a straight decode of SOURCE.mp4's AAC?
src_aac = rd(f"{BASE}/SOURCE/Confidential leaked ufo-ebe footage continuation of disclosure (1080p).mp4")
n = min(len(full), len(src_aac))
d = full[:n] - src_aac[:n]
print(f"\n[1] LC WAV vs my ffmpeg decode of LC SOURCE.mp4 AAC:")
print(f"    lengths {len(full)} vs {len(src_aac)}  compared {n}")
print(f"    max|diff| = {np.abs(d).max():.3e}   rms diff = {np.sqrt((d**2).mean()):.3e}")
print(f"    bit-identical samples: {np.count_nonzero(np.all(full[:n]==src_aac[:n],axis=1))}/{n}"
      f"  ({100*np.count_nonzero(np.all(full[:n]==src_aac[:n],axis=1))/n:.3f}%)")

# 2. vs OUR opus audio
ours = rd("/home/user/new-skinny-bob/videos/2026/OpSTlDJWFFI.mkv", sr=44100)
print(f"\n[2] LC WAV (from AAC 44.1k) vs our Opus track (resampled to 44.1k):")
print(f"    ours {len(ours)} samples = {len(ours)/44100:.4f}s")
n2 = min(len(full), len(ours))
a = full[:n2,0].astype(np.float64); b = ours[:n2,0].astype(np.float64)
a -= a.mean(); b -= b.mean()
print(f"    Pearson r (L ch, no lag)   = {np.corrcoef(a,b)[0,1]:.6f}")
# lag search
N = 1 << int(np.ceil(np.log2(n2*2)))
FA = np.fft.rfft(a, N); FB = np.fft.rfft(b, N)
cc = np.fft.irfft(FA*np.conj(FB), N)
cc = np.concatenate([cc[-2000:], cc[:2001]])
lag = int(np.argmax(np.abs(cc))) - 2000
print(f"    best lag = {lag} samples ({1000*lag/44100:+.3f} ms)")
if lag != 0:
    if lag > 0: aa, bb = a[lag:], b[:len(b)-lag]
    else: aa, bb = a[:len(a)+lag], b[-lag:]
    m = min(len(aa), len(bb))
    print(f"    Pearson r at best lag      = {np.corrcoef(aa[:m],bb[:m])[0,1]:.6f}")
rd_ = np.sqrt(((a-b)**2).mean())
print(f"    rms(LC) {np.sqrt((a**2).mean()):.6f}  rms(ours) {np.sqrt((b**2).mean()):.6f}  rms(diff) {rd_:.6f}")

# 3. locate the segment wav in the full track
seg = rd(f"{SEG}/05 - Tape 06 - Case 31 - Mk.5 virgin.wav")
print(f"\n[3] segment WAV: {len(seg)} samples = {len(seg)/44100:.4f}s peak={np.abs(seg).max():.6f}")
s = seg[:,0].astype(np.float64); s -= s.mean()
f = full[:,0].astype(np.float64); f -= f.mean()
N = 1 << int(np.ceil(np.log2(len(f)+len(s))))
cc = np.fft.irfft(np.fft.rfft(f,N)*np.conj(np.fft.rfft(s,N)), N)
pos = int(np.argmax(cc[:len(f)]))
print(f"    best alignment offset in full track = sample {pos} = {pos/44100:.4f}s = frame {pos/44100*29.97:.1f}")
m = min(len(s), len(f)-pos)
seg_a = s[:m]; ful_a = f[pos:pos+m]
print(f"    Pearson r there = {np.corrcoef(seg_a, ful_a)[0,1]:.6f}")
dd = seg[:m] - full[pos:pos+m]
print(f"    max|diff| = {np.abs(dd).max():.3e}  identical samples = {np.count_nonzero(np.all(seg[:m]==full[pos:pos+m],axis=1))}/{m}")
print(f"    -> corresponds to video frames {pos/44100*29.97:.0f} .. {(pos+len(s))/44100*29.97:.0f}")

# 4. the processed variants
print(f"\n[4] processed variants (all 11.8169s, pcm_s32le):")
print(f"{'file':>18} {'peak':>10} {'rms':>10} {'r vs raw seg':>13} {'spectral centroid Hz':>21} {'>4kHz energy %':>15} {'<300Hz %':>10}")
def spec(x):
    w = np.hanning(8192)
    acc = np.zeros(4097)
    cnt = 0
    for i in range(0, len(x)-8192, 8192//2):
        acc += np.abs(np.fft.rfft(x[i:i+8192]*w))**2; cnt += 1
    return acc/max(cnt,1)
fr = np.fft.rfftfreq(8192, 1/44100)
raw = seg[:,0].astype(np.float64)
Sraw = spec(raw)
for name in ["05 - Tape 06 - Case 31 - Mk.5 virgin.wav","A_voice.wav","B_radio.wav","C_highpass.wav","D_lowpass.wav","voice_filtered.wav"]:
    x = rd(f"{SEG}/{name}")
    xm = x[:,0].astype(np.float64)
    S = spec(xm); tot = S.sum()
    cen = (S*fr).sum()/tot if tot else 0
    hi = 100*S[fr>4000].sum()/tot if tot else 0
    lo = 100*S[fr<300].sum()/tot if tot else 0
    m = min(len(xm), len(raw))
    r = np.corrcoef(xm[:m]-xm[:m].mean(), raw[:m]-raw[:m].mean())[0,1]
    print(f"{name[:18]:>18} {np.abs(x).max():10.6f} {np.sqrt((xm**2).mean()):10.6f} {r:13.5f} {cen:21.1f} {hi:15.3f} {lo:10.3f}")

print("\n[5] octave-band energy (dB rel. raw segment) -- shows what each filter did")
bands = [(0,150),(150,300),(300,600),(600,1200),(1200,2400),(2400,4800),(4800,9600),(9600,22050)]
print(f"{'file':>18} " + " ".join(f"{str(b[0])+'-'+str(b[1]):>10}" for b in bands))
for name in ["A_voice.wav","B_radio.wav","C_highpass.wav","D_lowpass.wav","voice_filtered.wav"]:
    x = rd(f"{SEG}/{name}")[:,0].astype(np.float64)
    S = spec(x)
    row = []
    for lo_, hi_ in bands:
        m_ = (fr>=lo_)&(fr<hi_)
        e = S[m_].sum(); e0 = Sraw[m_].sum()
        row.append(10*np.log10(e/e0) if e>0 and e0>0 else -99)
    print(f"{name[:18]:>18} " + " ".join(f"{v:10.2f}" for v in row))
