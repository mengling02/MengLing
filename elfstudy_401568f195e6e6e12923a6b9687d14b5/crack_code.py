import math, collections
d = open('elfstudy','rb').read()
blob = d[0x739a:0x76c6]
text = d[0x2540:0x7317]

freq = collections.Counter(text)
tot = len(text)
# smoothed log-prob of each byte as x86 code
logp = [math.log((freq.get(b, 0) + 0.5) / (tot + 128)) for b in range(256)]

def score(bs):
    return sum(logp[b] for b in bs)

best = []
for L in range(1, 65):
    key = bytearray()
    for col in range(L):
        colbytes = blob[col::L]
        bs, bk = -1e18, 0
        for k in range(256):
            s = sum(logp[b ^ k] for b in colbytes)
            if s > bs:
                bs, bk = s, k
        key.append(bk)
    dec = bytes(c ^ key[i % L] for i, c in enumerate(blob))
    best.append((score(dec) / len(dec), L, bytes(key), dec))

best.sort(reverse=True)
for sc, L, key, dec in best[:5]:
    print(f'L={L:3d} score={sc:.3f} key={key.hex()}')
    print('   ', dec[:80].hex(' '))
    print('   ', ''.join(chr(c) if 32 <= c < 127 else '.' for c in dec[:80]))
