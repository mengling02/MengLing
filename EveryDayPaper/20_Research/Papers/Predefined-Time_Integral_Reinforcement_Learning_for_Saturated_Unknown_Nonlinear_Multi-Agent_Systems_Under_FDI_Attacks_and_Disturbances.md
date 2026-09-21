---
document_id: arxiv-2609.14075
source_type: arxiv
source_url: https://arxiv.org/abs/2609.14075
arxiv_id: "2609.14075"
title: "Predefined-Time Integral Reinforcement Learning for Saturated Unknown Nonlinear Multi-Agent Systems Under FDI Attacks and Disturbances"
authors: "Tien Dat Vu, Minh Doan"
published: 2026-09-12
domain: 电网安全与网络攻防
venue: arXiv (eess.SY) — 预印本
keywords: [false data injection, FDI attack, resilient control, reinforcement learning, predefined-time convergence, multi-agent systems, zero-sum game, HJI]
tags: ["paper-note", "grid-security", "FDI", "reinforcement-learning"]
---

# Predefined-Time Integral Reinforcement Learning for Saturated Unknown Nonlinear Multi-Agent Systems Under FDI Attacks and Disturbances

> **arXiv**: [2609.14075](https://arxiv.org/abs/2609.14075) ｜ **提交日期**: 2026-09-12 ｜ **分类**: eess.SY ｜ **作者**: Tien Dat Vu, Minh Doan（胡志明市理工大学 / 越南国家大学胡志明市）

---

## 一、研究背景与问题

随着分布式发电、微电网与网联化控制架构的大规模部署，**电力系统越来越多地表现为"网络化多智能体系统"**：多台逆变器、储能单元、分布式控制器通过通信图协同工作。这一架构在提升灵活性的同时，也把攻击面从"单点设备"扩展到"整个协同网络"。

**虚假数据注入（False Data Injection, FDI）攻击**是电力信息物理系统（CPPS）中最具威胁的攻击形式之一：攻击者篡改测量数据或控制指令，可在不触发传统坏数据检测的前提下误导控制决策，进而破坏频率稳定、诱发连锁故障。

论文要解决的核心矛盾被概括为一个"三难问题"：

1. **动力学未知** —— 实际电网设备（逆变器、同步机）的非线性漂移项 $f_i(x_i)$ 难以精确建模，传统基于模型的弹性控制失效；
2. **执行器饱和** —— 物理执行机构存在物理上限，安全策略必须在饱和约束**内部**生成；
3. **攻击可传播** —— FDI 攻击沿交互图传播，单点被攻陷会污染邻居的协同误差，形成级联影响。

而现有工作的共同缺口是：**缺乏一个统一的多智能体框架，同时融合未知非线性、有界执行器、对抗信道与"设计者指派的收敛截止时间"。** 已有方法要么只处理单体系统（Kokolakis 等），要么收敛时间由预选增益被动决定、无法由设计者主动指定（固定时间方法，Gong 等 / 作者前期工作）。

**为什么"预定义时间"对电网安全至关重要？** 电网保护与稳定控制有严格的时间窗口（如暂态稳定的临界切除时间、AGC 的响应时限）。一个"最终会收敛但不知道多久收敛"的控制器，在电力场景中是不可接受的。

---

## 二、系统模型与问题表述

### 2.1 领导者—跟随者动力学

**领导者**（可视为电网的参考轨迹 / 调度指令）：

$$\dot{x}_0 = f_0(x_0), \quad x_0 \in \mathbb{R}^n$$

**第 $i$ 个跟随者**（逆变器 / 分布式控制器）：

$$\dot{x}_i = f_i(x_i) + \mathbf{g}_i(x_i)u_i + \mathbf{d}_i(x_i)\omega_i, \quad i=1,\ldots,N$$

- $f_i$ —— **未知**非线性漂移（学习控制器不依赖它）
- $\mathbf{g}_i$ —— 状态相关的输入矩阵
- $\omega_i$ —— 外部扰动，满足 $\|\omega_i(t)\| \le \bar{\omega}_i$

### 2.2 执行器通道 FDI 攻击模型

这是本文攻击建模的**关键设计点**：

$$u_i(t) = u_{ci}(t) + u_{ai}(t)$$

- $u_{ci}$ —— 防御方生成的**安全**控制指令
- $u_{ai}$ —— FDI 攻击信号，满足 $\|u_{ai}(t)\| \le \bar{u}_{ai}$

代入后系统变为：

$$\dot{x}_i = f_i(x_i) + \mathbf{g}_i(x_i)u_{ci} + \underbrace{\mathbf{g}_i(x_i)u_{ai} + \mathbf{d}_i(x_i)\omega_i}_{\text{对抗输入}\ \varpi_i}$$

> **建模要点（Remark 1）**：FDI 信号在**有界安全指令 $u_{ci}$ 生成之后**注入。若攻击在物理饱和元件之前注入，则需要写成 $sat(u_{ci}+u_{ai})$，这会导致完全不同的博弈表述。这一假设把问题优雅地转化为"控制 vs. 对抗"的零和博弈。

### 2.3 对称输入约束（饱和建模）

$$u_{ci} \in \mathbb{U}_i := \{u_{ci}\in\mathbb{R}^m: |u_{ci\ell}| < \bar{u}_{i\ell},\ \ell=1,\ldots,m\}$$

### 2.4 图耦合协同误差

设通信图 $\mathcal{G}=(\mathcal{V},\mathcal{E},\mathbf{A})$，拉普拉斯矩阵 $\mathbf{L}$，牵制增益 $\mathbf{B}_0=\operatorname{diag}(b_{10},\ldots,b_{N0})$，令 $\mathbf{H}:=\mathbf{L}+\mathbf{B}_0$。

- 期望偏移 $h_i(t)$，个体误差 $e_i := x_i - x_0 - h_i$
- **图耦合协同误差**（把"邻居偏差"聚合进单个可测量量）：

$$\chi_i := \sum_{j\in\mathcal{N}_i} a_{ij}(e_i-e_j) + b_{i0}e_i, \qquad \chi = (\mathbf{H}\otimes\mathbf{I}_n)e$$

**协同误差动力学**（核心方程）：

$$\dot{\chi}_i = F_i^\chi(\xi_i) + \mathbf{G}_{ii}^\chi(x_i)u_{ci} + \mathbf{G}_{i\mathcal{N}}^\chi(x_{\mathcal{N}_i})u_{c\mathcal{N}_i} + \mathbf{D}_i^\chi(x_i,x_{\mathcal{N}_i})\nu_i$$

- $\mathbf{G}_{ii}^\chi = \kappa_i\mathbf{g}_i$（$\kappa_i = b_{i0}+\sum_{j\in\mathcal{N}_i}a_{ij}$）—— 自安全控制通道
- $\mathbf{G}_{i\mathcal{N}}^\chi$ —— **邻居的安全控制通道**（耦合项，体现攻击可传播）
- $\mathbf{D}_i^\chi\nu_i$ —— 本地与邻居对抗输入通道

### 2.5 关键假设

| 假设 | 内容 | 电力场景含义 |
|---|---|---|
| **A1** | 图连通，$\mathbf{H}$ 非奇异且存在正对角 $\boldsymbol{\Pi}$ 使 $\mathbf{H}_s>0$ | 协同网络可达成一致 |
| **A2** | $f_0, f_i, \mathbf{g}_i, \mathbf{d}_i$ 局部 Lipschitz，$h_i,\dot{h}_i$ 有界 | 设备动力学正则 |
| **A3** | 局部状态充分性（Markov 条件） | 相同 $\chi_i$、输入 → 相同右端项 |
| **A4** | RBF 神经网络逼近 $V_i^*(\chi_i)=W_i^{*\top}\phi_i(\chi_i)+\varepsilon_i(\chi_i)$ | 值函数可用 NN 表示 |
| **A5** | 保留回放信息性：$t\ge T_{E,i}$ 后回放栈满秩，$\varsigma_i=\sigma_{\min}(\boldsymbol{\Psi}_i)>0$ | **替代持续激励（PE）要求** |

---

## 三、方法 / 技术路线

### 3.1 零和微分博弈建模

把"安全控制"与"FDI + 扰动"的对峙建模为**局部图零和微分博弈**，代价函数：

$$J_i = \int_0^\infty \Big[ Q_{ii}(\chi_i) + \mathcal{U}_i(u_{ci}) + \sum_{j\in\mathcal{N}_i}\mathcal{U}_{ij}(u_{cj}) - \gamma_i^2\varpi_i^\top\mathbf{T}_{ii}\varpi_i - \gamma_i^2\sum_{j\in\mathcal{N}_i}\varpi_j^\top\mathbf{T}_{ij}\varpi_j \Big]dt$$

- 正项 = 状态偏差 + 控制代价（**最小化**方）
- 负二次项 = 扰动与 FDI 的作用（**最大化**方）
- $\gamma_i$ 是 $L_2$ 增益（鲁棒性旋钮）

值函数与 Nash 鞍点：

$$V_i^*(\chi_i(0)) = \min_{u_{ci}}\max_{\varpi_i,\varpi_{-i}} J_i(\cdot), \qquad J_i(u_{ci}^*,\cdot,\varpi_i^*,\varpi_{-i}^*) \le J_i(u_{ci}^*,u_{c,-i}^*,\varpi_i,\varpi_{-i}) \le \dots$$

### 3.2 饱和感知 HJI 与非二次效用函数

**非二次输入效用**（关键创新之一）：

$$\mathcal{U}_i(u_{ci}) = 2\sum_{\ell=1}^m \bar{u}_{i\ell}r_{i\ell}\int_0^{u_{ci,\ell}}\tanh^{-1}\left(\frac{s}{\bar{u}_{i\ell}}\right)ds$$

由驻点条件导出**安全控制鞍点策略**：

$$u_{ci}^* := -\bar{\mathbf{U}}_i\tanh\left(\frac{1}{2}\mathbf{R}_i^{-1}\bar{\mathbf{U}}_i^{-1}\mathbf{G}_{ii}^{\chi\top}(x_i)\nabla V_i^*\right)$$

> ✅ **关键性质**：由于 $\tanh(\cdot)\in(-1,1)$，**饱和约束由构造自动满足** —— $|u_{ci,\ell}^*|<\bar{u}_{i\ell}$ 对任意有限梯度恒成立。这是"safe by construction"，而非事后裁剪（事后裁剪会破坏最优性）。

**对抗策略**（攻击方的最优响应，用于博弈分析）：

$$\varpi_i^* := \frac{1}{2\gamma_i^2}\mathbf{T}_{ii}^{-1}\mathbf{B}_i^{\chi\top}(x_i)\nabla V_i^*, \qquad \varpi_j^* := \frac{1}{2\gamma_i^2}\mathbf{T}_{ij}^{-1}\mathbf{B}_{ij}^{\chi\top}(x_j)\nabla V_i^*$$

**HJI 方程**：

$$0 = \min_{u_{ci}\in\mathbb{U}_i}\max_{\varpi_i,\varpi_{-i}}\bar{\mathcal{H}}_i(\chi_i,\nabla V_i^*,u_{ci},\varpi_i,\varpi_{-i})$$

### 3.3 代价诱导的预定义时间结构（核心创新）

**两幂状态代价**：

$$Q_{ii}(\chi_i) = \chi_i^\top\mathbf{Q}_i\chi_i + \lambda_x\kappa_{i1}\|\chi_i\|^{2\gamma_1} + \lambda_x\kappa_{i2}\|\chi_i\|^{2\nu}$$

其中 $0<\gamma_1<1<\gamma_2$，$\nu=(\gamma_2+1)/2$。

> **精妙之处**：借助界 $V_i^*(\chi_i)\le\bar{c}_i\|\chi_i\|^2$，可得 $\|\chi_i\|^{2\gamma_1}\ge\bar{c}_i^{-\gamma_1}(V_i^*)^{\gamma_1}$，于是 **HJI 方程自然"长出"两幂耗散项** $-\lambda_x c_{i1}(V_i^*)^{\gamma_1} - \lambda_x c_{i2}(V_i^*)^{\nu}$，**无需对未知的理想值函数施加限制性条件**。

这解决了固定时间方法的根本缺陷：固定时间法直接对**未知的** $V_i^*$ 施加减衰条件（无法验证），而本文让耗散结构从**已知的代价函数**中涌现。

### 3.4 预定义时间比较定理

**Theorem 1**：若 $\dot{V}(t)\le -\frac{\gamma_{p,q,r}}{T_s}[\alpha V^p + \beta V^q]^r$（$0<p<q$，$pr<1<qr$），则原点全局预定义时间稳定且 $T(x_0)\le T_s$。常数 $\gamma_{p,q,r}$ 由 Euler Gamma 函数显式给出。

**Lemma 2（精确两幂收敛时间积分）** —— 解决**逆设计问题**：

若 $\dot{Y}\le -aY^{\frac{\gamma_1+1}{2}} - bY^{\frac{\gamma_2+1}{2}}$，则

$$T(Y(t_0))\le\int_0^{Y(t_0)}\frac{ds}{as^{\frac{\gamma_1+1}{2}}+bs^{\frac{\gamma_2+1}{2}}} < C_\gamma a^{-A_\gamma}b^{-B_\gamma}$$

> **Remark 6 的关键洞见**：不是问"给定不等式能否保证选定收敛时间"，而是问"由两幂方程系数生成的最大均匀收敛时间是多少"，从而**允许从期望时间预算反推系数** —— 这正是"预定义时间"的数学基础。令 $A_\gamma=\frac{\gamma_2-1}{\gamma_2-\gamma_1}$、$B_\gamma=\frac{1-\gamma_1}{\gamma_2-\gamma_1}$，则 $A_\gamma+B_\gamma=1$。

### 3.5 积分 Bellman-Isaacs 恒等式（消除未知漂移）

**核心思想**：把 $\dot{V}_i^*$ 在窗口 $[t-T_i, t]$ 上积分，得到积分形式的 HJI 恒等式，从而**从评论家回归中彻底移除未知漂移 $F_i^\chi$**。

**在线 Bellman-Isaacs 残差**：

$$\delta_i(t) = \hat{W}_i^\top\Delta\phi_i(t) + \int_{t-T_i}^t \hat{r}_i(\tau)d\tau, \qquad \Delta\phi_i(t)=\phi_i(\chi_i(t))-\phi_i(\chi_i(t-T_i))$$

- 若 $\hat{W}_i=W_i^*$ 且为鞍点策略，则 $\delta_i(t)=0$
- **驱动 $\delta_i(t)\to 0$ 等价于沿测量轨迹强制满足 HJI，无需显式知道 $F_i^\chi$**

### 3.6 有限经验回放替代持续激励（PE）

数据栈 $\mathcal{D}_i:=\{(\Delta\phi_{ik},\rho_{ik})\}_{k=1}^{M_i}$，归一化回归量 $\psi_i := \frac{\Delta\phi_i}{1+\Delta\phi_i^\top\Delta\phi_i}$。

- 用**有限回放信息性条件** $\varsigma_i=\sigma_{\min}(\boldsymbol{\Psi}_i)>0$ 替代严苛的持续激励（PE）要求
- 数据信息性瞬态 $T_E = \max_i T_{E,i}$（若离线预采集，可取 $T_E=0$）

> PE 条件在工程中几乎无法保证，这是 IRL 落地的经典障碍。用有限回放替换，显著提升了实用性。

### 3.7 两幂评论家权重更新律

**残差目标**：

$$\mathcal{E}_i(\hat{W}_i) = \frac{|\delta_i|^{\gamma_1+1}}{(\gamma_1+1)\mu_i} + \frac{|\delta_i|^{\gamma_2+1}}{(\gamma_2+1)\mu_i} + \sum_{k=1}^{M_i}\left(\frac{|\delta_{ik}|^{\gamma_1+1}}{(\gamma_1+1)\mu_{ik}} + \frac{|\delta_{ik}|^{\gamma_2+1}}{(\gamma_2+1)\mu_{ik}}\right)$$

**更新律**：

$$\dot{\hat{W}}_i = -\boldsymbol{\Gamma}_i\Big\{ \psi_i[k_{i1}|\delta_i|^{\gamma_1}\operatorname{sgn}(\delta_i) + k_{i2}|\delta_i|^{\gamma_2}\operatorname{sgn}(\delta_i)] + \sum_{k=1}^{M_i}\psi_{ik}[k_{i1}^r|\delta_{ik}|^{\gamma_1}\operatorname{sgn}(\delta_{ik}) + k_{i2}^r|\delta_{ik}|^{\gamma_2}\operatorname{sgn}(\delta_{ik})]\Big\}$$

- $\boldsymbol{\Gamma}_i = \alpha_{c,i}\mathbf{I}_{N_i}$，$\alpha_{c,i}$ **由指派的评论家学习时域 $T_W$ 反推**
- 指数 $\gamma_1$ 在残差原点附近**增强学习**，$\gamma_2$ 在残差较大时**防止学习缓慢**

### 3.8 稳定性分析要点

**评论家学习收敛（Theorem 2）**：Lyapunov 函数 $V_{c,i} := \frac{1}{2\alpha_{c,i}}\widetilde{W}_i^\top\widetilde{W}_i$（$\widetilde{W}_i := W_i^*-\hat{W}_i$）

- **精确残差**：若 $\alpha_{c,i}\ge\frac{\Gamma_E(A_\gamma)\Gamma_E(B_\gamma)}{T_W(\gamma_2-\gamma_1)\varsigma_i^2(k_{i1}^r)^{A_\gamma}(k_{i2}^r)^{B_\gamma}M_i^{\frac{(1-\gamma_1)(1-\gamma_2)}{2(\gamma_2-\gamma_1)}}}$，则 $\widetilde{W}_i(t)=0, \ t\ge T_E+T_W$
- **非零残差**：$V_{c,i}$ 不迟于 $T_E+T_W$ 进入前向不变集 $\mathcal{B}_{W_i}=\{V_{c,i}\le\bar{V}_{c,i}\}$

**关键引理 Lemma 5（扰动符号幂不等式）**：

$$z\left\lceil-z+\epsilon\right\rfloor^\gamma \le -2^{-(\gamma+1)}|z|^{\gamma+1} + (1+2\cdot 3^\gamma)|\epsilon|^{\gamma+1}$$

### 3.9 时间预算分配（工程视角的核心）

总收敛时域**先被指派**，再显式分配为四部分：

$$\underbrace{T_E}_{\text{数据信息性}} + \underbrace{T_W}_{\text{评论家学习}} \rightarrow \underbrace{T_i}_{\text{强化窗口}} \rightarrow \underbrace{\text{编队收敛}}_{\text{指派总时域 } T_p}$$

> **与固定时间方法的本质区别**：固定时间的收敛界由预选增益被动决定；预定义时间方法**先指派截止时间，再反推增益**。这使控制器设计与电网保护的时限要求可以直接对齐。

---

## 四、关键创新点

1. **端到端弹性架构**：首次为未知非线性多智能体系统集成「图耦合安全编队 + 饱和感知图博弈 + IRL + FDI/扰动抑制 + 预定义时间认证」五个要素。

2. **代价诱导的预定义时间 HJI 构造**：用低阶与高阶（两幂）状态惩罚生成所需的耗散结构，**无需对未知理想值函数施加限制性条件** —— 这是对固定时间方法的根本性改进。

3. **仅评论家的积分学习律**：可从指派的评论家学习时域**显式合成增益**，并用**有限回放信息性替代持续激励**，大幅提升工程可行性。

4. **统一点式—积分 Lyapunov 分析**：结合导数受限移动窗不等式与显式时间预算分配，建立学习与编队的实用预定义时间收敛，同时**通过构造保持执行器约束**（safe by construction）。

---

## 五、实验与结果

### 5.1 仿真设置

| 项目 | 配置 |
|---|---|
| 系统 | 1 个领导者 + 4 个非线性跟随者，二维平面 |
| 状态 | $x_i = \operatorname{col}(p_{ix}, p_{iy}, v_{ix}, v_{iy}) \in \mathbb{R}^4$ |
| 未知非线性漂移 | $f_i = \operatorname{col}(v_{ix},v_{iy},F_{ix},F_{iy})$，含三角函数耦合项与交叉项 $c_i=0.02v_{ix}v_{iy}/[1+0.2(v_{ix}^2+v_{iy}^2)]$ |
| 输入矩阵 | $\mathbf{g}_i = \operatorname{col}(\mathbf{0}_{2\times2}, \operatorname{diag}(g_{ix},g_{iy}))$，$g_{ix},g_{iy}$ 随状态变化 |
| 通信拓扑 | **环图 $C_4$**（$a_{12}=a_{21}=a_{23}=\dots=a_{14}=1$） |
| 牵制增益 | $\mathbf{B}_0=\operatorname{diag}(1.4, 0, 0, 1.2)$ |
| 期望偏移 | $h_1=(-10,-6,0,0)$，$h_2=(10,-6,0,0)$，$h_3=(-10,6,0,0)$，$h_4=(10,6,0,0)$ |
| 评论家实现 | **六节点高斯 RBF 神经网络**，$\hat{W}_i\in\mathbb{R}^6$ |
| 扰动 | 多频正弦分量叠加（幅度 0.32/0.15/0.41/0.12 等，频率含二次谐波） |
| 攻击/约束/初值 | 在不同 FDI 攻击、输入约束、初始条件下重复验证 |

> 重要说明：仿真模型**仅用于生成数据，学习控制器不依赖它**。

### 5.2 主要结果

- **图1**：领导者与跟随者的位置、速度轨迹，同时标注预定义时间里程碑（$T_E$、$T_E+T_W$、$T_p$）
- **图2**：二维编队轨迹，虚线为期望轨迹

**核心观察**：随着指派截止时间 $T_p$ 逼近，**跟随者速度与领导者近乎同步，编队误差进入原点的小邻域，同时保持规定的相对偏移**。这验证了：

1. ✅ 预定义时间收敛 —— 收敛发生在**指派时刻**附近，与初始条件无关
2. ✅ FDI 攻击与扰动下的鲁棒性 —— 在对抗输入下仍保持编队
3. ✅ 执行器约束满足 —— 控制量始终在饱和边界内（由构造保证）
4. ✅ 学习有效性 —— 仅评论家、仅用有限回放数据即可完成学习

---

## 六、对电网安全领域的意义

### 6.1 直接价值

1. **为 CPPS 弹性控制提供了"时限可保证"的范式**。电网保护有严格的临界时限（如暂态稳定临界切除时间），"预定义时间"让控制器收敛时间可被主动指派，与保护整定直接对齐。

2. **FDI 攻击建模贴近执行器通道**。与常见的"测量端 FDI"不同，本文攻击注入在控制指令通道，对逆变器控制、二次调频等场景更具工程对应性。

3. **图耦合误差把"攻击传播"内生建模**。$\mathbf{G}_{i\mathcal{N}}^\chi$ 和 $\mathbf{D}_i^\chi$ 项显式刻画邻居被攻陷对本节点的影响，这对分析电网连锁失效有方法论启发。

### 6.2 方法迁移潜力

- **分布式 FaCT 架构 / 虚拟电厂协同控制**：多逆变器编队可类比多智能体协同
- **微电网孤岛—并网切换**：领导者—跟随者可映射为参考单元—从属单元
- **AGC 与二次调频的弹性控制**：$L_2$ 增益 $\gamma_i$ 可作为鲁棒性旋钮

### 6.3 需要谨慎之处

- 论文对象是通用非线性 MAS，**不是实际电网模型** —— 需验证在 IEEE 标准测试系统（如 IEEE 9/39 节点）上的表现
- 攻击模型为有界 $L_2$ 信号，**未覆盖隐蔽性攻击**（stealthy attack，如保持残差不变的 FDI）
- 拓扑为**固定环图**，未考虑电网典型的分区、切换拓扑

---

## 七、局限与展望

### 论文明确的未来工作
> 作者声明：未来将考虑**通信约束（communication constraints）**、**切换拓扑（switching topologies）**，以及**实验验证（experiments）**。

### 本文隐含局限（分析者补充）

| 局限 | 说明 |
|---|---|
| **注入位置假设** | 假设攻击在安全指令之后注入；若 `sat(u_ci + u_ai)`，博弈表述需重构（Remark 1） |
| **拓扑固定** | 仿真为固定 $C_4$ 环图，未考虑电网常见的切换/时变拓扑 |
| **Markov 条件** | 依赖 Assumption 3（局部状态充分性），在强时滞系统中可能不成立 |
| **紧致域分析** | 分析在 $\Omega_i^r$ 上展开（排除原点），Remark 3 说明这是纯分析性处理 |
| **攻击类型单一** | 仅考虑有界 FDI，未涉及隐蔽性攻击、DoS、重放攻击 |
| **无实测验证** | 全部为数值仿真，无 HIL（硬件在环）或实际电网验证 |

### 阅读建议

- **值得精读章节**：§III（问题建模与 HJI 构造）、§III-E（时间预算分配理念）、§IV（稳定性证明）
- **可略读章节**：§II 图论预备知识（标准内容）
- **重点公式**：非二次效用 (23)、两幂代价 (21)、Lemma 2、积分 Bellman-Isaacs 残差 δ

---

## 八、评分

| 维度 | 评分 | 说明 |
|---|---|---|
| 创新性 | 8.5/10 | 预定义时间 + 饱和感知 + 图博弈的结合有新意；代价诱导耗散结构是亮点 |
| 理论严谨性 | 9.0/10 | 四定理 + 多引理，Lyapunov 分析完整（仅评论家学习需注意局部有效性） |
| 工程实用性 | 6.5/10 | 方法重、参数多（$\gamma_1,\gamma_2$、RBF 节点、时间预算分配）；离电网落地有距离 |
| 与电网安全相关性 | 7.0/10 | 方法论高度相关（FDI + MAS + 时限），但缺少电网专用模型验证 |
| 写作清晰度 | 7.5/10 | 结构清晰，但符号极重，需一定控制理论储备 |
| **综合** | **7.7/10** | 理论与方法扎实，电网安全方向**方法类**参考价值高，直接应用需进一步适配 |

---

## 九、延伸阅读

- **同批 arXiv（2026-09-13）**：[[LLaTSA_Large_Language_Model-Aligned_General-Purpose_Transient_Stability_Analysis|LLaTSA：大模型对齐的通用暂态稳定分析]] —— arXiv:2609.14374，LLM 用于暂态稳定，属"AI+电网安全"方向
- **同批 arXiv（2026-09-12）**：arXiv:2609.14067 —— *Fixed-Time Resilient Integral Reinforcement Learning ... Under FDI Attacks*，同作者前期工作，可与本文对比理解"固定时间 → 预定义时间"的演进
- **FDI 攻击检测经典综述**：arXiv:2407.07966 —— *A Comprehensive Survey on the Security of Smart Grid*

---

*笔记生成时间：2026-09-15 ｜ 来源：arXiv 2609.14075v1 ｜ 由 evil-read-arxiv 工作流生成*
