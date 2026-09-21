"""
FDIA 最小验证脚本 —— 零重依赖（只需 numpy）

目的：用 5 秒跑通一个实验，亲眼看到虚假数据注入攻击（FDIA）的核心结论：

    ★ 攻击后，坏数据检测（BDD）的残差几乎完全不变（1e-15 量级），
      但状态估计结果被偏移了 —— 也就是说 BDD 从数学上"看不见"这次攻击。

这就是 Day 38 讲的那个核心漏洞，也是你论文选题的起点。

运行：
    python code/fdia_minimal.py

作者：小电 ⚡  ｜  对应课程：Day 38 / Day 41
"""

import numpy as np

np.random.seed(42)


# ============================================================
# 第一步：构造一个直流潮流（DC power flow）量测模型
# ============================================================
# 电力系统状态估计的线性化模型：
#     z = H · x + e
#   z : 量测量（m 维，m > n，存在冗余）
#   H : 量测矩阵（m × n），描述"状态"如何映射到"量测"
#   x : 状态量（n 维，即各节点的电压相角）
#   e : 量测误差（高斯噪声）

n_states = 5      # 5 个节点（除参考节点外的相角）
m_meas = 12       # 12 个量测（存在冗余，这是能做状态估计的前提）

# 构造一个结构化的 H 矩阵（模拟真实的网络拓扑）
#
# 真实系统里 H 由两部分组成：
#   ① PMU 直接量测：直接测节点电压相角  → 对应下面前 5 行（单位阵）
#   ② 线路潮流量测：测的是相角差        → 对应下面后 7 行
#
# 注意：只有"相角差"量测时 H 的秩会退化（只能确定相对关系，
# 无法确定绝对水平）。加入 PMU 直接量测后秩才满 —— 这就是
# 为什么 PMU 对状态可观性如此重要。
H = np.array([
    # ① PMU 直接量测节点相角（5 行，保证满秩）
    [ 1,  0,  0,  0,  0],
    [ 0,  1,  0,  0,  0],
    [ 0,  0,  1,  0,  0],
    [ 0,  0,  0,  1,  0],
    [ 0,  0,  0,  0,  1],
    # ② 线路潮流量测（相角差，提供冗余）
    [ 1, -1,  0,  0,  0],   # 支路 1-2
    [ 0,  1, -1,  0,  0],   # 支路 2-3
    [ 0,  0,  1, -1,  0],   # 支路 3-4
    [ 0,  0,  0,  1, -1],   # 支路 4-5
    [ 1,  0, -1,  0,  0],   # 支路 1-3
    [ 1,  1, -1, -1,  0],   # 支路组合
    [ 0,  1,  0, -1,  0],   # 支路 2-4
], dtype=float)

assert H.shape == (m_meas, n_states), "H 的形状不对"

# 检查量测冗余度：H 的秩必须等于状态数，否则状态不可观测
rank = np.linalg.matrix_rank(H)
print(f"[1] 量测矩阵 H: {H.shape}, 秩 = {rank} (需等于状态数 {n_states})")
assert rank == n_states, "系统不可观测！"


# ============================================================
# 第二步：生成"正常"量测数据
# ============================================================
x_true = np.random.uniform(-0.3, 0.3, size=n_states)     # 真实状态（相角，弧度）
noise_std = 0.005                                        # 量测噪声标准差
e = np.random.normal(0, noise_std, size=m_meas)

z = H @ x_true + e          # 正常量测

print(f"[2] 真实状态 x_true = {np.round(x_true, 4)}")
print(f"    正常量测 z (前 4 个) = {np.round(z[:4], 4)}")


# ============================================================
# 第三步：加权最小二乘（WLS）状态估计
# ============================================================
# 估计公式（权重矩阵取单位阵）：
#     x_hat = (Hᵀ H)⁻¹ Hᵀ z
# 残差：
#     r = z - H · x_hat
# 坏数据检测（BDD）：
#     ||r||₂ > τ  →  报警

def wls_estimate(H, z):
    """加权最小二乘状态估计（权重为单位阵）"""
    G = H.T @ H                       # 增益矩阵
    x_hat = np.linalg.solve(G, H.T @ z)
    return x_hat


def residual(H, z, x_hat):
    """量测残差"""
    return z - H @ x_hat


# 坏数据检测阈值（工程上常用卡方分布或经验阈值，这里取 3 倍噪声水平）
tau = 3.0 * noise_std * np.sqrt(m_meas - n_states)

x_hat_normal = wls_estimate(H, z)
r_normal = residual(H, z, x_hat_normal)
norm_r_normal = np.linalg.norm(r_normal)

print(f"[3] 正常情况：")
print(f"    估计状态 x_hat = {np.round(x_hat_normal, 4)}")
print(f"    ||x_hat - x_true|| = {np.linalg.norm(x_hat_normal - x_true):.6f}")
print(f"    ||r|| = {norm_r_normal:.6f}  (阈值 τ = {tau:.6f})")
print(f"    BDD 判定：{'⚠ 报警' if norm_r_normal > tau else '✓ 通过（无坏数据）'}")


# ============================================================
# 第四步：构造 FDI 攻击
# ============================================================
# 攻击者的核心构造：
#     任选一个偏移量 Δx（攻击者想让状态被误估成什么样子）
#     令 Δz = H · Δx
#     注入后：z_bad = z + Δz
#
# 数学证明（这是整个攻击的关键）：
#     x_hat_bad = (HᵀH)⁻¹ Hᵀ (z + HΔx)
#               = (HᵀH)⁻¹ Hᵀ z + (HᵀH)⁻¹ (Hᵀ H) Δx
#               = x_hat + Δx              ← 状态被精确偏移了 Δx
#
#     r_bad = z_bad - H · x_hat_bad
#           = (z + HΔx) - H(x_hat + Δx)
#           = z - H · x_hat
#           = r                       ← 残差完全不变！
#
# 所以 BDD 完全无法检测 —— 因为从残差看，这组量测"自洽"。

delta_x = np.array([0.05, -0.03, 0.02, -0.04, 0.01])   # 攻击者想造成的状态偏移
delta_z = H @ delta_x                                   # 精心构造的注入量
z_bad = z + delta_z                                     # 被污染的量测

print(f"\n[4] FDI 攻击：")
print(f"    目标状态偏移 Δx = {np.round(delta_x, 4)}")
print(f"    构造注入量 Δz = H·Δx = {np.round(delta_z[:4], 4)} ... (共 {m_meas} 维)")
print(f"    篡改幅度 ||Δz|| = {np.linalg.norm(delta_z):.6f}")
print(f"    单点最大篡改 = {np.abs(delta_z).max():.6f}  "
      f"(占量测幅度 {np.abs(delta_z).max() / np.abs(z).max() * 100:.1f}%)")


# ============================================================
# 第五步：攻击后的检测与估计 —— 核心结论
# ============================================================
x_hat_bad = wls_estimate(H, z_bad)
r_bad = residual(H, z_bad, x_hat_bad)
norm_r_bad = np.linalg.norm(r_bad)

state_shift = np.linalg.norm(x_hat_bad - x_hat_normal)
residual_diff = abs(norm_r_bad - norm_r_normal)

print(f"\n[5] 攻击后的状态估计与检测：")
print(f"    估计状态 x_hat_bad = {np.round(x_hat_bad, 4)}")
print(f"    估计值偏移 ||x_hat_bad - x_hat_normal|| = {state_shift:.6f}")
print(f"    ||r_bad|| = {norm_r_bad:.6f}  (阈值 τ = {tau:.6f})")
print(f"    BDD 判定：{'⚠ 报警' if norm_r_bad > tau else '✓ 通过（无坏数据）'}")

print("\n" + "=" * 62)
print("★ 核心结论 ★")
print("=" * 62)
print(f"  状态被偏移了        : {state_shift:.6f}   ← 攻击成功")
print(f"  残差范数变化        : {residual_diff:.2e}   ← BDD 完全看不见")
print(f"  BDD 能否检出        : {'能' if norm_r_bad > tau else '不能（漏报！）'}")
print("=" * 62)
print("""
这说明：任何基于"量测残差"的传统坏数据检测（BDD），
对满足 Δz = H·Δx 的虚假数据注入攻击都是无效的。

★ 但请注意一个重要的事实（很多人在这里想错）：
  这种攻击之所以检测不出，是因为被篡改的量测在统计上
  就等价于"另一个合法状态"的量测。也就是说 ——
  **单快照下它是信息论层面不可检测的，堆任何深度学习模型都没用。**

  所以"用深度学习检测 FDI"这个说法本身太粗。真正有空间的是：
    ① 攻击者信息不完整时（残差出现结构化模式）
    ② 引入时序约束（状态物理上应平滑变化）
    ③ 从"检测攻击"转向"检测状态是否物理可信"

  完整实验（三个场景的对比 + 结论）见：
    python code/fdia_detection_demo.py
  原理讲解见：
    docs/Week06_论文阅读与电网场景.md 的 Day 38
    docs/实验_FDI注入与异常检测.md
""")

# 额外：验证攻击的可检测性取决于攻击者的知识
# 如果攻击者不知道完整的 H（只用了部分行），残差就会变化
print("[6] 补充实验：攻击者只掌握部分 H 时会怎样？")
k = 8   # 攻击者只知道前 8 行
H_partial = H[:k, :]
delta_z_partial = np.zeros(m_meas)
delta_z_partial[:k] = H_partial @ delta_x     # 只能构造前 8 个量测的注入
z_bad_partial = z + delta_z_partial

x_hat_p = wls_estimate(H, z_bad_partial)
r_p = residual(H, z_bad_partial, x_hat_p)
print(f"    部分信息攻击：||r|| = {np.linalg.norm(r_p):.6f}  "
      f"(对比正常 {norm_r_normal:.6f})")
print(f"    BDD 判定：{'⚠ 报警（被检出）' if np.linalg.norm(r_p) > tau else '✓ 未检出'}")
print("""
→ 结论：攻击者掌握的信息越少，攻击越容易被检出。
   这就是论文里"威胁模型"必须写清楚"攻击者知道什么"的原因。
""")
