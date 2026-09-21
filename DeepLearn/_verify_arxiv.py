"""批量核验所有 arXiv 编号是否与文档中标注的题名一致。用完即删。"""
import glob
import io
import os
import re
import ssl
import time
import urllib.request
import xml.etree.ElementTree as ET

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

ROOT = r"C:\WorkBuddy\DeepLearn"
FILES = sorted(glob.glob(os.path.join(ROOT, "*.md"))) + \
        sorted(glob.glob(os.path.join(ROOT, "docs", "*.md"))) + \
        sorted(glob.glob(os.path.join(ROOT, "论文精读", "*.md")))

# 收集 (id, 文件, 行号, 该行原文)
found = {}
pat = re.compile(r"arxiv\.org/abs/(\d{4}\.\d{4,5})")
for f in FILES:
    for i, line in enumerate(io.open(f, encoding="utf-8"), 1):
        for m in pat.finditer(line):
            found.setdefault(m.group(1), []).append(
                (os.path.relpath(f, ROOT), i, line.strip()))

ids = sorted(found)
print(f"共 {len(ids)} 个唯一 arXiv 编号，开始向 arXiv API 查询…\n")

# 批量查询（arXiv API 建议每次 <= 100 个）
titles = {}
BATCH = 20
for k in range(0, len(ids), BATCH):
    chunk = ids[k:k + BATCH]
    url = ("https://export.arxiv.org/api/query?id_list=" + ",".join(chunk)
           + "&max_results=100")
    req = urllib.request.Request(url, headers={
        "User-Agent": "DeepLearn-DocAudit/1.0 (mailto:audit@example.com)"})
    for attempt in range(4):
        try:
            raw = urllib.request.urlopen(req, timeout=90, context=CTX).read()
            root = ET.fromstring(raw)
            ns = {"a": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("a:entry", ns):
                eid = entry.find("a:id", ns).text.rsplit("/", 1)[-1]
                base = eid.split("v")[0]
                t = " ".join(entry.find("a:title", ns).text.split())
                titles[base] = t
            break
        except Exception as e:
            if attempt == 3:
                print(f"批次 {k // BATCH + 1} 查询失败: {e}")
            else:
                time.sleep(20 * (attempt + 1))
    time.sleep(15)  # 遵守 arXiv API 的礼貌间隔

print(f"成功取回 {len(titles)} 条标题\n")
print("=" * 100)

# 判断题名是否与文档描述相符：取文档行里 *斜体* 或 **粗体** 里的英文题名做模糊比对
def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())

bad = []
for aid in ids:
    real = titles.get(aid)
    if real is None:
        bad.append((aid, found[aid][0][0], "API 未返回（可能编号不存在）", ""))
        continue
    rn = norm(real)
    for rel, ln, line in found[aid]:
        # 抽出行内所有英文题名候选（*...* 之间）
        cands = re.findall(r"\*([A-Za-z][^*]{12,})\*", line)
        if not cands:
            cands = re.findall(r"\*\*([A-Za-z][^*]{12,})\*\*", line)
        if not cands:
            continue
        cn = norm(cands[0])
        # 允许前缀/子串匹配（题名可能被截断或用了 arXiv 版标题）
        if cn[:40] not in rn and rn[:40] not in cn:
            bad.append((aid, rel, real, cands[0]))

print(f"疑似不匹配 {len(bad)} 条")
print("=" * 100)
for aid, rel, real, claimed in bad:
    print(f"\narXiv:{aid}   [{rel}]")
    print(f"   文档写的 : {claimed[:90]}")
    print(f"   实际是   : {real[:90]}")
