---
document_id: "2609.29572"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2609.29572"
arxiv_id: "2609.29572"
title: "DynaTrust-VVC: Directional Physics-Informed Trust-Based Detection and Mitigation for Cyber-Resilient Multi-Agent Volt-VAR Control"
authors: ["Md Fazley Rafy", "Kamrul Hasan", "Anurag K. Srivastava"]
published: "2026-08-30"
domain: "电网安全与网络攻防"
venue: "2026 Cyber Awareness and Research Symposium (CARS), 已录用；6 页 / 2 图；West Virginia University, Lane Dept. of CSEE；DOE + DARPA 资助"
keywords:
  - "Volt-VAR control"
  - "false data injection"
  - "false data injection attack"
  - "attack detection"
  - "attack mitigation"
  - "physics-informed detection"
  - "sensitivity matrix"
  - "multi-agent system"
  - "distribution system"
  - "cyber resilience"
  - "inverter-based resource"
  - "trust mechanism"
tags:
  - "电网安全"
  - "配电网"
  - "Volt-VAR控制"
  - "FDIA"
  - "物理信息检测"
  - "灵敏度矩阵"
  - "多智能体"
  - "协同攻击"
  - "信任机制"
  - "IEEE123节点"
  - "WVU"
  - "CARS2026"
---

# DynaTrust-VVC: Directional Physics-Informed Trust-Based Detection and Mitigation for Cyber-Resilient Multi-Agent Volt-VAR Control

> **一句话总结**：分布式 Volt–VAR 控制靠"邻居互相印证"来区分"网络攻击"和"物理扰动"，但这个前提是**邻居本身可信**；本文抓住这个前提，用**潮流灵敏度矩阵**给每条邻居报文打一个**方向性物理信任分**（物理不一致 → 信任瞬间崩到谷底；持续一致 → 信任缓慢爬回），再配上**物理自适应告警门限**和**反事实安全电压恢复**，在 IEEE 123 节点非线性馈线上把**三母线协同 FDI 攻击**的检测率从 **0/27 提升到 27/27**，同时良性误报率不显著上升。

---

## 一、研究背景与问题

### 1.1 场景：屋顶光伏把配电网变成"控制问题"

高渗透率屋顶光伏带来两个后果：

- **电压快速波动**——云遮、负荷突变都会让节点电压在分钟级尺度上抖；
- **双向潮流**——传统按"单向辐射状、电压单调下降"设计的馈线不再成立。

标准化的应对手段是**逆变器本地 Volt–VAR 控制（VVC）**（IEEE Std 1547-2018）：逆变器按本地电压偏差做无功下垂，把电压拉回区间。进一步地，**多智能体 VVC** 让多个母线通过通信协调无功出力，比纯本地控制有更好的调压效果。

> ⚡ 关键因果链：**调压性能 ↑ ⟹ 通信依赖 ↑ ⟹ 攻击面 ↑**。一旦控制决策依赖"从别人那里收到的电压量测"，篡改量测就能直接改写控制行为。

### 1.2 攻击者能做什么

论文的威胁模型是**量测完整性破坏**（measurement-integrity corruption）：

$$\tilde v_i(t) = v_i(t) + \delta_i(t)$$

其中 $\delta_i(t)$ 可以是 **偏置（bias）、斜坡（ramp）、重放（replay）、间歇（intermittent）、噪声（noise）** 五种形态。注意两个约束：

- **馈线物理与真实功率注入不被直接改动**——攻击者只改"报出来的电压"；
- 由于 VVC 直接依赖电压量测，被污染的电压会导致**错误的无功调度**，并通过电气耦合母线**传播电压偏差**。

### 1.3 前人方案为什么在这里失效

已有的"边沿防御"思路是**灵敏度加权的邻居印证**：真实的物理扰动（云遮导致的光伏跌落、负荷突变）会让**电气耦合的多个母线产生一致的电压响应**，而孤立的量测篡改不会。于是：

- 本地异常分高 **且** 邻居印证度高 → 判为**物理扰动**；
- 本地异常分高 **但** 邻居印证度低 → 判为**网络攻击**。

这套逻辑有效，但它**隐含假设"邻居是可信的"**。本文的攻击场景正是冲着这个假设去的：

> **协同攻击**：多个电气耦合的邻居**同时被攻陷**，它们互相"印证"彼此的伪造量测，导致协同攻击被误判为合法物理扰动。

同时，论文还指出另外两条前人路线的短板：

| 路线 | 代表 | 短板 |
|---|---|---|
| 集中式潮流校验检测 | [9]–[11] | 引入通信时延、单点故障，馈线规模一大就不可行 |
| 通用 FDI 检测（监测 / 状态估计） | [12] | 与**控制环解耦**，检测到了也不一定知道怎么改控制 |
| 学习型多智能体 VVC | [4]–[6] | 只优化调压，**不显式处理攻击检测/定位/缓解** |
| 语言模型检测 | [14] | 算力需求不适合逆变器级实时部署 |

### 1.4 本文要解决的问题

> 在**每个逆变器控制环内**（算力受限、单分钟级）做一个边沿防御：既能区分"协同篡改"与"真实物理扰动"，又能在判定为攻击后**安全地继续调压**，而不是简单地冻结控制。

---

## 二、系统模型与问题表述

### 2.1 物理侧：径向馈线 + 可控逆变器智能体

考虑一条径向馈线，可控逆变器智能体集合 $\mathcal{A} = \{1,\dots,N\}$。分钟 $t$ 时，智能体 $i$ 收到电压 $\tilde v_i(t)$ 并下达无功指令 $q_i(t)$。

**无功容量约束**（逆变器视在容量 $s_i$、有功 $p_i(t)$）：

$$\bar q_i(t) = \sqrt{\max\left(s_i^2 - p_i^2(t),\; 0\right)} \tag{1}$$

**标称下垂指令**：

$$q_i^0(t) = \mathrm{clip}\left(k_i\left(V_{\mathrm{ref}} - \tilde v_i(t)\right),\; -\bar q_i(t),\; \bar q_i(t)\right) \tag{2}$$

**增量定义**（1 分钟差分，全文反复使用）：

$$\Delta y_i(t) = y_i(t) - y_i(t-1) \tag{3}$$

### 2.2 基线公共层（Eqs. 1–16）

论文把"现有分布式 VVC + 边沿异常检测"这套公共层完整写出，再在其上加三处扩展。公共层的四个环节：

**① 本地证据**——每个智能体构造 4 维特征并过自编码器：

$$x_i(t) = \left[\tilde v_i(t),\ \frac{q_i(t)}{\bar q_i(t)},\ \Delta \tilde v_i(t),\ \frac{\Delta q_i(t)}{\bar q_i(t)}\right] \tag{4}$$

$$a_i(t) = \mathrm{clip}\left(\frac{\lVert x_i(t) - \hat x_i(t)\rVert_2^2}{\theta_i},\ 0,\ 1\right) \tag{5}$$

自编码器结构 **4–8–3–8–4 + ReLU，仅 135 个参数**（为嵌入式部署而刻意做小）；$\theta_i$ 取验证集重建误差的 **99 百分位**。

**② 安全态偏离通道**——把当前电压与"最后一次可信安全电压" $v_i^{\mathrm{safe}}(t)$ 比较：

$$\iota_i(t) = \tilde v_i(t) - v_i^{\mathrm{safe}}(t),\qquad
b_i(t) = \mathrm{clip}\left(\frac{\lVert \iota_i(t)\rVert_2}{\eta_i},\ 0,\ 1\right) \tag{6,7}$$

**③ 持续性门控 + 本地证据输出**：二值持续性变量 $\gamma_i(t)$ **仅在证据候选连续两分钟越过跳闸水平、且偏离符号一致时**置 1：

$$\ell_i(t) = \gamma_i(t)\max\left(a_i(t),\, b_i(t)\right) \tag{8}$$

**④ 邻居印证**——智能体 $i$ 只与邻居集 $\mathcal{N}_i$ 交换 $\{\ell_i, \bar\iota_i, \overline{dq}_i, \Delta p_i, \Delta q_i, \Delta\tilde v_i\}$，计算相容因子：

$$\phi_{ij}(t) = \exp\!\left(-\frac{|\bar\iota_i - \bar\iota_j|}{\eta_i}\right)\exp\!\left(-\frac{|\overline{dq}_i - \overline{dq}_j|}{\eta_i^q}\right)\chi_{ij}(t) \tag{9}$$

$\chi_{ij}$ 是符号相容因子：非零偏离同号（或一方为零）取 1，异号取 **0.35**。固定灵敏度权重满足 $\sum_{j\in\mathcal{N}_i} w_{ji} = 1$，**优先给电气影响大的邻居更高权重**。

**⑤ 印证分与"网络/物理"二分解**：

$$c_i(t) = \sum_{j\in\mathcal{N}_i} w_{ji}\,\ell_j(t)\,\phi_{ij}(t) \tag{10}$$

$$z_i^{\mathrm{cyb}}(t) = \ell_i(t)\big[1 - c_i(t)\big],\qquad
z_i^{\mathrm{phy}}(t) = \ell_i(t)\,c_i(t) \tag{11,12}$$

> 直觉：**本地证据高 + 邻居印证低 ⇒ 局部腐败（网络攻击）；本地证据高 + 邻居印证高 ⇒ 共同物理扰动。**

**⑥ 缓解增益与安全指令**：二值怀疑锁存 $\lambda_i(t)$ 在持续证据越过跳闸水平 $\zeta_i(t)$ 后激活，在印证度超过物理释放水平 $c^\star$ 或锁存时窗耗尽时释放。

$$g_i(t) = \lambda_i(t)\,\mathbb{1}\!\left[c_i(t) < c^\star\right]\mathrm{clip}\!\left(\frac{d_i(t) - \zeta_i(t)}{1 - \zeta_i(t)},\ 0,\ 1\right),\quad d_i(t)=\max\{z_i^{\mathrm{cyb}},\ell_i\} \tag{13}$$

最终指令在标称指令与安全指令之间按增益混合，再按可用无功的 $\rho_i$ 比例限速率并投影：

$$q_i^{\mathrm{tgt}}(t) = \big[1 - g_i(t)\big]q_i^{\mathrm{nom}}(t) + g_i(t)\,q_i^{\mathrm{safe}}(t) \tag{15}$$

$$q_i(t) = \mathrm{clip}\!\left(q_i(t-1) + \mathrm{clip}\!\left(q_i^{\mathrm{tgt}}(t)-q_i(t-1),\ -\rho_i\bar q_i(t),\ \rho_i\bar q_i(t)\right),\ -\bar q_i(t),\ \bar q_i(t)\right) \tag{16}$$

### 2.3 本文的三处扩展（DynaTrust 核心）

#### 扩展 A：方向性物理信任（本文的"发动机"）

**核心机制**：智能体 $i$ 用**一阶灵敏度模型**预测邻居 $j$ 应该报出的电压增量：

$$\Delta \hat v_{j|i}(t) = \sum_{k\in\mathcal{M}_i}\left[S_{jk}^{P}\Delta p_k(t) + S_{jk}^{Q}\Delta q_k(t)\right],\qquad \mathcal{M}_i = \{i\}\cup\mathcal{N}_i \tag{17}$$

其中 $S_{jk}^{P} = \partial v_j/\partial p_k$、$S_{jk}^{Q} = \partial v_j/\partial q_k$ 是**有功/无功电压灵敏度**，由馈线模型**中心差分**得到（OpenDSS 有限差分）。

**归一化物理残差**（$\sigma_{\mathrm{phy}} = 0.020$ p.u.）：

$$\varepsilon_{j\to i}^{\mathrm{phy}}(t) = \frac{\left|\Delta \tilde v_j(t) - \Delta \hat v_{j|i}(t)\right|}{\sigma_{\mathrm{phy}}} \tag{18}$$

**瞬时信任**（高斯核）：

$$\tau_{j\to i}^{\mathrm{inst}}(t) = \exp\!\left(-\frac{\left(\varepsilon_{j\to i}^{\mathrm{phy}}(t)\right)^2}{2}\right) \tag{19}$$

**非对称更新（全文最关键的设计）**：

$$\tau_{j\to i}(t) =
\begin{cases}
\tau_{j\to i}^{\mathrm{inst}}(t), & \text{若 } \tau^{\mathrm{inst}} < \tau_{j\to i}(t-1) \quad \text{（物理不一致 → 立即折扣）}\\[4pt]
\lambda_\tau \tau_{j\to i}(t-1) + (1-\lambda_\tau), & \text{否则（持续一致 → 缓慢恢复）}
\end{cases} \tag{20a,20b}$$

所有信任初值为 1，$0<\lambda_\tau<1$ 控制恢复速率（本文 $\lambda_\tau = 0.998$）。

> ⚡ **为什么必须"快降慢升"**：如果信任也能快速恢复，攻击者只要**间歇性地注入**（一会儿伪造一会儿不伪造）就能把信任反复"刷"回高位；而慢恢复意味着**一次物理不一致就要付出数小时的影响力代价**，攻击者无法靠"打一下、停一下"来维持可信外观。这是典型的**非对称惩罚**设计思想（与入侵检测里的"信任衰减/惩罚积分"同源）。

**信任加权印证分**（分母为零时取 0）：

$$c_i^{\mathrm{DT}}(t) = \frac{\sum_{j\in\mathcal{N}_i} w_{ji}\,\tau_{j\to i}(t)\,\ell_j(t)\,\phi_{ij}(t)}{\sum_{j\in\mathcal{N}_i} w_{ji}\,\tau_{j\to i}(t)} \tag{21}$$

$c_i^{\mathrm{DT}}(t)$ 直接**替换** Eqs. (11)(12)(13) 中的 $c_i(t)$。

#### 扩展 B：物理自适应证据门限

**预期电压偏移幅度**（由灵敏度 × 功率变化估计）：

$$\Omega_i(t) = \left|S_{ii}^{P}\Delta p_i + S_{ii}^{Q}\Delta q_i\right| + \sum_{j\in\mathcal{N}_i}\left[\left|S_{ij}^{P}\Delta p_j\right| + \left|S_{ij}^{Q}\Delta q_j\right|\right] \tag{22}$$

$$\zeta_i(t) = \mathrm{clip}\left(\zeta\left(1 + \kappa_\theta \Omega_i(t)\right),\ \zeta,\ \zeta_{\max}\right),\qquad \kappa_\theta = 5.0,\ \zeta = 0.5 \tag{23}$$

> 直觉：**真实物理大事件（如云遮导致光伏骤降）会带来大电压偏移**。固定门限 $\zeta$ 在这种时候会狂报警。$\Omega_i(t)$ 给出"这次偏移在物理上应该有多大"，门限随之抬高，于是**可解释的电气变化不会被误判**。注意：该扩展**只改证据门限，不改自编码器阈值 $\theta_i$**（Eq. 5 保持不动）。

#### 扩展 C：反事实安全电压恢复（缓解）

锁存激活时，智能体维护一条**"如果没有被污染，电压应该是多少"**的虚拟轨迹——只累加**受信任**的功率变化贡献：

$$v_i^{\mathrm{cf}}(t) = \mathrm{clip}\!\left(v_i^{\mathrm{cf}}(t-1) + S_{ii}^{P}\Delta p_i + S_{ii}^{Q}\Delta q_i + \sum_{j\in\mathcal{N}_i}\tau_{j\to i}(t)\left[S_{ij}^{P}\Delta p_j + S_{ij}^{Q}\Delta q_j\right],\ v_{\min},\ v_{\max}\right) \tag{24}$$

该估计在锁存起始时由 $v_i^{\mathrm{safe}}(t)$ 初始化，锁存释放时重置。安全指令就是把**下垂律作用在反事实电压上**：

$$q_i^{\mathrm{safe}}(t) = q_i^0(t)\Big|_{\tilde v_i(t) = v_i^{\mathrm{cf}}(t)} \tag{25}$$

> ⚡ **这一步比"冻结控制"高明在哪里**：SA 消融版在被怀疑时用 $q_i^{\mathrm{hold}}$（最后一个指令）——**直接停摆**。而反事实恢复是**继续按物理规律调压，只是换用一个"干净"的电压输入**。这样攻击期间系统仍在提供电压支撑，只是不再听被污染的那条路。这是"**降级运行**"而非"**停机**"的思路。

### 2.4 算法流程（Algorithm 1）

```
每步在智能体 i 处：
1. 收 ṽ_i(t)；算 q̄_i(t)，缓存 Δp_i, Δq_i
2. 由 (4) 构造 x_i(t)；(5) 算 a_i(t)；(8) 更新 ℓ_i(t)
3. 向 N_i 广播 {ℓ_i, ῑ_i, Δp_i, Δq_i, Δṽ_i}
4. 对每个 j∈N_i：(17) 预测 → (20) 更新 τ_{j→i}
5. (23) 算 ζ_i(t)；(21) 算 c^DT_i(t)；(13) 算 g_i(t)
6. 若 λ_i(t)=1 且 g_i(t)>0：
7.     (24) 更新 v^cf_i(t) → (25) 得 q^safe_i(t)
8. 否则：
9.     q^safe_i(t) ← q^hold_i(t)
10. 结束
11. (15) 构造 q^tgt_i(t)；(16) 限速率并投影
```

### 2.5 参数与出处（Table I）

论文把每个参数的来源分成三类：**V = 验证集选定 / P = 物理推导 / D = 固定设计常数**。这一点值得单独表扬——它让"哪些参数是调出来的、哪些是物理给的"一目了然。

| 符号 | 含义 | 取值 | 来源 |
|---|---|---|---|
| AE | 自编码器 4−8−3−8−4, ReLU | 135 参数 | D |
| $\theta_i^0$ | AE 重建阈值 | 99 百分位 | V |
| $\eta_i$ | 安全态偏离尺度 | 95 百分位 | V |
| $\lvert\mathcal{N}_i\rvert$ | 邻居数（最强灵敏度） | 3 | D |
| $S^P, S^Q$ | 电压灵敏度 | OpenDSS 有限差分 | **P** |
| $\sigma_{\mathrm{phy}}$ | 物理残差尺度 | 0.020 p.u. | D |
| $\lambda_\tau$ | 信任恢复率 | 0.998 | D |
| $\kappa_\theta$ | 门限增益 | 5.0 | D |
| $\zeta$ | 证据跳闸/告警水平 | 0.5 | D |
| $c^\star$ | 物理释放水平 | 0.35 | D |
| — | 持续性要求 | 2 min | D |
| — | 锁存时窗 | 45 min | D |
| $\rho_i$ | 无功速率限制 | 5%/min | D |
| $\kappa$ | 检测时延衰减常数 | 15 min | D |

---

## 三、方法/技术路线

### 3.1 一张图看懂五级流水线

![[dynatrust_fig1_framework.png|800]]

*Fig. 1｜DynaTrust-VVC 多智能体控制流水线。上层物理层（OpenDSS 非线性馈线 + 协调攻击走廊 101/114/450）、中层网络与通信层（FDI 作用于电压流）、下层代表性智能体 i 的五步决策；右侧对照 Static Corroboration（SA，被判为 physical → missed attack）与 DynaTrust（判为 detected & mitigated）的判定分支。*

框架分三层、五步：

| 步骤 | 名称 | 作用 | 对应公式 |
|---|---|---|---|
| ① | Local evidence | AE 重建误差 + 安全态偏离 | (4)(5)(6)(7)(8) |
| ② | **Physics-trust residual** | 灵敏度预测 vs 实报电压增量 → 方向性信任 | (17)(18)(19)(20) |
| ③ | **Trust-weighted corroboration** | 信任加权邻居印证 | (21) |
| ④ | Cyber-physical decision | $z^{\mathrm{cyb}}, z^{\mathrm{phy}}, \lambda, g$ | (11)(12)(13) |
| ⑤ | **Counterfactual safe VVC** | 反事实电压 → 安全指令 → 限速投影 | (24)(25)(15)(16) |

虚线回路表示闭环更新；紫色框 $\zeta_i(t)$ 是物理自适应门限（扩展 B）。

### 3.2 与基线的差异：三个模块的"叠罗汉"消融

论文的消融设计非常干净——**逐模块叠加**，而不是一次性对比：

| 配置 | 含义 |
|---|---|
| **SA**（Static-trust Ablation） | 关掉三处扩展：$\tau_{j\to i}(t)\equiv 1$、$\zeta_i(t)\equiv\zeta$、$q_i^{\mathrm{safe}}=q_i^{\mathrm{hold}}$ |
| **SA + PT** | SA + 物理信任（Eqs. 17–21） |
| **SA + PT + AT** | 再加自适应门限（Eqs. 22–23） |
| **DT（full）** | 再加反事实恢复（Eqs. 24–25） |

### 3.3 灵敏度失配鲁棒性研究

额外设置一个变体：把**每个智能体侧的** $S_{jk}^P, S_{jk}^Q$ 元素乘以一个从 $\mathcal{U}[0.8, 1.2]$ 抽取的固定因子，而**馈线本体（plant）保持不变**——即模拟"智能体的灵敏度模型与实际馈线有偏差"。这个实验直接对应工程现实：**拓扑重构、DER 投切、运行点漂移都会让灵敏度失准**。

---

## 四、关键创新点

**创新 1：把"邻居可信"这个隐含假设显式化为攻击目标，并给出方向性、非对称的信任状态。**

前人 [8] 的灵敏度加权印证是"静态权重"，本文把它升级为**每链路时变信任 $\tau_{j\to i}(t)$**，且信任的来源不是统计异常而是**物理残差**（Eq. 18）。"方向性"体现在 $\tau_{j\to i} \neq \tau_{i\to j}$——每个智能体对每条入站报文独立打分，因此**协同攻击者无法互相"洗白"**：它们的报文各自都要过接收方的物理检验。

**创新 2：非对称信任动力学（快降慢升）。**

$$\text{降：}\ \tau \leftarrow \tau^{\mathrm{inst}} \quad\text{(瞬时)}\qquad
\text{升：}\ \tau \leftarrow \lambda_\tau \tau + (1-\lambda_\tau),\ \lambda_\tau = 0.998$$

恢复时间常数 $\frac{1}{1-\lambda_\tau} \approx 500$ 分钟（约 8 小时）。这个数字意味着：**一次物理不一致 = 数小时的信任代价**。它同时抵抗"间歇注入刷信任"和"攻击后快速重获影响力"两种自适应策略。

**创新 3：物理自适应证据门限。**

$$\zeta_i(t) = \zeta\left(1 + \kappa_\theta \Omega_i(t)\right)$$

$\Omega_i(t)$（Eq. 22）是**"这次功率变化物理上应该造成多大电压偏移"**的一阶估计。门限随它抬高，于是云遮/负荷突变这类**大而可解释**的电气变化不会触发误报。这是"**用物理量解释异常幅度**"而非"用统计阈值压制异常"的思路。

**创新 4：反事实安全电压恢复。**

$$v_i^{\mathrm{cf}}(t) \leftarrow v_i^{\mathrm{cf}}(t-1) + \underbrace{S_{ii}\Delta p_i + S_{ii}\Delta q_i}_{\text{本地（可信）}} + \sum_j \tau_{j\to i}\underbrace{\left[S_{ij}\Delta p_j + S_{ij}\Delta q_j\right]}_{\text{邻居（按信任加权）}}$$

安全指令 = 下垂律作用于 $v_i^{\mathrm{cf}}$。这是**"物理降级运行"**：攻击期间系统继续调压，只是把被污染的输入替换为物理推演的替代品。

---

## 五、实验与结果

### 5.1 实验设置

| 项目 | 设置 |
|---|---|
| 馈线 | **非线性 IEEE 123 节点**，OpenDSS 求解，**1 分钟分辨率** |
| 数据 | Pecan Street Dataport 的分钟级居民负荷 / 光伏曲线；负荷重构为 grid + solar |
| 天数划分 | 281 个完整公共日 → **训练 168 / 验证 56 / 测试 57** 天（按时间顺序切分） |
| 智能体 | $N=10$ 个同质智能体，**有向三邻居链路**（对应已演示的分布式嵌入式控制器 [19]） |
| 攻击窗口 | 第 **360 → 600** 分钟（共 240 分钟） |
| 统计协议 | **27 个匹配重复实验** = 9 个随机种子 × 3 个留出测试日；报告 mean ± std；主对比用 **20,000 次重采样的配对 bootstrap 95% CI** |

### 5.2 攻击与良性场景（Table II）

| 类别 | 场景 | 说明 |
|---|---|---|
| Cyber | **Bias / Ramp / Replay @ 母线 114** | 单母线三种攻击形态 |
| Cyber | **Corridor bias: −0.035 p.u. @ 101, 114, 450** | **协同三母线攻击**（本文的核心靶子） |
| Benign | Coupled PV drop | 耦合光伏跌落（真实物理事件，用于测误报） |

### 5.3 评价指标

**检测分**（时延越小越高）：

$$D = \begin{cases}\exp\left(-\ell_{\det}/\kappa\right), & \text{若报警}\\ 0, & \text{否则}\end{cases},\qquad \kappa = 15\ \text{min} \tag{26}$$

**定位分**（召回与特异度的均衡平均）：

$$L = \tfrac{1}{2}\left(\mathrm{rec} + \mathrm{spec}\right) \tag{27}$$

**缓解分**（相对"无保护"运行的加权电压–无功跟踪代价 $J$）：

$$M = \mathrm{clip}\left(1 - \frac{J_{\mathrm{defended}}}{J_{\mathrm{unprotected}}},\ 0,\ 1\right) \tag{28}$$

同时报告**无截断版** $M_{\mathrm{raw}} = 1 - J_{\mathrm{def}}/J_{\mathrm{unprot}}$——论文明确说明这是为了**暴露被 clip 掩盖的劣化**（👍 诚实做法）。

**可用性** $A$：攻击窗口内电压落在 $[0.95, 1.05]$ p.u. 的母线占比均值。
**良性误报率** FAR：良性事件窗口内满足 $z^{\mathrm{cyb}} \ge \zeta$ 的"节点-分钟"比例。
**综合韧性指数**（加权几何平均）：

$$\mathrm{CRVI} = \exp\left(\sum_r w_r \ln\left(\max(m_r, \epsilon)\right)\right),\quad m_r \in \{D, L, M, A\},\ w_r = \{0.35, 0.20, 0.30, 0.15\} \tag{29}$$

### 5.4 主结果：SA vs DT（Table III，27 匹配重复）

| 场景 | $D$ (SA → DT) | $M_{\mathrm{raw}}$ (SA → DT) | CRVI (SA → DT) |
|---|---|---|---|
| Bias @ 114 | 0.936 → 0.936 | +0.18 → **+0.26** | 0.566 → 0.621 |
| Ramp @ 114 | 0.001 → 0.000 | −0.05 → −0.03 | 0.017 → 0.013 |
| Replay @ 114 | 0.000 → 0.000 | −0.10 → −0.24 | 0.002 → 0.002 |
| **Corridor（协同）** | **0.000 → 0.936** | +0.02 → +0.03 | **0.007 → 0.290** |
| Benign PV-drop FAR | SA 0.115 ± 0.144 → DT 0.107 ± 0.099 | | |

> **这是全文的核心结果**：协同走廊攻击下，SA **27/27 全部漏报**（因为互相攻陷的邻居保留了完整印证权重），DT **27/27 全部在起始后 1 分钟检出**，场景 CRVI 从 0.007 跃升到 0.290。良性 FAR 变化 **−0.008**，配对 95% CI **[−0.048, 0.026]**（即**不显著上升**）。

### 5.5 模块消融（Table IV，四个基准攻击上的汇总）

| 方法 | $D$ | $L$ | $M$ | $A$ | CRVI | FAR |
|---|---|---|---|---|---|---|
| No defense | 0.000 | 0.500 | 0.000 | 0.996 | 0.000 | 0.000 |
| SA | 0.234 | 0.553 | 0.058 | 0.994 | 0.227 | 0.115 |
| **SA + PT** | **0.468** | 0.557 | 0.077 | 0.994 | **0.315** | 0.111 |
| SA + PT + AT | 0.468 | 0.558 | 0.076 | 0.994 | 0.315 | 0.120 |
| DT (full) | 0.468 | **0.561** | 0.076 | 0.994 | 0.315 | **0.107** |

**结论清晰**：

1. **物理信任（PT）是协同攻击检测的主要来源**——汇总 $D$ 从 0.234 跳到 0.468，而 CRVI 从 0.227 直接到 0.315。**AT 和 CR 都不再提升 CRVI**。
2. **AT 的作用是"保住这个增益"**——在有可解释电气变化的场景中防止误报（FAR 0.111 → 0.120，但 DT 最终 0.107）。
3. **CR（反事实恢复）主要体现在协同走廊场景的缓解上**——$M_{\mathrm{raw}}$ 从 PT+AT 的 **+0.003** 升到 full DT 的 **+0.028**。
4. 综合 CRVI 从 0.227 → 0.315，**配对每重复变化 +0.101，bootstrap 95% CI [0.079, 0.127]，27/27 全部为正**；且在**等权 / 偏检测 / 偏缓解**三组权重下优势保持为正。

### 5.6 协同攻击的逐时步行为（Fig. 2）

![[dynatrust_fig2_corridor.png|800]]

*Fig. 2｜母线 101 的协同走廊攻击响应（seed-0、中间测试日的重复）。(a) 被污染量测 $\tilde v_{101}$ 与真实电压（SA / DynaTrust）；(b) 物理信任 $\min_j \tau_{j\to101}$ 与印证度 $c_{101}$；(c) 诊断分 $z^{\mathrm{cyb}}_{101}$ 与缓解增益 $g_{101}$。*

图中可读出三个关键现象：

- **(a) 量测被拉低约 0.035 p.u.**（从 ~0.998 掉到 ~0.965），但**真实电压**在 SA 下也跟着掉（蓝线），在 DynaTrust 下保持在 1.00 附近（绿虚线）——说明**缓解确实起作用**。
- **(b) 信任瞬间崩落**：$\min_j \tau_{j\to101}$ 从 ~0.96 一步跌到 ~0.2（第 360 分钟），随后按 $\lambda_\tau = 0.998$ 缓慢回升，到第 470 分钟仍只有 **~0.37**（110 分钟才恢复这么点）。同时 SA 的印证度 $c_{101}$ 冲到 ~0.5（高于物理释放水平 $c^\star=0.35$）→ **被判为物理扰动、锁存释放、漏报**；DT 的 $c^{\mathrm{DT}}_{101}$ 被压到 ~0.02。
- **(c) 诊断分越门限、缓解增益同步抬升**：DT 的 $z^{\mathrm{cyb}}_{101}$ 与 $g_{101}$ 在第 361 分钟越过 $\zeta = 0.5$，**起始后 1 分钟**完成检测 + 缓解；SA 的诊断分只到 ~0.48（未越门限）。

> 攻击者手法：三个被攻陷母线**报出同样的 −0.035 p.u. 阶跃，却没有对应的 P–Q 变化**。物理残差 $\varepsilon^{\mathrm{phy}}$ 立刻放大 → 信任崩塌 → 无法互相印证。

### 5.7 灵敏度失配鲁棒性

对**每个智能体侧**的 $S^P_{jk}, S^Q_{jk}$ 元素施加 $\mathcal{U}[0.8,1.2]$ 的固定扰动（plant 不变）：

| 指标 | 无扰动 | ±20% 失配 |
|---|---|---|
| 协同攻击检测分 $D$ | 0.936 | **0.936**（不变） |
| 原始缓解 $M_{\mathrm{raw}}$ | +0.028 | **+0.028**（不变） |
| 良性 FAR | 0.107 | 0.125（略升） |

即：**±20% 的灵敏度偏差不影响协同检测能力，代价只是良性误报略升**。

### 5.8 作者自陈的失败面（👍）

论文**没有藏负结果**，明确指出：

> **斜坡（ramp）和重放（replay）对 SA 和 DT 都很难。** 在 240 分钟攻击窗口内，它们的"增量式或重放式"特征与**标称负荷–光伏变化**区分度不足。

| 场景 | $D$ | $M_{\mathrm{raw}}$ | 评价 |
|---|---|---|---|
| Ramp @ 114 | ~0 | 负值 | **基本失效** |
| Replay @ 114 | 0.000 | −0.24（DT 甚至更差） | **基本失效** |

作者给出的方向：**序列感知检测（sequence-aware detection）** + **改进负荷灵敏度估计**。

---

## 六、对电网安全领域的意义

### 6.1 它填的是哪一类"逻辑缺口"

本文的价值不在于"又做了一个更好的检测器"，而在于它**攻击了前人防御方案的隐含前提**：

| 前人方案的隐含前提 | 本文的攻击 | 本文的修复 |
|---|---|---|
| 邻居是可信任的 | 多邻居同时被攻陷，互相印证 | **方向性、非对称信任**——每个接收方独立对每条入站报文做物理检验 |
| 检测可以独立于控制环 | —— | 把检测/定位/缓解**全部塞进 VVC 控制环**（Eqs. 13–16、24–25） |
| 异常幅度用固定阈值判 | —— | **物理自适应门限**（Eq. 23），用 $\Omega_i(t)$ 解释"这次偏移该有多大" |

这套"**攻击防御的假设 → 修补假设**"的研究范式，对我们做选题非常有参考价值。

### 6.2 与"物理护城河"的直接呼应

> ⚡ 这篇论文是**"物理约束即防御资源"的教科书式示范**。

- **灵敏度矩阵 $S^P, S^Q$（潮流方程的线性化）** 是全文的**唯一信任来源**——不是统计、不是学习，而是 $\partial v/\partial p$、$\partial v/\partial q$；
- **反事实电压推演（Eq. 24）** 本质上就是**在攻击下继续求解线性化潮流**，用一个"干净"的电压替代被污染的输入；
- 自适应门限 $\Omega_i(t)$（Eq. 22）也是**灵敏度 × 功率变化**的一阶预测。

也就是说：**整篇论文的防御能力，全部来自"我知道电压和功率之间必须满足什么关系"这一条物理先验。** 这正是"物理 + 信息"双重视角能做的事，也是纯 ML 研究者拿不出来的东西。

### 6.3 与实验室方向的接口

| 实验室方向 | 本文可迁移的点 |
|---|---|
| **工业AI与智能体** | 多智能体 VVC 本身就是一个**分布式智能体协同**问题；"信任机制 + 共识"的框架可直接迁移到其他工业多智能体系统（如分布式能源调度、微电网二次控制） |
| **AI与数据安全** | 攻击目标是**训练/部署在边沿的 135 参数自编码器**；可以研究**针对这个小模型的数据投毒 / 规避攻击**——本文完全没做 |
| **入侵检测** | "快降慢升"的非对称信任与非对称惩罚是入侵检测的经典思想，本文把它**物理化**（残差驱动而非统计驱动），是很好的交叉点 |
| **假消息检测** | 协同攻击 = "多个信源互相印证同一假消息"，与**协同虚假信息**的结构同构；信任传播 + 一致性校验的方法可借鉴 |

### 6.4 对我们的 FDIA + GNN 方向的具体启发

1. **图结构天然在这里**：$\mathcal{N}_i$ 是"电气耦合邻居"，$S^P/S^Q$ 是带符号的加权邻接矩阵。本文用的是**固定权重 $w_{ji}$ + 线性灵敏度**，完全可以换成 **GNN 学习图上的信任传播**——而物理约束（灵敏度矩阵）作为**结构先验**注入。这是一个自然、且论文数量还很少的交叉点。
2. **监督信号稀缺时的物理先验**：本文几乎不需要标注攻击数据（$\sigma_{\mathrm{phy}}$、$\theta_i$、$\eta_i$ 都来自验证集分位数，$\zeta$、$c^\star$ 是设计常数）。这对"攻击样本稀缺"的现实场景极有价值，也是 GNN 方法可以学习的"弱监督 + 物理先验"范式。
3. **"检测 → 定位 → 缓解"闭环**：本文把三者放在同一个控制环里。若把**定位**换成图上的节点分类任务（哪些母线被攻陷），正好是 GNN 的强项——而本文的定位指标 $L$ 表现很弱（见下文批判），**说明这里有真空白**。

---

## 七、局限与展望

### 7.1 作者自陈的局限

1. **只在 IEEE 123 节点单馈线上评估**；
2. **多个控制器设计常数在测试集评估前固定**（按 Table I 的验证流程选定）——存在过拟合验证集的风险；
3. **实际部署需要灵敏度估计在拓扑与运行条件变化时依然可靠**；
4. 未来工作：参数敏感性分析、**在线灵敏度估计**、更多馈线模型、实时控制平台。

### 7.2 我的批判（供选题参考）

#### ⚠️ 批判 1（最重要）：威胁模型与防御的信息假设不自洽

威胁模型明确说**只篡改电压量测**（$\tilde v_i = v_i + \delta_i$），"真实功率注入不被改动"。但防御式（17）预测 $\Delta\hat v_{j|i}$ 时，用的是**邻居上报的** $\Delta p_j, \Delta q_j$——这些是**传输量**。

> **问题**：如果攻击者能改 3 个母线的电压量测，为什么不能同时改这 3 个母线上报的 $\Delta p, \Delta q$？只要让伪造的功率变化**与伪造的电压阶跃自洽**（即 $\Delta\tilde v_j \approx \sum_k S^P_{jk}\Delta p_k + S^Q_{jk}\Delta q_k$），物理残差 $\varepsilon^{\mathrm{phy}} \to 0$，**信任不降、攻击重新隐身**。

这是一个**自适应攻击者**的缺口。论文只在引言里讨论了"学习型/语言模型检测"，但**没有分析"已知灵敏度矩阵与信任机制的攻击者"**。

> ⚡ 好消息是：这个缺口**两面都能发论文**。
> - **攻击面**：构造"物理自洽的协同 FDI"——求解 $\min \|\Delta \tilde v - S\Delta u\|$ 约束下的最优伪造功率序列，证明 DynaTrust 在自适应攻击下失效。
> - **防御面**：把 $\Delta p_j, \Delta q_j$ 也纳入信任检验（例如用本地可测的**潮流入侵**做交叉校验，或用 KCL/KVL 约束检验邻居上报的功率是否与本地量测一致）。

#### ⚠️ 批判 2：$D$ 指标实际上几乎是二值的，信息量被高估

$D = \exp(-\ell_{\det}/15)$。所有检测都发生在 $\ell_{\det} = 1$ 分钟，因此

$$D = e^{-1/15} = 0.9355 \approx 0.936$$

——**与 Table III 中所有成功检测的 $D$ 值完全吻合**。也就是说，$D$ 只是"时延"的单调变换，报告两者其实是**冗余**的；而 $D \in \{0, 0.936\}$ 在实测中只取两个值，**不是连续的评价量**。真正该被强调的对比是 **27/27 检出 vs 0/27 检出**，而不是 $0.234 \to 0.468$ 这种"看起来像连续提升"的数字。

#### ⚠️ 批判 3：定位指标 $L$ 几乎是随机水平，与"定位"主张不符

- **No defense 的 $L = 0.500$**——即"从不报警"的检测器在 $L = \frac{1}{2}(\mathrm{rec}+\mathrm{spec})$ 下取到的**平凡值**；
- SA 为 0.553，DT 为 0.561。

DT 相对平凡值只高出 **0.061**。而论文引言明确把"**localization**"列为现有学习型 VVC 方法缺失的能力之一，摘要也以"检测"为主张。**但报告的 $L$ 值几乎不支撑"能定位到哪些母线"这一说法。** 这里需要向作者求证 $L$ 的计算口径（是否只在报警窗口/报警智能体上统计）。无论如何，**定位是本文最弱的一环**——也是后续工作最容易改进的地方。

#### ⚠️ 批判 4：斜坡/重放失效的根因可能就在 $\sigma_{\mathrm{phy}}$ 的标定方式上

论文把 ramp/replay 的失败归因于"信号特征与标称负荷–光伏变化区分度不足"。但从机制上看更可能是：

- 残差（Eq. 18）是在**1 分钟增量**上算的。斜坡攻击每分钟只改一点点电压 → **单步增量很小 → $\varepsilon^{\mathrm{phy}}$ 小 → 信任几乎不降**；
- 而 $\sigma_{\mathrm{phy}} = 0.020$ p.u. 是在**高光伏波动**的验证日上标定的，本来就偏松。

**建议**：改用**滑动窗口累积残差**（CUSUM / 广义似然比），或对残差做时间积分 $\sum_{s=t-W}^{t}\varepsilon^{\mathrm{phy}}(s)$。这几乎是"一个公式的改动"，但很可能把 ramp 从 $D\approx 0$ 拉到可用水平。**这是一个低成本、高成功率的改进点。**

#### ⚠️ 批判 5：基线偏弱，缺少外部 SOTA 对照

Table IV 的对照只有 `No defense` 与自己的 SA。**没有与 [10] Isozaki et al.、[11] Sarker/Rafy/Srivastava（同组前作）、[14] LLM 检测器**做比较。因此论文能证明的只是"DT 优于自己的消融版"，**不能证明"DT 优于现有技术"**。

#### ⚠️ 批判 6：鲁棒性研究的设计偏"温和"

$\mathcal{U}[0.8,1.2]$ 的**逐元素独立乘性扰动**是一种相当温和的失配：

- 真实失配是**结构性**的（拓扑重构 → 灵敏度矩阵的**零元素变非零**、符号翻转、近奇异）；
- 配电网灵敏度矩阵在**高 R/X 比、长馈线**场景下可能接近奇异，逐元素 ±20% 扰动**测不出这种退化**。

**建议**：直接做**拓扑变更实验**（开关重构、DER 投切）——这比 ±20% 的 i.i.d. 扰动有说服力得多。

#### ⚠️ 批判 7：可用性 $A$ 饱和，CRVI 的判别力集中在 $D$ 和 $M$

所有配置的 $A$ 都在 **0.994–0.996**，说明"电压落在 [0.95,1.05] 的比例"这个指标**几乎不区分方法**。作者做了 CRVI 权重敏感性检验（等权/偏检测/偏缓解）来缓解这个问题，值得肯定；但从指标设计上，$A$ 更该换成**电压越限的严重度**（如最大越限幅度、越限持续时间）而不是**越限母线占比**。

#### ⚠️ 批判 8：检测时延"1 分钟"与 2 分钟持续性判据的表述张力

$\gamma_i(t)$ 要求证据候选**连续两分钟**越过跳闸水平才置 1；而攻击从第 360 分钟开始，报警在第 361 分钟——$\ell_{\det} = 1$ 分钟。这在定义上是自洽的（若把第 360 分钟算作攻击的第 0 分钟），但**表述上容易被审稿人追问**：如果从"攻击第一个被污染的采样时刻"起算，时延应当是 0 而非 1。论文最好明确 $\ell_{\det}$ 的起算点定义。

#### 批判 9：可复现性

论文未提及代码开源。好在 **OpenDSS（开源）+ Pecan Street Dataport（公开）** 都是可获得资源，复现门槛不算高。若能放出脚本会显著提升影响力。

### 7.3 我给出的改进优先级（如果我来做后续工作）

| 优先级 | 改进 | 预期收益 | 成本 |
|---|---|---|---|
| ★★★ | 累积/窗口化物理残差（对 ramp 有效） | 补上最大的功能空白 | 低（改一个公式） |
| ★★★ | 自适应攻击者分析（伪造自洽的 P/Q） | 明确防御边界；攻防两侧都能出论文 | 中 |
| ★★☆ | 拓扑变更下的灵敏度鲁棒性 | 大幅提升说服力 | 中 |
| ★★☆ | 与外部 SOTA 对比 | 补上"优于现有技术"的证据 | 中 |
| ★★☆ | 把定位换成图节点分类（GNN + 灵敏度先验） | 直击最弱指标 $L$；与我们的方向对接 | 高 |
| ★☆☆ | 反事实恢复中加入电压上下限与保护协同 | 提升工程可信度 | 低 |

---

## 八、评分

| 维度 | 分数 | 理由 |
|---|---|---|
| 问题重要性 | **8.5** / 10 | 配电网级 DER 控制安全是真实且尚未拥挤的战场；"协同攻击打破邻居印证假设"是真缺口 |
| 方法创新性 | **7.5** / 10 | 物理信任的**思想**并非全新（[8] 已有灵敏度加权印证），但**方向性 + 非对称动力学 + 自适应门限 + 反事实恢复**的组合是新的，且每一步都有物理动机 |
| 理论深度 | **6.5** / 10 | 无形式化保证（无 stealth 判据、无检测可达性分析）；本质是启发式 + 物理先验 |
| 实验严谨性 | **8.5** / 10 | 27 匹配重复 + 20,000 次 bootstrap + 逐模块消融 + 权重敏感性 + 失配研究 + **主动报告负结果**；远超 6 页会议论文的平均水准 |
| 实验充分性 | **6.0** / 10 | 仅单馈线；无外部 SOTA 对照；定位指标近乎平凡；ramp/replay 失效；拓扑变更未测 |
| 写作与可复现 | **8.0** / 10 | 公式完整、参数表标注来源（V/P/D）、图 1 表达清晰；但未开源代码 |
| 领域影响潜力 | **7.0** / 10 | 思路可直接迁移到微电网二次控制、DER 协调、工业多智能体系统；短会议论文，深度受限 |
| **综合** | **7.5 / 10** | **"抓住了正确的假设、用了正确的工具（物理）、做了正确的消融"，但实验边界偏窄、自适应攻击者未分析，因此停在"好论文"而非"突破性论文"** |

> ⚡ **一句话判词**：这是一篇**方法论对路、实验态度诚实、但边界未探到底**的工作。它最大的价值不是结果数字，而是**示范了"用潮流灵敏度把'邻居可信'从假设变成可检验量"这条路径**——这条路径对我们做 GNN + 物理约束的方向几乎是开着的门。

---

## 九、延伸阅读

### 9.1 直接前作与理论基础

| 文献 | 内容 | 为什么读 |
|---|---|---|
| **[8]** S. Majumder, A. Vosughi, H. M. Mustafa, T. E. Warner, A. K. Srivastava, *On the cyber-physical needs of DER-based voltage control/optimization algorithms in active distribution network*, **IEEE Access**, vol. 11, pp. 64397–64429, 2023 | 本文"灵敏度加权邻居印证"的原始出处 | **必读**——理解本文的出发点和被攻击的前提 |
| **[11]** P. S. Sarker, M. F. Rafy, A. K. Srivastava, *Enabling cyber-resilient distribution systems with DERs: Distributed vs. centralized control*, **IEEE Trans. Power Delivery**, 2025 | 同组前作，分布式 vs 集中式控制的安全对比 | 理解"为什么必须做边沿（分布式）防御" |
| **[10]** Y. Isozaki et al., *Detection of cyber attacks against voltage control in distribution power grids with PVs*, **IEEE Trans. Smart Grid**, 7(4), 2015 | 集中式潮流校验检测的代表 | 本文 baseline 的对照组（但论文未做实验对比） |
| **[7]** G. Liang et al., *A review of false data injection attacks against modern power systems*, **IEEE Trans. Smart Grid**, 8(4), 2016 | FDIA 综述（经典） | 威胁模型分类（bias/ramp/replay/…）的来源 |
| **[12]** A. S. Musleh, G. Chen, Z. Y. Dong, *A survey on the detection algorithms for false data injection attacks in smart grids*, **IEEE Trans. Smart Grid**, 11(3), 2019 | FDIA 检测算法综述 | 理解"检测与控制环解耦"这一批评的语境 |
| **[14]** A. Selim, J. Zhao, B. Yang, *Large language model for smart inverter cyber-attack detection via textual analysis of Volt/VAR commands*, **IEEE Trans. Smart Grid**, 15(6), 2024 | LLM 检测逆变器攻击 | 与本文形成"轻量物理 vs 重型语言模型"的对照 |

### 9.2 Vault 内已解读的相关论文（建议成对阅读）

| Vault 笔记 | arXiv | 与本文的关系 |
|---|---|---|
| [[Exposing the Invisible: Detecting Stealthy Parameter-Based Cyber-Attacks on Inverter Synchronization Loops]] | 2608.30574 | **同为"逆变器控制层攻击 + 物理不变量检测"路线**。它攻的是 PLL 增益（平衡点不变 ⇒ 不可检测），本文防的是电压量测（灵敏度不一致 ⇒ 可检测）。**对照读可看清"哪类控制层攻击在物理上不可检测"** |
| [[Adversarially-Informed Node Criticality Identification in Power Grid Measurements]] | 2608.27393 | 同样用**灵敏度/物理结构**做安全分析（节点关键性），与本文的 $w_{ji}$ 灵敏度权重同源 |
| [[From Cycle Space to Cycle Manifold: Limits and Achievability of Blind False Data Injection Attacks]] | 2609.10631 | 隐蔽攻击空间的**理论边界**（回路空间/零空间）。本文的自适应攻击缺口（批判 1）本质上是"如何让 $\varepsilon^{\mathrm{phy}}=0$"——正是这套理论的用武之地 |
| [[Cybersecurity in Power Grids: Standards and Research Challenges]] | 2609.16928 | 标准与全景（IEC 62351/62443）；本文对应其中"MTD/检测"研究方向 |

### 9.3 值得跟进的同期相关工作

| arXiv | 日期 | 标题 | 关联点 |
|---|---|---|---|
| **2609.12305** | 2026-09-11 | Self-Verifying Anomaly Detection using Explainable AI for Cybersecurity of DER Networks（Iowa State, Govindarasu 组） | **同为 DER 网络异常检测**，但走 **LightGBM + SHAP 可解释性**路线。与本文"纯物理、零标注"形成**两条对立技术路线**，最适合做"物理 vs 可解释 ML"的对照选题 |
| **2609.21148** | 2026-09-17 | Distribution-Free Budgeted Stealthy Attack Scheduling for Remote State Estimation | **预算约束下的隐蔽 FDI 调度**，用 split-conformal 校准触发器。直接对应本文批判 1 的"自适应攻击者"——**如果要写攻击侧论文，这是必读** |
| **2608.13823** | 2026-08-13 | Hierarchical Sensor-Spoofing Defence Framework for Networked DC Microgrids via Cyber-Physical Coordination | 直流微电网**传感器欺骗**的分层防御（网络侧 + 物理侧协调），与本文"物理 + 信息"双域防御同构 |
| **2606.08062** | 2026-06-06 | Multidimensional Resilience for Electrical Power Systems: Systematic Review, Integrated Index, and Validation under Real-World Cyber-Physical Attack Scenarios（Zografopoulos 组） | **多维韧性指数**的系统综述——本文的 CRVI 正属于这一范式；想看"韧性指标该怎么设计"读这篇 |
| **2606.15047** | 2026-06-13 | BT-MTD: Bus Traversal-based Moving Target Defense for Smart Grid | **MTD 主动防御**（改支路导纳、识别无效支路）。与本文的"检测 + 缓解"被动路线互补——"检测 + MTD"的组合是明显空白 |
| **2609.24583** | 2026-09-21 | Optimal Allocation of Grid-Forming Frequency Shaping Control | 构网型**频率塑形控制的最优配置**；与本文的逆变器侧控制安全同属"IBR 控制层"话题，但不涉安全——可作为"控制侧最新进展"背景读 |

### 9.4 建议的动手复现路径

1. **搭环境**：OpenDSS + IEEE 123 节点馈线（`OpenDSSDirect.py` 可 pip 安装），用中心差分算 $S^P, S^Q$；
2. **复现公共层**：先只做 SA（静态信任）——目标是**复现"协同走廊攻击 27/27 漏报"**这一现象。这是验证理解是否到位的试金石；
3. **加 PT**：实现 Eqs. (17)–(21)，观察信任曲线是否与 Fig. 2(b) 形态一致（瞬时崩落 → $\lambda_\tau$ 慢恢复）；
4. **加 AT + CR**：实现 Eqs. (22)–(25)；
5. **做我提的改进**：把 Eq. (18) 换成**窗口累积残差**，看 ramp 场景的 $D$ 能否从 ~0 提升到可用水平。**如果有效，这就是一篇可投稿的改进工作。**

---

## 十、元信息

| 项 | 内容 |
|---|---|
| arXiv ID | [2609.29572](https://arxiv.org/abs/2609.29572)（v1，2026-08-30 提交） |
| DOI | 10.48550/arXiv.2609.29572 |
| 分类 | eess.SY（主）、cs.MA |
| 篇幅 | 6 页 / 2 图 / 4 表 |
| 发表 | **已录用：2026 Cyber Awareness and Research Symposium (CARS)** |
| 单位 | West Virginia University, Lane Department of Computer Science and Electrical Engineering, Morgantown, WV, USA |
| 作者 | Md Fazley Rafy（Graduate Student Member, IEEE）、Kamrul Hasan（Graduate Student Member, IEEE）、**Anurag K. Srivastava（Fellow, IEEE）** |
| 资助 | U.S. DOE + DARPA（部分支持）；致谢 Niloy Patari 博士技术支持 |
| 全文规模 | 28,460 字符（PyMuPDF 提取） |
| 图片提取 | 2 张嵌入位图（Fig. 1 framework / Fig. 2 corridor），已逐张目视校验 ✅ |
| 解读日期 | 2026-09-28 |
