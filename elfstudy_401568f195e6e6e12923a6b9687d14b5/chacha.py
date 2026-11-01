import struct, hashlib, zlib
from Crypto.Cipher import ChaCha20, Salsa20

d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]
crib = b'flag{'
target0 = bytes(a ^ b for a, b in zip(blob[:5], crib))   # keystream[0:5] if flag at 0
print('target keystream[0:5]:', target0.hex())

# ---- mt19937 (C++ init_genrand) ----
class MT:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed & 0xffffffff
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xffffffff
        self.idx = 624
    def gen(self):
        if self.idx >= 624:
            mt = self.mt
            for i in range(624):
                y = (mt[i] & 0x80000000) + (mt[(i + 1) % 624] & 0x7fffffff)
                nxt = mt[(i + 397) % 624] ^ (y >> 1)
                if y & 1:
                    nxt ^= 0x9908b0df
                mt[i] = nxt
            self.idx = 0
        y = self.mt[self.idx]; self.idx += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x2636ec28
        y ^= (y << 15) & 0x9d2c5680
        y ^= y >> 18
        return y

seed_materials = {
    'zero': 0, 'one': 1, '42': 42, '1337': 1337, '2024': 2024, '2025': 2025, '2026': 2026,
    'e_entry': 0x2e90, 'filesize': len(d), 'deadbeef': 0xdeadbeef,
    'crc32': zlib.crc32(d), 'crc32head': zlib.crc32(d[:0x739a]),
    'bid_w0': struct.unpack('<I', d[0x350 + 16:0x350 + 20])[0],
    'bid_w3': struct.unpack('<I', d[0x350 + 28:0x350 + 32])[0],
    'magic': 0x464c457f,
}
for name, s in seed_materials.items():
    g = MT(s)
    ks = b''.join(struct.pack('<I', g.gen()) for _ in range(4))
    if ks[:5] == target0:
        print('HIT mt19937 word_le seed', name, s)
    g = MT(s)
    ks = bytes(g.gen() & 0xff for _ in range(8))
    if ks[:5] == target0:
        print('HIT mt19937 and_ff seed', name, s)

# ---- ChaCha20 / Salsa20 with derived keys ----
keymats = []
for name, m in [('elfstudy', b'elfstudy'), ('ELFStudy', b'ELFStudy'), ('142', b'1.4.2'),
                ('whole', d), ('head', d[:0x739a]), ('bid', d[0x350:0x364])]:
    keymats.append((name + ':md5', hashlib.md5(m).digest()))
    keymats.append((name + ':sha256', hashlib.sha256(m).digest()))
    keymats.append((name + ':raw16', m[:16].ljust(16, b'\0')))
    keymats.append((name + ':raw32', m[:32].ljust(32, b'\0')))

for kname, key in keymats:
    for nonce in (b'\0' * 8, b'\0' * 12, blob[:8], blob[:12], d[:8], d[:12]):
        try:
            if len(key) == 32:
                c = ChaCha20.new(key=key, nonce=nonce)
                p = c.decrypt(blob[:16])
                if p[:5] == crib:
                    print('HIT chacha', kname, nonce.hex(), p)
                c = Salsa20.new(key=key, nonce=nonce[:8])
                p = c.decrypt(blob[:16])
                if p[:5] == crib:
                    print('HIT salsa', kname, nonce.hex(), p)
        except Exception as e:
            pass
print('done')
