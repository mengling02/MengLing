from capstone import *
from capstone.x86 import *
import sys

d = open('elfstudy','rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

lo, hi = 0x7325, 0x8000
hits = []
for i in md.disasm(d[0x2540:0x7317], 0x2540):
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            tgt = i.address + i.size + op.mem.disp
            if lo <= tgt < hi:
                hits.append((i.address, tgt, i.mnemonic, i.op_str))
            elif 0x8000 <= tgt < 0x8520:
                pass
for h in hits:
    print(f'{h[0]:#06x} -> {h[1]:#06x}  {h[2]} {h[3]}')
print('total hits', len(hits))
