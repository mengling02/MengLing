import string
d = open('elfstudy','rb').read()
blob = d[0x739a:0x76c6]

def show(tag, data):
    txt = ''.join(chr(c) if 32 <= c < 127 else '.' for c in data)
    ratio = sum(1 for c in data if 32 <= c < 127) / len(data)
    print(f'{tag:30s} r={ratio:.2f} {txt[:90]}')

regions = {
    'rela_copy': d[0x76c6:0x7a6e],
    'rodata': d[0x8000:0x8500],
    'text': d[0x2540:0x7317],
    'dynstr': d[0x9b0:0x9b0+0x82c],
    'elfhdr': d[0:64],
    'shdr': d[0xa168:],
    'gap1': d[0x1988:0x1d40],
    'fini': d[0x7318:0x7325],
}
for name, r in regions.items():
    if len(r) < len(blob):
        r = (r * (len(blob)//len(r)+1))[:len(blob)]
    else:
        r = r[:len(blob)]
    out = bytes(a ^ b for a, b in zip(blob, r))
    show('XOR ' + name, out)

# XOR blob with itself shifted
for sh in (1, 2, 4, 8, 16):
    out = bytes(blob[i] ^ blob[i-sh] for i in range(sh, len(blob)))
    show(f'XOR self shift{sh}', out)
