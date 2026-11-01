import string
d = open('elfstudy','rb').read()
blob = d[0x7396:0x76c6]          # 816 bytes incl 4 nops
blob2 = d[0x739a:0x76c6]         # 812 bytes

PRINT = set(bytes(string.printable, 'ascii'))

def score(b):
    p = sum(1 for c in b if chr(c) in string.printable) / len(b)
    txt = ''.join(chr(c) if chr(c) in string.printable else '.' for c in b)
    bonus = 0
    for kw in ('flag', 'FLAG', 'ctf', 'CTF', '{', '}'):
        if kw in txt:
            bonus += 5
    return p + bonus, txt

print('=== single-byte XOR (top 10) ===')
res = []
for k in range(256):
    s, t = score(bytes(c ^ k for c in blob2))
    res.append((s, k, t))
for s, k, t in sorted(res, reverse=True)[:10]:
    print(f'key={k:#04x} score={s:.3f}')
    print('   ', t[:200])

print()
print('=== single-byte ADD (top 10) ===')
res = []
for k in range(256):
    s, t = score(bytes((c + k) & 0xff for c in blob2))
    res.append((s, k, t))
for s, k, t in sorted(res, reverse=True)[:10]:
    print(f'key={k:#04x} score={s:.3f}')
    print('   ', t[:200])

print()
print('=== repeating key XOR ===')
keys = [b'elfstudy', b'ELFStudy', b'ELFStudy1.4.2', b'1.4.2', b'ELF structure inspector',
        b'ELFStudy \xe2\x80\x94 ELF structure inspector', b'elfstudy1.4.2', b'ELF', b'ELF64',
        b'elfstudy\x00', b'ELFStudy\x00', b'flag', b'elf', b'ELFStudy 1.4.2']
for k in keys:
    out = bytes(c ^ k[i % len(k)] for i, c in enumerate(blob2))
    s, t = score(out)
    print(f'{k!r:50s} score={s:.3f} {t[:80]}')
