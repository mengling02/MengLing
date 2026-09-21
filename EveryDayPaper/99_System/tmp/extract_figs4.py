import pymupdf, os, shutil

doc = pymupdf.open("2608.30574.pdf")
OUT = "C:/WorkBuddy/EveryDayPaper/20_Research/Papers/images"

# ---- 1) direct high-fidelity bitmaps, correctly named ----
BITMAPS = {
    564: "fig1_frequency_support_curve",          # p3
    565: "fig2_gfl_grid_support_control_scheme",  # p4
    567: "fig3_gfl_dynamic_grid_testbench",       # p5
    579: "fig9_proposed_rsu_pll",                 # p9
    582: "fig10_experimental_chil_benchmark",     # p11
}
for xref, name in BITMAPS.items():
    im = doc.extract_image(xref)
    fn = os.path.join(OUT, f"{name}.{im['ext']}")
    open(fn, "wb").write(im["image"])
    print(f"[bitmap] {name}.{im['ext']}  {im['width']}x{im['height']}")

# ---- 2) caption-anchored band renders ----
BANDS = [
    (5,  45,  45, 570, 188, "fig4_modal_analysis_pll_bandwidth"),      # p6 top, 2 panels
    (6,  45,  45, 305, 170, "fig5_dominant_eigenvalues_reduced_bw"),   # p7 left
    (6, 310,  45, 570, 170, "fig6_infinite_bus_dominant_eigenvalues"), # p7 right
]
for pi, x0, y0, x1, y1, name in BANDS:
    pix = doc[pi].get_pixmap(clip=pymupdf.Rect(x0, y0, x1, y1), dpi=250)
    pix.save(os.path.join(OUT, name + ".png"))
    print(f"[band] {name}.png  {pix.width}x{pix.height}")

# ---- 3) remove the mis-named leftovers ----
for junk in ["fig2_gfl_grid_support_control_scheme.png"]:
    p = os.path.join(OUT, junk)
    # only remove if it's the stale duplicate (bitmap version now saved as .png too)
for junk in ["fig4_modal_analysis_pll_bandwidth.png", "fig5_dominant_eigenvalues_reduced_bw.png",
             "fig10_experimental_chil_benchmark.png", "fig1_frequency_support_curve.png"]:
    pass

print("\n--- final image inventory ---")
for f in sorted(os.listdir(OUT)):
    if f.startswith(("fig", "cybergrid", "cycle", "nodecrit")):
        print(f, os.path.getsize(os.path.join(OUT, f)) // 1024, "KB")
