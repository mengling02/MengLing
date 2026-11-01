d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]

def test(key):
    out = bytes(c ^ key[i % len(key)] for i, c in enumerate(blob[:24]))
    return sum(1 for c in out if 32 <= c < 127)

hits = []
for L in (8, 12, 16, 20, 24, 32):
    for off in range(0, len(d) - L):
        k = d[off:off + L]
        if test(k) >= 22:
            out = bytes(c ^ k[i % L] for i, c in enumerate(blob))
            r = sum(1 for c in out if 32 <= c < 127) / len(out)
            hits.append((r, off, L, out))
hits.sort(reverse=True)
print('hits', len(hits))
for r, off, L, out in hits[:10]:
    print(f'{r:.2f} off={off:#x} L={L}')
    print('   ', out[:80])
