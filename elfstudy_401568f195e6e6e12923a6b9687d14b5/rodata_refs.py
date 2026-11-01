from capstone import *
from capstone.x86 import *

d = open('elfstudy','rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

def cstr(addr):
    if not (0 <= addr < len(d)):
        return '<out>'
    e = d.find(b'\0', addr)
    s = d[addr:e]
    try:
        return s.decode('ascii')
    except Exception:
        return repr(s)

rows = []
for i in md.disasm(d[0x2540:0x7317], 0x2540):
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            tgt = i.address + i.size + op.mem.disp
            if 0x8000 <= tgt < 0x8500:
                rows.append((i.address, tgt, cstr(tgt), i.mnemonic + ' ' + i.op_str))

# group by target
from collections import defaultdict
g = defaultdict(list)
for a, t, s, ins in rows:
    g[(t, s)].append(a)
for (t, s), addrs in sorted(g.items()):
    print(f'{t:#06x} {s!r:60s} used at ' + ','.join(hex(x) for x in addrs))
