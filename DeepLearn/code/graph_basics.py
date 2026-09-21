"""
graph_basics.py —— 电网图建模的最小可运行示例（只需 numpy）

对应 docs/Week10_图神经网络与电网拓扑建模.md 的 Day 61-62。

跑它能看到三件事：
  1. IEEE 14 节点系统的邻接矩阵长什么样，为什么它是"稀疏 + 对称"的
  2. 为什么 GCN 要做对称归一化 —— 不做会怎样（数值会爆炸）
  3. 一个 GCN 层的前向传播到底在算什么（就是"邻居加权平均 + 线性变换"）

运行：
    python code/graph_basics.py

依赖：numpy（无需 torch / PyG）
"""

import numpy as np

np.set_printoptions(precision=3, suppress=True, linewidth=120)

# ---------------------------------------------------------------------------
# 一、IEEE 14 节点系统的拓扑（公开标准测试系统，非任何真实电网数据）
# ---------------------------------------------------------------------------
# 20 条支路。其中 4-7、4-9、5-6 三条在标准算例里是变压器支路。
# ⚠️ 新手最容易犯的错：只遍历 pandapower 的 net.line，会漏掉这 3 条变压器，
#    图就断了（IEEE 14 会退化成多个不连通子图）。这里把 20 条全列出来。
BRANCHES = [
    (1, 2), (1, 5),
    (2, 3), (2, 4), (2, 5),
    (3, 4),
    (4, 5), (4, 7), (4, 9),      # 4-7、4-9 是变压器
    (5, 6),                       # 5-6 是变压器
    (6, 11), (6, 12), (6, 13),
    (7, 8), (7, 9),
    (9, 10), (9, 14),
    (10, 11),
    (12, 13),
    (13, 14),
]

N_BUS = 14


def build_adjacency(n_bus, branches):
    """由支路列表构造邻接矩阵 A（对称、对角为 0）。"""
    A = np.zeros((n_bus, n_bus), dtype=float)
    for i, j in branches:
        A[i - 1, j - 1] = 1.0
        A[j - 1, i - 1] = 1.0
    return A


# ---------------------------------------------------------------------------
# 二、GCN 的对称归一化：Â = D̃^(-1/2) Ã D̃^(-1/2)，其中 Ã = A + I
# ---------------------------------------------------------------------------
def gcn_normalize(A):
    """
    Kipf & Welling (ICLR 2017) 的对称归一化邻接矩阵。

    为什么必须归一化：
      · 不归一化时，一个节点的输出是"邻居特征之和"，
        度数高的节点输出会远大于度数低的节点（能量不守恒）
      · 堆几层之后数值会指数增长 → 梯度爆炸 / 训练发散
      · 归一化后，每个节点看到的是"邻居特征的加权平均"，量级稳定
    """
    n = A.shape[0]
    A_tilde = A + np.eye(n)                      # 加自环：自己也参与聚合
    deg = A_tilde.sum(axis=1)                    # 度数（含自环）
    d_inv_sqrt = np.diag(1.0 / np.sqrt(deg))
    return d_inv_sqrt @ A_tilde @ d_inv_sqrt


# ---------------------------------------------------------------------------
# 三、一个 GCN 层的前向传播
# ---------------------------------------------------------------------------
def gcn_layer(A_hat, X, W):
    """
    H = Â · X · W   （省略激活函数）

    A_hat: [N, N]  归一化邻接矩阵
    X    : [N, F]  节点特征
    W    : [F, F'] 可学习权重

    这就是 GCN 的全部 —— 它没有任何神奇之处：
      ① Â · X  → 每个节点把自己的特征和邻居特征加权平均（聚合）
      ② (·) · W → 过一层线性变换（和普通全连接层一样）
    """
    return A_hat @ X @ W


def main():
    print("=" * 72)
    print("一、邻接矩阵：把 IEEE 14 的拓扑写成一个 14×14 矩阵")
    print("=" * 72)

    A = build_adjacency(N_BUS, BRANCHES)
    n_edges = int(A.sum() / 2)

    print(f"节点数（母线）  : {N_BUS}")
    print(f"边数（支路）    : {n_edges}")
    print(f"矩阵元素总数    : {N_BUS * N_BUS}")
    print(f"稀疏度          : {1 - A.sum() / A.size:.3f}   ← 只有约 20% 的位置非零")
    print()
    print("A 的前 6×6 子块：")
    print(A[:6, :6].astype(int))
    print()
    print("验证三条性质：")
    print(f"  对称（A == A.T）      : {np.allclose(A, A.T)}")
    print(f"  对角全为 0            : {np.all(np.diag(A) == 0)}")
    print(f"  是否连通（无孤立节点）: {np.all(A.sum(axis=1) > 0)}")
    print()

    print("各节点度数（连接了几条支路）：")
    deg = A.sum(axis=1).astype(int)
    for bus, d in enumerate(deg, start=1):
        bar = "█" * d
        print(f"  母线 {bus:>2} : {d:>2}  {bar}")
    print(f"  → 度数最高的母线是 {int(np.argmax(deg)) + 1} 号（{deg.max()} 条支路）")
    print("  → 度数分布不均匀，这正是图神经网络要处理的结构信息")
    print()

    print("=" * 72)
    print("二、为什么必须做对称归一化")
    print("=" * 72)

    # 造一个假的特征矩阵：每个节点 2 维特征（比如 [电压幅值, 有功注入]）
    rng = np.random.default_rng(42)
    X = rng.normal(size=(N_BUS, 2))
    W = np.eye(2)  # 用单位阵，先隔离归一化的影响

    # --- 不归一化 ---
    A_no_norm = A + np.eye(N_BUS)                     # 只加自环，不归一化
    H_no_norm = A_no_norm @ X @ W

    # --- 归一化 ---
    A_hat = gcn_normalize(A)
    H_norm = A_hat @ X @ W

    print("用同一个输入特征 X，对比两种聚合方式输出的量级：")
    print()
    print(f"{'节点':>4} {'度数':>5} {'未归一化 ‖h‖':>14} {'归一化 ‖h‖':>13}")
    print("-" * 42)
    for i in range(N_BUS):
        n1 = np.linalg.norm(H_no_norm[i])
        n2 = np.linalg.norm(H_norm[i])
        print(f"{i + 1:>4} {int(deg[i]):>5} {n1:>14.3f} {n2:>13.3f}")
    print()
    print(f"未归一化输出的范数范围 : [{np.linalg.norm(H_no_norm, axis=1).min():.3f}, "
          f"{np.linalg.norm(H_no_norm, axis=1).max():.3f}]")
    print(f"归一化后输出的范数范围 : [{np.linalg.norm(H_norm, axis=1).min():.3f}, "
          f"{np.linalg.norm(H_norm, axis=1).max():.3f}]")
    print()

    # 堆多层看会怎样
    print("把它堆 10 层（每层都用同样的 A，不做任何归一化 vs 做归一化）：")
    print()
    h_no = X.copy()
    h_yes = X.copy()
    for layer in range(1, 11):
        h_no = A_no_norm @ h_no @ W
        h_yes = A_hat @ h_yes @ W
        if layer in (1, 3, 5, 10):
            print(f"  第 {layer:>2} 层后  未归一化最大幅值 = {np.abs(h_no).max():>12.3e}"
                  f"   归一化后最大幅值 = {np.abs(h_yes).max():>10.3f}")
    print()
    print("  → 未归一化：数值随层数指数增长（这里用单位阵都能看出来）")
    print("    真实网络里 W 是可学习的，几层之后就会梯度爆炸 / 训练发散")
    print("  → 归一化后：数值稳定在合理范围，可以放心堆深度")
    print()

    print("=" * 72)
    print("三、一个 GCN 层到底在算什么")
    print("=" * 72)

    print("公式：H = Â · X · W     （省略激活函数）")
    print()
    print("拆开看，对节点 i 来说就是：")
    print("  h_i = Σ_{j ∈ N(i) ∪ {i}}  (1 / √(d_i · d_j)) · x_j · W")
    print()
    print("  ① 先按 1/√(d_i·d_j) 加权，把邻居 j 的特征聚合过来")
    print("     → 度数高的邻居贡献被压低，避免「话多的人主导」")
    print("  ② 再乘 W 做线性变换（和全连接层完全一样）")
    print()

    # 手工验证一个节点
    node = 3  # 0-indexed → 母线 4，度数最高
    neighbors = [int(i) + 1 for i in np.where(A[node] > 0)[0]]
    print(f"手工验证母线 {node + 1}（度数 {int(deg[node])}，邻居 {neighbors}）：")
    manual = np.zeros(2)
    for j in range(N_BUS):
        manual += A_hat[node, j] * (X[j] @ W)
    auto = H_norm[node]
    print(f"  手工聚合结果 : {manual}")
    print(f"  矩阵乘法结果 : {auto}")
    print(f"  是否一致     : {np.allclose(manual, auto)}")
    print()

    print("=" * 72)
    print("四、和电网安全的关系")
    print("=" * 72)
    print("""
  这段代码和 Day 37 的状态估计方程 z = H·x + e 是同一件事的两种写法：

    · H 的每一行 = 一个量测，每一列 = 一个状态
    · H 的稀疏结构【完全由拓扑决定】：只有物理相连的节点之间才有非零元
    · 换句话说：H 就是这张图的邻接关系在物理定律（基尔霍夫定律）下的具体化

  这对 FDI 检测意味着什么？

    · 攻击者要构造 Δz = H·Δx 绕过 BDD，就必须【知道 H 的结构】
    · 而 H 的结构 = 拓扑 —— 所以"攻击者知道多少拓扑"
      直接决定了他能构造多隐蔽的攻击
    · 这正是【选题 B（攻击者信息边界）】的物理基础：
      把"知道 k 行 H"和"知道图的一部分"对应起来，
      你就有了一个可参数化、可实验的攻击强度定义

  ⚠️ 但也要诚实：GNN 不是电网检测的万能解。
     如果拓扑固定不变、数据本身没有明显的图结构优势，
     GNN 未必打得过调好参的 MLP —— 因为 GNN 的额外结构先验
     在没有"结构变化"的场景下，只是多余的约束。
     什么时候 GNN 真正有用？拓扑会变（N-1、检修、拓扑攻击）
     或量测缺失导致部分节点不可观测的时候。
""")


if __name__ == "__main__":
    main()
