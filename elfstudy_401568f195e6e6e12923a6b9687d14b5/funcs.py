from capstone import *
from capstone.x86 import *

d = open('elfstudy','rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

insns = list(md.disasm(d[0x2540:0x7317], 0x2540))
# function starts = endbr64
starts = [i.address for i in insns if i.mnemonic == 'endbr64']
print('endbr count', len(starts))

targets = set()
for i in insns:
    if i.mnemonic in ('call', 'jmp', 'je', 'jne', 'jz', 'jnz', 'ja', 'jb', 'jae', 'jbe',
                      'jg', 'jl', 'jge', 'jle', 'js', 'jns', 'jo', 'jno', 'jp', 'jnp',
                      'jecxz', 'jrcxz'):
        if i.operands and i.operands[0].type == X86_OP_IMM:
            targets.add(i.operands[0].imm)

# also rip-relative lea targets (function pointers)
for i in insns:
    for op in i.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            t = i.address + i.size + op.mem.disp
            if 0x2540 <= t < 0x7317:
                targets.add(t)

print('--- functions never targeted ---')
for s in starts:
    if s not in targets:
        print(hex(s))
print()
print('--- all endbr64 starts ---')
print(' '.join(hex(s) for s in starts))
