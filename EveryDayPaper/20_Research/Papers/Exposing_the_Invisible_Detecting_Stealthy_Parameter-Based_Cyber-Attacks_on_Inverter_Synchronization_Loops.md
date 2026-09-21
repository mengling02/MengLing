---
document_id: "2608.30574"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2608.30574"
arxiv_id: "2608.30574"
title: "Exposing the Invisible: Detecting Stealthy Parameter-Based Cyber-Attacks on Inverter Synchronization Loops"
authors: ["Zaint A. Alexakis", "Michal M. Drewniak", "Charalambos Konstantinou"]
published: "2026-08-31"
domain: "电网安全与网络攻防"
venue: "arXiv preprint (eess.SY); 14 页；KAUST CEMSE / UT Austin Energy Institute / AGH Krakow"
keywords:
  - "phase-locked loop"
  - "cyber attack"
  - "attack detection"
  - "stability analysis"
  - "synchronization"
  - "inverter-based resources"
  - "parameter tampering"
  - "equilibrium point"
  - "grid-following converter"
  - "cyber-physical power system"
tags:
  - "电网安全"
  - "PLL攻击"
  - "参数篡改"
  - "平衡点指纹"
  - "IBR"
  - "小信号稳定"
  - "CHIL实验"
  - "KAUST"
---

# Exposing the Invisible: Detecting Stealthy Parameter-Based Cyber-Attacks on Inverter Synchronization Loops

> **一句话总结**：攻击者不伪造测量数据，而是悄悄改写逆变器同步环（PLL）的控制器增益——稳态下**平衡点分毫不动**，所以任何基于"状态偏离期望值"的监测都看不见它；本文把这个"隐身性"精确刻画成一个数学条件（$\eta_s = 0$），然后设计了一个**与 SRF PLL 小信号等价、但平衡点会随增益漂移**的替代结构（RSU-based PLL），把原本不可见的增益篡改变成可观测的稳态偏移。

---

## 一、研究背景与问题

### 1.1 电网形态变了，攻击面跟着变

电力系统正从"集中式同步发电机"转向"分布式逆变器资源（IBR）协调"。这一转变带来三重新风险：

- **惯量与阻尼下降**，形成弱网/孤岛网络，对电压扰动更敏感；
- **IoT 监控与控制技术被粗糙地塞进电厂协调链路**，攻击面显著扩大；
- **通信与监控层（SCADA/PLC）成为可直接触及控制参数的入口**。

论文列举了三个真实事件作为威胁可信度支撑：

| 事件 | 内容 | 来源 |
|---|---|---|
| 加州/怀俄明 | 攻击者切断公用事业与 IBR 之间的通信 | NREL 报告 [8] |
| 2019 犹他 | 多座可再生能源场站通信中断 | [8] |
| 波兰电网（2025-12-29） | 绕过本地防火墙、**擦除监控设备固件且不留取证痕迹** | CERT Polska [9] |

前两类是"断通信"，第三类才是本文真正关心的：**有写权限、能改参数、且不留下痕迹**。

### 1.2 为什么 PLL 成了"皇冠上的靶子"

PLL 原本只负责同步。但 **IEEE 1547（2018 修订版）[14]** 现在强制要求并网型（GFL）逆变器像构网型（GFM）一样提供**一次调频/调压支持**——而频率支持必须依赖准确的频率估计，传统上就来自 PLL。

结果：PLL 不再只是同步器，它还要支撑 droop 等**更长时间尺度的控制环**，从而"支配了整个 IBR 的小信号特性"。它同时与**所有控制环**耦合，一旦被篡改，影响会通过控制层逐级放大。

> ⚡ 这里有个值得记住的因果链：**电网规程升级（要求 GFL 提供一次调频）→ 新控制环 → 新攻击面**。安全研究者往往只盯着协议和网络，而真正的攻击面常常是**控制架构演进**的副产品。

### 1.3 前人做了什么，缺什么

| 文献 | 做法 | 问题 |
|---|---|---|
| Kontou et al. [17]（同组前作） | 提出"PLL 增益篡改在稳态不可见、只在后续扰动中显形"的威胁模型 | **只观察到现象，没解释隐身机理**，因此无法设计检测 |
| Bamigbade et al. [18] | 把积分增益置零（$k_i^a = 0$），制造功率调节误差 | 这个攻击**一点都不隐身**：失去相位锁定会立刻留下痕迹并触发保护；且功率转移只在"没有专用一次控制器"时成立（IEEE 1547 下几乎不可能） |
| Bamigbade & de León [19] | 干脆去掉 PLL，用延迟 DSOGI 的电流控制 | 性能不如常规 PLL 方案 |

**缺口很清晰**：需要一个系统化框架，能（a）严格分析这条攻击路径、（b）量化影响、（c）在**不牺牲原有性能**的前提下暴露隐蔽入侵。

本文的两个目标正好对应这三点。

---

## 二、系统模型与问题表述

### 2.1 建模层次：局部 dq 坐标系 + 全局坐标系

这是全文分析的地基，也是最容易读晕的地方。关键设计是**双坐标系**：

- **局部坐标系（上标 $L_i$）**：每台换流器有自己的 dq 帧，其控制器在该帧内实现；
- **全局坐标系（上标 $G$）**：以角频率 $\omega_g$ 旋转的公共帧，用于**把各局部帧数学上互连**。

换流器用平均值模型（理想电压源 + RL 滤波器 + 并联电容），电流动态：

$$
l_i \dot{\imath}^{L_i}_{d,i} = -r_i \imath^{L_i}_{d,i} + \omega_{p,i} l_i \imath^{L_i}_{q,i} + v^{L_i}_{f,d,i} - v^{L_i}_{c,d,i}
$$

$$
l_i \dot{\imath}^{L_i}_{q,i} = -r_i \imath^{L_i}_{q,i} - \omega_{p,i} l_i \imath^{L_i}_{d,i} + v^{L_i}_{f,q,i} - v^{L_i}_{c,q,i}
$$

其中 $\omega_{p,i}$ 是第 $i$ 台 IBR 的频率——**GFL 由 PLL 给出，GFM 由摇摆方程给出**。这个符号是全文的枢纽：攻击者要动的就是决定 $\omega_{p,i}$ 的那个环节。

与文献 [17] 不同，本文**保留了线路与负荷的完整非线性模型**（式 5–6），以便准确刻画它们的相互作用及对 IBR 稳定性的影响。

帧间变换通过相量表示导出：

$$
X^{G} = X^{L_i} e^{j\int(\omega_{p,i} - \omega_g)dt} = \left(x^{L_i}_d + jx^{L_i}_q\right) e^{-j\Delta\theta},
\qquad \dot{\Delta\theta}_i = \omega_g - \omega_{p,i}
$$

稳态时必须有 $\omega_g = \omega^s_{p,i}\ (\forall i \in \mathcal{C})$，此时全局帧下的 dq 量保持常数，**平衡点是一个常向量**——这正是后续稳定性分析与检测设计的立足点。

### 2.2 电网规程要求的一次控制结构

按 ENTSO-E Frequency Sensitive Mode [22]，GFL 换流器须跟随下垂特性：

$$
P_r = P_s + f\!\left(m_P(\omega_n - \omega_g)\right), \qquad
Q_r = Q_s + f\!\left(m_Q(|v|_n - |v|_{pcc})\right)
$$

死区函数 $f(\cdot)$ 的阈值 $\delta$ 上限为 0.5 Hz。参考功率再经过**速率限制器（RL）**：

$$
\dot{P}_{sr} = \dot{P}_m \, \mathrm{sat}\!\left(a(P_r - P_{sr})\right)
$$

![[fig1_frequency_support_curve.png|800]]

![[fig2_gfl_grid_support_control_scheme.png|800]]

### 2.3 一个重要的工程性设计：把"同步"和"测频"拆成两个 PLL

这是本文**在建模阶段就埋下的关键伏笔**。

问题：PLL 被调得"瞬时响应"以便支撑上层控制，于是**任何微小的电网侧扰动都会剧烈激励 PLL 动态**，进而让一次控制器做出过度反应（死区也拦不住）。

解法：把**同步**与**频率估计**拆成两个独立整定的 PLL：

- 同步环用 SRF PLL：

$$
\omega_p = \omega_n + k_{p,s} v^{L}_{c,q} + z, \qquad \dot{z} = k_{i,s} v^{L}_{c,q}
$$

- 外环频率估计器用同一套结构（增益记为 $k_{p,o}, k_{i,o}$，输出 $\omega_o$）。

好处：弱网下可以**单独把同步 PLL 调慢以保稳定**，同时保持频率估计环的响应性——两个目标解耦。论文指出这与"单个 PLL + 额外测频环"结构等价，因此**不失一般性**。

> 这个拆分不只是工程优化。它意味着**攻击者可以选择打哪一个环**——打同步环影响故障穿越，打测频环影响一次调频。后文实验正是分别验证。

---

## 三、方法/技术路线

### 3.1 第一步：把"隐身"变成可计算的量

攻击模型极其简单（也正因此才危险）：攻击者通过被攻陷的监控接口（SCADA/PLC）**一次性覆写** PLL 增益

$$
k_p^n \to k_p^a, \qquad k_i^n \to k_i^a
$$

**不需要实时观测，不需要持续注入**——就改一次参数，然后走人。

考虑 $\hat{V} = 1$ pu，PLL 闭环为：

$$
\dot{\Delta\theta} = \omega_g - \omega_n - k_p \sin\Delta\theta - z, \qquad \dot{z} = k_i \sin\Delta\theta
$$

平衡点：

$$
\Delta\theta^s = 0, \qquad z^s = \omega_g - \omega_n
$$

**核心定义**——设 $\eta_s$ 为攻击前后平衡点之差：

$$
\eta_s = \left(\Delta\theta^s, z^s\right)_n - \left(\Delta\theta^s, z^s\right)_a
$$

> **Remark 1（本文的理论支点）**：PLL 增益篡改攻击**当且仅当** $\eta_s = 0$ 时是隐身的。

由平衡点表达式立即看出：**只要积分作用被保留，平衡点就完全不变**，$\eta_s = 0$，攻击在稳态下**零痕迹**。

这解释了 [17] 的观察，也把 [18] 的攻击重新定位：

- 若 $k_i^a = 0$，则 $\eta_s = \left[(\omega_g - \omega_n)/k_p^a,\ 0\right] \neq [0,0]$ → **立刻暴露**（相位误差导致失锁，触发保护）；
- [17] 考虑的所有"保留积分作用"的增益组合，**恒有 $\eta_s = 0$** → 这才是真正危险的威胁模型，本文即以此为准。

$\eta_s$ 的精妙之处在于：它**恰好**捕获了被监测稳态值的任何偏移，因此给出了"隐身性"的精确数学刻画。同时也给出了**检测设计的充分条件**：

> 想检测增益篡改，就必须让 $\eta_s \neq 0$ ——而常规 SRF PLL 结构**做不到**这一点。

### 3.2 第二步：量化攻击能造成多大破坏（小信号）

用简化单母线模型（GFM + GFL + 负荷接于同一母线），摇摆方程：

$$
J\dot{\Delta\omega} = -D\Delta\omega + P_{GFM} + P_{GFL} - P_L
$$

代入 PLL 动态、在 $\Delta\phi^* = 0$ 处线性化，得到状态矩阵

$$
\begin{bmatrix}
-D/J & -m_P k_{p,o}/J & -m_P k_{i,o}/J \\
1 & -k_{p,o} & -k_{i,o} \\
0 & 1 & 0
\end{bmatrix}
$$

对其实施 Routh–Hurwitz 判据，得到稳定性条件：

$$
\frac{m_P k_{i,o}}{J} < k_{p,o}\left(k_{i,o} + \frac{k_{p,o} D}{J} + \frac{m_P k_{p,o}}{J} + \left(\frac{D}{J}\right)^2 + \frac{D m_P}{J^2}\right)
$$

三个可读的推论：

1. **并非所有参数组合都稳定**——PLL 极度欠阻尼时组合系统很容易失稳；
2. 若 $k_{p,o} = 0$，常规 PLL 只是**临界稳定**，但在该组合模型下**整个系统不稳定**；
3. 若 GFL 接无穷大母线（$J \to \infty$），条件退化为 $-k_{p,o}k_{i,o} < 0$，**恒成立**——两个子系统解耦，各自独立稳定。

简化模型抓不住完整动态，于是作者对图 3 测试台（GFL 0.1 MVA + GFM 1 MVA，下垂 1%，2.5 mH 线路）做**完整非线性模型的雅可比特征值分析**：

![[fig3_gfl_dynamic_grid_testbench.png|800]]

![[fig4_modal_analysis_pll_bandwidth.png|800]]

![[fig5_dominant_eigenvalues_reduced_bw.png|800]]

![[fig6_infinite_bus_dominant_eigenvalues.png|800]]

主要发现（弱网，SCR = 2.9，同步 PLL 带宽 40 Hz，扫频率估计器带宽 0→10 Hz，$\zeta = 1/\sqrt{2}$）：

- **图 4a**：低带宽下系统不稳定（弱网所致）；估计器带宽升高后一次控制器反而**稳住**了系统（带来构网特性，调节 PCC 频率与电压）；但带宽继续升高又失稳——功率/电流控制器与 PLL **跟不上**一次控制器的输出。
- **图 5**：把控制器带宽整体降 3 倍，则**没有频率支持就必然失稳**，且稳定所需的估计器带宽更低、稳定区间更宽。
- **图 4b**：把**同步** PLL 带宽降到 1 Hz，可同时缓解小信号失稳与低频振荡模态；此时提高专用测频环带宽**反而增强故障穿越能力**（主导特征值继续左移）；但继续升高仍会失稳。
- **图 6**：接无穷大母线后，两种配置的主导特征值**完全重合**，对所有 PLL 带宽都稳定。

> ⚡ 结论：**"调得太慢"和"调得太快"都危险**。这本身就是攻击者的操作空间——不需要让系统崩溃，只需要把它推到稳定裕度很薄的区域，然后等一次扰动。

### 3.3 第三步：大信号下的破坏量化

4 台 IBR 的仿真算例（图 7：2×GFM + 2×GFL，各 100 kVA，下垂 1%，母线 1–4，攻击者挂在 GFL 1 上），在母线 3 加 +0.15 MW 负荷，测**电压暂降持续时间**，扫死区、RL 导数限值、测频环带宽：

![[fig7_simulation_benchmark.png|800]]

![[fig8_voltage_sag_duration.png|800]]

- **感性网络（图 8a）**：无死区时恢复最快；RL 导数约束收紧能显著改善**低带宽**下的响应（抑制过于激进的控制动作）；带宽较高时恢复时间趋于饱和。死区 $\pm 0.5$ Hz 时，带宽 < 4 Hz **完全不参与**恢复，4–9 Hz 区间**帮倒忙**（反而延长恢复时间），更高带宽才改善。死区放宽到 $\pm 1$ Hz 效果类似但更显著。
- **阻性网络（X/R = 0.6，图 8b）**：测频环影响**更突出**，恢复时间跨度从 0.1 ms 到 300 ms；与感性网络相反，带 RL 时**降低带宽反而缩短恢复时间**，提高带宽则逐渐变长。

> 这一节的真正价值不在数字，而在确立一个判断：**要让攻击对系统小信号行为产生实质影响，攻击者必须显著改变 $k_p$、$k_i$ 或两者**。这句话直接成为检测机制的设计前提。

### 3.4 第四步：RSU-based PLL —— 让平衡点变成"指纹"

检测思路：**换一个与 SRF PLL 行为等价、但平衡点结构不同的实现**，把不可观测的增益变成可观测的稳态偏移。

采用 [24] 提出的鲁棒同步单元（RSU）：

$$
\dot{\theta}_R = \omega_R = \omega_N + k_i z, \qquad
\dot{z} = \arctan v^{R}_{c,q} - k_p z, \qquad
\theta_P = \theta_R + k_p z
$$

![[fig9_proposed_rsu_pll.png|800]]

其**攻击前平衡点**为：

$$
\Delta\theta^s = \frac{k_p^n(\omega_g - \omega_N)}{k_i^n}, \qquad
z^s = \frac{\omega_g - \omega_N}{k_i^n}
$$

关键差别：平衡点**同时依赖 $k_p^n$ 和 $k_i^n$**，因此 $\eta_s$ 现在能捕获**任意**增益篡改，攻击者再也找不到"不移动平衡点"的伪装组合。

**$\omega_N$ 的三重作用**（全文最巧妙的设计）：

| 作用 | 机理 |
|---|---|
| **隐私保护** | 取 $\omega_N \neq \omega_n$ 时，式 (43) 是"2 个方程、3 个未知数（$k_p, k_i, \omega_N$）"，拦截者无法反解增益；只有掌握实现结构和 $\omega_N$ 的厂站运行方可以 |
| **设定检测裕度** | $\omega_N$ 按比例缩放平衡点，增大 $|\omega_g - \omega_N|$ 就放大稳态偏移 $|\Delta\theta^s|, |z^s|$，使增益变化更容易与频率波动、测量噪声、电网扰动区分 |
| **不影响暂态** | $\omega_N$ 是常数前馈项，**不改变 PLL 的小信号动态**，因此可开机时一次整定，且**无需暴露在 SCADA 接口上** |

另外，由 $\Delta\theta^s = k_p^n z^s$ 可知两个平衡点之间存在**与 $\omega_N$ 无关的固定比例关系**——所以 $k_p$ 的任何变化都会破坏这个比例，从而暴露攻击。$\omega_N$ 还可用密码学方案**定期重键（re-key）**，即使泄露也只在下次更新前有效。

**检测算法（Algorithm 1）**：每采样点比较 $\eta_s$ 与 $T_w$ 之前的窗口值，逐元素差值 $\Delta\eta$ 持续超过阈值 $\epsilon$ 达 $T_d$（驻留时间）即置标志 $\sigma$。

- $T_w$（观测窗口）按运行方可能使用的最慢 PLL 整定，保守取几秒；
- $T_d$ 短 → 检测快但可能把暂态误报；$T_d$ 长 → 延迟但零误报；
- 由于攻击影响**只在显著暂态时显现**（几秒内不太可能发生），**保守的 $T_d$ 更可取**；
- 平衡点只是"增益 + 电网频率"的函数，而后者在攻击时间尺度上近似常数，因此**持续偏移只可能来自增益变化** → 原则上不产生误报。

**小信号等价性证明**（采纳的最大理由）：

$$
\frac{\theta_P}{\theta_g} = \frac{k_p s + k_i}{s^2 + k_p s + k_i}
$$

与 SRF PLL **完全一致**。因此所有针对 SRF PLL 的稳定性分析（包括第五节的结果）**原封不动适用于**该替代结构；状态数相同、计算量低，可**直接替换**现有 GFL 装置中的同步环。

此外，它给出了**显式的旋转频率** $\omega_P = \omega_N + k_i z + k_p \dot{z}$，这是图 2 控制器实现 dq 解耦所必需的——而 [18][19] 的方案没有这个量，因而难以移植到工业控制器。配合 QSG 正负序分离 [26]，还可工作于不平衡与含 5/7 次谐波的电网。

**向多层控制器的推广（Sec VI-A）**：把 PI 控制器改为 $u = k_p(a x_r - x) + k_i\!\int(x_r - x)$，其中 $a \in (0,1)$ 用于"掩蔽"平衡点，得到唯一的非线性平衡点映射 $0 = g(k_p, k_i, x_r)$，从 $g = 0$ 的解即可反解增益——同样只有掌握结构与参数 $a$ 的运行方可做到。

---

## 四、关键创新点

1. **把"隐身性"形式化为 $\eta_s = 0$**（Remark 1）。这是全文最漂亮的一步：一个之前只被"观察到"的现象，被还原成一条可计算、可设计的判据，并直接推出"常规 SRF PLL 结构原理上无法检测此类攻击"这一否定性结论。

2. **用"平衡点指纹"替代"异常检测"**。不训练模型、不设统计阈值，而是**改控制器结构**让物理量本身携带增益信息。这是一种"白盒 + 物理"的检测范式，与主流 ML/IDS 路线形成鲜明对比。

3. **RSU-based PLL 做到了"零性能代价"**。通过证明 $\theta_P/\theta_g$ 与 SRF PLL 完全相同，把"可检测性"作为**纯增量能力**叠加到既有装置上——工程可采纳性极高。

4. **$\omega_N$ 的三重角色**（隐私 / 检测裕度 / 不影响暂态），把密钥管理思想引入控制器参数设计。

5. **完整的"攻击—影响—防御"闭环**：小信号 + 大信号影响分析 → 由此推出检测设计前提 → 设计检测 → CHIL 实验验证。

6. **可推广性**：平衡点原理被明确推广到一般 PI 控制器层，暗示这是一类**方法论**而非单点技巧。

---

## 五、实验与结果

### 5.1 实验平台

控制器硬件在环（CHIL）：**Speedgoat Baseline** 实时目标机生成 GFL 的触发脉冲，**Typhoon HIL 404** 仿真电网与电力电子部分。

![[fig10_experimental_chil_benchmark.jpeg|800]]

主要参数（Table II）：GFL 0.1 MVA / GFM 1 MVA；频率下垂 5% / 2%；电压下垂 5% / 5%；基础负荷 0.3 MVA；线路 0.01 Ω、0.2 mH；开关频率 15 kHz；额定线电压 400 V。

### 5.2 平衡电网条件

整定：同步 PLL 带宽 20 Hz，测频环带宽 2.5 Hz，$\zeta = 1/\sqrt{2}$，$f_N = 49.9$ Hz（即 $\omega_N/2\pi$）；检测参数 $\epsilon_{\Delta\theta} = 2\times10^{-2}$，$\epsilon_z = 5\times10^{-4}$，$T_d = T_w = 0.8$ s；信号经 100 Hz 低通。

![[fig11_srf_vs_proposed_pll_response.png|800]]

图 11 验证**两套 PLL 行为一致**：t = 7.5 s 因负荷突增（15 kW / 45 kVar）频率冲出 $\pm 0.1$ Hz 死区，功率随即按新工况调整。

**攻击场景一：只改积分增益**（$k_i^a = k_i^n/3$，t = 5 s）

![[fig12_integral_gain_tampering_detection.png|800]]

- 攻击瞬间**所有状态都被扰动**（图 12a、12d 的功率与频率），随后**收敛回同一平衡点**——正是"稳态不可见"的体现；
- 但**内部相位误差（图 12b）与 $z$（图 12c）的平衡点发生显著偏移** → 两个标志约在攻击后 **0.8 s**（由 $T_d$ 决定）同时置 1（图 12e）；
- 对照组 [18] 的检测器（基于 SRF PLL 相位估计误差）**完全未能察觉**。

**攻击场景二、三**：$k_p^a = k_p^n/2,\ k_i^a = 3k_i^n$（图 13）；$k_p^a = 2k_p^n$（图 14）——同样被检出，而 [18] 依旧无感。

![[fig13_pi_gain_tampering_detection.png|800]]

![[fig14_proportional_gain_tampering_detection.png|800]]

**最小检测延迟**：条件滤波（≈0.04 s）+ PLL 整定（≈0.34 s）串联，保守上界 **≈0.38 s**（真实响应更快）。$T_d$ 可从此下限取到数秒。

### 5.3 不平衡与畸变电网条件

三相电压设为 0.98∠+0.5°、1.05∠−1.5°、0.96∠−0.5° pu，引入明显负序；PLL 配 QSG 解耦 [26]；同步 PLL 带宽 25 Hz；死区从 $\pm 0.1$ Hz 收紧到 $\pm 0.05$ Hz（加压测试）；**单个 PLL 同时承担同步与测频**（同 [17]），$\omega_o$ 由 PLL 频率经 5 Hz 低通获得；$f_N = 46$ Hz（**故意拉大 $|\omega_g - \omega_N|$ 以放大平衡点偏移、提升灵敏度**）；检测参数 $\epsilon_{\Delta\theta} = 5\times10^{-3}$，$\epsilon_z = 1\times10^{-4}$，$T_d = T_w = 1$ s；**开关频率降至 10 kHz**（验证低采样率下仍有效）。

![[fig15_unbalanced_distorted_grid_response.png|800]]

图 15 施加扰动序列：t = 2 s 频率阶跃至 50.1 Hz、t = 4 s 至 49.9 Hz、t = 6 s 电压暂降至 70%（t = 8 s 清除）、t = 10 s 注入 5/7 次谐波（0.06 / 0.09 pu）。两套实现**表现几乎完全相同**，暂态中频率估计也一致；无功功率在暂降期间饱和于 14 kVar。

**攻击场景：以扰动为掩护**——t = 4 s 发生 0.7 pu 电压暂降（t = 4.5 s 清除），攻击者趁暂降刚清除，在 t = 6 s 对**同步 PLL** 施加 $k_p^a = 0.8 k_p^n$：

![[fig16_proportional_tampering_unbalanced_grid.png|800]]

- 由于**平衡点只依赖增益与电网频率**，暂降和谐波**都无法掩蔽**该篡改；
- 篡改表现为功率输出（图 16d）与 $z$（图 16c）的暂态——其中 $z$ 因 $z^s$ 与 $k_p$ 无关而**回到攻击前平衡点**；更关键的是**内部相位误差平衡点出现持续偏移**（图 16b）；
- 约 1 s（由 $T_d$ 决定）后 $\sigma_{\Delta\theta}$ 置 1；[18] 的检测器依然不知情。
- 该场景最小检测延迟 ≈ 0.04 s（滤波）+ 0.04 s（PLL）= **≈0.08 s**。

---

## 六、对电网安全领域的意义

### 6.1 一类被忽视的攻击面：不是"改数据"，而是"改参数"

主流电网安全研究（尤其 FDIA 文献）关注**测量数据完整性**：攻击者篡改量测 → 欺骗状态估计 → 误导调度决策。

本文关注的是**控制器参数完整性**：攻击者篡改 PLL 增益 → 改变换流器动态 → 削弱稳定裕度。两者都是"数据/参数完整性攻击"，但作用**层次完全不同**：

| | FDIA（经典） | PLL 增益篡改（本文） |
|---|---|---|
| 攻击对象 | 量测量 | 控制器参数 |
| 影响路径 | 状态估计 → 调度决策 | 动态响应 → 稳定裕度 → 保护动作 |
| 触发条件 | 需持续注入 | **一次性覆写** |
| 可见性 | 残差检验可查 | **稳态零痕迹** |
| 破坏形态 | 错误决策 | 故障穿越失败 / 保护误动 |

这张对照表值得记住：**"参数层"攻击在隐身性上天然优于"数据层"攻击**，因为它不需要持续行动。

### 6.2 一个可迁移的方法论：先问"平衡点会不会动"

本文的真正遗产不是 RSU 这个具体电路，而是那条推理链：

> **对任意控制器，问：它的平衡点映射 $g(\text{参数}, \text{外部输入}) = 0$ 是什么？参数变化会不会移动平衡点？**
> 如果不会 → 该参数是**不可观测的**，就是攻击者的乐园。
> 如果会 → 那么稳态偏移就是**天然的入侵指纹**，不需要机器学习。

这条思路可以直接搬到其他控制层（励磁、AGC、构网控制、FACTS），甚至可以反过来当作**脆弱性审计工具**：扫一遍控制器参数，看哪些是"平衡点不变"的。

### 6.3 对"物理约束是护城河"的直接印证

对南有乔木同学而言，本文是一个几乎教科书级的例证：**整套检测机制里没有一行机器学习代码**。它靠的是

- 平衡点分析（物理 / 动力学），
- Routh–Hurwitz 判据（经典控制），
- 小信号等价性证明（传递函数），
- CHIL 硬件验证。

而它解决的问题（隐蔽参数攻击检测）恰恰是纯 ML 方法**理论上无法保证**的——你没法用异常检测去发现一个"稳态完全正常"的攻击。**物理不变量能给出 ML 给不了的确定性保证。**

### 6.4 与实验室方向的对接点

- **与 FDIA + GNN 主线的互补**：本文提供了一个**非 ML 的强基线**。任何 GNN 检测器都应先回答"相比平衡点指纹，它多发现了什么？"
- **可组合的物理特征**：$\eta_s$、$z^s$、$\Delta\theta^s$ 这类平衡点偏移量，可以做成 GNN 的**物理信息特征**（physics-informed features），而不是让网络从原始量测里盲学。
- **数字孪生的安全用法**：RSU 本质上是在装置内并行运行一个"影子 PLL"，比对内部状态——这正是**数字孪生式入侵检测**的一个具体、可实现的形态。
- **新的可研究缺口**：**自适应攻击者**。如果攻击者知道 RSU 结构，能否构造一组增益使 $\eta_s$ 仍为 0？（见下节）

---

## 七、局限与展望

### 7.1 我认为最值得质疑的一点：隐私论证存在逻辑循环 ⚠️

论文的隐私性论证是：$\omega_N$ 不暴露在 SCADA 接口上，所以拦截者无法反解增益。

但**威胁模型本身**就是"攻击者获得了监控接口的写权限"。既然能**写** $k_p, k_i$，那么在多数现实攻击链中（例如获得 PLC/SCADA 的高权限会话），**读**取 $\omega_N$ 通常也不成问题。论文用"无需暴露在 SCADA 接口上"来回应，但一个能改写控制参数的攻击者，其能力边界未必止于 SCADA 接口。

**这一点的意义在于**：如果 $\omega_N$ 可被读取，那么攻击者就能利用式 (43) 反推并**主动掩蔽**攻击——即构造"保持 $\eta_s = 0$"的增益组合。而论文并未分析这种自适应攻击者。**这是我认为最值得跟进的研究缺口。**

### 7.2 论文未充分处理的其它问题

| 局限 | 说明 |
|---|---|
| **无自适应攻击评估** | 未考虑知晓 RSU 结构、主动设计掩蔽策略的对手 |
| **误报率未量化** | 只有定性论证（"持续偏移只可能来自增益变化"）；未在真实噪声、量测偏差、**合法的自适应增益调度**下测 FPR |
| **规模偏小** | CHIL 仅 1×GFL + 1×GFM；仿真仅 4 台 IBR。未在 IEEE 39/118 节点级系统或大规模 IBR 场站上验证 |
| **未涉及协同攻击** | 多台 IBR 同时被篡改、或"部分篡改 + 部分伪造通信"的组合未讨论 |
| **检测延迟 vs 保护时限未对齐** | 0.08–1 s 的延迟相对继电保护（ms 级）意味着什么？论文未讨论。虽然攻击只在暂态显形使该延迟可接受，但最坏情况未量化 |
| **参数层防护缺失** | 既然攻击入口是监控接口，为何不先做参数写入的完整性保护 / 签名？论文把问题定位在"检测"而非"预防" |
| **推广部分未验证** | Sec VI-A 的多层控制器推广只是推导，无实验 |

### 7.3 我认为最有价值的三个后续方向

1. **自适应攻击下的隐身性边界**：形式化"攻击者已知 RSU 结构"时的最优掩蔽问题，求出 $\eta_s = 0$ 的可达增益集合。若为空集 → 强化了本文结论；若非空 → 直接构成新的攻击论文。**这是最容易出成果、也最契合"攻防对偶"的方向。**

2. **平衡点指纹 + 图学习**：把各 IBR 的 $\eta_s$ 向量作为节点特征，用 GNN 建模**跨装置的相关性**——单机检测可能被小增益变化绕过，但**多机协同的平衡点偏移模式**可能暴露攻击意图。这正好把物理不变量与 GNN 结合，落在他的主线上。

3. **脆弱性审计工具化**：把"平衡点是否随参数移动"作为**通用指标**，扫描 IBR 全控制栈（PLL、电流环、电压环、droop、限幅器），产出一张"参数可观测性地图"，指出哪些参数是攻击者的隐身区。

---

## 八、评分

### 综合评分：**7.5 / 10**

| 维度 | 评分 | 说明 |
|---|---|---|
| **问题重要性** | 9/10 | IBR 占比快速上升 + IEEE 1547 强制一次控制 = 真实且正在扩大的攻击面；真实事件（波兰）支撑威胁可信度 |
| **理论贡献** | 8.5/10 | $\eta_s = 0$ 的隐身性刻画简洁、精确、可设计；"常规结构原理上不可检测"的否定性结论有分量 |
| **方法创新** | 8/10 | 用"改结构让物理量携带信息"替代"建模型检测异常"，思路新颖；小信号等价性证明使方案几乎无采纳成本 |
| **实验强度** | 7.5/10 | CHIL 硬件在环 + 平衡/不平衡双场景 + 多攻击模式，且刻意做了低采样率与谐波压力测试；但系统规模小，仅单机攻击 |
| **严谨性** | 7/10 | 推导扎实、对比表诚实；扣分在于隐私论证的循环性，以及缺乏自适应攻击者分析 |
| **可复现性** | 7/10 | 参数表完整（Table II），但未提供代码/数据集；CHIL 平台成本较高 |
| **写作与结构** | 8.5/10 | Table I 的对比表清晰；从威胁模型 → 影响分析 → 检测设计的逻辑闭环完整 |

**一句话评价**：这是一篇**思想密度高于篇幅密度**的论文——它真正的贡献是提出了一个可迁移的检测范式（平衡点指纹），而非某个具体电路。它的短板也很清楚：**没有认真对待一个知道你防御方案的对手**。

> ⚡ 如果只带走一句话：**当一个参数的变化不改变任何稳态可观测量时，它在数学上就是不可检测的——想检测它，你必须先改变系统结构。**

---

## 九、延伸阅读

### 9.1 本文直接对话的前作（按理解顺序）

1. **[17] Kontou, Syed, Paspatis, Feng, Konstantinou, Hatziargyriou**, "Exploiting the inherent cyber resilience of inverter-dominated microgrids against PLL attack," *IEEE Trans. Industrial Electronics*, vol. 73, no. 1, pp. 1487–1492, 2026.
   → **本文威胁模型的来源**（同组前作，Konstantinou 参与）。先读它才知道本文在补什么洞。

2. **[18] Bamigbade, Dvorkin, Karri**, "Cyberattack on phase-locked loops in inverter-based energy resources," *IEEE Trans. Smart Grid*, vol. 15, no. 1, pp. 821–833, 2024.
   → 积分增益置零攻击。本文实验中的**对照组检测器**就来自这里，读它能看懂图 12–16 中"为何 [18] 无感"。

3. **[19] Bamigbade, de León**, "Secure voltage-modulated vector current control of DER using delayed DSOGI under distorted and unbalanced grid conditions," *IEEE Trans. Industry Applications*, vol. 61, no. 1, pp. 1091–1101, 2025.
   → 去 PLL 路线的代表。

4. **[24] Alexakis, Alexandridis, Papageorgiou, Konstantopoulos**, "Novel VSI synchronization unit with increased robustness: Detailed analysis and validation," *IEEE Trans. Power Delivery*, vol. 39, no. 4, pp. 2219–2230, 2024.
   → **RSU 结构的原始出处**（本文第一作者前作）。想真正吃透式 (40)–(42) 必须读。

### 9.2 支撑性文献（非安全，但建模必需）

- **[14] IEEE Std 1547-2018** —— 理解"为什么 GFL 现在必须提供一次调频"的规范依据。**这是本文攻击面的制度性成因。**
- **[22] ENTSO-E Frequency Sensitive Mode 实施指南（2018）** —— 死区 $\delta \le 0.5$ Hz 的来源。
- **[25] Wu, Wu, Zhao, Li, Wang**, "Influence of PLL on stability of interconnected grid-forming and grid-following converters," *IEEE TPEL*, vol. 39, no. 10, 2024. → GFM/GFL 低带宽互作用失稳，本文图 4 的现象与之一致。
- **[21] Kundur**, *Power System Stability and Control* —— 摇摆方程与 Routh–Hurwitz 的基础。
- **[26] Rodríguez et al.（PESC 2006）** —— QSG 正负序分离，理解第 5.3 节不平衡工况的前提。

### 9.3 威胁可信度支撑（工程报告）

- **[8] Walker, Desai, Saleem, Gunda**, "Cybersecurity in photovoltaic plant operations," NREL Technical Report, Mar. 2021. → 加州/怀俄明 IBR 通信中断事件。
- **[9] CERT Polska**, "Energy Sector Incident Report – 29 December 2025," Jan. 2026. → **波兰电网事件：绕过本地防火墙、擦除监控设备固件、不留取证痕迹**。与本文"一次覆写、零痕迹"的威胁模型高度吻合，值得单独细读。

### 9.4 同期可对照的电网安全新论文（本次检索命中，尚未解读）

| arXiv ID | 日期 | 标题 | 为何值得追 |
|---|---|---|---|
| **2609.12305** | 2026-09-11 | Self-Verifying Anomaly Detection using Explainable AI for Cybersecurity of DER Networks | **Iowa State（Govindarasu 组）**；LightGBM + SHAP 做"自验证"告警，恰好是本文的**AI 对照路线**（一个用物理指纹，一个用可解释 ML）——建议成对阅读 |
| **2608.13823** | 2026-08-13 | Hierarchical Sensor-Spoofing Defence Framework for Networked DC Microgrids via Cyber-Physical Coordination | 传感器欺骗攻击的**分层物理+网络协同防御**，与本文"物理指纹"思路同源 |
| **2608.01375** | 2026-08-02 | AdaptoNet: Modular Foundation-Adaptive Neural Networks for Cyber-Physical Attack Detection in Power Grids | 数据拒绝攻击（denial）下 F1 恢复，是"AI 检测在极端场景退化"的实证 |
| **2607.27661** | 2026-07-30 | Strategy Phasing of Cyber Attacks on Digital Substations | **IEC 61850 数字变电站**的 HMM 攻击阶段推断（Chen-Ching Liu 组），攻击链视角 |
| **2607.06213** | 2026-07-07 | FDIFormer: Protocol-Aware Transformer Learning for FDIA Detection in Smart Grid Networks | **GOOSE 报文级 FDIA 检测**（协议感知 Transformer），与他的 FDIA 主线最近 |
| **2607.25093** | 2026-07-27 | Functional Subspace Projection for Detection of Coordinated Stealthy Attacks in Power Systems | FSU Anubi 组（已在 09-18 笔记中追踪的研究线），RKHS 函数子空间检测 |

### 9.5 建议的阅读顺序

```
[17] 威胁模型来源  →  本文（核心）  →  [24] RSU 原始出处
                          ↓
                    [18] 对照组检测器
                          ↓
              2609.12305（AI 对照路线，成对读）
```

---

## 附：核心公式速查卡

| 量 | 公式 | 含义 |
|---|---|---|
| SRF PLL 动态 | $\dot{\Delta\theta} = \omega_g - \omega_n - k_p\sin\Delta\theta - z,\ \ \dot{z} = k_i\sin\Delta\theta$ | 常规结构 |
| SRF PLL 平衡点 | $\Delta\theta^s = 0,\ z^s = \omega_g - \omega_n$ | **与增益无关** → 可被隐身篡改 |
| 隐身性判据 | $\eta_s = (\Delta\theta^s, z^s)_n - (\Delta\theta^s, z^s)_a = 0$ | **攻击当且仅当 $\eta_s = 0$ 时隐身** |
| RSU PLL | $\dot\theta_R = \omega_N + k_i z,\ \dot z = \arctan v^R_{c,q} - k_p z,\ \theta_P = \theta_R + k_p z$ | 平衡点随增益移动 |
| RSU 平衡点 | $\Delta\theta^s = \dfrac{k_p^n(\omega_g - \omega_N)}{k_i^n},\ z^s = \dfrac{\omega_g - \omega_N}{k_i^n}$ | **同时依赖 $k_p^n$ 与 $k_i^n$** |
| 小信号等价性 | $\dfrac{\theta_P}{\theta_g} = \dfrac{k_p s + k_i}{s^2 + k_p s + k_i}$ | 与 SRF PLL 完全一致 → 可无损替换 |
| RSU 旋转频率 | $\omega_P = \omega_N + k_i z + k_p\dot{z}$ | dq 解耦所需 |
| 稳定条件 | $\dfrac{m_P k_{i,o}}{J} < k_{p,o}\!\left(k_{i,o} + \dfrac{k_{p,o}D}{J} + \dfrac{m_P k_{p,o}}{J} + \left(\dfrac{D}{J}\right)^2 + \dfrac{D m_P}{J^2}\right)$ | 带宽过低/过高均失稳 |
| 检测判据 | $\Delta\eta = \lvert\eta_s(n) - \eta_s(n-w)\rvert$ 持续 $> \epsilon$ 达 $T_d$ | 窗口 + 驻留时间 |
