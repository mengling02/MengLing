import string
d = open('elfstudy','rb').read()
blob = d[0x739a:0x76c6]

def rev_bits(b):
    return int('{:08b}'.format(b)[::-1], 2)

def show(tag, data):
    txt = ''.join(chr(c) if 32 <= c < 127 else '.' for c in data)
    ratio = sum(1 for c in data if 32 <= c < 127) / len(data)
    print(f'{tag:24s} r={ratio:.2f} {txt[:80]}')

show('raw', blob)
show('not', bytes(c ^ 0xff for c in blob))
show('nibble swap', bytes(((c & 0xf) << 4) | (c >> 4) for c in blob))
show('bit reverse', bytes(rev_bits(c) for c in blob))
show('add 0x80', bytes((c + 0x80) & 0xff for c in blob))
show('reversed', blob[::-1])

for r in range(1, 8):
    out = bytes((((c << r) | (c >> (8 - r))) & 0xff) for c in blob)
    show(f'rol{r}', out)
    out = bytes((((c >> r) | (c << (8 - r))) & 0xff) for c in blob)
    show(f'ror{r}', out)

# subtract index / add index
show('xor idx', bytes(c ^ (i & 0xff) for i, c in enumerate(blob)))
show('sub idx', bytes((c - i) & 0xff for i, c in enumerate(blob)))
show('add idx', bytes((c + i) & 0xff for i, c in enumerate(blob)))
show('xor idx*2', bytes(c ^ ((i * 2) & 0xff) for i, c in enumerate(blob)))
show('xor idx^0x55', bytes(c ^ ((i ^ 0x55) & 0xff) for i, c in enumerate(blob)))
show('xor (i*0x9e)>>3', bytes(c ^ (((i * 0x9e) >> 3) & 0xff) for i, c in enumerate(blob)))
show('sub (i*0x9e)>>3', bytes((c - ((i * 0x9e) >> 3)) & 0xff for i, c in enumerate(blob)))
