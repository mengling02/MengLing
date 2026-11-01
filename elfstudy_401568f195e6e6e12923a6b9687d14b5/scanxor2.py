d = open('elfstudy','rb').read()
n = len(d)
PRINTABLE = set(range(32, 127))

xor_ok = [set(k for k in range(256) if (b ^ k) in PRINTABLE) for b in range(256)]
add_ok = [set(k for k in range(256) if ((b + k) & 0xff) in PRINTABLE) for b in range(256)]

def scan(table, name, minlen=10, maxhits=20):
    res = []
    n = len(d)
    i = 0
    while i <= n - minlen:
        s = table[d[i]]
        j = 1
        while j < minlen and s:
            s = s & table[d[i + j]]
            j += 1
        if s:
            for k in s:
                ln = minlen
                while i + ln < n:
                    b = d[i + ln]
                    v = (b ^ k) if name == 'xor' else ((b + k) & 0xff)
                    if v not in PRINTABLE:
                        break
                    ln += 1
                out = bytes(((d[i+t] ^ k) if name == 'xor' else ((d[i+t] + k) & 0xff)) for t in range(ln))
                res.append((ln, i, k, out))
            i += 1
        else:
            i += 1
        if len(res) > 5000:
            break
    res.sort(reverse=True)
    print(f'== {name}: {len(res)} hits')
    seen = set()
    shown = 0
    for ln, i, k, s in res:
        if i in seen:
            continue
        seen.add(i)
        print(f'  off={i:#06x} key={k:#04x} len={ln} {s[:70]!r}')
        shown += 1
        if shown >= maxhits:
            break

scan(xor_ok, 'xor', 10)
scan(add_ok, 'add', 10)
