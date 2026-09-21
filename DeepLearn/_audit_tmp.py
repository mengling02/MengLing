"""临时审计脚本：扫描 DeepLearn 全部 md 文件的结构性问题。用完即删。"""
import glob
import io
import os
import re

ROOT = r"C:\WorkBuddy\DeepLearn"


def check_table(tbl, rel, issues):
    """检查表头与分隔行列数是否一致。"""
    if len(tbl) < 2:
        return
    def ncols(s):
        return len([c for c in s.strip().strip("|").split("|")])
    head_i, head = tbl[0]
    sep_i, sep = tbl[1]
    if not re.match(r"^\s*\|[\s:|-]+\|\s*$", sep):
        return
    if ncols(head) != ncols(sep):
        issues.append(("表格列数不匹配", rel,
                       f"L{head_i}: 表头 {ncols(head)} 列 vs 分隔行 {ncols(sep)} 列"))


files = sorted(glob.glob(os.path.join(ROOT, "*.md"))) + \
        sorted(glob.glob(os.path.join(ROOT, "docs", "*.md"))) + \
        sorted(glob.glob(os.path.join(ROOT, "论文精读", "*.md")))

issues = []

for f in files:
    rel = os.path.relpath(f, ROOT)
    text = io.open(f, encoding="utf-8").read()
    lines = text.split("\n")

    # --- 1. 代码围栏配对 ---
    fence = sum(1 for s in lines if s.strip().startswith("```"))
    if fence % 2 != 0:
        issues.append(("围栏未闭合", rel, f"``` 出现 {fence} 次（奇数）"))

    # --- 2. 标题层级跳跃（跳过围栏内）---
    in_fence = False
    prev_level = 0
    for i, s in enumerate(lines, 1):
        if s.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6}) ", s)
        if m:
            lv = len(m.group(1))
            if prev_level and lv > prev_level + 1:
                issues.append(("标题跳级", rel, f"L{i}: {prev_level}级 → {lv}级 | {s[:50]}"))
            prev_level = lv

    # --- 3. 表格列数不一致 ---
    in_fence = False
    tbl = []
    for i, s in enumerate(lines, 1):
        if s.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if s.strip().startswith("|"):
            tbl.append((i, s))
        else:
            if len(tbl) >= 2:
                check_table(tbl, rel, issues)
            tbl = []
    if len(tbl) >= 2:
        check_table(tbl, rel, issues)

    # --- 4. 重复的 Day 标题 ---
    days = re.findall(r"^## (Day \d+) ", text, re.M)
    dup = {d for d in days if days.count(d) > 1}
    for d in dup:
        issues.append(("Day 重复", rel, d))

    # --- 5. emoji 乱码 / 替换字符 ---
    for bad in ["\ufffd", "â€", "Ã¤", "???"]:
        if bad in text:
            issues.append(("疑似乱码", rel, f"含 {bad!r}"))

    # --- 6. 空章节（标题后紧跟另一个标题）---
    in_fence = False
    for i in range(len(lines) - 2):
        if lines[i].strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r"^#{2,4} ", lines[i]) and lines[i + 1].strip() == "" and re.match(r"^#{2,4} ", lines[i + 2]):
            issues.append(("空章节", rel, f"L{i+1}: {lines[i][:45]}"))

    # --- 7. 相对链接目标是否存在 ---
    for m in re.finditer(r"\]\((?!https?://|#)([^)]+)\)", text):
        tgt = m.group(1)
        p = os.path.normpath(os.path.join(os.path.dirname(f), tgt))
        if not os.path.exists(p):
            issues.append(("相对链接失效", rel, tgt))


print("=" * 78)
print(f"审计范围：{len(files)} 个文件")
print("=" * 78)
if not issues:
    print("\n✅ 未发现结构性问题")
else:
    from collections import Counter
    print(f"\n共发现 {len(issues)} 处，按类型统计：")
    for k, v in Counter(i[0] for i in issues).most_common():
        print(f"  {k:<18} {v} 处")
    print()
    for typ, rel, detail in issues:
        print(f"[{typ}] {rel}\n    {detail}")
