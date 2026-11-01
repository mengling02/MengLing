import struct

DELTA = 0x9E3779B9

def to_uint32(data, bigend=False):
    n = len(data) // 4
    return list(struct.unpack(('>' if bigend else '<') + str(n) + 'I', data[:n*4]))

def to_bytes(v, bigend=False):
    return struct.pack(('>' if bigend else '<') + str(len(v)) + 'I', *v)

def xxtea_decrypt(data, key):
    if len(data) < 8:
        return None
    v = to_uint32(data)
    n = len(v)
    if n < 2:
        return None
    k = to_uint32((key * 4)[:16])
    rounds = 6 + 52 // n
    total = (rounds * DELTA) & 0xffffffff
    y = v[0]
    while total:
        e = (total >> 2) & 3
        for p in range(n - 1, -1, -1):
            z = v[(p - 1) % n]
            mx = (((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ ((total ^ y) + (k[(p & 3) ^ e] ^ z))
            v[p] = (v[p] - mx) & 0xffffffff
            y = v[p]
        total = (total - DELTA) & 0xffffffff
    return to_bytes(v)

def xtea_decrypt_block(block, key, rounds=32):
    v0, v1 = struct.unpack('<2I', block)
    k = struct.unpack('<4I', key)
    s = (DELTA * rounds) & 0xffffffff
    for _ in range(rounds):
        v1 = (v1 - ((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (s + k[(s >> 11) & 3]))) & 0xffffffff
        s = (s - DELTA) & 0xffffffff
        v0 = (v0 - ((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (s + k[s & 3]))) & 0xffffffff
    return struct.pack('<2I', v0, v1)

def tea_decrypt_block(block, key, rounds=32):
    v0, v1 = struct.unpack('>2I', block)
    k = struct.unpack('>4I', key)
    s = (DELTA * rounds) & 0xffffffff
    for _ in range(rounds):
        v1 = (v1 - (((v0 << 4) + k[2]) ^ (v0 + s) ^ ((v0 >> 5) + k[3]))) & 0xffffffff
        v0 = (v0 - (((v1 << 4) + k[0]) ^ (v1 + s) ^ ((v1 >> 5) + k[1]))) & 0xffffffff
        s = (s - DELTA) & 0xffffffff
    return struct.pack('>2I', v0, v1)

d = open('elfstudy', 'rb').read()
cands = {
    '812': d[0x739a:0x76c6],
    '816': d[0x7396:0x76c6],
}
keys = [b'elfstudy', b'ELFStudy', b'ELFStudy1.4.2', b'elfstudy1.4.2', b'1.4.2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        b'elfstudyelfstudy', b'ELFStudyELFStudy', b'\x00' * 16, b'1234567890123456']
keys = [k.ljust(16, b'\x00')[:16] for k in keys]

def show(tag, out):
    if not out:
        return
    r = sum(1 for c in out if 32 <= c < 127) / len(out)
    if r > 0.6:
        print(f'{tag:44s} r={r:.2f} {out[:60]!r}')

for cname, data in cands.items():
    for k in keys:
        out = xxtea_decrypt(data, k)
        show(f'xxtea {cname} {k[:8]!r}', out)
        # block ciphers need multiple of 8
        if len(data) % 8 == 0:
            o1 = b''.join(xtea_decrypt_block(data[i:i+8], k) for i in range(0, len(data), 8))
            show(f'xtea {cname} {k[:8]!r}', o1)
            o2 = b''.join(tea_decrypt_block(data[i:i+8], k) for i in range(0, len(data), 8))
            show(f'tea  {cname} {k[:8]!r}', o2)
print('done')
