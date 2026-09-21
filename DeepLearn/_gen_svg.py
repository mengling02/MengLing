"""生成 day61（电网=图）与 day37（状态估计 H 矩阵）两张 SVG。用完即删。"""
import io

BRANCHES = [(1,2),(1,5),(2,3),(2,4),(2,5),(3,4),(4,5),(4,7),(4,9),(5,6),
            (6,11),(6,12),(6,13),(7,8),(7,9),(9,10),(9,14),(10,11),(12,13),(13,14)]
N = 14

# 节点坐标（示意布局，非严格地理坐标）
POS = {
    1: (140, 70),  2: (100, 132), 3: (58, 194),  4: (172, 194),
    5: (232, 132), 6: (302, 194), 7: (128, 252), 8: (66, 312),
    9: (198, 312), 10: (300, 292), 11: (372, 232), 12: (422, 170),
    13: (392, 252), 14: (318, 352),
}
# 变压器支路（画成虚线以示区分）
TRAFO = {(4,7), (4,9), (5,6)}

FONT = "system-ui, -apple-system, 'Segoe UI', 'Microsoft YaHei', sans-serif"


def graph_svg():
    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 500" width="760" height="500"')
    p.append(f'     font-family="{FONT}">')
    p.append('  <rect width="760" height="500" fill="#ffffff"/>')
    p.append('  <text x="380" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">'
             '电网本来就是一张图 —— 不需要任何"类比"</text>')
    p.append('  <text x="380" y="52" text-anchor="middle" font-size="12.5" fill="#64748b">'
             '左：IEEE 14 节点系统拓扑（示意布局）　右：由它得到的邻接矩阵 A</text>')

    # --- 边 ---
    for a, b in BRANCHES:
        x1, y1 = POS[a]
        x2, y2 = POS[b]
        dash = ' stroke-dasharray="6,4"' if (a, b) in TRAFO or (b, a) in TRAFO else ''
        color = '#d97706' if dash else '#94a3b8'
        w = '2.2' if dash else '1.8'
        p.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                 f'stroke="{color}" stroke-width="{w}"{dash}/>')

    # --- 节点 ---
    for i in range(1, N + 1):
        x, y = POS[i]
        r = 15 if i == 4 else 13
        fill = '#dbeafe' if i == 4 else '#ffffff'
        stroke = '#2563eb' if i == 4 else '#475569'
        p.append(f'  <circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
        p.append(f'  <text x="{x}" y="{y + 4.5}" text-anchor="middle" font-size="11.5" '
                 f'font-weight="600" fill="#0f172a">{i}</text>')

    # --- 图例 ---
    p.append('  <g font-size="11" fill="#334155">')
    p.append('    <line x1="42" y1="396" x2="76" y2="396" stroke="#94a3b8" stroke-width="1.8"/>')
    p.append('    <text x="84" y="400">线路（Line）</text>')
    p.append('    <line x1="190" y1="396" x2="224" y2="396" stroke="#d97706" stroke-width="2.2" stroke-dasharray="6,4"/>')
    p.append('    <text x="232" y="400">变压器（Transformer）</text>')
    p.append('  </g>')
    p.append('  <text x="42" y="422" font-size="11.5" fill="#b91c1c">'
             '⚠️ 只遍历 pandapower 的 net.line，会丢掉 4-7 / 4-9 / 5-6 这三条，图会断开</text>')

    # --- 邻接矩阵 ---
    cx, cy, cell = 520, 100, 15.5
    p.append(f'  <text x="{cx + N * cell / 2}" y="84" text-anchor="middle" font-size="12.5" '
             f'font-weight="700" fill="#1e3a8a">邻接矩阵 A（{N}×{N}）</text>')
    # 外框与网格
    p.append(f'  <rect x="{cx}" y="{cy}" width="{N * cell}" height="{N * cell}" '
             f'fill="#f8fafc" stroke="#94a3b8" stroke-width="1.4"/>')
    for k in range(N + 1):
        p.append(f'  <line x1="{cx + k * cell}" y1="{cy}" x2="{cx + k * cell}" y2="{cy + N * cell}" '
                 f'stroke="#e2e8f0" stroke-width="0.8"/>')
        p.append(f'  <line x1="{cx}" y1="{cy + k * cell}" x2="{cx + N * cell}" y2="{cy + k * cell}" '
                 f'stroke="#e2e8f0" stroke-width="0.8"/>')
    # 非零元
    for a, b in BRANCHES:
        for (r, c) in ((a, b), (b, a)):
            x = cx + (c - 1) * cell
            y = cy + (r - 1) * cell
            is_t = (a, b) in TRAFO or (b, a) in TRAFO
            fill = '#fbbf24' if is_t else '#2563eb'
            p.append(f'  <rect x="{x + 1.2}" y="{y + 1.2}" width="{cell - 2.4}" height="{cell - 2.4}" fill="{fill}"/>')
    # 行列标签
    for k in range(1, N + 1):
        p.append(f'  <text x="{cx + (k - 0.5) * cell}" y="{cy - 5}" text-anchor="middle" '
                 f'font-size="8.5" fill="#64748b">{k}</text>')
        p.append(f'  <text x="{cx - 6}" y="{cy + (k - 0.5) * cell + 3}" text-anchor="end" '
                 f'font-size="8.5" fill="#64748b">{k}</text>')

    # 统计
    nz = len(BRANCHES) * 2
    total = N * N
    p.append(f'  <text x="{cx}" y="{cy + N * cell + 22}" font-size="11.5" fill="#334155">'
             f'非零元 {nz} 个 / 共 {total} 个 → 稀疏度 {1 - nz / total:.3f}</text>')
    p.append(f'  <text x="{cx}" y="{cy + N * cell + 42}" font-size="11.5" fill="#1e3a8a">'
             f'A 完全由拓扑决定，与运行状态无关</text>')
    p.append(f'  <text x="{cx}" y="{cy + N * cell + 62}" font-size="11.5" fill="#64748b">'
             f'（黄色 = 变压器支路）</text>')

    # 底部结论（横跨全宽，避免溢出）
    p.append('  <rect x="40" y="438" width="688" height="48" rx="9" fill="#eff6ff" stroke="#2563eb" stroke-width="1.3"/>')
    p.append('  <text x="58" y="459" font-size="11.5" font-weight="700" fill="#1e3a8a">'
             '和状态估计的接口：A 的稀疏结构 = H 的稀疏结构，两者都由拓扑决定</text>')
    p.append('  <text x="58" y="477" font-size="11" fill="#334155">'
             '所以"把电网建成图"不是换个模型玩玩，而是把 H 里本来就有的结构信息显式地交给神经网络。</text>')
    p.append('</svg>')
    return "\n".join(p)


def hmatrix_svg():
    """状态估计流程 + H 矩阵的稀疏结构。"""
    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 572" width="760" height="572"')
    p.append(f'     font-family="{FONT}">')
    p.append('  <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
             'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/></marker></defs>')
    p.append('  <rect width="760" height="572" fill="#ffffff"/>')
    p.append('  <text x="380" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">'
             '状态估计：把量测压成状态，再用残差判断"数据脏没脏"</text>')
    p.append('  <text x="380" y="54" text-anchor="middle" font-size="12.5" fill="#64748b">'
             'z = H·x + e　→　x̂ = (HᵀH)⁻¹Hᵀz　→　r = z − H·x̂　→　‖r‖ &gt; τ ?</text>')

    # ---- 流程：两个输入 + 一个过程 + 两个输出 ----
    p.append('  <text x="40" y="84" font-size="12.5" font-weight="700" fill="#2563eb">① 两个输入</text>')

    p.append('  <rect x="40" y="98" width="150" height="56" rx="9" fill="#eff6ff" stroke="#2563eb" stroke-width="1.6"/>')
    p.append('  <text x="115" y="122" text-anchor="middle" font-size="13" font-weight="700" fill="#1e3a8a">量测 z</text>')
    p.append('  <text x="115" y="141" text-anchor="middle" font-size="10.5" fill="#475569">m 维 · SCADA / PMU 采集</text>')

    p.append('  <rect x="40" y="184" width="150" height="56" rx="9" fill="#fff7ed" stroke="#ea580c" stroke-width="1.6"/>')
    p.append('  <text x="115" y="208" text-anchor="middle" font-size="13" font-weight="700" fill="#9a3412">H 矩阵</text>')
    p.append('  <text x="115" y="227" text-anchor="middle" font-size="10.5" fill="#9a3412">m×n · 由拓扑与线路参数决定</text>')

    p.append('  <text x="240" y="84" font-size="12.5" font-weight="700" fill="#2563eb">② 估计过程</text>')
    p.append('  <rect x="240" y="128" width="180" height="84" rx="9" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.6"/>')
    p.append('  <text x="330" y="156" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">加权最小二乘</text>')
    p.append('  <text x="330" y="178" text-anchor="middle" font-size="11.5" fill="#334155">x̂ = (HᵀH)⁻¹Hᵀz</text>')
    p.append('  <text x="330" y="197" text-anchor="middle" font-size="10.5" fill="#64748b">假设噪声高斯 → 等价于 MLE</text>')

    p.append('  <text x="460" y="84" font-size="12.5" font-weight="700" fill="#2563eb">③ 两个输出</text>')
    p.append('  <rect x="460" y="128" width="120" height="84" rx="9" fill="#f5f3ff" stroke="#7c3aed" stroke-width="1.6"/>')
    p.append('  <text x="520" y="158" text-anchor="middle" font-size="13" font-weight="700" fill="#5b21b6">状态 x̂</text>')
    p.append('  <text x="520" y="178" text-anchor="middle" font-size="10.5" fill="#6d28d9">n 维：电压幅值 + 相角</text>')
    p.append('  <text x="520" y="196" text-anchor="middle" font-size="10.5" fill="#6d28d9">EMS 的"当前快照"</text>')

    p.append('  <rect x="610" y="128" width="120" height="84" rx="9" fill="#fef2f2" stroke="#dc2626" stroke-width="1.6"/>')
    p.append('  <text x="670" y="158" text-anchor="middle" font-size="13" font-weight="700" fill="#991b1b">残差 r</text>')
    p.append('  <text x="670" y="178" text-anchor="middle" font-size="10.5" fill="#b91c1c">r = z − H·x̂</text>')
    p.append('  <text x="670" y="196" text-anchor="middle" font-size="10.5" fill="#b91c1c">攻击者要让它不变</text>')

    # 箭头
    p.append('  <line x1="190" y1="126" x2="236" y2="150" stroke="#475569" stroke-width="1.8" marker-end="url(#ah)"/>')
    p.append('  <line x1="190" y1="212" x2="236" y2="190" stroke="#475569" stroke-width="1.8" marker-end="url(#ah)"/>')
    p.append('  <line x1="420" y1="170" x2="456" y2="170" stroke="#475569" stroke-width="1.8" marker-end="url(#ah)"/>')
    p.append('  <line x1="580" y1="170" x2="606" y2="170" stroke="#475569" stroke-width="1.8" marker-end="url(#ah)"/>')
    # 残差还需要 z 本身
    p.append('  <path d="M 115 154 L 115 244 L 670 244 L 670 216" fill="none" stroke="#94a3b8" '
             'stroke-width="1.4" stroke-dasharray="5,4" marker-end="url(#ah)"/>')
    p.append('  <text x="360" y="238" text-anchor="middle" font-size="10.5" fill="#64748b">'
             '残差还要用到原始 z（虚线）</text>')

    # ---- H 矩阵稀疏示意 ----
    p.append('  <text x="40" y="286" font-size="12.5" font-weight="700" fill="#9a3412">'
             'H 长什么样：每行一个量测，每列一个状态，非零元只出现在"物理相连"的位置</text>')
    mx, my, cw, ch, rows, cols = 60, 300, 42, 17, 6, 6
    p.append(f'  <rect x="{mx}" y="{my}" width="{cols * cw}" height="{rows * ch}" fill="#ffffff" stroke="#94a3b8" stroke-width="1.3"/>')
    for k in range(cols + 1):
        p.append(f'  <line x1="{mx + k * cw}" y1="{my}" x2="{mx + k * cw}" y2="{my + rows * ch}" stroke="#e2e8f0" stroke-width="0.9"/>')
    for k in range(rows + 1):
        p.append(f'  <line x1="{mx}" y1="{my + k * ch}" x2="{mx + cols * cw}" y2="{my + k * ch}" stroke="#e2e8f0" stroke-width="0.9"/>')
    nz_pattern = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 3), (2, 4), (3, 2), (3, 5), (4, 0), (4, 4), (5, 3), (5, 5)]
    for (r, c) in nz_pattern:
        p.append(f'  <rect x="{mx + c * cw + 3}" y="{my + r * ch + 2.5}" width="{cw - 6}" height="{ch - 5}" fill="#ea580c" rx="2"/>')
    p.append(f'  <text x="{mx}" y="{my + rows * ch + 22}" font-size="11" fill="#334155">'
             f'行 = 一个量测　|　列 = 一个状态　|　橙色 = 非零元</text>')
    p.append(f'  <text x="{mx}" y="{my + rows * ch + 42}" font-size="10.5" fill="#64748b">'
             f'（示意：真实 H 更稀疏，元素值由线路阻抗决定）</text>')

    # 右侧说明
    p.append('  <rect x="346" y="296" width="382" height="150" rx="9" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>')
    p.append('  <text x="364" y="320" font-size="12.5" font-weight="700" fill="#0f172a">为什么 H 这么重要</text>')
    p.append('  <text x="364" y="344" font-size="11.5" fill="#334155">① 它把"物理"编码进了检测问题</text>')
    p.append('  <text x="364" y="366" font-size="11.5" fill="#334155">② 它的结构 = 拓扑，与运行数据无关</text>')
    p.append('  <text x="364" y="388" font-size="11.5" fill="#334155">③ 攻击者要绕过 BDD，必须先知道它</text>')
    p.append('  <text x="364" y="412" font-size="11.5" font-weight="700" fill="#b91c1c">'
             '⇒ 所以"知道多少 H" = 攻击强度</text>')
    p.append('  <text x="364" y="434" font-size="10.5" fill="#64748b">'
             '这正是选题 B 能把"信息边界"参数化的原因</text>')

    # 底部
    p.append('  <rect x="40" y="462" width="688" height="94" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.3"/>')
    p.append('  <text x="58" y="486" font-size="12.5" font-weight="700" fill="#15803d">残差为什么能当检测器</text>')
    p.append('  <text x="58" y="508" font-size="11.5" fill="#334155">'
             '数据干净时，r 里只有噪声；某个量测被随机篡改时，r 里会多出一份"对不上物理"的成分，‖r‖ 变大。</text>')
    p.append('  <text x="58" y="530" font-size="11.5" fill="#334155">'
             '但若攻击者按 Δz = H·Δx 改，这份成分恰好落在 H 的列空间里 —— 残差里一点都留不下。</text>')
    p.append('  <text x="58" y="550" font-size="11.5" font-weight="600" fill="#b91c1c">'
             '这就是 FDI 的核心，也是"残差法"在完全信息攻击下必然失效的原因。</text>')
    p.append('</svg>')
    return "\n".join(p)


io.open(r"C:\WorkBuddy\DeepLearn\assets\day61_grid_graph.svg", "w", encoding="utf-8").write(graph_svg())
io.open(r"C:\WorkBuddy\DeepLearn\assets\day37_state_estimation.svg", "w", encoding="utf-8").write(hmatrix_svg())
print("已生成 day61_grid_graph.svg 与 day37_state_estimation.svg")
