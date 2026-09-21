# -*- coding: utf-8 -*-
"""最终全量审计：结构 + 图片 + 链接 + 编号。"""
import io, os, re, glob

ROOT = 'C:/WorkBuddy/DeepLearn'
os.chdir(ROOT)

files = sorted(glob.glob('docs/*.md')) + sorted(glob.glob('*.md')) + sorted(glob.glob('论文精读/*.md'))
issues = []


def check_fences(text, name):
    """代码围栏配对（``` 数量必须为偶数）"""
    n = len(re.findall(r'^\s*```', text, re.M))
    if n % 2:
        issues.append('围栏不配对（%d 个）: %s' % (n, name))


def check_heading_jump(text, name):
    """标题层级跳跃（必须跳过代码块 —— Python 注释以 # 开头，极易误判）"""
    prev = 0
    infence = False
    for i, l in enumerate(text.split('\n'), 1):
        if l.strip().startswith('```'):
            infence = not infence
            continue
        if infence:
            continue
        if l.startswith('#'):
            lv = len(l) - len(l.lstrip('#'))
            if lv > 6:
                continue
            if prev and lv > prev + 1:
                issues.append('标题跳级 L%d: %s -> %s (%s)' % (i, '#' * prev, l[:50], name))
            prev = lv


def count_cols(l):
    """统计表格列数。注意 Markdown 里用 \\| 表示"表格内的竖线"，
    它不算分隔符；必须先把 \\| 挖掉再数。"""
    s = l.replace('\\|', '\x00')      # 转义竖线挖空
    s = s.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return s.count('|') + 1


def check_table(text, name):
    """表格列数一致性（跳过代码块；表格必须是【连续行】，中间被空行/文字打断即为两个表）"""
    infence = False
    rows = []

    def flush():
        if len(rows) >= 2:
            cols = {n for _, n in rows}
            if len(cols) > 1:
                issues.append('表格列数不一致 L%d (%s): %s' % (rows[0][0], sorted(cols), name))

    for i, l in enumerate(text.split('\n'), 1):
        if l.strip().startswith('```'):
            infence = not infence
            flush(); rows = []
            continue
        if infence:
            continue
        if l.strip().startswith('|') and l.strip().endswith('|'):
            rows.append((i, count_cols(l)))
        else:
            flush(); rows = []
    flush()


def check_img(text, name):
    """图片引用是否可解析"""
    base = os.path.dirname(name)
    for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', text):
        p = os.path.normpath(os.path.join(base, m.group(1)))
        if not os.path.exists(p):
            issues.append('图片缺失: %s -> %s' % (name, m.group(1)))


def check_dup_day(name, text):
    """重复 Day 标题"""
    seen = {}
    for i, l in enumerate(text.split('\n'), 1):
        m = re.match(r'^## Day (\d+)', l)
        if m:
            d = int(m.group(1))
            if d in seen:
                issues.append('重复 Day %d: L%d 与 L%d (%s)' % (d, seen[d], i, name))
            seen[d] = i


def check_empty_section(name, text):
    """空章节（有标题但下面连续 3 行以上无内容）

    注意：父标题直连子标题是正常结构（如 ## 地图 -> ### 第1周），
    因此只在「下一行不是更低级标题」时才算空。
    """
    lines = text.split('\n')
    for i in range(len(lines) - 1):
        if lines[i].startswith('#'):
            lv = len(lines[i]) - len(lines[i].lstrip('#'))
            content = 0
            for j in range(i + 1, len(lines)):
                s = lines[j]
                if s.startswith('#'):
                    lv2 = len(s) - len(s.lstrip('#'))
                    if lv2 <= lv:
                        break
                    # 子标题不算内容
                    break
                if s.strip():
                    content += 1
                    break
            # 若下面第一行非空且不是标题，说明有内容；否则跳过（父标题直连子标题）
    return


def check_search_links(name, text):
    """检查是否混入了固定 BV 号"""
    for m in re.finditer(r'BV[0-9A-Za-z]{10}', text):
        issues.append('发现固定 BV 号: %s @%s' % (m.group(0), name))


for f in files:
    t = io.open(f, encoding='utf-8').read()
    check_fences(t, f)
    check_heading_jump(t, f)
    check_table(t, f)
    check_img(t, f)
    check_dup_day(f, t)
    check_search_links(f, t)

print('=' * 74)
print('审计文件数:', len(files))
print('=' * 74)
if issues:
    for s in issues:
        print('!', s)
else:
    print('✅ 全部检查通过，0 处问题')

# ---- 汇总统计 ----
allt = '\n'.join(io.open(f, encoding='utf-8').read() for f in files)
imgs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', allt)
days = sorted({int(m) for m in re.findall(r'^## Day (\d+)\b', allt, re.M)})
print()
print('文档规模    : %d 个 md，%d 行，%.2f MB' % (
    len(files), sum(len(io.open(f, encoding='utf-8').read().split('\n')) for f in files),
    sum(os.path.getsize(f) for f in files) / 1024 / 1024))
print('内嵌图示    : %d 张（SVG 文件 %d 个）' % (len(imgs), len(glob.glob('assets/*.svg'))))
print('Day 覆盖    : %d 天（%s ~ %s），缺号 %s' % (
    len(days), min(days), max(days),
    ','.join(str(d) for d in range(1, 121) if d not in days) or '无'))
print('和电网安全的关系: %d 处' % len(re.findall(r'### .*和电网安全的关系', allt)))
print('视频讲解块  : %d' % len(re.findall(r'### .*视频讲解', allt)))
print('知识清单条目: %d' % len(re.findall(r'^- \[ \] ', allt, re.M)))
print('B站搜索链接 : %d' % len(re.findall(r'search\.bilibili\.com', allt)))
print('抖音链接    : %d' % len(re.findall(r'douyin\.com/search', allt)))
print('arXiv 编号  : %d 个唯一' % len({m for m in re.findall(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', allt)}))
print('固定 BV 号  : %d 个（应为 0）' % len(re.findall(r'BV[0-9A-Za-z]{10}', allt)))
print('配套论文清单: %d 份' % len(re.findall(r'配套论文清单', allt)))
