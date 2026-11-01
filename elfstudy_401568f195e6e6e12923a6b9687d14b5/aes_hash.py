import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter

d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]
crib = b'flag{'

def pr(b):
    return sum(1 for c in b if 32 <= c < 127) / len(b)

materials = {
    'whole': d,
    'head': d[:0x739a],
    'blob': blob,
    'text': d[0x2540:0x7317],
    'rodata': d[0x8000:0x8500],
    'buildid': d[0x350:0x350 + 20],
    'shdrs': d[0xa168:],
    'gap1': d[0x1988:0x1d40],
}
keys = []
for name, m in materials.items():
    for h in ('md5', 'sha1', 'sha256', 'sha512'):
        dg = hashlib.new(h, m).digest()
        for n in (16, 32):
            if len(dg) >= n:
                keys.append((f'{h}({name})', dg[:n]))

hits = []
for kname, key in keys:
    for label, ct, mode in [
        ('ECB blk0', blob[:16], 'ecb0'),
        ('ECB blk1', blob[16:32], 'ecb1'),
        ('CBC iv0 blk0', blob[:16], 'cbc0'),
        ('CBC iv=hdr blk1', blob[16:32], 'cbc1'),
    ]:
        if mode == 'ecb0' or mode == 'ecb1' or mode == 'cbc0':
            c = AES.new(key, AES.MODE_ECB)
            p = c.decrypt(ct)
        else:
            c = AES.new(key, AES.MODE_ECB)
            p = bytes(a ^ b for a, b in zip(c.decrypt(ct), blob[:16]))
        if p[:5] == crib or pr(p) == 1.0:
            hits.append((kname, label, p))
    # CTR variants
    for nl, nv in ((8, blob[:8]), (12, blob[:12])):
        try:
            ctr = Counter.new(128 - nl * 8, prefix=nv, initial_value=0)
            c = AES.new(key, AES.MODE_CTR, counter=ctr)
            p = c.decrypt(blob[nl:nl + 16])
        except Exception:
            continue
        if p[:5] == crib:
            hits.append((kname, f'CTR nonce{nl}', p))
    # CTR with zero counter, full blob
    try:
        ctr = Counter.new(128, initial_value=0)
        c = AES.new(key, AES.MODE_CTR, counter=ctr)
        p = c.decrypt(blob[:32])
    except Exception:
        p = b''
    if p and (p[:5] == crib or pr(p) == 1.0):
        hits.append((kname, 'CTR ctr0', p))

print('hits:', len(hits))
for h in hits[:20]:
    print(h)
