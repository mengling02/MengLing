import struct, random

d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]
M32 = 1 << 32

crib = b'flag{'
# keystream candidate at offset o: blob[o:o+5] ^ crib
targets = {}
for o in range(0, 40):
    targets[o] = bytes(a ^ b for a, b in zip(blob[o:o + 5], crib))

print('keystream targets (offset: hex):')
for o in range(0, 8):
    print(f'  {o}: {targets[o].hex()}')

# ---------- C++ std::mt19937 (init_genrand) ----------
class MT:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed & 0xffffffff
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xffffffff
        self.idx = 624
    def gen(self):
        if self.idx >= 624:
            mt = self.mt
            for i in range(624):
                y = (mt[i] & 0x80000000) + (mt[(i + 1) % 624] & 0x7fffffff)
                nxt = mt[(i + 397) % 624] ^ (y >> 1)
                if y & 1:
                    nxt ^= 0x9908b0df
                mt[i] = nxt
            self.idx = 0
        y = self.mt[self.idx]
        self.idx += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x2636ec28
        y ^= (y << 15) & 0x9d2c5680
        y ^= y >> 18
        return y

def first_bytes_mt(seed, n):
    g = MT(seed)
    out = bytearray()
    while len(out) < n:
        out += struct.pack('<I', g.gen())
    return bytes(out[:n])

# ---------- glibc rand() ----------
def glibc_first(seed, n):
    r = [0] * (344 + n)
    s = seed & 0x7fffffff
    if s == 0:
        s = 1
    r[0] = s
    for i in range(1, 31):
        hi, lo = divmod(r[i - 1], 127773)
        w = 16807 * lo - 2836 * hi
        if w < 0:
            w += 2147483647
        r[i] = w
    for i in range(31, 34):
        r[i] = r[i - 31]
    for i in range(34, 344):
        r[i] = (r[i - 31] + r[i - 3]) & 0xffffffff
    out = bytearray()
    for i in range(344, 344 + ((n + 3) // 4) * 1):
        pass
    # generate outputs one per call
    vals = []
    for i in range(344, 344 + n):
        r.append((r[i - 31] + r[i - 3]) & 0xffffffff)
        vals.append(r[i] >> 1)
    return vals

# ---------- MSVC rand ----------
def msvc_first(seed, n):
    out = []
    s = seed & 0xffffffff
    for _ in range(n):
        s = (s * 214013 + 2531011) & 0xffffffff
        out.append((s >> 16) & 0x7fff)
    return out

def match(vals, o, mode):
    # build byte stream from vals
    if mode == 'word_le':
        bs = b''.join(struct.pack('<I', v) for v in vals)
    elif mode == 'and_ff':
        bs = bytes(v & 0xff for v in vals)
    elif mode == 'mod_256':
        bs = bytes(v % 256 for v in vals)
    elif mode == 'and_7fff':
        bs = bytes(v & 0xff for v in vals)
    return bs[:5] == targets[o]

N = 30000
print('scanning seeds 0..%d ...' % N)
hits = []
for seed in range(N):
    # mt19937 word_le
    b = first_bytes_mt(seed, 5)
    for o in range(0, 40):
        if b == targets[o]:
            hits.append(('mt19937 word_le', seed, o))
    # glibc
    vals = glibc_first(seed, 6)
    for mode in ('and_ff', 'mod_256'):
        bs = bytes((v & 0xff) if mode == 'and_ff' else (v % 256) for v in vals)
        for o in range(0, 40):
            if bs[:5] == targets[o]:
                hits.append(('glibc ' + mode, seed, o))
    # msvc
    vals = msvc_first(seed, 6)
    bs = bytes(v & 0xff for v in vals)
    for o in range(0, 40):
        if bs[:5] == targets[o]:
            hits.append(('msvc', seed, o))
    # python random
    random.seed(seed)
    py = bytes(random.getrandbits(8) for _ in range(5))
    for o in range(0, 40):
        if py == targets[o]:
            hits.append(('python getrandbits8', seed, o))
    random.seed(seed)
    py = bytes(random.randrange(256) for _ in range(5))
    for o in range(0, 40):
        if py == targets[o]:
            hits.append(('python randrange', seed, o))

print('hits:', hits[:10])
