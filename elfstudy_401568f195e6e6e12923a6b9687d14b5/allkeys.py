import re
d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]

keys = set()
for m in re.finditer(rb'[ -~]{3,}', d):
    s = m.group()
    for L in (3, 4, 5, 6, 8, 12, 16, 20, 24, 32):
        if len(s) >= L:
            keys.add(s[:L])
keys.add(bytes.fromhex('e9e5c048fa11349c8486d9944e2c5ad0f4256f8a'))
keys = sorted(keys)
print('candidate keys:', len(keys))

best = []
for k in keys:
    out = bytes(c ^ k[i % len(k)] for i, c in enumerate(blob))
    r = sum(1 for c in out if 32 <= c < 127) / len(out)
    best.append((r, k, out))
best.sort(key=lambda x: -x[0])
for r, k, out in best[:6]:
    print(f'{r:.2f} key={k!r}')
    print('   ', out[:70])
