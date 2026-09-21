import pymupdf, re, os

PDF = "2608.30574.pdf"
OUT = "C:/WorkBuddy/EveryDayPaper/20_Research/Papers/images"
doc = pymupdf.open(PDF)

# ---- collect all image bboxes + vector drawing bboxes per page ----
def page_regions(page):
    rects = []
    for info in page.get_image_info():
        b = info["bbox"]
        w, h = b[2]-b[0], b[3]-b[1]
        if w > 8 and h > 8:            # ignore hairlines
            rects.append(pymupdf.Rect(b))
    for d in page.get_drawings():
        r = d["rect"]
        if r.width > 6 and r.height > 6 and r.width < 560:
            rects.append(pymupdf.Rect(r))
    return rects

def cluster(rects, gap=14):
    """merge overlapping/nearby rects into groups"""
    groups = []
    for r in sorted(rects, key=lambda x: (round(x.y0, 1), x.x0)):
        placed = False
        for g in groups:
            gg = g["rect"] + (-gap, -gap, gap, gap)
            if gg.intersects(r):
                g["rect"] = g["rect"] | r
                placed = True
                break
        if not placed:
            groups.append({"rect": pymupdf.Rect(r)})
    # second pass to merge groups that now touch
    changed = True
    while changed:
        changed = False
        for i in range(len(groups)):
            for j in range(i+1, len(groups)):
                a = groups[i]["rect"] + (-gap, -gap, gap, gap)
                if a.intersects(groups[j]["rect"]):
                    groups[i]["rect"] = groups[i]["rect"] | groups[j]["rect"]
                    groups.pop(j); changed = True; break
            if changed: break
    return [g["rect"] for g in groups]

# ---- captions with page + y ----
cap_re = re.compile(r"^\s*(Fig\.\s*\d+|TABLE\s+[IVX]+)\s*[:.]", re.I)
caps = []
for pi, page in enumerate(doc):
    for b in page.get_text("blocks"):
        t = b[4].strip()
        if cap_re.match(t):
            caps.append((pi, b[1], b[3], t.replace("\n", " ")))

def label_for(pi, ymid):
    """caption whose y is closest to (and just below) the figure"""
    best, bd = None, 1e9
    for cpi, cy0, cy1, txt in caps:
        d = abs(cy0 - ymid)
        if d < bd:
            bd, best = d, (txt, d)
    return best[0] if best else "?"

def slug(txt):
    m = re.match(r"(Fig\.\s*\d+|TABLE\s+[IVX]+)", txt)
    return m.group(1).replace(".", "").replace(" ", "").lower()

NAMED = {
    "fig1":  "fig1_frequency_support_curve",
    "fig2":  "fig2_gfl_grid_support_control_scheme",
    "fig3":  "fig3_gfl_dynamic_grid_testbench",
    "fig4":  "fig4_modal_analysis_pll_bandwidth",
    "fig5":  "fig5_dominant_eigenvalues_reduced_bw",
    "fig6":  "fig6_infinite_bus_dominant_eigenvalues",
    "fig7":  "fig7_simulation_benchmark",
    "fig8":  "fig8_voltage_sag_duration",
    "fig9":  "fig9_proposed_rsu_pll",
    "fig10": "fig10_experimental_chil_benchmark",
    "fig11": "fig11_srf_vs_proposed_pll_response",
    "fig12": "fig12_integral_gain_tampering_detection",
    "fig13": "fig13_pi_gain_tampering_detection",
    "fig14": "fig14_proportional_gain_tampering_detection",
    "fig15": "fig15_unbalanced_distorted_grid_response",
    "fig16": "fig16_proportional_tampering_unbalanced_grid",
}

for pi, page in enumerate(doc):
    regs = cluster(page_regions(page))
    for r in regs:
        if r.width < 70 or r.height < 45:
            continue
        if r.height > 700:      # full-page artifact
            continue
        lbl = label_for(pi, r.y1)
        key = slug(lbl)
        name = NAMED.get(key, f"p{pi+1}_{key}")
        fn = f"{name}.png"
        path = os.path.join(OUT, fn)
        if os.path.exists(path) and os.path.getsize(path) > 40000:
            continue
        pix = page.get_pixmap(clip=r + (-4, -4, 4, 4), dpi=240)
        pix.save(path)
        print(f"p{pi+1} {fn}  {pix.width}x{pix.height}  (label {lbl[:60]})")
