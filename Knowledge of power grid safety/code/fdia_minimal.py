# -*- coding: utf-8 -*-
"""
FDIA 最小验证脚本（零重依赖版）
=========================================================

作用：只依赖 numpy，用 15 分钟让你亲手验证 Liu 2009 的核心结论 ——
      "FDIA 能绕过坏数据检测（BDD）"。

为什么要有这个脚本？
  pandapower / scikit-learn / PyTorch 安装可能受网络影响。
  但这个脚本只用 numpy（几乎必然已安装），
  只要你跑通它，就掌握了 FDIA 最核心的思想。

运行：
  python code/fdia_minimal.py

前置：pip install numpy
（连 numpy 都没有？pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple）
"""

import numpy as np

np.random.seed(42)

print("=" * 66)
print("  FDIA 最小验证 —— 证明 a = Hc 可以绕过坏数据检测")
print("  对应论文：Liu, Ning, Reiter. ACM CCS 2009")
print("=" * 66)


# ============================================================
# 第 1 步：构造一个微型电网的 H 矩阵
# ============================================================
# 为了不用任何电网库，我们手工构造一个 5 节点系统的 H 矩阵。
# 这对应 IEEE 5 节点算例的 DC 潮流模型。
#
# 拓扑（5 个节点，6 条线路）：
#        1 --- 2
#        | \  /|
#        |  \/ |
#        |  /\ |
#        | /  \|
#        3 --- 4
#         \   /
#          \ /
#           5
#
# 状态向量 x = [θ1, θ2, θ3, θ4]（θ5 是平衡节点，不作为状态）
# 量测 z = 各线路潮流 + 各节点注入

print("\n[1/5] 构造微型电网的 H 矩阵...")

# 线路电抗（标幺值）
lines = [
    (0, 1, 0.06),   # 线路: (from, to, x)
    (0, 3, 0.08),
    (0, 4, 0.05),
    (1, 2, 0.07),
    (1, 4, 0.06),
    (2, 3, 0.09),
    (3, 4, 0.08),
]

n_bus = 5
slack = 4                      # 节点 5（下标 4）为平衡节点
state_buses = [0, 1, 2, 3]     # 其余为状态
n_state = len(state_buses)     # n = 4
bus2col = {b: i for i, b in enumerate(state_buses)}

rows, cols, vals = [], [], []
meas_desc = []
row = 0

# ---- ① 支路潮流量测 ----
for (f, t, x) in lines:
    b = 1.0 / x
    if f in bus2col:
        rows.append(row); cols.append(bus2col[f]); vals.append(b)
    if t in bus2col:
        rows.append(row); cols.append(bus2col[t]); vals.append(-b)
    meas_desc.append(f"P_{f+1}{t+1}")
    row += 1

# ---- ② 节点注入量测 ----
for b_bus in state_buses:
    for (f, t, x) in lines:
        bb = 1.0 / x
        if f == b_bus:
            rows.append(row); cols.append(bus2col[f]); vals.append(bb)
            if t in bus2col:
                rows.append(row); cols.append(bus2col[t]); vals.append(-bb)
        elif t == b_bus:
            rows.append(row); cols.append(bus2col[t]); vals.append(bb)
            if f in bus2col:
                rows.append(row); cols.append(bus2col[f]); vals.append(-bb)
    meas_desc.append(f"P_inj_{b_bus+1}")
    row += 1

H = np.zeros((row, n_state))
for r, c, v in zip(rows, cols, vals):
    H[r, c] += v

m = H.shape[0]
print(f"      电网: {n_bus} 节点, {len(lines)} 条线路")
print(f"      H 矩阵维度: {m} 量测 × {n_state} 状态")
print(f"      量测构成: {len(lines)} 个支路潮流 + {n_state} 个节点注入")


# ============================================================
# 第 2 步：生成正常量测
# ============================================================

print("\n[2/5] 生成正常量测数据...")

SIGMA = 0.01                                # 量测噪声标准差
x_true = np.random.uniform(-0.1, 0.1, n_state)   # 真实状态（相角，弧度）
z_true = H @ x_true                          # 无噪声量测
z_normal = z_true + np.random.normal(0, SIGMA, m)

print(f"      真实状态 x: {np.round(x_true, 4)}")
print(f"      噪声标准差: {SIGMA}")
print(f"      量测数量: {m}")


# ============================================================
# 第 3 步：状态估计 + 坏数据检测（BDD）
# ============================================================

def wls_estimate(H, z, sigma):
    """加权最小二乘状态估计：x̂ = (HᵀWH)⁻¹HᵀWz"""
    W = np.eye(len(z)) / (sigma ** 2)
    A = H.T @ W @ H
    b = H.T @ W @ z
    x_hat = np.linalg.solve(A, b)
    return x_hat


def bdd(H, z, sigma):
    """
    坏数据检测：返回 (残差范数, 状态估计)
    残差 r = z - Hx̂
    """
    x_hat = wls_estimate(H, z, sigma)
    r = z - H @ x_hat
    return float(np.linalg.norm(r)), x_hat


print("\n[3/5] 对正常量测做状态估计与 BDD...")

r_normal, x_hat_normal = bdd(H, z_normal, SIGMA)
err_normal = np.linalg.norm(x_hat_normal - x_true)

print(f"      残差范数 ||r||:      {r_normal:.6f}")
print(f"      状态估计误差 ||x̂-x||: {err_normal:.6f}")
print(f"      → 无攻击时，残差小、估计准（正常）")


# ============================================================
# 第 4 步：注入 FDIA —— 核心！
# ============================================================

print("\n[4/5] 注入 FDIA：构造攻击向量 a = Hc ...")

# 攻击者想要造成的状态偏移
c = np.random.normal(0, 0.05, n_state)

# ★★★ 关键的一行：a = Hc ★★★
a = H @ c

z_attacked = z_normal + a

print(f"      攻击者预定状态偏移 c:  {np.round(c, 4)}")
print(f"      攻击向量 ||a||:         {np.linalg.norm(a):.6f}")
print(f"      受影响量测数:           {np.sum(np.abs(a) > 1e-9)} / {m}")

r_attacked, x_hat_attacked = bdd(H, z_attacked, SIGMA)
err_attacked = np.linalg.norm(x_hat_attacked - x_true)
actual_shift = np.linalg.norm(x_hat_attacked - x_hat_normal)


# ============================================================
# 第 5 步：验证结论
# ============================================================

print("\n[5/5] 验证：BDD 能否发现攻击？")
print("-" * 66)
print(f"{'指标':<28s} {'正常':>12s} {'被攻击':>12s} {'变化':>12s}")
print("-" * 66)
print(f"{'残差范数 ||r||':<28s} {r_normal:>12.6f} {r_attacked:>12.6f} "
      f"{abs(r_attacked - r_normal):>12.2e}")
print(f"{'状态估计误差 ||x̂-x_true||':<28s} {err_normal:>12.6f} {err_attacked:>12.6f} "
      f"{err_attacked - err_normal:>12.6f}")
print("-" * 66)

print(f"\n攻击者的实际效果：")
print(f"  · 状态估计偏移量:  {actual_shift:.6f}")
print(f"  · 攻击者预定偏移:  {np.linalg.norm(c):.6f}")
print(f"  · 两者比值:        {actual_shift / np.linalg.norm(c):.4f}  （应接近 1.0）")

# BDD 判据
threshold = 3 * SIGMA * np.sqrt(m)      # 典型阈值：3σ × √m
print(f"\nBDD 判据阈值 τ = {threshold:.6f}（3σ√m）")
print(f"  正常量测残差 {r_normal:.6f} {'≤' if r_normal <= threshold else '>'} τ  "
      f"→ {'判定正常 ✓' if r_normal <= threshold else '报警 ✗'}")
print(f"  攻击量测残差 {r_attacked:.6f} {'≤' if r_attacked <= threshold else '>'} τ  "
      f"→ {'判定正常 ○← 漏检！' if r_attacked <= threshold else '报警'}")

print("\n" + "=" * 66)
print("  结  论")
print("=" * 66)
residual_change = abs(r_attacked - r_normal)
if residual_change < 1e-6 and actual_shift > 0.01:
    print("  ✅ FDIA 攻击成功！")
    print(f"     残差几乎不变（变化 {residual_change:.2e}），BDD 完全检测不到；")
    print(f"     但状态估计已被偏移 {actual_shift:.4f} —— 调度员看到的是假数据。")
    print()
    print("  这印证了 Liu 2009 的核心定理：")
    print("     当 a = Hc 时，攻击向量的残差 r = z - Hx̂ 保持不变，")
    print("     因为 Hc 项在残差计算中被精确抵消。")
    print()
    print("  ⚠️ 重要提醒：在'理想条件'下（H 完全精确 + 噪声协方差已知），")
    print("     残差【向量】本身也完全不变（下面会验证）。")
    print("     那为什么现实中 ML 还能检测出 FDIA？")
    print("     → 因为现实从来不理想。见下节。")
else:
    print("  ⚠️ 结果异常，请检查 H 矩阵构造与攻击向量计算。")
print("=" * 66)


# ============================================================
# 深入一步：为什么"理想 FDIA"下 ML 也检测不出，现实中却能？
# ============================================================

print("\n" + "-" * 66)
print("  深入一步：理想假设一旦松动，攻击就会露出破绽")
print("-" * 66)

x_hat_n = wls_estimate(H, z_normal, SIGMA)
x_hat_a = wls_estimate(H, z_attacked, SIGMA)
r_vec_normal = z_normal - H @ x_hat_n
r_vec_attacked = z_attacked - H @ x_hat_a

cos_sim = (r_vec_normal @ r_vec_attacked) / (
    np.linalg.norm(r_vec_normal) * np.linalg.norm(r_vec_attacked) + 1e-30)

print("【情形一】理想条件（H 精确、噪声已知）")
print(f"  残差范数:  正常 {np.linalg.norm(r_vec_normal):.6f} | "
      f"攻击 {np.linalg.norm(r_vec_attacked):.6f}")
print(f"  残差向量余弦相似度: {cos_sim:.8f}")
print(f"  → 残差向量完全一致。此时 BDD 查不出，ML 也查不出。")
print(f"     这是 FDIA 的'完美形态'—— 但前提是攻击者知道全部信息。")

# ---- 情形二：防御方有"额外信息"（负荷预测）----
print("\n【情形二】防御方掌握额外信息（如负荷预测）")

# 模拟：真实负荷有规律，攻击者让它偏离了预测值
# 防御方用预测注入功率 p_forecast 做一致性校验
p_forecast = H[:n_state] @ x_true + np.random.normal(0, SIGMA * 0.5, n_state)
# 攻击后的注入量测（前 n_state 个）
p_inj_attacked = H[:n_state] @ x_hat_attacked + r_vec_attacked[:n_state]

dev_normal = np.abs(p_forecast - (H[:n_state] @ x_hat_normal + r_vec_normal[:n_state]))
dev_attacked = np.abs(p_forecast - p_inj_attacked)

print(f"  与负荷预测的平均偏差:")
print(f"    正常情形: {dev_normal.mean():.6f}")
print(f"    攻击情形: {dev_attacked.mean():.6f}")
print(f"    放大倍数: {dev_attacked.mean() / (dev_normal.mean() + 1e-12):.2f}×")
print(f"  → {'攻击被发现有明显偏离 ✓' if dev_attacked.mean() > dev_normal.mean() * 1.5 else '偏差不显著'}")

# ---- 情形三：攻击者不知道精确的线路参数（现实中最常见）----
print("\n【情形三】攻击者只知道'近似'拓扑（现实中最常见）")

H_wrong = H + np.random.normal(0, 0.02, H.shape)   # 攻击者用错误的 H
a_wrong = H_wrong @ c                                # 但仍然构造 a = H_error · c
z_att_wrong = z_normal + a_wrong

r_wrong, _ = bdd(H, z_att_wrong, SIGMA)             # 防御方用正确的 H 检测

print(f"  攻击者用带 2% 误差的 H 构造攻击 → 残差范数: {r_wrong:.6f}")
print(f"  正常残差: {r_normal:.6f}（阈值 τ={threshold:.6f}）")
if r_wrong > threshold:
    print(f"  → ⚠️ 攻击被 BDD 检测出来！残差 {r_wrong:.4f} 超过阈值。")
    print(f"     原因：a = H_error·c 不再严格落在真实 H 的列空间里，")
    print(f"     残差中残留了 (H_error - H)·c 这一项，无法抵消。")
else:
    print(f"  → 残差仍在阈值内，攻击仍可隐蔽。")

print("\n" + "=" * 66)
print("  💡 【关键洞见】为什么'传统 BDD 失效'而'AI 仍有效'")
print("=" * 66)
print("""
  1. 理想 FDIA（a = Hc 且 H 精确）下，残差【完全】不变。
     这意味着：任何只看'状态估计残差'的方法（无论 BDD 还是 ML）都无效。

  2. 但现实中，"理想"几乎不可能满足：
       · 攻击者未必掌握精确的线路参数（情形三）
       · 攻击者未必知道当前负荷水平（情形二）
       · 攻击者未必能篡改所有量测（稀疏攻击）
       · 攻击者未必知道防御方用的是哪种状态估计
     只要有一处不精确，攻击就会在残差/量测上留下'痕迹'。

  3. AI 方法的用武之地：
       · 用【负荷预测】做物理一致性校验（Ashok 2017 的思路）
       · 用【图结构】捕捉'量测与邻居对不上'的模式（GNN 的思路）
       · 用【时序】捕捉'突变的模式'（LSTM 的思路）
     它们利用的都是"理想 FDIA 之外"的信息。

  4. ★ 这就是你论文选题的立足点：
      真正的防御不是"检测 a = Hc"（理论上做不到），
      而是"利用攻击者必然无法完美的那一部分信息"。
""")
print("=" * 66)

print("\n✅ 最小验证完成！")
print("\n下一步：")
print("  1. 装好 pandapower 后，跑 code/fdia_gnn_demo.py（完整版，含 GNN）")
print("  2. 阅读 精读笔记_FDIA与GNN.md 第二部分的公式推导")
print("  3. 试试把 H_wrong 的误差从 2% 调到 5%，看攻击如何从'隐蔽'变'被检测'")
