import string
d = open('elfstudy','rb').read()
blob = d[0x739a:0x76c6]

def bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        v = 0
        for b in bits[i:i+8]:
            v = (v << 1) | b
        out.append(v)
    return bytes(out)

def show(tag, data):
    txt = ''.join(chr(c) if 32 <= c < 127 else '.' for c in data)
    ratio = sum(1 for c in data if 32 <= c < 127) / len(data)
    print(f'{tag:28s} ratio={ratio:.2f} {txt[:100]}')

print('len', len(blob))
for pos in range(8):
    bits = [(c >> pos) & 1 for c in blob]
    show(f'bit{pos} msb-first', bits_to_bytes(bits))
    rev = []
    for i in range(0, len(bits) - 7, 8):
        v = 0
        for j, b in enumerate(bits[i:i+8]):
            v |= b << j
        rev.append(v)
    show(f'bit{pos} lsb-first', bytes(rev))

# also try the whole gap incl rela copy
blob2 = d[0x7396:0x7a6e]
print('len2', len(blob2))
for pos in [0, 7]:
    bits = [(c >> pos) & 1 for c in blob2]
    show(f'ALL bit{pos} msb-first', bits_to_bytes(bits))
