d = open('elfstudy','rb').read()

PRINTABLE = set(range(32, 127))

# precompute: for each byte value, the set of k such that (byte ^ k) printable
xormask = []
for b in range(256):
    m = 0
    for k in range(256):
        if (b ^ k) in PRINTABLE:
            m |= 1 << k
    xormask.append(m)

addmask = []
for b in range(256):
    m = 0
    for k in range(256):
        if ((b + k) & 0xff) in PRINTABLE:
            m |= 1 << k
    addmask.append(m)

def scan(masks, name, minlen=8):
    res = []
    n = len(d)
    for i in range(n - minlen + 1):
        m = (1 << 256) - 1
        for j in range(minlen):
            m &= masks[d[i + j]]
            if m == 0:
                break
        if m:
            # try each key, extend
            kk = m
            while kk:
                low = kk & -kk
                k = low.bit_length() - 1
                kk ^= low
                ln = 0
                while i + ln < n and ((d[i+ln] ^ k) if name == 'xor' else ((d[i+ln] + k) & 0xff)) in PRINTABLE:
                    ln += 1
                if ln >= minlen:
                    s = bytes((d[i+t] ^ k) if name == 'xor' else ((d[i+t] + k) & 0xff) for t in range(ln))
                    res.append((ln, i, k, s))
    res.sort(reverse=True)
    print(f'== {name}: {len(res)} hits')
    for ln, i, k, s in res[:12]:
        print(f'  off={i:#06x} key={k:#04x} len={ln} {s[:70]!r}')

scan(xormask, 'xor', 10)
scan(addmask, 'add', 10)
