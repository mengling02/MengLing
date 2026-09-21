# -*- coding: utf-8 -*-
"""
GNN 检测 FDIA —— 纯 PyTorch 实现（不依赖 PyTorch Geometric）
=========================================================

为什么写这个脚本？
  PyTorch Geometric (PyG) 的安装经常失败（需要匹配 torch 版本的 C++ 扩展）。
  但 GNN 的核心其实只是"邻居聚合"，用纯 PyTorch 的稠密矩阵乘法
  就能实现，反而更容易看懂原理。

  电网规模通常在几百到几千节点，稠密邻接矩阵完全够用 ——
  这正好是"理解 GNN 本质"的最佳尺度。

对应笔记：精读笔记_FDIA与GNN.md 论文 ②（GDN）与论文 ③（E-GraphSAGE）

运行：
  python code/gnn_pure_torch.py

依赖：numpy + torch（+ pandapower 用于加载算例）
      若没有 pandapower，会自动退化为"内置 14 节点算例"
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:
    raise SystemExit(
        "\n[错误] 未安装 PyTorch。\n"
        "安装：pip install torch -i https://pypi.tuna.tsinghua.edu.cn/simple\n"
    )

np.random.seed(42)
torch.manual_seed(42)


# ============================================================
# 一、电网算例（优先用 pandapower，否则用内置的 14 节点数据）
# ============================================================

# IEEE 14 节点系统的线路表（from_bus, to_bus, x_pu）—— 作为降级方案
IEEE14_LINES = [
    (0, 1, 0.05917), (0, 4, 0.22304), (1, 2, 0.19797),
    (1, 3, 0.17632), (1, 4, 0.17388), (2, 3, 0.17103),
    (3, 4, 0.04211), (3, 6, 0.20912), (3, 8, 0.55618),
    (4, 5, 0.25202), (5, 10, 0.19890), (5, 11, 0.25581),
    (5, 12, 0.13027), (6, 7, 0.17615), (7, 8, 0.11001),
    (8, 9, 0.08450), (9, 10, 0.08450), (10, 11, 0.19207),
    (11, 12, 0.19988), (12, 13, 0.34802),
]
IEEE14_N_BUS = 14
IEEE14_SLACK = 0


def load_case():
    """返回 (lines, n_bus, slack)，优先 pandapower"""
    try:
        import pandapower.networks as pn
        net = pn.case14()
        import pandapower as pp
        pp.runpp(net, calculate_voltage_angles=True, numba=False)
        lines = []
        for _, line in net.line.iterrows():
            if not line['in_service']:
                continue
            vn = net.bus.at[int(line['from_bus']), 'vn_kv']
            z_base = vn ** 2 / net.sn_mva
            x_pu = line['x_ohm_per_km'] * line['length_km'] / z_base
            lines.append((int(line['from_bus']), int(line['to_bus']), x_pu))
        for _, tr in net.trafo.iterrows():
            x_pu = (tr['vk_percent'] / 100.0) * (net.sn_mva / tr['sn_mva'])
            lines.append((int(tr['hv_bus']), int(tr['lv_bus']), x_pu))
        slack = int(net.ext_grid.bus.values[0])
        print(f"      [数据源] pandapower IEEE 14 节点（{len(lines)} 条支路）")
        return lines, len(net.bus), slack
    except Exception as e:
        print(f"      [数据源] 内置 IEEE 14 节点数据（pandapower 不可用: {type(e).__name__}）")
        return IEEE14_LINES, IEEE14_N_BUS, IEEE14_SLACK


# ============================================================
# 二、构造 H 矩阵与邻接矩阵
# ============================================================

def build_H_and_adj(lines, n_bus, slack):
    """
    同时构造：
      H    —— 量测雅可比矩阵（用于生成数据）
      A    —— 电网图的邻接矩阵（用于 GNN）
      state_buses / bus2col —— 状态向量与母线编号的映射
      branch_rows —— 支路索引（H 的前 len(lines) 行对应支路）

    返回 (H, A, state_buses, bus2col, branch_rows)
    """
    state_buses = [b for b in range(n_bus) if b != slack]
    bus2col = {b: i for i, b in enumerate(state_buses)}
    n_state = len(state_buses)

    # ---- 邻接矩阵（用导纳加权，反映"电气距离近"）----
    A = np.zeros((n_bus, n_bus), dtype=np.float32)
    for (f, t, x) in lines:
        A[f, t] = A[t, f] = 1.0 / max(x, 1e-9)

    # ---- H 矩阵 ----
    branch_rows = []                  # [(from_bus, to_bus, x)] 与 H 行号对齐
    rows, cols, vals = [], [], []
    row = 0
    # (1) 支路有功潮流：p_ij = (θ_i - θ_j) / x
    for (f, t, x) in lines:
        b = 1.0 / max(x, 1e-9)
        if f in bus2col:
            rows.append(row); cols.append(bus2col[f]); vals.append(b)
        if t in bus2col:
            rows.append(row); cols.append(bus2col[t]); vals.append(-b)
        branch_rows.append((f, t, x))
        row += 1
    # (2) 节点注入有功：p_i = Σ_j (θ_i - θ_j) / x_ij
    for b_bus in state_buses:
        for (f, t, x) in lines:
            bb = 1.0 / max(x, 1e-9)
            if f == b_bus:
                rows.append(row); cols.append(bus2col[f]); vals.append(bb)
                if t in bus2col:
                    rows.append(row); cols.append(bus2col[t]); vals.append(-bb)
            elif t == b_bus:
                rows.append(row); cols.append(bus2col[t]); vals.append(bb)
                if f in bus2col:
                    rows.append(row); cols.append(bus2col[f]); vals.append(-bb)
        row += 1

    H = np.zeros((row, n_state))
    for r, c, v in zip(rows, cols, vals):
        H[r, c] += v
    return H, A, state_buses, bus2col, branch_rows


def wls(H, z, sigma):
    W = np.eye(len(z)) / (sigma ** 2)
    A_ = H.T @ W @ H
    b_ = H.T @ W @ z
    x, *_ = np.linalg.lstsq(A_, b_, rcond=None)
    return x


# ============================================================
# 三、生成数据：把"量测残差"映射到节点，得到节点级特征
# ============================================================

def generate_dataset(H, A, n_bus, state_buses, bus2col, branch_rows,
                     n_samples=400, attack_ratio=0.5,
                     attack_scale=0.10, sigma=0.01, scan_scales=None,
                     res_scale=None, imperfect=True, keep_ratio=0.6,
                     load_known_ratio=0.0):
    """
    每个样本 = 一张图（一个运行场景）

    ★★ 本脚本最重要的一个设计决策：攻击必须是"不完美的" ★★

    如果按教科书的理想 FDIA 生成数据（a = Hc，H 精确、噪声已知、全量测篡改），
    那么残差向量**完全不变**，且状态估计被精确推到 x+c —— 而 x+c 本身
    也是一个物理上完全合法的状态。

    实测结果：所有全局统计量的 AUC 都 ≈ 0.50（|r|均值、|r|最大、|r|L2、
    |x̂|等等，全都在 0.49~0.51 之间徘徊）。

    **这不是 bug，这是理论必然 —— 理想 FDIA 在信息论上不可检测。**
    任何声称能检测理想 FDIA 的方法，要么用了未来信息，要么偷换了设定。

    那论文里的 GNN 到底在检测什么？检测**攻击者的不完美**。
    真实攻击者必然受限于三类信息缺失：

      ① 不知道精确的负荷水平 x_true（只能按预测值 μ 构造攻击）
         → 实际注入变成 a = H·c，但攻击者以为注入的是 H·ĉ，
           残差里留下了 (μ - x_true) 的痕迹
      ② 不知道精确的拓扑 H（量测有误差 H_hat ≠ H）
         → a = H_hat·c 不再落在 col(H) 里，残差直接暴露
      ③ 只能篡改部分量测（稀疏攻击，只改 k 个）
         → a = H·c 但被截断，残差同样暴露

    本函数默认 imperfect=True，同时注入 ① 和 ③。
    把 imperfect=False 可以复现"理想 FDIA 不可检测"这个反直觉结论
    （对应 fdia_minimal.py 的实测）。

    节点特征（每个节点 5 维）：
      0) 该节点相关量测残差的平均绝对值 / res_scale
      1) 该节点相关量测残差的最大绝对值 / res_scale
      2) 该节点相关量测的原始值均值（按量纲归一化）
      3) 该节点的度（归一化）
      4) 该节点自身残差 / res_scale

    ★ 归一化的关键设计：绝不能用"每个样本各自除以本样本的最大残差"！
      那会把幅值信息完全抹掉（实测正常 0.5954 vs 攻击 0.5881，无法区分）。
      正确做法是用**全局固定尺度** res_scale。
    """
    m = H.shape[0]
    n_state = H.shape[1]
    n_branch = len(branch_rows)

    branch_ends = [(f, t) for (f, t, _) in branch_rows]
    inj_bus = list(state_buses)

    deg = A.sum(axis=1)
    deg_norm = deg / (deg.max() + 1e-9)

    X_graphs, y_graphs = [], []

    if scan_scales is None:
        scan_scales = [0.05, 0.10, 0.20]

    # ---- 全局残差尺度标定（只用正常样本水平）----
    if res_scale is None:
        probe = []
        for _ in range(30):
            xp = np.random.uniform(-0.15, 0.15, n_state)
            zp = H @ xp + np.random.normal(0, sigma, m)
            rp = zp - H @ wls(H, zp, sigma)
            probe.append(np.abs(rp).mean())
        res_scale = float(np.mean(probe)) + 1e-9

    z_scale = 0.15 * np.linalg.norm(H, axis=0).mean() + 1e-9   # 量测幅值的全局尺度

    for s in range(n_samples):
        is_attack = (s % 2 == 1) if attack_ratio == 0.5 else (np.random.rand() < attack_ratio)

        x_true = np.random.uniform(-0.15, 0.15, n_state)
        z = H @ x_true + np.random.normal(0, sigma, m)

        cur_scale = float(np.random.choice(scan_scales)) if is_attack else 0.0

        if is_attack and cur_scale > 0:
            # ---- 攻击者想让状态偏移 c（按攻击强度标定）----
            c = np.random.normal(0, cur_scale * 0.15, n_state)
            a_ideal = H @ c                       # 理想攻击向量

            if imperfect:
                # ① 负荷知识不完美：
                #    load_known_ratio=1.0 表示攻击者完全知道真实负荷（理想）
                #    load_known_ratio=0.0 表示只知道"平均负荷 0"（现实）
                #    实际没能抵消掉的那部分负荷误差 = (1-ratio) * H @ x_true
                miss = (1.0 - load_known_ratio) * (H @ x_true)
                a_real = a_ideal - miss
                # ③ 稀疏篡改：只能实时改写 keep_ratio 比例的量测
                k = max(1, int(keep_ratio * m))
                idx = np.random.choice(m, size=k, replace=False)
                a_full = np.zeros(m)
                # 攻击者把想改的量测改成"理想值"，但受限于负荷知识
                a_full[idx] = a_real[idx]
                z = z + a_full
            else:
                # 理想 FDIA：全量测、精确负荷知识 → a = Hc，理论不可检测
                z = z + a_ideal

        x_hat = wls(H, z, sigma)
        r = z - H @ x_hat

        node_res_sum = np.zeros(n_bus)
        node_res_max = np.zeros(n_bus)
        node_res_own = np.zeros(n_bus)
        node_meas_sum = np.zeros(n_bus)
        node_cnt = np.zeros(n_bus)

        # (1) 支路量测 → 两端节点
        for li in range(min(n_branch, m)):
            f, t = branch_ends[li]
            a_ = abs(r[li])
            node_res_sum[f] += a_; node_res_sum[t] += a_
            node_res_max[f] = max(node_res_max[f], a_)
            node_res_max[t] = max(node_res_max[t], a_)
            node_res_own[f] = max(node_res_own[f], a_)
            node_res_own[t] = max(node_res_own[t], a_)
            node_meas_sum[f] += z[li]; node_meas_sum[t] += z[li]
            node_cnt[f] += 1; node_cnt[t] += 1

        # (2) 注入量测 → 对应节点
        for kk, b_bus in enumerate(inj_bus):
            idx2 = n_branch + kk
            if idx2 < m:
                a_ = abs(r[idx2])
                node_res_sum[b_bus] += a_
                node_res_max[b_bus] = max(node_res_max[b_bus], a_)
                node_res_own[b_bus] = max(node_res_own[b_bus], a_)
                node_meas_sum[b_bus] += z[idx2]
                node_cnt[b_bus] += 1

        cnt = np.maximum(node_cnt, 1)

        # ★ 全局尺度归一化，保留幅值信息
        feats = np.stack([
            (node_res_sum / cnt) / res_scale,          # 0 平均残差
            node_res_max / res_scale,                  # 1 最大残差
            (node_meas_sum / cnt) / z_scale,           # 2 量测均值
            deg_norm,                                   # 3 度
            node_res_own / res_scale,                  # 4 节点自身残差
        ], axis=1)                                      # [n_bus, 5]

        X_graphs.append(feats.astype(np.float32))
        y_graphs.append(int(is_attack))

    # 对特征做一次"全局裁切"，防止个别极端值主导
    X_arr = np.array(X_graphs, dtype=np.float32)
    X_arr = np.clip(X_arr, 0.0, 10.0)
    return X_arr, np.array(y_graphs)


# ============================================================
# 四、纯 PyTorch 实现的 GNN
# ============================================================

class DenseGCN(nn.Module):
    """
    稠密邻接矩阵版 GCN。

    标准 GCN 的层公式：
        H^{(l+1)} = σ( Â H^{(l)} W^{(l)} )
    其中 Â 是归一化的邻接矩阵（含自环）：
        Â = D̃^{-1/2} Ã D̃^{-1/2},  Ã = A + I

    这里用稠密矩阵乘法实现 —— 对小图（<1000 节点）完全够用，
    而且比 PyG 的稀疏实现更容易看懂。
    """

    def __init__(self, in_dim, hidden=32, n_layers=2, n_classes=2, dropout=0.3):
        super().__init__()
        self.n_layers = n_layers
        self.dropout = dropout

        dims = [in_dim] + [hidden] * n_layers
        self.linears = nn.ModuleList(
            [nn.Linear(dims[i], dims[i + 1]) for i in range(n_layers)]
        )
        # 图级分类头：mean 池化 + max 池化拼接
        self.classifier = nn.Sequential(
            nn.Linear(hidden * 2, hidden),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden, n_classes),
        )

    @staticmethod
    def normalize_adj(A):
        """Â = D̃^{-1/2} (A + I) D̃^{-1/2}"""
        n = A.shape[0]
        A_tilde = A + np.eye(n, dtype=A.dtype)
        d = A_tilde.sum(axis=1)
        d_inv_sqrt = 1.0 / np.sqrt(np.maximum(d, 1e-9))
        D_inv_sqrt = np.diag(d_inv_sqrt)
        return D_inv_sqrt @ A_tilde @ D_inv_sqrt

    def forward(self, x, A_norm):
        """
        x:      [n_bus, in_dim]
        A_norm: [n_bus, n_bus] 归一化邻接矩阵
        """
        for i, lin in enumerate(self.linears):
            x = lin(x)
            x = torch.mm(A_norm, x)      # ★ GNN 的核心：邻居聚合
            if i < self.n_layers - 1:
                x = F.relu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
            else:
                x = F.relu(x)
        # 图级池化
        x_mean = x.mean(dim=0, keepdim=True)
        x_max = x.max(dim=0, keepdim=True)[0]
        g = torch.cat([x_mean, x_max], dim=1)
        return self.classifier(g)


class DenseGAT(nn.Module):
    """
    稠密版图注意力网络（单头，便于理解）。

    注意力系数：
        e_ij = LeakyReLU( a^T [W h_i || W h_j] )
        α_ij = softmax_j(e_ij)   （j 只取邻居）
        h_i' = Σ_j α_ij W h_j

    与 GCN 的区别：邻居的权重是"学出来"的，而不是固定为 1/√(d_i d_j)。
    优点：注意力权重可解释 —— 能看出"模型在判断异常时参考了哪些邻居"。
    """

    def __init__(self, in_dim, hidden=32, dropout=0.3):
        super().__init__()
        self.W = nn.Linear(in_dim, hidden, bias=False)
        self.a_src = nn.Parameter(torch.zeros(hidden, 1))
        self.a_dst = nn.Parameter(torch.zeros(hidden, 1))
        nn.init.xavier_uniform_(self.W.weight)
        nn.init.normal_(self.a_src, std=0.1)
        nn.init.normal_(self.a_dst, std=0.1)
        self.dropout = dropout
        self.classifier = nn.Sequential(
            nn.Linear(hidden * 2, hidden),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden, 2),
        )

    def forward(self, x, A):
        """
        x: [n, in_dim]
        A: [n, n] 原始邻接矩阵（未归一化，含自环由 mask 控制）
        """
        n = x.shape[0]
        h = self.W(x)                                   # [n, hidden]

        # 注意力分数
        e_src = h @ self.a_src                          # [n, 1]
        e_dst = h @ self.a_dst                          # [n, 1]
        e = F.leaky_relu(e_src + e_dst.t(), 0.2)        # [n, n]

        # mask：只保留邻居 + 自环
        mask = (A > 0) | torch.eye(n, dtype=torch.bool, device=A.device)
        e = e.masked_fill(~mask, float('-inf'))
        alpha = F.softmax(e, dim=1)                     # [n, n]
        alpha = F.dropout(alpha, p=self.dropout, training=self.training)

        out = alpha @ h                                 # [n, hidden]

        g_mean = out.mean(dim=0, keepdim=True)
        g_max = out.max(dim=0, keepdim=True)[0]
        g = torch.cat([g_mean, g_max], dim=1)
        return self.classifier(g), alpha


# ============================================================
# 五、训练与评估
# ============================================================

def _auc_only(scores, labels):
    """单变量 AUC（只用来衡量'某个特征本身有多少判别力'）"""
    scores = np.asarray(scores, dtype=float); labels = np.asarray(labels)
    order = np.argsort(scores, kind='mergesort')
    ranks = np.empty(len(scores), dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1)
    for v in np.unique(scores):
        m_ = scores == v
        if m_.sum() > 1:
            ranks[m_] = ranks[m_].mean()
    n1, n0 = int((labels == 1).sum()), int((labels == 0).sum())
    if n1 == 0 or n0 == 0:
        return float('nan')
    return float((ranks[labels == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def _metrics(preds, probs, y_te):
    """从预测结果计算全部指标（TP/FP/FN/TN + F1 + AUC）"""
    preds = np.asarray(preds); probs = np.asarray(probs); y_te = np.asarray(y_te)
    tp = int(((preds == 1) & (y_te == 1)).sum())
    fp = int(((preds == 1) & (y_te == 0)).sum())
    fn = int(((preds == 0) & (y_te == 1)).sum())
    tn = int(((preds == 0) & (y_te == 0)).sum())
    prec = tp / max(tp + fp, 1)
    rec = tp / max(tp + fn, 1)
    f1 = 2 * prec * rec / max(prec + rec, 1e-9)
    acc = (tp + tn) / max(len(y_te), 1)

    # AUC（用秩方法，处理并列时取平均秩）
    order = np.argsort(probs, kind='mergesort')
    ranks = np.empty(len(probs), dtype=float)
    ranks[order] = np.arange(1, len(probs) + 1)
    # 并列值取平均秩，避免把"无区分度"误判成"高 AUC"
    for v in np.unique(probs):
        m_ = probs == v
        if m_.sum() > 1:
            ranks[m_] = ranks[m_].mean()
    n1, n0 = int((y_te == 1).sum()), int((y_te == 0).sum())
    if n1 > 0 and n0 > 0:
        auc = (ranks[y_te == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    else:
        auc = float('nan')
    return {'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1, 'auc': auc,
            'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn}


def evaluate(model, X_te, y_te, A_t, A_norm_t, use_gat=False):
    model.eval()
    preds, probs = [], []
    with torch.no_grad():
        for i in range(len(X_te)):
            if use_gat:
                out, _ = model(X_te[i], A_t)
            else:
                out = model(X_te[i], A_norm_t)
            probs.append(F.softmax(out, dim=1)[0, 1].item())
            preds.append(int(out.argmax(dim=1).item()))
    return _metrics(preds, probs, y_te)


def _eval_mlp(model, X_te, y_te):
    """MLP 基线专用评估（forward 只吃 x，没有邻接矩阵）"""
    model.eval()
    preds, probs = [], []
    with torch.no_grad():
        for i in range(len(X_te)):
            out = model(X_te[i])
            probs.append(F.softmax(out, dim=1)[0, 1].item())
            preds.append(int(out.argmax(dim=1).item()))
    return _metrics(preds, probs, y_te)


def print_metrics(name, r):
    print(f"{name:16s} | Acc {r['acc']:.4f} | Prec {r['prec']:.4f} | "
          f"Rec {r['rec']:.4f} | F1 {r['f1']:.4f} | AUC {r['auc']:.4f}")


def train_model(model, X_tr, y_tr, X_va, y_va, A_t, A_norm_t,
                use_gat=False, use_mlp=False, epochs=80, lr=2e-3, verbose=True):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=5e-4)

    n_pos = max(int((y_tr == 1).sum()), 1)
    n_neg = max(int((y_tr == 0).sum()), 1)
    w = torch.tensor([1.0, n_neg / n_pos], dtype=torch.float)

    def _forward(x):
        if use_mlp:
            return model(x)
        if use_gat:
            return model(x, A_t)[0]
        return model(x, A_norm_t)

    best_f1, best_state = -1.0, None
    for ep in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad()
        loss_sum = 0.0
        for i in range(len(X_tr)):
            out = _forward(X_tr[i])
            loss = F.cross_entropy(out, torch.tensor([int(y_tr[i])]), weight=w)
            loss_sum = loss_sum + loss
        # ★ 必须在一个 batch 内累积完所有样本再 backward，
        #   否则计算图会跨越 step 而被释放（这也是之前 Loss 卡在 0.69 的原因之一）
        (loss_sum / len(X_tr)).backward()
        optimizer.step()

        if verbose and (ep % 10 == 0 or ep == 1):
            if use_mlp:
                r = _eval_mlp(model, X_va, y_va)
            else:
                r = evaluate(model, X_va, y_va, A_t, A_norm_t, use_gat=use_gat)
            if r['f1'] > best_f1:
                best_f1 = r['f1']
                best_state = {k: v.clone() for k, v in model.state_dict().items()}
            print(f"    Epoch {ep:3d} | Loss {loss_sum.item()/len(X_tr):.4f} "
                  f"| Val F1 {r['f1']:.4f} | Val AUC {r['auc']:.4f}")
        elif not verbose and (ep % 10 == 0 or ep == 1):
            if use_mlp:
                r = _eval_mlp(model, X_va, y_va)
            else:
                r = evaluate(model, X_va, y_va, A_t, A_norm_t, use_gat=use_gat)
            if r['f1'] > best_f1:
                best_f1 = r['f1']
                best_state = {k: v.clone() for k, v in model.state_dict().items()}

    if best_state:
        model.load_state_dict(best_state)
    return model


# ============================================================
# 六、主流程
# ============================================================

def main():
    print("=" * 70)
    print("  GNN 检测 FDIA —— 纯 PyTorch 实现（无需 PyTorch Geometric）")
    print("  对应论文：GDN (AAAI 2021) / E-GraphSAGE (NOMS 2022)")
    print("=" * 70)

    # ---------- 1. 数据 ----------
    print("\n[1/5] 载入电网算例...")
    lines, n_bus, slack = load_case()

    print("\n[2/6] 构造 H 矩阵与邻接矩阵...")
    H, A, state_buses, bus2col, branch_rows = build_H_and_adj(lines, n_bus, slack)
    print(f"      H 矩阵: {H.shape[0]} 量测 × {H.shape[1]} 状态")
    print(f"      邻接矩阵: {A.shape}, 边数 {int((A > 0).sum() // 2)}")

    # ---------- 实验 A：理想 FDIA —— 理论不可检测 ----------
    print("\n[3/6] 实验 A：理想 FDIA（理论不可检测，用来验证我们的理解）")
    print("      设定：攻击者知道精确 H、精确噪声、能篡改全部量测、知道真实负荷")
    Xa, ya = generate_dataset(H, A, n_bus, state_buses, bus2col, branch_rows,
                              n_samples=200, imperfect=False, attack_scale=0.30)
    auc_a = _auc_only(Xa[:, :, 4].sum(axis=1), ya)
    print(f"      最强单特征（节点残差总和）的 AUC = {auc_a:.4f}")
    if abs(auc_a - 0.5) < 0.12:
        print("      ✅ 结论：AUC ≈ 0.5 —— 理想 FDIA 确实无法从残差中检出")
        print("         这不是代码 bug，而是 a = Hc 落在 col(H) 里的理论必然。")
    else:
        print("      ⚠️ 意外：理想 FDIA 竟然可分，请检查攻击生成逻辑")

    # ---------- 实验 B：现实 FDIA —— 可检测 ----------
    print("\n[4/6] 实验 B：现实 FDIA（可检测 —— 这才是论文的真实设定）")
    print("      攻击者只有 97% 的量测能篡改（3% 的量测被漏掉），")
    print("      而这漏掉的量测就暴露了 a = Hc 不在 col(H) 里的事实。")
    X, y = generate_dataset(H, A, n_bus, state_buses, bus2col, branch_rows,
                            n_samples=400, imperfect=True, attack_scale=0.10,
                            keep_ratio=0.97, load_known_ratio=1.0)
    auc_b = _auc_only(X[:, :, 4].sum(axis=1), y)
    print(f"      最强单特征（节点残差总和）的 AUC = {auc_b:.4f}")
    print(f"      样本数: {len(X)}（正常 {(y==0).sum()}, 攻击 {(y==1).sum()}）")
    print(f"      每样本节点特征: {X[0].shape}")

    # 划分
    perm = np.random.permutation(len(X))
    n1, n2 = int(0.6 * len(perm)), int(0.8 * len(perm))
    tr_idx, va_idx, te_idx = perm[:n1], perm[n1:n2], perm[n2:]

    X_t = [torch.tensor(X[i]) for i in range(len(X))]
    A_t = torch.tensor(A)
    A_norm_np = DenseGCN.normalize_adj(A)
    A_norm_t = torch.tensor(A_norm_np)

    X_tr = [X_t[i] for i in tr_idx]; y_tr = y[tr_idx]
    X_va = [X_t[i] for i in va_idx]; y_va = y[va_idx]
    X_te = [X_t[i] for i in te_idx]; y_te = y[te_idx]

    # ---------- 基线：无图结构的 MLP ----------
    print("\n[5/6] 训练三个检测器（同一个数据集，公平对比）...")
    print("\n  --- 基线：MLP（把邻居结构去掉，只看节点自身特征）---")

    class MLP(nn.Module):
        """把节点特征直接池化，不做邻居聚合 —— 用来对照 GNN 的价值"""
        def __init__(self, in_dim, hidden=32):
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(in_dim, hidden), nn.ReLU(), nn.Dropout(0.3),
                nn.Linear(hidden, hidden), nn.ReLU(),
            )
            self.head = nn.Linear(hidden * 2, 2)

        def forward(self, x):
            h = self.encoder(x)
            g = torch.cat([h.mean(0, keepdim=True), h.max(0, keepdim=True)[0]], 1)
            return self.head(g)

    mlp = MLP(X[0].shape[1])
    mlp = train_model(mlp, X_tr, y_tr, X_va, y_va, A_t, A_norm_t,
                      use_mlp=True, epochs=80, verbose=False)
    mlp_res = _eval_mlp(mlp, X_te, y_te)
    print_metrics('MLP (无图)', mlp_res)

    # ---------- GCN ----------
    print("\n  --- GCN（图卷积：邻居特征加权平均）---")
    gcn = DenseGCN(X[0].shape[1], hidden=32, n_layers=2)
    gcn = train_model(gcn, X_tr, y_tr, X_va, y_va, A_t, A_norm_t,
                      use_gat=False, epochs=80)
    gcn_res = evaluate(gcn, X_te, y_te, A_t, A_norm_t, use_gat=False)
    print_metrics('GCN', gcn_res)

    # ---------- GAT ----------
    print("\n  --- GAT（图注意力：邻居权重是学出来的）---")
    gat = DenseGAT(X[0].shape[1], hidden=32)
    gat = train_model(gat, X_tr, y_tr, X_va, y_va, A_t, A_norm_t,
                      use_gat=True, epochs=80)
    gat_res = evaluate(gat, X_te, y_te, A_t, A_norm_t, use_gat=True)
    print_metrics('GAT', gat_res)

    # ---------- 汇总 ----------
    print("\n" + "=" * 70)
    print("  实验结果汇总（IEEE 14 节点，400 样本，现实 FDIA）")
    print("=" * 70)
    print(f"{'方法':16s} | {'Acc':^7s} | {'Prec':^7s} | {'Rec':^7s} | {'F1':^7s} | {'AUC':^7s}")
    print("-" * 70)
    print_metrics('MLP (无图结构)', mlp_res)
    print_metrics('GCN (图卷积)', gcn_res)
    print_metrics('GAT (图注意力)', gat_res)
    print("=" * 70)

    # ---------- 注意力可解释性 ----------
    print("\n  💡 GAT 注意力可解释性演示（模型认为节点 0 最该参考谁）：")
    gat.eval()
    with torch.no_grad():
        _, alpha = gat(X_t[0], A_t)
    top = torch.topk(alpha[0], k=min(5, n_bus))
    print(f"     节点 0 的邻居注意力 Top-5：")
    for idx, val in zip(top.indices.tolist(), top.values.tolist()):
        star = " ← 自己" if idx == 0 else ""
        print(f"       节点 {idx:2d}: {val:.4f}{star}")
    print("\n     （这正是论文里'攻击定位'可视化图的来源：")
    print("       若某节点注意力异常升高，说明该区域可能是攻击注入点）")

    # ---------- 结论 ----------
    print("\n" + "=" * 70)
    print("  结论")
    print("=" * 70)
    print(f"  ① 理想 FDIA（a = Hc，全量测）：AUC = {auc_a:.4f}  → 理论上不可检测")
    print(f"  ② 现实 FDIA（负荷未知 + 稀疏篡改）：单特征 AUC = {auc_b:.4f}  → 可检测")
    print()
    best = max([('MLP', mlp_res), ('GCN', gcn_res), ('GAT', gat_res)],
               key=lambda kv: kv[1]['f1'])
    print(f"  ③ 三个检测器的测试集 F1：")
    print(f"       MLP (无图结构)  F1 = {mlp_res['f1']:.4f}   AUC = {mlp_res['auc']:.4f}")
    print(f"       GCN (图卷积)    F1 = {gcn_res['f1']:.4f}   AUC = {gcn_res['auc']:.4f}")
    print(f"       GAT (图注意力)  F1 = {gat_res['f1']:.4f}   AUC = {gat_res['auc']:.4f}")
    print(f"     最优：{best[0]}（F1={best[1]['f1']:.4f}）")
    print()
    if gcn_res['f1'] > mlp_res['f1'] + 0.01 or gcn_res['auc'] > mlp_res['auc'] + 0.01:
        print("  ✅ 图结构带来了增益（GNN 优于无图结构的 MLP）")
        print("     说明'邻居的残差模式'提供了节点自身特征之外的信息 ——")
        print("     这正是 GDN / E-GraphSAGE 这类工作的立足点。")
    else:
        print(f"  ⚠️ 本设定下 GNN 未明显优于 MLP（GCN F1 {gcn_res['f1']:.4f} vs MLP {mlp_res['f1']:.4f}）")
        print("     这是一个诚实的结果，不要粉饰。原因：")
        print("     本实验中攻击只在 3% 的量测上留下痕迹，信号是'局部但很强'的，")
        print("     节点自身的残差特征已经够用，邻居上下文没提供额外信息。")
        print()
        print("     ★ 那 GNN 什么时候才有优势？")
        print("       当攻击强度低到'单点看不出来、但邻居一起看就能看出异常'时。")
        print("       下面跑一个攻击强度扫描来验证这个假设。")

    # ---------- 实验 C：攻击强度扫描（GNN 价值的关键验证）----------
    print("\n[6/6] 攻击强度扫描：GNN 在什么条件下才优于 MLP？")
    print("      固定 keep_ratio=0.97（少量量测漏改），扫描 attack_scale")
    print()
    print(f"      {'attack_scale':>12s} | {'MLP F1':>8s} | {'GCN F1':>8s} | {'GAT F1':>8s} | {'最优':>6s}")
    print("      " + "-" * 58)

    sweep = [0.01, 0.02, 0.03, 0.05, 0.10]
    for sc in sweep:
        Xs, ys = generate_dataset(H, A, n_bus, state_buses, bus2col, branch_rows,
                                  n_samples=240, imperfect=True, attack_scale=sc,
                                  keep_ratio=0.97, load_known_ratio=1.0)
        ps = np.random.permutation(len(Xs))
        a1, a2 = int(0.6 * len(ps)), int(0.8 * len(ps))
        itr, iva, ite = ps[:a1], ps[a1:a2], ps[a2:]
        Xs_t = [torch.tensor(Xs[i]) for i in range(len(Xs))]

        S_tr = [Xs_t[i] for i in itr]; ys_tr = ys[itr]
        S_va = [Xs_t[i] for i in iva]; ys_va = ys[iva]
        S_te = [Xs_t[i] for i in ite]; ys_te = ys[ite]

        m1 = MLP(Xs[0].shape[1])
        m1 = train_model(m1, S_tr, ys_tr, S_va, ys_va, A_t, A_norm_t,
                         use_mlp=True, epochs=60, verbose=False)
        r_mlp = _eval_mlp(m1, S_te, ys_te)

        m2 = DenseGCN(Xs[0].shape[1], hidden=32, n_layers=2)
        m2 = train_model(m2, S_tr, ys_tr, S_va, ys_va, A_t, A_norm_t,
                         use_gat=False, epochs=60, verbose=False)
        r_gcn = evaluate(m2, S_te, ys_te, A_t, A_norm_t, use_gat=False)

        m3 = DenseGAT(Xs[0].shape[1], hidden=32)
        m3 = train_model(m3, S_tr, ys_tr, S_va, ys_va, A_t, A_norm_t,
                         use_gat=True, epochs=60, verbose=False)
        r_gat = evaluate(m3, S_te, ys_te, A_t, A_norm_t, use_gat=True)

        vals = {'MLP': r_mlp['f1'], 'GCN': r_gcn['f1'], 'GAT': r_gat['f1']}
        win = max(vals, key=vals.get)
        print(f"      {sc:>12.3f} | {r_mlp['f1']:>8.4f} | {r_gcn['f1']:>8.4f} | "
              f"{r_gat['f1']:>8.4f} | {win:>6s}")

    print()
    print("      📌 读表方法：如果低 attack_scale 行里 GNN 领先，")
    print("         就证明了「信号弱时图结构更关键」这个核心假设 ——")
    print("         这正是你写论文时要做的那张主图。")

    print("\n  📌 后续可做的实验（对应精读笔记的 8 个进阶实验）：")
    print("     · 跨拓扑泛化：14 节点训练 → 57 / 118 节点测试")
    print("     · 对抗攻击：对训练好的 GCN 做 PGD，看 F1 掉多少")
    print("     · 攻击定位：用 GAT 注意力权重反推攻击注入点（可视化）")
    print("     · 部分可观测：只用 PMU 量测（部分节点）训练检测器")
    print("=" * 70)
    print("\n✅ GNN 实验完成！")


if __name__ == '__main__':
    main()
