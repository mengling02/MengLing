import pymupdf, os

doc = pymupdf.open("2608.30574.pdf")
OUT = "C:/WorkBuddy/EveryDayPaper/20_Research/Papers/images"

BANDS = [
    # (page_idx, x0, y0, x1, y1, name)
    (6, 310, 225, 570, 356, "fig7_simulation_benchmark"),
    (7,  45,  45, 570, 300, "fig8_voltage_sag_duration"),
    (10, 310,  45, 570, 432, "fig11_srf_vs_proposed_pll_response"),
    (11, 45,   45, 305, 432, "fig12_integral_gain_tampering_detection"),
    (11, 45,  446, 305, 692, "fig13_pi_gain_tampering_detection"),
    (11, 310,  45, 570, 296, "fig14_proportional_gain_tampering_detection"),
    (12, 45,   45, 305, 470, "fig15_unbalanced_distorted_grid_response"),
    (12, 310,  45, 570, 434, "fig16_proportional_tampering_unbalanced_grid"),
]

for pi, x0, y0, x1, y1, name in BANDS:
    page = doc[pi]
    r = pymupdf.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(clip=r, dpi=250)
    fn = os.path.join(OUT, name + ".png")
    pix.save(fn)
    print(f"{name}.png  {pix.width}x{pix.height}  {os.path.getsize(fn)//1024}KB")
