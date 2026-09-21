import os, ssl, time, json, sys
os.environ.setdefault("ARXIV_INSECURE_SSL", "1")
if os.environ.get("ARXIV_INSECURE_SSL") == "1":
    _ctx = ssl.create_default_context()
    _ctx.check_hostname = False
    _ctx.verify_mode = ssl.CERT_NONE
    ssl._create_default_https_context = lambda: _ctx

import arxiv

QUERIES = [
    ('all:"false data injection" AND all:"power"', 40),
    ('abs:"power grid" AND abs:"cyber"', 40),
    ('abs:"smart grid" AND abs:"attack"', 40),
    ('abs:"state estimation" AND abs:"attack"', 40),
    ('abs:"microgrid" AND abs:"security"', 30),
    ('abs:"cyber-physical" AND abs:"power system"', 40),
    ('abs:"substation" AND abs:"intrusion"', 30),
    ('abs:"power system" AND abs:"anomaly detection"', 40),
    ('abs:"inverter-based" AND abs:"stability"', 30),
    ('abs:"power system" AND abs:"resilience"', 30),
]

client = arxiv.Client(page_size=100, delay_seconds=4.0, num_retries=4)
seen = {}
for q, n in QUERIES:
    try:
        s = arxiv.Search(query=q, max_results=n,
                         sort_by=arxiv.SortCriterion.SubmittedDate)
        cnt = 0
        for r in client.results(s):
            aid = r.get_short_id()
            if aid not in seen:
                seen[aid] = {
                    "arxiv_id": aid,
                    "title": r.title.strip().replace("\n", " "),
                    "published": r.published.strftime("%Y-%m-%d"),
                    "updated": r.updated.strftime("%Y-%m-%d"),
                    "categories": r.categories,
                    "summary": r.summary.strip().replace("\n", " "),
                    "authors": [a.name for a in r.authors],
                    "pdf_url": r.pdf_url,
                    "url": r.entry_id,
                    "query": q,
                }
            cnt += 1
        print(f"OK  [{cnt:3d}] {q}", flush=True)
    except Exception as e:
        print(f"ERR [{q}] {type(e).__name__}: {str(e)[:120]}", flush=True)
    time.sleep(3)

items = sorted(seen.values(), key=lambda x: x["published"], reverse=True)
json.dump(items, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("TOTAL UNIQUE:", len(items))
for it in items[:60]:
    print(it["published"], it["arxiv_id"], "|", it["title"][:105])
