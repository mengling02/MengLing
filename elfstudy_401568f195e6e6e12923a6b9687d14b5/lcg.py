import struct

d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]
M32 = 1 << 32
M64 = 1 << 64

def inv32(a):
    return pow(a, -1, M32)

def inv64(a):
    return pow(a, -1, M64)

# ---- 32-bit LCG test on 4-byte words ----
w = struct.unpack('<%dI' % (len(blob) // 4), blob)
found32 = None
for p in range(len(w) - 6):
    d1 = (w[p + 1] - w[p]) % M32
    d2 = (w[p + 2] - w[p + 1]) % M32
    d3 = (w[p + 3] - w[p + 2]) % M32
    if d1 % 2 == 0:
        continue
    a = (d2 * inv32(d1)) % M32
    c = (w[p + 1] - a * w[p]) % M32
    ok = all((a * w[p + k] + c) % M32 == w[p + k + 1] for k in range(1, min(8, len(w) - p - 1)))
    if ok and len(w) - p >= 8:
        print(f'32-bit LCG found at word {p}: a={a:#x} c={c:#x}')
        found32 = (a, c, p)
        break

# ---- 64-bit LCG test on 8-byte words ----
n8 = len(blob) // 8
q = struct.unpack('<%dQ' % n8, blob[:n8 * 8])
found64 = None
for p in range(len(q) - 6):
    d1 = (q[p + 1] - q[p]) % M64
    d2 = (q[p + 2] - q[p + 1]) % M64
    d3 = (q[p + 3] - q[p + 2]) % M64
    if d1 % 2 == 0:
        continue
    a = (d2 * inv64(d1)) % M64
    c = (q[p + 1] - a * q[p]) % M64
    ok = all((a * q[p + k] + c) % M64 == q[p + k + 1] for k in range(1, min(8, len(q) - p - 1)))
    if ok and len(q) - p >= 8:
        print(f'64-bit LCG found at word {p}: a={a:#x} c={c:#x}')
        found64 = (a, c, p)
        break

if not found32 and not found64:
    print('no plain LCG structure in 4/8-byte words')

# ---- also test: consecutive-byte difference LCG (glibc-rand style is complex; skip) ----
# ---- test xorshift32: w[i+1] = xorshift(w[i]) ----
def xs32(x):
    x ^= (x << 13) & 0xffffffff
    x ^= x >> 17
    x ^= (x << 5) & 0xffffffff
    return x

hits = [p for p in range(len(w) - 4) if xs32(w[p]) == w[p + 1]]
print('xorshift32 hits:', hits[:5])

def xs64(x):
    x ^= (x << 13) & 0xffffffffffffffff
    x ^= x >> 7
    x ^= (x << 17) & 0xffffffffffffffff
    return x

hits = [p for p in range(len(q) - 2) if xs64(q[p]) == q[p + 1]]
print('xorshift64 hits:', hits[:5])
