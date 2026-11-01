from Crypto.Cipher import ARC4

d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]
n = len(blob)
crib = b'flag{'
T0 = bytes(blob[o] ^ crib[0] for o in range(n))
Tfull = [bytes(a ^ b for a, b in zip(blob[o:o + 5], crib)) for o in range(n - 4)]

def check(ks, tag):
    x = bytes(a ^ b for a, b in zip(ks[:n], T0))
    i = x.find(0)
    cnt = 0
    while i >= 0 and cnt < 4:
        if i + 5 <= n and ks[i:i + 5] == Tfull[i]:
            print(f'*** HIT {tag} offset={i}')
            print('    ', bytes(a ^ b for a, b in zip(blob[i:i + 60], ks[i:])))
            return True
        i = x.find(0, i + 1)
        cnt += 1
    return False

# RC4 with every k-byte window of the file as key
for klen in (5, 8, 16, 32):
    for off in range(0, len(d) - klen + 1):
        key = d[off:off + klen]
        ks = ARC4.new(key).encrypt(b'\0' * n)
        if check(ks, f'rc4 win@{off:#x} len{klen}'):
            raise SystemExit
print('rc4 windows: done')

# RC4 with format-ish keys
for key in (b'flag{', b'flag{}', b'flag', b'{', b'}', b'flag{}', b'elfstudy', b'ELFStudy'):
    ks = ARC4.new(key).encrypt(b'\0' * n)
    check(ks, f'rc4 {key!r}')
print('done')
