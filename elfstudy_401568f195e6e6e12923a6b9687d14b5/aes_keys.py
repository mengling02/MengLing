from Crypto.Cipher import AES
import string

d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]
crib = b'flag{'

def printable_ratio(b):
    return sum(1 for c in b if 32 <= c < 127) / len(b)

hits = []
N = len(d)
for klen, mode_name in ((16, 'AES128'), (32, 'AES256')):
    for off in range(N - klen):
        key = d[off:off + klen]
        # 1) ECB on first block
        c = AES.new(key, AES.MODE_ECB)
        p = c.decrypt(blob[:16])
        if p[:5] == crib or printable_ratio(p) == 1.0:
            hits.append((f'{mode_name} ECB blk0', off, p))
        # 2) CBC iv=0 on first block (same as ECB) -> skip
        # 3) CBC: iv = blob[0:16], ct = blob[16:32]
        c = AES.new(key, AES.MODE_ECB)
        p = bytes(a ^ b for a, b in zip(c.decrypt(blob[16:32]), blob[:16]))
        if p[:5] == crib or printable_ratio(p) == 1.0:
            hits.append((f'{mode_name} CBC iv=hdr', off, p))
        # 4) CTR: keystream = E(ctr=0..) with nonce = blob[0:8], counter 8B
        c = AES.new(key, AES.MODE_CTR, nonce=blob[:8], initial_value=0)
        p = c.decrypt(blob[8:24])
        if p[:5] == crib:
            hits.append((f'{mode_name} CTR nonce8', off, p))
        c = AES.new(key, AES.MODE_CTR, nonce=blob[:12], initial_value=0)
        p = c.decrypt(blob[12:28])
        if p[:5] == crib:
            hits.append((f'{mode_name} CTR nonce12', off, p))
        c = AES.new(key, AES.MODE_CTR, nonce=b'', initial_value=0)
        p = c.decrypt(blob[:16])
        if p[:5] == crib:
            hits.append((f'{mode_name} CTR ctr0', off, p))

print('hits:', len(hits))
for h in hits[:20]:
    print(h)
