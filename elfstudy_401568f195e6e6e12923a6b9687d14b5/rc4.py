import string, re
d = open('elfstudy','rb').read()
blob = d[0x739a:0x76c6]

def rc4(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 0xff
        S[i], S[j] = S[j], S[i]
    out = bytearray()
    i = j = 0
    for c in data:
        i = (i + 1) & 0xff
        j = (j + S[i]) & 0xff
        S[i], S[j] = S[j], S[i]
        out.append(c ^ S[(S[i] + S[j]) & 0xff])
    return bytes(out)

cands = [b'elfstudy', b'ELFStudy', b'ELFStudy1.4.2', b'elfstudy1.4.2', b'1.4.2',
         b'ELF structure inspector', b'ELFStudy - ELF structure inspector',
         b'elf', b'ELF', b'ELF64', b'flag', b'key', b'secret', b'password',
         b'ELFStudy\x00', b'elfstudy\x00', bytes.fromhex('e9e5c048fa11349c8486d9944e2c5ad0f4256f8a'),
         b'GNU', b'elfstudy-1.4.2', b'ELFSTUDY', b'ElfStudy']

def score(b):
    txt = b.decode('latin1')
    runs = re.findall(r'[ -~]{6,}', txt)
    return len(runs), txt

for k in cands:
    out = rc4(k, blob)
    n, txt = score(out)
    print(f'{k!r:46s} runs={n} {txt[:60]!r}')
