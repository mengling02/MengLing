from capstone import *
from capstone.x86 import *
from collections import defaultdict

d = open('elfstudy','rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

g = defaultdict(list)
for i in md.disasm(d[0x2540:0x7317], 0x2540):
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            tgt = i.address + i.size + op.mem.disp
            if 0xa000 <= tgt < 0x1b340:
                g[tgt].append((i.address, i.mnemonic + ' ' + i.op_str))
for t in sorted(g):
    print(f'{t:#06x} x{len(g[t])}')
    for a, ins in g[t]:
        print(f'    {a:#06x} {ins}')
