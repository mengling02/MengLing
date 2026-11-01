d = open('elfstudy','rb').read()
blob = d[0x739a:0x76c6]
bits = []
for c in blob:
    for i in range(7, -1, -1):
        bits.append((c >> i) & 1)

def tobytes(bs):
    out = bytearray()
    for i in range(0, len(bs) - 7, 8):
        v = 0
        for b in bs[i:i+8]:
            v = (v << 1) | b
        out.append(v)
    return bytes(out)

best = []
for s in range(1, 257):
    for o in range(s):
        sub = bits[o::s]
        if len(sub) < 40:
            continue
        bs = tobytes(sub)
        if not bs:
            continue
        r = sum(1 for c in bs if 32 <= c < 127) / len(bs)
        best.append((r, s, o, bs))
best.sort(key=lambda x: -x[0])
for r, s, o, bs in best[:8]:
    print(f'bitstride={s:4d} off={o:4d} ratio={r:.2f} n={len(bs)}')
    print('   ', ''.join(chr(c) if 32 <= c < 127 else '.' for c in bs[:70]))
