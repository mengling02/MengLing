from capstone import *
from capstone.x86 import *
import sys

d = open('elfstudy','rb').read()
TEXT_LO, TEXT_HI = 0x2540, 0x7317
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

insn_at = {}
def decode(addr, limit=15):
    for i in md.disasm(d[addr:addr+limit], addr):
        return i
    return None

# pre-decode linearly for speed of lookup
linear = {}
for i in md.disasm(d[TEXT_LO:TEXT_HI], TEXT_LO):
    linear[i.address] = i

def get(addr):
    return linear.get(addr)

JUMP = {'jmp'}
COND = {'je','jne','jz','jnz','ja','jb','jae','jbe','jg','jl','jge','jle','js','jns','jo','jno','jp','jnp','jecxz','jrcxz'}
RET = {'ret','hlt','ud2','int3'}

seen = set()
work = [0x2e90, 0x2f70, 0x2f30, 0x2a50]
# also all endbr64 as potential entries
for a, i in linear.items():
    if i.mnemonic == 'endbr64':
        work.append(a)

while work:
    a = work.pop()
    while True:
        if a in seen:
            break
        i = get(a)
        if i is None:
            break
        seen.add(a)
        m = i.mnemonic
        nxt = a + i.size
        if m == 'call':
            if i.operands and i.operands[0].type == X86_OP_IMM:
                t = i.operands[0].imm
                if TEXT_LO <= t < TEXT_HI:
                    work.append(t)
            a = nxt
            continue
        if m in JUMP:
            if i.operands and i.operands[0].type == X86_OP_IMM:
                t = i.operands[0].imm
                if TEXT_LO <= t < TEXT_HI:
                    work.append(t)
            break
        elif m in COND:
            if i.operands and i.operands[0].type == X86_OP_IMM:
                t = i.operands[0].imm
                if TEXT_LO <= t < TEXT_HI:
                    work.append(t)
            a = nxt
        elif m in RET:
            break
        else:
            a = nxt

# report gaps in .text not covered
covered = sorted(seen)
gaps = []
prev_end = TEXT_LO
for a in covered:
    i = get(a)
    if a > prev_end:
        gaps.append((prev_end, a))
    prev_end = max(prev_end, a + i.size)
if prev_end < TEXT_HI:
    gaps.append((prev_end, TEXT_HI))

print('reachable insns', len(seen))
print('uncovered ranges:')
for a, b in gaps:
    if b - a >= 8:
        print(f'  {a:#06x}-{b:#06x} len={b-a:#x}')
        print('   ', d[a:b].hex(' '))
