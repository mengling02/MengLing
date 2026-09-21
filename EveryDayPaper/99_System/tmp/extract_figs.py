import pymupdf, re, os, json

PDF = "2608.30574.pdf"
OUT = "C:/WorkBuddy/EveryDayPaper/20_Research/Papers/images"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

# ---------- 1) direct bitmap extraction for large single figures ----------
TARGETS = {
    564: "fig2_gfl_grid_support_control_scheme",
    565: "fig4_modal_analysis_pll_bandwidth",
    567: "fig5_dominant_eigenvalues_reduced_bw",
    575: "fig7_simulation_benchmark",
    579: "fig9_proposed_rsu_pll",
    582: "fig10_experimental_chil_benchmark",
}
for xref, name in TARGETS.items():
    try:
        base = doc.extract_image(xref)
        ext = base["ext"]
        fn = f"{name}.{ext}"
        with open(os.path.join(OUT, fn), "wb") as f:
            f.write(base["image"])
        print(f"[bitmap] {fn}  {base['width']}x{base['height']}  {len(base['image'])//1024}KB")
    except Exception as e:
        print(f"[bitmap ERR] {xref} {name}: {e}")

# ---------- 2) locate captions & figure blocks (text coords) ----------
cap_re = re.compile(r"^\s*(Fig\.\s*\d+|TABLE\s+[IVX]+)\s*[:.]", re.I)
blocks = []  # (page_idx, caption_text, y_top_of_caption, bbox)
for pi, page in enumerate(doc):
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, txt = b[0], b[1], b[2], b[3], b[4]
        t = txt.strip()
        if cap_re.match(t):
            blocks.append((pi, t.replace("\n", " ")[:110], y0, (x0, y0, x1, y1)))

print("\n--- captions found ---")
for pi, t, y, bb in blocks:
    print(f"p{pi+1}  y={y:7.1f}  {t}")

# ---------- 3) render figure regions by clip ----------
# map: caption key -> (output name, page_idx, top_y)
def render(pi, y_top, y_bot, name, x0=40, x1=572, dpi=260):
    page = doc[pi]
    r = pymupdf.Rect(x0, y_top, x1, y_bot)
    pix = page.get_pixmap(clip=r, dpi=dpi)
    fn = f"{name}.png"
    pix.save(os.path.join(OUT, fn))
    print(f"[clip] {fn}  {pix.width}x{pix.height}")
    return fn

# gather page heights
H = [doc[i].rect.height for i in range(len(doc))]

# Fig 1 (frequency-support curve) - p2 top area, caption y
caps = {(pi, t.split(":")[0].strip().lower().replace(" ", "")): (y, bb) for pi, t, y, bb in blocks}

def find(pageno, label):
    for pi, t, y, bb in blocks:
        if pi == pageno - 1 and t.lower().startswith(label.lower()):
            return y, bb
    return None, None

# Fig 1 on p2
y, bb = find(2, "Fig. 1")
if y: render(1, 55, y - 2, "fig1_frequency_support_curve")

# Fig 3 on p4 (caption near bottom of p4)
y, bb = find(4, "Fig. 3")
if y: render(3, H[3]*0.55, y - 2, "fig3_gfl_dynamic_grid_testbench")

# Fig 8 (two panels a/b) p7
y, bb = find(7, "Fig. 8")
if y: render(6, H[6]*0.42, y - 2, "fig8_voltage_sag_duration")

# Fig 11 (3 panels) p11
y, bb = find(11, "Fig. 11")
if y: render(10, H[10]*0.40, y - 2, "fig11_srf_vs_proposed_pll_response")

# Fig 12 (5 panels) p11
y, bb = find(11, "Fig. 12")
if y: render(10, H[10]*0.66, y - 2, "fig12_integral_gain_tampering_detection")

# Fig 13 (4 panels) p12
y, bb = find(12, "Fig. 13")
if y: render(11, H[11]*0.40, y - 2, "fig13_pi_gain_tampering_detection")

# Fig 16 (5 panels) p13
y, bb = find(13, "Fig. 16")
if y: render(12, H[12]*0.35, y - 2, "fig16_proportional_tampering_unbalanced_grid")

print("\n--- files ---")
for f in sorted(os.listdir(OUT)):
    print(f, os.path.getsize(os.path.join(OUT, f))//1024, "KB")
