import math, collections

d = open('elfstudy','rb').read()

def ent(b):
    if not b:
        return 0
    c = collections.Counter(b)
    n = len(b)
    return -sum(v/n*math.log2(v/n) for v in c.values())

print('== entropy by 256B window (only >=6.0) ==')
for off in range(0, len(d), 256):
    w = d[off:off+256]
    e = ent(w)
    if e >= 6.0:
        print(f'{off:#06x} {e:.2f}')

print()
print('== known magics anywhere ==')
magics = {
    b'\x89PNG': 'PNG', b'PK\x03\x04': 'ZIP', b'\x1f\x8b': 'GZIP', b'\x78\x9c': 'ZLIB',
    b'\x7fELF': 'ELF', b'flag': 'flag', b'FLAG': 'FLAG', b'CTF{': 'CTF{', b'DASCTF': 'DASCTF',
    b'\xfd7zXZ': 'XZ', b'BZh': 'BZIP2', b'7z\xbc\xaf': '7Z',
}
for m, name in magics.items():
    idx = 0
    while True:
        i = d.find(m, idx)
        if i < 0:
            break
        print(f'{name:8s} at {i:#06x}')
        idx = i+1
