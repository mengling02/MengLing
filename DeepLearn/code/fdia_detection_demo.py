"""
FDIA 检测完整实验 —— 只用 numpy（无需 PyTorch / sklearn）

目的：回答一个关键问题 ——
    "传统坏数据检测（BDD）失效后，机器学习到底能不能检测 FDI 攻击？"

★ 这个脚本的结论可能和你预期的不一样，但它是诚实的：
  **深度学习不是万能药。搞清楚"它在哪儿有用、在哪儿没用"，
    比盲目套模型更有价值 —— 这本身就是你论文的立论基础。**

三个场景，每个场景教一个教训：

    场景 A · 完全信息攻击（攻击者掌握完整 H）
        → 所有单快照方法（含 ML）AUC ≈ 0.5，全部失效。
        → 教训：这是信息论层面的不可检测。别在这里堆模型。

    场景 B · 部分信息攻击（攻击者只掌握部分 H）
        → 传统 BDD 反而检测得很好（残差范数变大）。
        → 教训：判别信息就在"残差范数"里，BDD 已经抓到了。
                 ML 如果不做特征工程，反而不如 BDD。

    场景 C · 时序攻击（状态发生突变）
        → 快照方法全部失效，但"状态跳变"特征可以检出。
        → 教训：物理规律（状态应平滑变化）是免费的先验。
                 这才是 ML 真正有优势的地方。

运行：
    python code/fdia_detection_demo.py

作者：小电 ⚡  ｜  对应课程：Day 38 / Day 41 / Day 48
"""

import numpy as np

np.random.seed(0)


# ============================================================
# 0. 基础工具：手写 AUC / PR-AUC / F1（避免引入 sklearn）
# ============================================================

def roc_auc(y_true, scores):
    """ROC-AUC = 随机取一正一负，正样本分数更高的概率（Mann-Whitney U）。"""
    pos, neg = scores[y_true == 1], scores[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    all_s = np.concatenate([pos, neg])
    order = np.argsort(all_s, kind="mergesort")
    ranks = np.empty(len(all_s), dtype=float)
    ranks[order] = np.arange(1, len(all_s) + 1)
    # 并列取平均秩
    ss = all_s[order]
    i = 0
    while i < len(ss):
        j = i
        while j + 1 < len(ss) and ss[j + 1] == ss[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = ranks[order[i:j + 1]].mean()
        i = j + 1
    u = ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2
    return u / (len(pos) * len(neg))


def average_precision(y_true, scores):
    """PR-AUC（Average Precision）。不平衡场景下比 ROC-AUC 更诚实。"""
    order = np.argsort(-scores)
    ys = y_true[order]
    tp = np.cumsum(ys)
    precision = tp / np.arange(1, len(ys) + 1)
    recall = tp / max(y_true.sum(), 1)
    ap, prev_r = 0.0, 0.0
    for p, r in zip(precision, recall):
        ap += (r - prev_r) * p
        prev_r = r
    return ap


def best_f1(y_true, scores):
    """扫描阈值取最佳 F1。"""
    order = np.argsort(-scores)
    ys = y_true[order]
    tp = np.cumsum(ys)
    fp = np.cumsum(1 - ys)
    fn = y_true.sum() - tp
    p = tp / np.maximum(tp + fp, 1e-12)
    r = tp / np.maximum(tp + fn, 1e-12)
    f1 = 2 * p * r / np.maximum(p + r, 1e-12)
    k = int(np.argmax(f1))
    return f1[k], scores[order][k]


# ============================================================
# 1. 系统模型：z = H x + e
# ============================================================

n_states, m_meas = 5, 12
noise_std = 0.005

# H：① 前 5 行 = PMU 直接量测相角（保证满秩）；② 后 7 行 = 线路潮流量测
H = np.array([
    [ 1,  0,  0,  0,  0],
    [ 0,  1,  0,  0,  0],
    [ 0,  0,  1,  0,  0],
    [ 0,  0,  0,  1,  0],
    [ 0,  0,  0,  0,  1],
    [ 1, -1,  0,  0,  0],
    [ 0,  1, -1,  0,  0],
    [ 0,  0,  1, -1,  0],
    [ 0,  0,  0,  1, -1],
    [ 1,  0, -1,  0,  0],
    [ 1,  1, -1, -1,  0],
    [ 0,  1,  0, -1,  0],
], dtype=float)

assert np.linalg.matrix_rank(H) == n_states, "H 必须满秩"

G_inv = np.linalg.inv(H.T @ H)
# 残差投影矩阵 (I - P)，P = H(HᵀH)⁻¹Hᵀ
M_res = np.eye(m_meas) - H @ G_inv @ H.T


def wls(z):
    """加权最小二乘状态估计"""
    return G_inv @ H.T @ z


def residual(z):
    """量测残差 r = z - H·x̂"""
    return z - H @ wls(z)


def bdd_stat(z):
    """BDD 统计量：残差范数"""
    return np.linalg.norm(residual(z))


class LogisticRegression:
    """手写逻辑回归（梯度下降），作为 ML 检测器。"""

    def __init__(self, lr=0.3, epochs=1500, l2=1e-4):
        self.lr, self.epochs, self.l2 = lr, epochs, l2

    def fit(self, X, y):
        n, d = X.shape
        self.w, self.b = np.zeros(d), 0.0
        for _ in range(self.epochs):
            p = self._sig(X @ self.w + self.b)
            err = p - y
            self.w -= self.lr * (X.T @ err / n + self.l2 * self.w)
            self.b -= self.lr * err.mean()
        return self

    def score(self, X):
        return self._sig(X @ self.w + self.b)

    @staticmethod
    def _sig(z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


def zscore_fit(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    return (Xtr - mu) / sd, (Xte - mu) / sd


def report(title, rows):
    print(f"\n  {'检测器':<34}{'ROC-AUC':>10}{'PR-AUC':>10}{'最佳F1':>10}")
    print(f"  {'-' * 62}")
    for name, y, s in rows:
        auc, ap = roc_auc(y, s), average_precision(y, s)
        f1, _ = best_f1(y, s)
        flag = "  ← 失效" if auc < 0.6 else ""
        print(f"  {name:<34}{auc:>10.4f}{ap:>10.4f}{f1:>10.4f}{flag}")


def banner(title, note):
    print(f"\n{'=' * 70}")
    print(title)
    print(f"{'=' * 70}")
    print(f"  {note}")


# ============================================================
# 场景 A · 完全信息攻击
# ============================================================

def scenario_A(rng):
    banner("场景 A · 完全信息攻击（攻击者掌握完整 H）",
           "攻击构造 Δz = H·Δx —— 被篡改的量测在统计上等价于"
           "'另一个合法状态'的量测。")

    def gen(n, attacked):
        X = rng.uniform(-0.3, 0.3, size=(n, n_states))
        Z = X @ H.T + rng.normal(0, noise_std, size=(n, m_meas))
        if attacked:
            dX = rng.uniform(-0.05, 0.05, size=(n, n_states))
            Z = Z + dX @ H.T
        return Z, np.full(n, int(attacked))

    Ztr_n, ytr_n = gen(3000, False)
    Ztr_a, ytr_a = gen(3000, True)
    Ztr, ytr = np.vstack([Ztr_n, Ztr_a]), np.concatenate([ytr_n, ytr_a])
    Zte_n, yte_n = gen(2000, False)
    Zte_a, yte_a = gen(2000, True)
    Zte, yte = np.vstack([Zte_n, Zte_a]), np.concatenate([yte_n, yte_a])

    # 特征：残差向量 拼接 残差范数
    Ftr = np.array([np.append(residual(z), np.linalg.norm(residual(z))) for z in Ztr])
    Fte = np.array([np.append(residual(z), np.linalg.norm(residual(z))) for z in Zte])
    Ftr_s, Fte_s = zscore_fit(Ftr, Fte)
    clf = LogisticRegression().fit(Ftr_s, ytr)

    report("场景 A", [
        ("传统 BDD（残差范数阈值）", yte, np.array([bdd_stat(z) for z in Zte])),
        ("ML（残差向量 + 范数）", yte, clf.score(Fte_s)),
    ])
    print("""
  → 结论：BDD 和 ML 都在 0.5 附近 = 全部失效。
     这不是方法不够好，是**信息论层面的不可能**：
     攻击后的量测就是"另一个合法状态"的合法量测，
     从单个快照里无论怎么挖都挖不出异常。
     ★ 任何声称"用深度学习检测完全信息 FDI"的论文，都值得怀疑。""")


# ============================================================
# 场景 B · 部分信息攻击
# ============================================================

def scenario_B(rng, known_rows=6):
    banner(f"场景 B · 部分信息攻击（攻击者只掌握 {known_rows}/12 行 H）",
           "攻击者信息不完整 → 注入量无法完全落在 H 的列空间里 → "
           "残差范数变大。")

    def gen(n, attacked):
        X = rng.uniform(-0.3, 0.3, size=(n, n_states))
        Z = X @ H.T + rng.normal(0, noise_std, size=(n, m_meas))
        if attacked:
            dX = rng.uniform(-0.05, 0.05, size=(n, n_states))
            dZ = np.zeros((n, m_meas))
            dZ[:, :known_rows] = dX @ H[:known_rows, :].T   # 只能注入已知行
            Z = Z + dZ
        return Z, np.full(n, int(attacked))

    Ztr_n, ytr_n = gen(3000, False)
    Ztr_a, ytr_a = gen(3000, True)
    Ztr, ytr = np.vstack([Ztr_n, Ztr_a]), np.concatenate([ytr_n, ytr_a])
    Zte_n, yte_n = gen(2000, False)
    Zte_a, yte_a = gen(2000, True)
    Zte, yte = np.vstack([Zte_n, Zte_a]), np.concatenate([yte_n, yte_a])

    # 只给"残差向量"，不给范数 —— 模拟"不做特征工程的 ML"
    Ftr = np.array([residual(z) for z in Ztr])
    Fte = np.array([residual(z) for z in Zte])
    Ftr_s, Fte_s = zscore_fit(Ftr, Fte)
    clf_raw = LogisticRegression().fit(Ftr_s, ytr)

    # 给"残差向量 + 范数" —— 模拟"做了特征工程的 ML"
    Ftr2 = np.array([np.append(residual(z), np.linalg.norm(residual(z))) for z in Ztr])
    Fte2 = np.array([np.append(residual(z), np.linalg.norm(residual(z))) for z in Zte])
    Ftr2_s, Fte2_s = zscore_fit(Ftr2, Fte2)
    clf_norm = LogisticRegression().fit(Ftr2_s, ytr)

    report("场景 B", [
        ("传统 BDD（残差范数阈值）", yte, np.array([bdd_stat(z) for z in Zte])),
        ("ML（仅残差向量，无特征工程）", yte, clf_raw.score(Fte_s)),
        ("ML（残差向量 + 范数）", yte, clf_norm.score(Fte2_s)),
    ])
    print("""
  → 结论：BDD 反而检测得很好！因为判别信息就在"残差范数"里，
     而 BDD 天然用了这个统计量。
     ML 如果不做特征工程（只喂残差向量），反而不如 BDD ——
     因为线性模型算不出"范数"这种二次型统计量。
     ★ 教训：不是"深度模型一定比传统方法好"。
       在信息已经充分暴露的场景里，传统方法可能又准又便宜。
       论文里必须解释"为什么非要用深度学习"，否则会被审稿人问住。""")


# ============================================================
# 场景 C · 时序攻击（ML 真正的用武之地）
# ============================================================

def scenario_C(rng, T=10, step_std=0.004):
    banner("场景 C · 时序攻击（状态在某一时刻发生突变）",
           "单快照完全看不出问题，但物理上状态应该平滑变化 —— "
           "这个'平滑性'是免费的先验。")

    def gen_seq(n, attacked):
        Zs = np.zeros((n, T, m_meas))
        for i in range(n):
            x = rng.uniform(-0.2, 0.2, size=n_states)
            t0 = rng.integers(2, T) if attacked else T + 1   # 攻击起始时刻
            dX = rng.uniform(-0.06, 0.06, size=n_states) if attacked else None
            for t in range(T):
                x = x + rng.normal(0, step_std, size=n_states)   # 平滑随机游走
                x_eff = x + dX if (attacked and t >= t0) else x
                Zs[i, t] = H @ x_eff + rng.normal(0, noise_std, size=m_meas)
        return Zs, np.full(n, int(attacked))

    Ztr_n, ytr_n = gen_seq(1500, False)
    Ztr_a, ytr_a = gen_seq(1500, True)
    Ztr, ytr = np.vstack([Ztr_n, Ztr_a]), np.concatenate([ytr_n, ytr_a])
    Zte_n, yte_n = gen_seq(800, False)
    Zte_a, yte_a = gen_seq(800, True)
    Zte, yte = np.vstack([Zte_n, Zte_a]), np.concatenate([yte_n, yte_a])

    def feat_snapshot(Zs):
        """快照特征：序列上最大的残差范数（BDD 思路）"""
        return np.array([[max(bdd_stat(z) for z in seq)] for seq in Zs])

    def feat_temporal(Zs):
        """时序特征：状态估计的最大跳变幅度"""
        out = []
        for seq in Zs:
            xs = np.array([wls(z) for z in seq])
            jumps = np.linalg.norm(np.diff(xs, axis=0), axis=1)
            out.append([jumps.max(), jumps.mean(), jumps.max() / (jumps.mean() + 1e-9)])
        return np.array(out)

    # 快照检测器（直接阈值）
    s_snap_te = feat_snapshot(Zte).ravel()
    # 时序检测器（ML 在时序特征上）
    Ftr, Fte = feat_temporal(Ztr), feat_temporal(Zte)
    Ftr_s, Fte_s = zscore_fit(Ftr, Fte)
    clf_t = LogisticRegression().fit(Ftr_s, ytr)

    report("场景 C", [
        ("快照 BDD（序列最大残差范数）", yte, s_snap_te),
        ("ML 时序特征（状态跳变统计）", yte, clf_t.score(Fte_s)),
    ])
    print("""
  → 结论：快照方法失效（残差不变），时序特征有效。
     ★ 教训：这才是 ML 真正有优势的地方 ——
       它能把"物理规律"（状态应平滑变化）编码成特征，
       捕获单快照方法根本看不到的异常。
       时序一致性约束是**免费的先验**，也是论文最容易做出新意的地方。""")


# ============================================================
# 主流程
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("FDIA 检测实验：传统 BDD vs 机器学习 —— 边界在哪里？")
    print("=" * 70)
    print(f"系统：{n_states} 状态 / {m_meas} 量测（冗余度 {m_meas / n_states:.1f}x）")
    print("说明：ROC-AUC = 0.5 等价于随机猜测（完全检测不出）")

    rng = np.random.default_rng(7)

    scenario_A(rng)
    scenario_B(rng, known_rows=6)
    scenario_C(rng)

    print(f"\n{'=' * 70}")
    print("★ 总结：机器学习在 FDI 检测上的真实边界 ★")
    print("=" * 70)
    print("""
  ┌─────────────────┬──────────────┬────────────────────────────────┐
  │ 攻击类型        │ 谁有效       │ 你的论文该怎么写               │
  ├─────────────────┼──────────────┼────────────────────────────────┤
  │ 完全信息攻击    │ 都不行       │ 别碰，这是信息论死胡同         │
  │ 部分信息攻击    │ 传统 BDD     │ 需论证"ML 相对 BDD 的增量价值" │
  │ 时序攻击        │ ML + 时序先验│ ★ 最有空间，重点做这里         │
  └─────────────────┴──────────────┴────────────────────────────────┘

  → 论文立论建议（不要写"我用深度学习检测 FDI"，太泛会被拒）：
     1. 明确攻击者的信息边界（威胁模型），选"部分信息"而非"完全信息"
     2. 把物理约束（时序平滑性 / 潮流方程 / 状态范围）显式建模进方法
     3. 和强 BDD 基线对比，并解释为什么你的方法有增量价值
     4. 在"完全信息攻击"上诚实承认不可检测，反而增加论文可信度

  下一步：把这里的思路落到真实数据上 ——
     docs/实验_FDI注入与异常检测.md   （实验手册：环境/步骤/进阶）
     docs/Week06_论文阅读与电网场景.md （Day 38 原理，Day 41 pandapower）
     docs/Week08_实验设计与论文写作.md （Day 50 威胁模型怎么写）
""")
