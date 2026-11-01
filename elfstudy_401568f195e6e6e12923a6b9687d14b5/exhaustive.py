d = open('elfstudy', 'rb').read()
blob = d[0x739a:0x76c6]
PR = set(range(32, 127))

for L in range(1, 65):
    cols_ok = []
    possible = True
    for c in range(L):
        col = blob[c::L]
        ks = [k for k in range(256) if all((b ^ k) in PR for b in col)]
        if not ks:
            possible = False
            break
        cols_ok.append(ks)
    if possible:
        print(f'L={L}: POSSIBLE, candidates per column: {[len(x) for x in cols_ok]}')
        # show first combination
        key = bytes(x[0] for x in cols_ok)
        out = bytes(c ^ key[i % L] for i, c in enumerate(blob))
        print('   key0=', key.hex(), out[:60])
print('scan done')
