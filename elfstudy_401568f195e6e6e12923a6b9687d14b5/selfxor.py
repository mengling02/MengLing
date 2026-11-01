d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]
n = len(blob)
bi = int.from_bytes(blob, 'big')

# quick filter: first 24 bytes printable ratio
def quick(bs):
    return sum(1 for c in bs if 32 <= c < 127) / len(bs)

hits = []
for off in range(0, len(d) - n):
    w = d[off:off + n]
    if w == blob:
        continue
    x = (int.from_bytes(w, 'big') ^ bi).to_bytes(n, 'big')
    # cheap filter on first 16 bytes
    head = x[:16]
    if sum(1 for c in head if 32 <= c < 127) < 12:
        continue
    r = quick(x)
    if r > 0.85:
        hits.append((r, off, x))
hits.sort(reverse=True)
print('hits', len(hits))
for r, off, x in hits[:10]:
    print(f'{r:.2f} off={off:#x}')
    print('   ', x[:80])
