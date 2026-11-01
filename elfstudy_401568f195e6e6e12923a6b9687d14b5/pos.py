d = open('elfstudy','rb').read()
blob = d[0x739a:0x76c6]

def score(bs):
    r = sum(1 for c in bs if 32 <= c < 127) / len(bs)
    return r

best = []
# keystream = (i + k) & 0xff
for k in range(256):
    out = bytes(c ^ ((i + k) & 0xff) for i, c in enumerate(blob))
    best.append((score(out), f'xor(i+{k})', out))
    out = bytes((c - (i + k)) & 0xff for i, c in enumerate(blob))
    best.append((score(out), f'sub(i+{k})', out))
    out = bytes((c + (i + k)) & 0xff for i, c in enumerate(blob))
    best.append((score(out), f'add(i+{k})', out))
# keystream = bytes of (addr+i)
base = 0x739a
for shift in (0, 8, 16, 24):
    out = bytes(c ^ (((base + i) >> shift) & 0xff) for i, c in enumerate(blob))
    best.append((score(out), f'xor(addr>>{shift})', out))
# keystream = (i*i)
out = bytes(c ^ ((i * i) & 0xff) for i, c in enumerate(blob))
best.append((score(out), 'xor(i*i)', out))
# keystream = i*0x41
for m in (3, 5, 7, 0x41, 0x9e, 0x1f, 0x3b):
    out = bytes(c ^ ((i * m) & 0xff) for i, c in enumerate(blob))
    best.append((score(out), f'xor(i*{m})', out))

best.sort(key=lambda x: -x[0])
for r, tag, out in best[:6]:
    print(f'{r:.2f} {tag:18s} {out[:60]!r}')
