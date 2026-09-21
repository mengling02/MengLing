"""生成第二批 SVG。用完即删。"""
import io

F = "system-ui, -apple-system, 'Segoe UI', 'Microsoft YaHei', sans-serif"
OUT = r"C:\WorkBuddy\DeepLearn\assets"


def head(w, h, title, sub):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"',
        f'     font-family="{F}">',
        '  <defs>',
        '    <marker id="mk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/></marker>',
        '    <marker id="mkr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#dc2626"/></marker>',
        '    <marker id="mkb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"/></marker>',
        '    <marker id="mkp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"/></marker>',
        '  </defs>',
        f'  <rect width="{w}" height="{h}" fill="#ffffff"/>',
        f'  <text x="{w / 2}" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#0f172a">{title}</text>',
        f'  <text x="{w / 2}" y="52" text-anchor="middle" font-size="12.5" fill="#64748b">{sub}</text>',
    ]


def box(x, y, w, h, fill, stroke, title, sub=None, tc="#0f172a", sc="#475569",
        fs=13, sfs=10.5, rx=8, sw=1.6):
    p = [f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>',
         f'  <text x="{x + w / 2}" y="{y + (h / 2 + 5 if not sub else h / 2 - 4)}" text-anchor="middle" '
         f'font-size="{fs}" font-weight="600" fill="{tc}">{title}</text>']
    if sub:
        p.append(f'  <text x="{x + w / 2}" y="{y + h / 2 + 15}" text-anchor="middle" '
                 f'font-size="{sfs}" fill="{sc}">{sub}</text>')
    return p


def arrow(x1, y1, x2, y2, color="#475569", marker="mk", dash=None, w=1.8):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return [f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d} '
            f'marker-end="url(#{marker})"/>']


# ===========================================================================
# 1. LSTM 三个门
# ===========================================================================
def lstm():
    p = head(760, 470, "LSTM：一条「细胞状态高速路」+ 三个门",
             "门不是开关，是 0~1 的阀门 —— 决定让多少信息通过")
    # 细胞状态主线
    p.append('  <text x="40" y="106" font-size="12.5" font-weight="700" fill="#7c3aed">细胞状态 c（长期记忆 · 唯一贯穿全程的通道）</text>')
    p.append('  <line x1="60" y1="132" x2="620" y2="132" stroke="#7c3aed" stroke-width="2.6"/>')
    p.append('  <text x="60" y="122" font-size="11" fill="#5b21b6">c_{t-1}</text>')
    p.append('  <text x="592" y="122" font-size="11" fill="#5b21b6">c_t</text>')
    p += arrow(620, 132, 648, 132, "#7c3aed", "mkp")

    # 遗忘门 ×
    p.append('  <circle cx="215" cy="132" r="20" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/>')
    p.append('  <text x="215" y="140" text-anchor="middle" font-size="17" font-weight="700" fill="#991b1b">×</text>')
    # 输入门 +
    p.append('  <circle cx="440" cy="132" r="20" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>')
    p.append('  <text x="440" y="140" text-anchor="middle" font-size="17" font-weight="700" fill="#15803d">+</text>')

    # 三个门（一行排开，互不重叠）
    p += box(40, 236, 150, 62, "#fef2f2", "#dc2626", "遗忘门 f", "σ(W_f·[h,x])", "#991b1b", "#b91c1c", 12.5)
    p += box(230, 236, 150, 62, "#f0fdf4", "#16a34a", "输入门 i", "σ(W_i·[h,x])", "#15803d", "#166534", 12.5)
    p += box(420, 236, 150, 62, "#eff6ff", "#2563eb", "输出门 o", "σ(W_o·[h,x])", "#1e3a8a", "#1d4ed8", 12.5)
    # 候选记忆（放最右，与三门同高，不重叠）
    p += box(600, 236, 148, 62, "#fff7ed", "#ea580c", "候选记忆", "c̃ = tanh(W_c·[h,x])", "#9a3412", "#ea580c", 11.5)

    p += arrow(115, 236, 115, 178, "#dc2626", "mk")
    p.append('  <path d="M 115 178 L 195 178 L 195 140" fill="none" stroke="#dc2626" stroke-width="1.6"/>')
    p.append('  <text x="24" y="214" font-size="10.5" fill="#b91c1c">"忘掉多少"</text>')

    p += arrow(305, 236, 305, 190, "#16a34a", "mk")
    p.append('  <path d="M 305 190 L 422 190 L 422 148" fill="none" stroke="#16a34a" stroke-width="1.6"/>')
    p.append('  <text x="222" y="214" font-size="10.5" fill="#15803d">"写入多少"</text>')

    # 候选记忆 → 先乘输入门，再进加法节点
    p.append('  <path d="M 674 236 L 674 206 L 460 206" fill="none" stroke="#ea580c" stroke-width="1.6"/>')
    p.append('  <circle cx="460" cy="206" r="9" fill="#fff7ed" stroke="#ea580c" stroke-width="1.6"/>')
    p.append('  <text x="460" y="210" text-anchor="middle" font-size="11" font-weight="700" fill="#9a3412">×</text>')
    p += arrow(460, 197, 458, 152, "#ea580c", "mk")
    p.append('  <text x="500" y="226" font-size="10.5" fill="#9a3412">先与输入门相乘，再写进细胞状态</text>')

    # 输入
    p += box(40, 340, 200, 56, "#f1f5f9", "#94a3b8", "h_{t-1} , x_t", "上一时刻隐状态 + 当前输入", "#0f172a", "#64748b", 12, 10)
    p.append('  <path d="M 240 368 L 285 368 L 285 302" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,4"/>')
    p.append('  <text x="296" y="352" font-size="10.5" fill="#64748b">同一个输入，喂给三个门</text>')

    # 输出门作用
    p += arrow(495, 298, 495, 322, "#2563eb", "mk")
    p.append('  <text x="508" y="316" font-size="10.5" fill="#1d4ed8">"放行多少"</text>')
    p.append('  <path d="M 648 132 L 700 132 L 700 350 L 560 350" fill="none" stroke="#2563eb" stroke-width="1.8" stroke-dasharray="5,4"/>')
    p.append('  <circle cx="560" cy="350" r="9" fill="#eff6ff" stroke="#2563eb" stroke-width="1.6"/>')
    p.append('  <text x="560" y="354" text-anchor="middle" font-size="11" font-weight="700" fill="#1e3a8a">×</text>')
    p += box(360, 400, 260, 54, "#eff6ff", "#2563eb", "h_t = o ⊙ tanh(c_t)", "输出给下一层 / 下一时刻", "#1e3a8a", "#1d4ed8", 12.5)
    p += arrow(490, 359, 490, 396, "#2563eb", "mk")
    return p + ['</svg>']


# ===========================================================================
# 2. 自编码器异常检测
# ===========================================================================
def autoencoder():
    p = head(760, 420, "自编码器做异常检测：只学「正常」长什么样",
             "训练时只喂正常样本 —— 模型没见过攻击，所以重建不出来")
    p += box(30, 150, 110, 130, "#eff6ff", "#2563eb", "输入 x", "高维量测", "#1e3a8a", "#1d4ed8", 12.5)
    p += box(180, 175, 110, 80, "#f1f5f9", "#94a3b8", "编码器", "压缩", "#0f172a", "#475569", 12.5)
    p += box(330, 195, 100, 40, "#fef3c7", "#d97706", "潜变量 z", "低维", "#92400e", "#b45309", 11.5)
    p += box(470, 175, 110, 80, "#f1f5f9", "#94a3b8", "解码器", "重建", "#0f172a", "#475569", 12.5)
    p += box(620, 150, 110, 130, "#dcfce7", "#16a34a", "重建 x̂", "同维度", "#15803d", "#166534", 12.5)
    p += arrow(140, 215, 176, 215)
    p += arrow(290, 215, 326, 215)
    p += arrow(430, 215, 466, 215)
    p += arrow(580, 215, 616, 215)

    p.append('  <path d="M 675 150 C 675 90, 85 90, 85 150" fill="none" stroke="#dc2626" '
             'stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#mkr)"/>')
    p.append('  <text x="380" y="88" text-anchor="middle" font-size="12" font-weight="600" fill="#b91c1c">'
             '重建误差 ‖x − x̂‖ = 异常分数</text>')

    p.append('  <rect x="40" y="300" width="680" height="104" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>')
    p.append('  <text x="58" y="324" font-size="12.5" font-weight="700" fill="#0f172a">为什么"只学正常"就够了</text>')
    p.append('  <text x="58" y="346" font-size="11.5" fill="#334155">'
             '训练目标是把输入重建回自己。模型只见过正常数据，于是它学会了"正常数据的压缩表示"。</text>')
    p.append('  <text x="58" y="368" font-size="11.5" fill="#334155">'
             '遇到正常样本 → 重建得准 → 误差小；遇到攻击样本 → 落不到学过的流形上 → 误差大。</text>')
    p.append('  <text x="58" y="392" font-size="11.5" font-weight="600" fill="#b91c1c">'
             '⚠️ 但这依赖一个前提：攻击样本"确实在分布外"。如果攻击者按 Δz = H·Δx 构造，它可能就在分布内 —— 这时自编码器也会失效。</text>')
    return p + ['</svg>']


# ===========================================================================
# 3. GCN 邻居聚合
# ===========================================================================
def gcn():
    p = head(760, 470, "GCN 一层在做什么：把邻居的信息按权重收过来",
             "h_i 的新表示 = 自己 + 所有邻居的加权平均，再乘一个可学习矩阵")
    cx, cy = 200, 210
    nb = [(200, 120), (110, 180), (110, 260), (200, 300), (290, 260), (290, 180)]
    for (x, y) in nb:
        p.append(f'  <line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#cbd5e1" stroke-width="1.6"/>')
        p.append(f'  <circle cx="{x}" cy="{y}" r="19" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>')
        p.append(f'  <text x="{x}" y="{y + 4}" text-anchor="middle" font-size="10.5" fill="#475569">邻居</text>')
    p.append(f'  <circle cx="{cx}" cy="{cy}" r="26" fill="#dbeafe" stroke="#2563eb" stroke-width="2.4"/>')
    p.append(f'  <text x="{cx}" y="{cy + 5}" text-anchor="middle" font-size="12" font-weight="700" fill="#1e3a8a">i</text>')

    p.append('  <text x="200" y="352" text-anchor="middle" font-size="11.5" fill="#334155">'
             '度数 d=6 的节点 i 与它的邻居</text>')

    p += arrow(360, 210, 430, 210)
    p.append('  <text x="395" y="198" text-anchor="middle" font-size="10.5" fill="#64748b">聚合</text>')

    p.append('  <rect x="450" y="96" width="280" height="230" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.4"/>')
    p.append('  <text x="590" y="122" text-anchor="middle" font-size="12.5" font-weight="700" fill="#0f172a">'
             'h_i′ = Σⱼ (1/√(dᵢ·dⱼ)) * hⱼ * W</text>')
    p.append('  <text x="470" y="152" font-size="11.5" fill="#334155">① 先加自环：自己也算一个"邻居"</text>')
    p.append('  <text x="470" y="176" font-size="11.5" fill="#334155">② 按 1/√(dᵢ*dⱼ) 加权求和</text>')
    p.append('  <text x="470" y="200" font-size="11.5" fill="#334155">③ 乘可学习矩阵 W 做变换</text>')
    p.append('  <text x="470" y="228" font-size="11.5" font-weight="600" fill="#b91c1c">为什么除以 √(dᵢ*dⱼ) ？</text>')
    p.append('  <text x="470" y="250" font-size="11" fill="#334155">度数高的节点"话多"，输出会偏大。</text>')
    p.append('  <text x="470" y="270" font-size="11" fill="#334155">归一化后每个节点看到的是</text>')
    p.append('  <text x="470" y="290" font-size="11" fill="#334155">"加权平均"而不是"求和"，量级稳定。</text>')
    p.append('  <text x="470" y="312" font-size="11" fill="#64748b">不归一化 → 堆几层就指数爆炸</text>')

    p.append('  <rect x="40" y="386" width="680" height="66" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-width="1.3"/>')
    p.append('  <text x="58" y="408" font-size="11.5" font-weight="700" fill="#1e3a8a">'
             '一句话：GCN 就是"带结构的加权平均"，没有任何魔法</text>')
    p.append('  <text x="58" y="432" font-size="11" fill="#334155">'
             '它的价值在于：把"谁和谁物理相连"这件事，直接写进了模型的聚合规则里 —— 这是普通 MLP 拿不到的免费先验。</text>')
    return p + ['</svg>']


# ===========================================================================
# 4. 扩散模型
# ===========================================================================
def diffusion():
    p = head(760, 430, "扩散模型：先学会「加噪」，再学会「去噪」",
             "生成过程 = 从纯噪声出发，一步步把噪声减掉")
    p.append('  <text x="40" y="96" font-size="12.5" font-weight="700" fill="#dc2626">① 前向加噪（训练时用，不需要学）</text>')
    xs = [60, 190, 320, 450, 580]
    labels = ["真实样本 x₀", "x₁", "x₂", "…", "x_T ≈ 纯噪声"]
    for i, (x, lab) in enumerate(zip(xs, labels)):
        shade = ["#dbeafe", "#bfdbfe", "#93c5fd", "#c7d2fe", "#cbd5e1"][i]
        p.append(f'  <rect x="{x}" y="112" width="100" height="58" rx="8" fill="{shade}" stroke="#64748b" stroke-width="1.3"/>')
        p.append(f'  <text x="{x + 50}" y="147" text-anchor="middle" font-size="11.5" font-weight="600" fill="#0f172a">{lab}</text>')
        if i < 4:
            p += arrow(x + 102, 141, x + 128, 141, "#dc2626", "mkr")
    p.append('  <text x="380" y="192" text-anchor="middle" font-size="11" fill="#b91c1c">'
             '每步加一点高斯噪声：x_t = √(1−β_t)·x_{t−1} + √β_t·ε</text>')

    p.append('  <text x="40" y="232" font-size="12.5" font-weight="700" fill="#16a34a">② 反向去噪（这才是要学的）</text>')
    for i, (x, lab) in enumerate(zip(xs, labels[::-1])):
        shade = ["#cbd5e1", "#c7d2fe", "#93c5fd", "#bfdbfe", "#dcfce7"][i]
        p.append(f'  <rect x="{x}" y="248" width="100" height="58" rx="8" fill="{shade}" stroke="#64748b" stroke-width="1.3"/>')
        p.append(f'  <text x="{x + 50}" y="283" text-anchor="middle" font-size="11.5" font-weight="600" fill="#0f172a">{lab}</text>')
        if i < 4:
            p += arrow(x + 102, 277, x + 128, 277, "#16a34a", "mk")
    p.append('  <text x="380" y="328" text-anchor="middle" font-size="11" fill="#15803d">'
             '网络每一步预测"这一步加了什么噪声"，然后减掉它</text>')

    p.append('  <rect x="40" y="352" width="680" height="62" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>')
    p.append('  <text x="58" y="374" font-size="11.5" font-weight="700" fill="#0f172a">为什么这在电力场景有价值</text>')
    p.append('  <text x="58" y="396" font-size="11" fill="#334155">'
             '攻击样本占比 &lt; 0.1%，直接训练判别模型容易过拟合。扩散模型能"造"出物理可行的合成样本，扩充少数类 —— 但必须过物理可行性过滤。</text>')
    return p + ['</svg>']


# ===========================================================================
# 5. FGSM vs PGD
# ===========================================================================
def fgsm_pgd():
    p = head(760, 450, "FGSM 与 PGD：一步走 vs 小步多走",
             "都盯着同一个目标：让损失变大 —— 也就是让检测器判错")
    # ---------------- FGSM ----------------
    p.append('  <rect x="30" y="80" width="340" height="280" rx="10" fill="#fef2f2" stroke="#dc2626" stroke-width="1.4"/>')
    p.append('  <text x="200" y="106" text-anchor="middle" font-size="13.5" font-weight="700" fill="#b91c1c">FGSM · 一步到位</text>')
    p.append('  <text x="200" y="132" text-anchor="middle" font-size="11.5" fill="#334155">x′ = x + ε * sign(∇ₓ L)</text>')
    # ε 球（以 x 为圆心）
    p.append('  <circle cx="110" cy="238" r="86" fill="#fee2e2" stroke="#f87171" stroke-width="1.4" stroke-dasharray="5,4"/>')
    p.append('  <text x="110" y="146" text-anchor="middle" font-size="10.5" fill="#b91c1c">ε 球：扰动允许范围</text>')
    p.append('  <circle cx="110" cy="238" r="7" fill="#2563eb"/>')
    p.append('  <text x="110" y="262" text-anchor="middle" font-size="10.5" font-weight="600" fill="#1e3a8a">原始样本 x</text>')
    # 一步走到球面
    p.append('  <circle cx="196" cy="238" r="7" fill="#dc2626"/>')
    p.append('  <text x="206" y="228" font-size="10.5" font-weight="600" fill="#b91c1c">对抗样本 x′</text>')
    p += arrow(118, 238, 188, 238, "#dc2626", "mkr", w=2.4)
    p.append('  <text x="152" y="292" text-anchor="middle" font-size="10.5" fill="#b91c1c">一次走满 ε（落在球面上）</text>')
    p.append('  <text x="200" y="342" text-anchor="middle" font-size="11" fill="#475569">快，但常常不够强</text>')

    # ---------------- PGD ----------------
    p.append('  <rect x="390" y="80" width="340" height="280" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.4"/>')
    p.append('  <text x="560" y="106" text-anchor="middle" font-size="13.5" font-weight="700" fill="#15803d">PGD · 小步多走 + 投影</text>')
    p.append('  <text x="560" y="132" text-anchor="middle" font-size="11.5" fill="#334155">x^{t+1} = Proj( x^t + α * sign(∇L) )</text>')
    # ε 球
    p.append('  <circle cx="480" cy="238" r="86" fill="#dcfce7" stroke="#4ade80" stroke-width="1.4" stroke-dasharray="5,4"/>')
    p.append('  <text x="480" y="146" text-anchor="middle" font-size="10.5" fill="#15803d">ε 球</text>')
    p.append('  <circle cx="480" cy="238" r="7" fill="#2563eb"/>')
    p.append('  <text x="480" y="262" text-anchor="middle" font-size="10.5" font-weight="600" fill="#1e3a8a">原始样本 x</text>')
    # 锯齿路径：走一步→投影回球面
    pts = [(480, 238), (526, 216), (552, 182), (560, 218), (586, 192), (548, 166), (522, 196), (558, 200)]
    d = 'M ' + ' L '.join(f'{x} {y}' for x, y in pts)
    p.append(f'  <path d="{d}" fill="none" stroke="#16a34a" stroke-width="1.8"/>')
    for (x, y) in pts[1:]:
        p.append(f'  <circle cx="{x}" cy="{y}" r="4.2" fill="#16a34a"/>')
    p.append('  <circle cx="558" cy="200" r="7" fill="#dc2626"/>')
    p.append('  <text x="572" y="206" font-size="10.5" font-weight="600" fill="#b91c1c">x′</text>')
    p.append('  <text x="560" y="292" text-anchor="middle" font-size="10.5" fill="#15803d">每步只走 α，越界就拉回球面</text>')
    p.append('  <text x="560" y="342" text-anchor="middle" font-size="11" fill="#475569">慢，但是评估鲁棒性的标准做法</text>')

    p.append('  <rect x="30" y="376" width="700" height="62" rx="10" fill="#fff7ed" stroke="#ea580c" stroke-width="1.3"/>')
    p.append('  <text x="48" y="398" font-size="11.5" font-weight="700" fill="#9a3412">'
             '在电力场景，ε 不是"像素扰动"，而是"量测允许被改多少"</text>')
    p.append('  <text x="48" y="420" font-size="11" fill="#334155">'
             '所以 ε 必须与量测精度、物理可行性挂钩 —— 一个不设上限的攻击，在真实系统里没有意义。</text>')
    return p + ['</svg>']


# ===========================================================================
# 6. PINN
# ===========================================================================
def pinn():
    p = head(760, 470, "PINN：把物理方程写进损失函数",
             '网络不只拟合数据，还要让输出的状态"满足潮流方程"')
    p.append('  <text x="40" y="104" font-size="11.5" fill="#b91c1c">'
             '纯数据驱动时，损失只有左边那一项 → 网络可能输出"物理上不可能"的解</text>')

    p += box(30, 122, 130, 82, "#eff6ff", "#2563eb", "输入", "量测 / 时间 / 负荷", "#1e3a8a", "#1d4ed8", 12.5)
    p += box(200, 122, 150, 82, "#f1f5f9", "#94a3b8", "神经网络", "MLP / GNN", "#0f172a", "#475569", 12.5)
    p += box(390, 122, 130, 82, "#f5f3ff", "#7c3aed", "输出 x̂", "电压幅值 + 相角", "#5b21b6", "#6d28d9", 12.5)
    p += arrow(160, 163, 196, 163)
    p += arrow(350, 163, 386, 163)

    # 物理残差
    p += arrow(455, 204, 455, 244, "#ea580c", "mk")
    p += box(340, 248, 230, 54, "#fff7ed", "#ea580c", "物理残差 r_phys", "r = z − H · x̂（潮流方程约束）", "#9a3412", "#ea580c", 12)
    p += arrow(455, 302, 455, 340, "#ea580c", "mk")

    # 两个损失
    p += box(60, 344, 250, 56, "#fef2f2", "#dc2626", "① 数据损失", "‖x̂ − x_true‖²", "#991b1b", "#dc2626", 12.5)
    p += box(370, 344, 320, 56, "#fff7ed", "#ea580c", "② 物理损失 λ · L_phys", "‖z − H·x̂‖²  （或方程残差）", "#9a3412", "#ea580c", 12.5)
    p.append('  <text x="536" y="168" font-size="11" fill="#9a3412">同一个 x̂，两条约束</text>')

    # 相加
    p.append('  <circle cx="340" cy="430" r="15" fill="#f1f5f9" stroke="#334155" stroke-width="1.8"/>')
    p.append('  <text x="340" y="436" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">+</text>')
    p.append('  <path d="M 185 400 L 185 430 L 322 430" fill="none" stroke="#94a3b8" stroke-width="1.5"/>')
    p.append('  <path d="M 530 400 L 530 430 L 358 430" fill="none" stroke="#94a3b8" stroke-width="1.5"/>')

    p.append('  <rect x="380" y="404" width="330" height="52" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-width="1.3"/>')
    p.append('  <text x="398" y="426" font-size="12.5" font-weight="700" fill="#1e3a8a">L = L_data + λ · L_phys</text>')
    p.append('  <text x="398" y="446" font-size="11" fill="#b91c1c">λ 是关键，也最难调：太大解不出数据，太小物理约束形同虚设</text>')
    p.append('  <path d="M 356 430 L 376 430" fill="none" stroke="#334155" stroke-width="1.8"/>')
    return p + ['</svg>']


# ===========================================================================
# 7. 联邦学习
# ===========================================================================
def federated():
    p = head(760, 500, "联邦学习：数据不动，模型动",
             "各方只上传梯度/参数，原始数据一步都不出本地")
    p += box(290, 84, 180, 60, "#eff6ff", "#2563eb", "中央服务器", "聚合各方更新（FedAvg）", "#1e3a8a", "#1d4ed8", 12.5)

    clients = [(30, 300, "变电站 A"), (208, 300, "变电站 B"), (386, 300, "变电站 C"), (564, 300, "变电站 D")]
    for (x, y, name) in clients:
        p += box(x, y, 166, 80, "#f0fdf4", "#16a34a", name, "本地数据 · 不出域", "#15803d", "#166534", 12.5)
        cxi = x + 83
        # 上行：走左侧通道 y=215
        p.append(f'  <path d="M {cxi} {y-4} L {cxi} 200 L 300 200 L 300 146" fill="none" '
                 f'stroke="#2563eb" stroke-width="1.6" stroke-dasharray="6,4"/>')
        # 下行：走右侧通道 y=258
        p.append(f'  <path d="M 380 144 L 380 268 L {cxi} 268 L {cxi} {y-4}" fill="none" '
                 f'stroke="#7c3aed" stroke-width="1.6" stroke-dasharray="6,4"/>')
        p.append(f'  <polygon points="{cxi},{y-4} {cxi-4},{y+6} {cxi+4},{y+6}" fill="#7c3aed"/>')

    p.append('  <text x="44" y="194" font-size="11" font-weight="600" fill="#1d4ed8">↑ 上传：梯度 / 参数更新</text>')
    p.append('  <text x="44" y="290" font-size="11" font-weight="600" fill="#6d28d9">↓ 下发：聚合后的全局模型</text>')

    p.append('  <rect x="40" y="400" width="330" height="88" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>')
    p.append('  <text x="58" y="424" font-size="12" font-weight="700" fill="#0f172a">它解决的真实痛点</text>')
    p.append('  <text x="58" y="446" font-size="11" fill="#334155">电力数据涉及关键基础设施与商业机密，</text>')
    p.append('  <text x="58" y="466" font-size="11" fill="#334155">跨主体（不同电网公司、不同厂站）无法集中。</text>')

    p.append('  <rect x="390" y="400" width="330" height="88" rx="10" fill="#fef2f2" stroke="#dc2626" stroke-width="1.2"/>')
    p.append('  <text x="408" y="424" font-size="12" font-weight="700" fill="#b91c1c">⚠️ 三个必须知道的坑</text>')
    p.append('  <text x="408" y="446" font-size="11" fill="#334155">① 数据不独立同分布 → 精度通常掉</text>')
    p.append('  <text x="408" y="466" font-size="11" fill="#334155">② 梯度会泄露信息（有攻击证明过）</text>')
    return p + ['</svg>']


# ===========================================================================
# 8. 多种子实验
# ===========================================================================
def multiseed():
    p = head(760, 430, "为什么要跑多个随机种子：单次结果是不可信的",
             "同一份代码、同一个数据集，换个种子指标就能差好几个点")
    p.append('  <text x="40" y="96" font-size="12.5" font-weight="700" fill="#dc2626">✗ 只跑一次（seed=42）</text>')
    for i, v in enumerate([0.92]):
        p.append(f'  <rect x="70" y="112" width="240" height="44" rx="7" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5"/>')
        p.append(f'  <text x="190" y="140" text-anchor="middle" font-size="13" font-weight="700" fill="#991b1b">F1 = {v:.2f}</text>')
    p.append('  <text x="330" y="140" font-size="11.5" fill="#b91c1c">'
             '→ 你无法回答"这个结果稳不稳"，审稿人一定会问</text>')

    p.append('  <text x="40" y="196" font-size="12.5" font-weight="700" fill="#15803d">✓ 跑 5 个种子，报均值 ± 标准差</text>')
    runs = [0.905, 0.921, 0.874, 0.933, 0.897]
    for i, v in enumerate(runs):
        w = int(v * 260)
        y = 212 + i * 26
        p.append(f'  <text x="60" y="{y + 14}" font-size="10.5" fill="#475569">seed {i}</text>')
        p.append(f'  <rect x="110" y="{y}" width="{w}" height="18" rx="4" fill="#93c5fd" stroke="#2563eb" stroke-width="1"/>')
        p.append(f'  <text x="{120 + w}" y="{y + 14}" font-size="10.5" fill="#1e3a8a">{v:.3f}</text>')

    mean = sum(runs) / len(runs)
    std = (sum((r - mean) ** 2 for r in runs) / len(runs)) ** 0.5
    p.append('  <rect x="420" y="212" width="310" height="120" rx="9" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.4"/>')
    p.append('  <text x="575" y="240" text-anchor="middle" font-size="14" font-weight="700" fill="#15803d">'
             f'{mean:.3f} ± {std:.3f}</text>')
    p.append('  <text x="575" y="266" text-anchor="middle" font-size="11" fill="#334155">'
             f'极差 = {max(runs) - min(runs):.3f}（{(max(runs) - min(runs)) * 100:.1f} 个点）</text>')
    p.append('  <text x="575" y="290" text-anchor="middle" font-size="11" fill="#334155">'
             '这个波动幅度，足以让"我提升了 2 个点"</text>')
    p.append('  <text x="575" y="308" text-anchor="middle" font-size="11" font-weight="600" fill="#b91c1c">'
             '变成一句站不住的话</text>')

    p.append('  <rect x="40" y="366" width="690" height="58" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-width="1.3"/>')
    p.append('  <text x="58" y="388" font-size="11.5" font-weight="700" fill="#1e3a8a">'
             '写作规范：任何"提升"都必须放在波动幅度里比较</text>')
    p.append('  <text x="58" y="410" font-size="11" fill="#334155">'
             '如果你的方法比 baseline 高 1.5 个点，而标准差是 2 个点 —— 这个"提升"在统计上不成立。</text>')
    return p + ['</svg>']


items = {
    "day24_lstm_gates.svg": lstm,
    "day26_autoencoder.svg": autoencoder,
    "day62_gcn_aggregation.svg": gcn,
    "day71_diffusion.svg": diffusion,
    "day75_fgsm_pgd.svg": fgsm_pgd,
    "day83_pinn.svg": pinn,
    "day97_federated.svg": federated,
    "day52_multiseed.svg": multiseed,
}
for name, fn in items.items():
    io.open(f"{OUT}\\{name}", "w", encoding="utf-8").write("\n".join(fn()))
    print("生成", name)
