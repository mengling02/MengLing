import struct, random

d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]
n = len(blob)
crib = b'flag{'

# target[o][0] for each offset (first keystream byte if flag starts at o)
T0 = bytes(blob[o] ^ crib[0] for o in range(n))
# full targets for verification
Tfull = [bytes(a ^ b for a, b in zip(blob[o:o + 5], crib)) for o in range(n - 4)]

def check_ks(ks, tag, seed):
    x = bytes(a ^ b for a, b in zip(ks, T0))
    i = x.find(0)
    while i >= 0:
        if i + 5 <= n and ks[i:i + 5] == Tfull[i]:
            print(f'*** HIT {tag} seed={seed} offset={i}')
            print('    decrypted:', bytes(a ^ b for a, b in zip(blob[i:i + 60], ks[i:])))
            return True
        i = x.find(0, i + 1)
    return False

# ---------- mt19937 C++ ----------
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
                nx = mt[(i + 397) % 624] ^ (y >> 1)
                if y & 1:
                    nx ^= 0x9908b0df
                mt[i] = nx
            self.idx = 0
        y = self.mt[self.idx]; self.idx += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x2636ec28
        y ^= (y << 15) & 0x9d2c5680
        y ^= y >> 18
        return y

NW = (n + 3) // 4
for seed in range(6000):
    g = MT(seed)
    ks = b''.join(struct.pack('<I', g.gen()) for _ in range(NW))[:n]
    if check_ks(ks, 'mt19937le', seed):
        break
else:
    print('mt19937le: no hit in 6000 seeds')

# ---------- glibc rand ----------
def glibc_ks(seed, n):
    r = [0] * (344 + n)
    s = seed & 0x7fffffff or 1
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
    for i in range(344, 344 + n):
        r.append((r[i - 31] + r[i - 3]) & 0xffffffff)
        out.append((r[i] >> 1) & 0xff)
    return bytes(out)

for seed in range(4000):
    ks = glibc_ks(seed, n)
    if check_ks(ks, 'glibc&ff', seed):
        break
else:
    print('glibc&ff: no hit in 4000 seeds')

# ---------- python random ----------
for seed in range(6000):
    random.seed(seed)
    ks = bytes(random.getrandbits(8) for _ in range(n))
    if check_ks(ks, 'py_randbits8', seed):
        break
else:
    print('py_randbits8: no hit in 6000 seeds')
for seed in range(6000):
    random.seed(seed)
    ks = bytes(random.randrange(256) for _ in range(n))
    if check_ks(ks, 'py_randrange', seed):
        break
else:
    print('py_randrange: no hit in 6000 seeds')
print('done')
