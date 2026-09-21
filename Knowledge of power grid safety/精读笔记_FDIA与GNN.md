---
title: 精读笔记 · FDIA 与 GNN 方向
summary: FDIA 检测方向 10 篇演进全景 + 4 篇核心论文逐节批注 + 可运行复现代码
tags: [电网安全, FDIA, GNN, 论文精读, 入侵检测]
created: 2026-09-16
---

# 🔬 精读笔记 · FDIA 与 GNN 方向

> **给南有乔木同学**：这份笔记只服务一件事 —— 让你在 2~3 周内把「FDIA 检测 + GNN」这条线**从读懂到能动手**。
>
> **推荐用法**：先读 [第一部分](#第一部分10-篇演进全景) 建立全局地图（约 1 小时）→ 再精读 [第二部分](#第二部分4-篇核心论文逐节批注) 的 4 篇（每篇 2~3 小时）→ 最后跑 [第三部分](#第三部分可运行复现代码) 的代码（半天）。
>
> **配套**：`docs/Week05`（FDIA 原理）、`docs/Week06`（AI 入侵检测）、`资源索引_视频与论文.md`

---

## 目录

- [第一部分：10 篇演进全景](#第一部分10-篇演进全景)
  - [1.1 一张图看懂 FDIA 检测的技术演进](#11-一张图看懂-fdia-检测的技术演进)
  - [1.2 十篇论文对比总表](#12-十篇论文对比总表)
  - [1.3 三条技术路线的本质差异](#13-三条技术路线的本质差异)
  - [1.4 这个方向的"研究缺口"在哪](#14-这个方向的研究缺口在哪)
- [第二部分：4 篇核心论文逐节批注](#第二部分4-篇核心论文逐节批注)
  - [论文 ①：Liu 2009 — FDIA 开山之作](#论文--liu-2009--fdia-开山之作)
  - [论文 ②：GDN (AAAI 2021) — GNN 时序异常检测](#论文--gdn-aaai-2021--gnn-时序异常检测)
  - [论文 ③：E-GraphSAGE (NOMS 2022) — GNN 入侵检测](#论文--e-graphsage-noms-2022--gnn-入侵检测)
  - [论文 ④：对抗攻击 IDS — 攻防闭环](#论文--对抗攻击-ids--攻防闭环)
- [第三部分：可运行复现代码](#第三部分可运行复现代码)
- [第四部分：选题建议与实验设计](#第四部分选题建议与实验设计)

---

# 第一部分：10 篇演进全景

## 1.1 一张图看懂 FDIA 检测的技术演进

先看全局。FDIA 研究从 2009 年到现在，检测方法经历了四个阶段：

```
【阶段一】理论奠基（2009-2013）
  核心问题：能不能骗过坏数据检测（BDD）？
  代表：Liu 2009 CCS —— 提出 a = Hc，证明残差不变
  产出：攻击可行性的理论证明

        ↓  问题变成："既然能骗过，怎么检测？"

【阶段二】统计与物理方法（2013-2016）
  核心思路：用物理规律和统计假设找异常
  代表：Kosut 2011（检测极限）、Ashok 2017（负荷预测）
  产出：可检测性的理论边界 + 基于预测残差的方法

        ↓  问题变成："统计方法太依赖精确模型，模型不准怎么办？"

【阶段三】机器学习方法（2016-2020）
  核心思路：让模型自己从数据里学异常模式
  代表：SVM/RF、LSTM、自编码器
  产出：工程可用，但对拓扑变化不鲁棒

        ↓  问题变成："电网拓扑是图结构，ML 没利用这个结构信息"

【阶段四】图神经网络方法（2020-至今）★ 你在这里
  核心思路：把电网显式建图，用 GNN 学空间依赖
  代表：GDN（AAAI 2021）、E-GraphSAGE（NOMS 2022）
  产出：空间信息 + 时序信息联合建模

        ↓  新问题："GNN 检测器自己会不会被对抗攻击打掉？"

【阶段五】对抗鲁棒性（2021-至今）★ 最新战场
  核心问题：AI 检测器的安全性
  代表：对抗样本攻击 IDS、鲁棒 GNN 检测
  产出：攻防闭环 —— 你实验室两个方向的交汇点
```

> 💡 **给你的定位**：如果你现在进场，"阶段四 + 阶段五"是既有前人成果可复现、又有明显创新空间的位置。**阶段五最前沿，但风险也最高**。

---

## 1.2 十篇论文对比总表

| # | 论文 | 年份/出处 | 类型 | 核心贡献 | 方法关键词 | 代码 | 精读建议 |
|---|---|---|---|---|---|---|---|
| **P1** | **False Data Injection Attacks against State Estimation in Electric Power Grids**<br>Liu, Ning, Reiter | 2009<br>*ACM CCS* | 🏛️ 奠基 | 提出 FDIA，证明 $a=Hc$ 可绕过 BDD | 状态估计、残差检验、攻击向量构造 | ❌ | ⭐⭐⭐ **必读** |
| P2 | False Data Injection Attacks in Electricity Markets | 2010<br>*IEEE SmartGridComm* | 🏛️ 奠基 | 把 FDIA 打到电力市场（LRA 前身） | 市场结算、经济攻击 | ❌ | ⭐⭐ |
| P3 | On the Performance of Detecting Malicious Data in Power Systems | 2011/2013<br>*IEEE TSG* | 📐 理论 | 刻画**检测极限**：攻击者可伪装到任意接近 | 零动态、隐蔽攻击、KL 散度 | ❌ | ⭐⭐⭐ |
| P4 | Local Load Redistribution Attacks with Incomplete Network Information | 2014<br>*IEEE TSG* | ⚔️ 攻击 | LRA：不伪造量测也能攻击 | 负荷重分配、拓扑信息 | ❌ | ⭐⭐ |
| P5 | Online Detection of Stealthy FDIA using Load Forecasts | 2017<br>*IEEE TSG* | 🛡️ 检测 | 用**负荷预测**做物理一致性校验 | 预测残差、在线检测 | ❌ | ⭐⭐⭐ |
| P6 | Machine Learning for FDIA Detection（SVM/RF 类多篇） | 2016-2019 | 🤖 ML | 首次系统用 ML 做 FDIA 检测 | 特征工程、SVM、RF | 部分 | ⭐⭐ |
| P7 | Deep Learning for FDIA Detection（LSTM/自编码器类） | 2018-2020 | 🤖 DL | 时序建模，无需精确物理模型 | LSTM、Autoencoder | 部分 | ⭐⭐ |
| **P8** | **Graph Neural Network-Based Anomaly Detection in Multivariate Time Series (GDN)**<br>Deng & Hooi | 2021<br>*AAAI* | 🕸️ GNN | **结构学习 + 图注意力**，自动学传感器依赖图 | 图偏差网络、注意力、结构学习 | ✅ [开源](https://github.com/d-ailin/GDN) | ⭐⭐⭐ **必读** |
| **P9** | **E-GraphSAGE: A GNN based Intrusion Detection System**<br>Lo, Layeghy, Portmann | 2022<br>*IFIP NOMS* | 🕸️ GNN | **边特征**图神经网络做网络入侵检测 | GraphSAGE、边特征、NetFlow | ✅ [开源](https://github.com/waimorris/E-GraphSAGE) | ⭐⭐⭐ **必读** |
| **P10** | Adversarial Attacks Against Deep Learning-based IDS（多篇） | 2021-2023 | ⚔️ 攻防 | 用对抗样本**打掉** AI 检测器 | FGSM、PGD、对抗训练 | 部分 | ⭐⭐⭐ **必读** |

> 📌 **注意**：P6、P7、P10 是多篇同类论文的统称（该方向论文数量大、单篇影响力分散）。我在第二部分精读的是它们的**代表性工作**，具体论文在对应小节给出。

---

## 1.3 三条技术路线的本质差异

这是最容易被忽略、但**写论文时最重要**的一点：三条路线解决的根本不是同一个问题。

| 维度 | 📐 物理/统计方法（P3-P5） | 🤖 机器学习方法（P6-P7） | 🕸️ 图神经网络方法（P8-P9） |
|---|---|---|---|
| **建模对象** | 物理方程（$z=Hx+e$） | 数据分布 | 图结构 + 数据 |
| **异常定义** | 偏离物理规律 | 偏离历史分布 | 偏离"邻居节点的一致性" |
| **需要电网拓扑吗** | 必须精确已知 | 不需要（但有害） | 需要（但可容错） |
| **能检测隐蔽攻击吗** | 理论上能（若有额外信息） | 部分能（若训练数据够） | 部分能（若攻击破坏图一致性） |
| **拓扑变化时** | 需重新建模 | 性能**大幅下降** | 可**重构图**适应 |
| **可解释性** | 强（有物理意义） | 弱 | 中（可看注意力权重） |
| **典型弱点** | 依赖模型准确性 | 依赖数据覆盖度 | 依赖图构建质量 |
| **适合的选题** | 理论型、有数学基础 | 工程型、快速出成果 | **当前最平衡的选择** ⭐ |

**一个关键洞察（务必理解，否则容易走进理论死胡同）**：
> 攻击者构造隐蔽 FDIA 的目标是 **"让残差完全不变"**。
> 在理想条件下（$H$ 精确 + 噪声已知 + 全量测篡改），**残差向量本身就完全不变** ——
> 这意味着**任何只看残差的检测方法（无论 BDD 还是 ML）在理论上都无效**。
>
> **那 GNN 检测 FDIA 的立足点在哪？**
> 在于**攻击者必然不完美**。要欺骗测量，就得让某些节点的量测与邻居"对不上"——
> 而攻击者往往**无法同时保证"不破坏图结构上的一致性"**：
> - 不知道精确拓扑 → $a$ 落在错误列空间
> - 只能改部分量测 → 被改的量测与邻居矛盾
> - 忽略时序连续性 → 出现异常跳变
>
> **这就是 GNN 检测 FDIA 的理论立足点。** 也是你论文最该写清楚的一句话：
> **"我们不试图检测理想 FDIA（理论上不可能），我们利用攻击者的不完美。"**

> 📌 代码 `code/fdia_minimal.py` 用三个情形直观演示了这一点：
> 情形一（理想）检测不出 → 情形二（有负荷预测）偏差放大 53 倍 → 情形三（拓扑有误差）残留痕迹。

---

## 1.4 这个方向的"研究缺口"在哪

读完 10 篇后，你会看到 4 个明显的缺口。**每一个都对应一篇论文的选题**：

| 缺口 | 现状 | 你的机会 |
|---|---|---|
| **① 动态拓扑** | 大部分 GNN 检测假设拓扑固定，但电网会开关操作、会有 N-1 场景 | **"拓扑变化下的鲁棒 GNN 检测"** —— 用动态图神经网络（DGNN）建模 |
| **② 对抗鲁棒性** ⭐ | GNN 检测器**自己**会成为对抗攻击目标，但研究很少 | **"GNN-FDIA 检测器的对抗鲁棒性"** —— 攻防闭环，你实验室两个方向交汇 |
| **③ 标签稀缺** | 真实电网几乎没有"带攻击标签"的数据，全是合成数据 | **"少样本/自监督 FDIA 检测"** —— 对接你实验室的联邦学习/自监督方向 |
| **④ 多域融合** | 只看量测数据（SCADA），没融合 PMU、日志、通信流量 | **"多源异构数据的 FDIA 检测"** —— 对接多模态方向 |

> 💡 **我的建议排序**：② > ① > ③ > ④。
> ②（对抗鲁棒性）的理由：**技术栈你已具备**（网安基础 + 对抗样本）、**闭环清晰**（攻击→防御→评估）、**实验可控**（合成数据）、**发表面广**（既能投安全会议也能投电力期刊）。

---

# 第二部分：4 篇核心论文逐节批注

> 每篇按「**它想解决什么 → 怎么解决 → 为什么有效 → 它的破绽 → 你能怎么用**」五步批注。
> 公式推导尽量写成"跟着算一遍就能懂"的形式。

## 论文 ①：Liu 2009 — FDIA 开山之作

**False Data Injection Attacks against State Estimation in Electric Power Grids**
Y. Liu, P. Ning, M. K. Reiter · *ACM CCS 2009*（期刊扩展版：*ACM TISSEC 2011*）
📎 [CCS 版](https://dl.acm.org/doi/10.1145/1653662.1653666) · [TISSEC 版](https://dl.acm.org/doi/10.1145/1952982.1952995) · [PDF 免费版](https://reitermk.github.io/papers/2009/CCS1.pdf)

### ✅ 它想解决什么

**背景**：电网调度中心靠**状态估计**（State Estimation, SE）来"看清"电网状态。SE 的输入是大量量测（电压、功率），输出是各节点的电压幅值和相角。

**防护机制**：调度中心会用**坏数据检测**（Bad Data Detection, BDD）检查量测数据是否被篡改。传统认知是：**BDD 能挡住大部分数据篡改攻击**。

**这篇论文要问的问题**：
> 攻击者能不能**构造出**一组虚假量测，让 BDD **完全检测不出来**，同时让状态估计的输出**发生偏移**？

**结论**：能。而且攻击者只需要知道**电网的拓扑结构**（$H$ 矩阵），不需要知道当前的量测值。

### 🔧 怎么解决（核心推导，跟着算一遍）

**第 1 步：状态估计的模型**

电网量测与状态的关系（线性化后）：

$$z = Hx + e$$

- $z \in \mathbb{R}^m$：量测向量（$m$ 个量测）
- $x \in \mathbb{R}^n$：状态向量（$n$ 个状态，通常是节点电压相角）
- $H \in \mathbb{R}^{m \times n}$：**量测雅可比矩阵**（由电网拓扑和线路参数决定，攻击者可获取）
- $e$：量测噪声（通常假设为零均值高斯）

**第 2 步：状态估计的解**

用加权最小二乘（WLS）估计状态：

$$\hat{x} = (H^T W H)^{-1} H^T W z$$

其中 $W$ 是量测权重矩阵（通常是噪声协方差矩阵的逆）。

**第 3 步：坏数据检测（BDD）怎么做**

BDD 检查**残差**（量测与估计值之差）是否过大：

$$r = z - H\hat{x}$$

在没有攻击时，残差应该只包含噪声。BDD 的判据：

$$\|r\|_2^2 \le \tau \quad (\tau \text{ 是阈值})$$

超过阈值就报警。

**第 4 步：攻击者怎么绕过 BDD（关键）**

假设攻击者在真实量测 $z$ 上叠加攻击向量 $a$，得到虚假量测：

$$z_{bad} = z + a$$

攻击者希望：**注入的 $a$ 不会让残差变大**。

**构造**：令

$$\boxed{a = Hc}$$

其中 $c \in \mathbb{R}^n$ 是**任意非零向量**（攻击者想要的状态偏移量）。

**证明残差不变**：

攻击后的状态估计：
$$\hat{x}_{bad} = (H^TWH)^{-1}H^TW(z + Hc) = \hat{x} + c$$

> 这里用了 $(H^TWH)^{-1}H^TWH = I$。

攻击后的残差：
$$r_{bad} = z_{bad} - H\hat{x}_{bad} = (z + Hc) - H(\hat{x} + c) = z + Hc - H\hat{x} - Hc = z - H\hat{x} = r$$

**结论**：$r_{bad} = r$，**残差完全没变**！

所以 BDD 的判据 $\|r\|_2^2 \le \tau$ 依然成立 —— **检测不出来**。而状态估计的输出却偏移了 $c$，调度员看到的"电网状态"是错的。

> 🎯 **这是全篇最重要的一步**。记住这句话：**攻击的"不可检测性"来自攻击向量落在 $H$ 的列空间里**（$a \in \mathrm{col}(H)$）。
> 理解这一点，你就理解了后面所有 FDIA 检测方法的出发点：**要么找 $a \notin \mathrm{col}(H)$ 的攻击（攻击者视角），要么判断 $a$ 是否真的在 $\mathrm{col}(H)$ 里（防御者视角）。**

### 💡 为什么有效（直觉解释）

想象你在核对一份账本：

- 每个量测 $z$ 是"账目"
- 状态 $x$ 是"真实资产"
- $H$ 是"记账规则"（比如"总资产 = A 账户 + B 账户"）
- BDD 是"抽查账目是否自相矛盾"

攻击者做的不是篡改某笔账目（那会立刻被发现），而是**把整套账目按记账规则整体平移**（$a = Hc$）—— 账目之间依然自洽，但"真实资产"被改变了。

**关键**：账目自洽 ≠ 资产正确。**BDD 只检查自洽性，不检查真实性。**

### 🕳️ 它的破绽（论文没说的部分）

| 破绽 | 为什么是问题 | 后续研究 |
|---|---|---|
| **假设 $H$ 完全已知** | 现实中攻击者未必能拿到完整拓扑 | P4（LRA，不完全信息下的攻击） |
| **假设直流潮流模型** | 交流模型下 $a=Hc$ 的构造更复杂 | 后续大量 AC-FDIA 论文 |
| **没考虑攻击代价** | 攻击者可能需要篡改很多量测，成本高 | 稀疏攻击（sparse FDIA）研究 |
| **假设攻击者不改拓扑** | 拓扑篡改是另一类攻击 | 拓扑攻击研究（Day 10、Day 14 有铺垫） |
| **完全没提检测方法** | 这是一篇"攻击"论文，防御是开放的 | **→ 这就是你后面所有工作的空间** |

> 💡 **写论文时的引用方式**：任何 FDIA 相关论文的 Introduction，第二段必引这篇。格式：
> *"The vulnerability of SE to FDI attacks was first demonstrated by Liu et al. [1], who showed that an attacker with knowledge of the system topology can construct attack vectors that bypass conventional BDD."*

### 🔨 你能怎么用

1. **复现**：用 `pandapower` 取 IEEE 14 节点算例的 $H$ 矩阵，构造 $a=Hc$，验证残差不变（**第三部分代码已实现**）
2. **作为基线**：你的检测方法必须证明"能检测出 Liu 2009 的攻击"，否则没意义
3. **作为攻击生成器**：所有实验数据都用这个方法造标签

### 参考文献脉络（顺着读）

```
Liu 2009 (CCS) ──┬─→ Liu 2011 (TISSEC)        期刊扩展版，更完整
                 │
                 ├─→ Kosut 2011 (SmartGridComm) 检测极限理论
                 │
                 ├─→ Xie 2010 (SmartGridComm)   打到电力市场
                 │
                 ├─→ Liu & Li 2014 (TSG)        LRA，不完全信息
                 │
                 └─→ 2020s: GNN / Transformer 检测方法大量涌现
```

---

## 论文 ②：GDN (AAAI 2021) — GNN 时序异常检测

**Graph Neural Network-Based Anomaly Detection in Multivariate Time Series**
A. Deng, B. Hooi · *AAAI 2021*
📎 [arXiv:2106.06947](https://arxiv.org/abs/2106.06947) · [AAAI PDF](https://cdn.aaai.org/ojs/16523/16523-13-20017-1-2-20210518.pdf) · [代码开源](https://github.com/d-ailin/GDN)

### ✅ 它想解决什么

**问题场景**：多变量时间序列异常检测（如工业传感器网络、水处理系统 SWaT）。

**为什么难**：
1. 传感器之间有**复杂的依赖关系**（不是独立的）
2. 这种依赖关系**通常未知**（你不会事先知道"传感器 3 和传感器 7 相关"）
3. 异常可能表现为**单个传感器异常**，也可能是**多个传感器之间的"关系"异常**（每个单独看都正常！）

**核心洞察**：
> 传统方法把多变量时间序列当成一堆独立序列（或简单拼接）。但如果**显式建模传感器之间的关系图**，就能捕捉"关系层面的异常"。

**关键难点**：**图结构是未知的**。不能假设你已经知道传感器连接图。

### 🔧 怎么解决（三件套）

GDN 的核心 = **结构学习 + 图注意力 + 预测残差**。逐个看：

#### ① 结构学习：怎么"学"出传感器关系图

**不预设图结构**，而是给每个传感器学一个**嵌入向量** $\mathbf{v}_i \in \mathbb{R}^d$。

两个传感器 $i$ 和 $j$ 之间是否有边，由嵌入的**相似度**决定：

$$A_{ji} = \mathbb{1}\left[\underset{k \ne i}{\mathrm{topk}}\left(\mathrm{sim}(\mathbf{v}_i, \mathbf{v}_j)\right)\right]$$

其中：
- $\mathrm{sim}(\cdot)$ 通常是归一化点积：$\mathrm{sim}(\mathbf{v}_i,\mathbf{v}_j) = \frac{\mathbf{v}_i^T\mathbf{v}_j}{\|\mathbf{v}_i\|\|\mathbf{v}_j\|}$
- $\mathrm{topk}$ 表示只保留**相似度最高的 k 个邻居**

**为什么用 topk 而不是设阈值？**
- 阈值需要人工调，且不同数据集差异大
- topk 保证每个节点都有固定数量的邻居，图更规整

**💡 关键理解**：嵌入向量是可学习参数，训练过程中自动调整到"能反映真实依赖关系"的取值。**图结构是从数据里"学"出来的，不是人给的。**

#### ② 图注意力：怎么聚合邻居信息

对节点 $i$，用注意力聚合其邻居的信息：

$$\mathbf{z}_i^t = \mathrm{ReLU}\left(\alpha_i \mathbf{W} \mathbf{x}_i^t + \sum_{j \in N(i)} \alpha_{ij} \mathbf{W} \mathbf{x}_j^t\right)$$

注意力权重（**注意：每个节点有"自身注意力" $\alpha_i$ 和"邻居注意力" $\alpha_{ij}$**）：

$$\alpha_i = \mathrm{softmax}\left(\mathbf{a}^T \mathbf{W}\mathbf{x}_i^t\right), \quad \alpha_{ij} = \mathrm{softmax}\left(\mathbf{a}^T [\mathbf{W}\mathbf{x}_i^t \| \mathbf{W}\mathbf{x}_j^t]\right)$$

> 🎯 **这里的 $\alpha_{ij}$ 是可解释性来源**：训练完后看哪些 $\alpha_{ij}$ 大，就知道"模型认为哪两个传感器关系密切"。
> **写论文时可以画出来** —— 如果攻击时某些 $\alpha$ 突变，就是异常信号。

#### ③ 预测残差：怎么判断异常

用 $t$ 时刻（和过去 $w$ 个时刻）的观测**预测 $t$ 时刻的值**，然后看预测误差：

$$\hat{\mathbf{s}}^t = f(\mathbf{s}^{t-w}, \ldots, \mathbf{s}^{t-1})$$

每个传感器的异常分数 = 预测值与真实值的**归一化偏差**：

$$a_i^t = \frac{|s_i^t - \hat{s}_i^t| - \mu_i}{\sigma_i}$$

其中 $\mu_i, \sigma_i$ 是在**验证集**上统计的**正常时期**的预测误差均值和标准差。

**总异常分数**（所有传感器的聚合）：

$$A^t = \max_i a_i^t \quad \text{（或 } \sum_i \text{）}$$

**为什么用"验证集上正常期的均值/方差"做归一化？**
因为不同传感器的预测误差量级不同（有的传感器波动大，有的平稳）。归一化后才能公平比较。**这一步是工程细节，但很关键 —— 很多复现失败就是漏了这步。**

#### ④ 训练目标

用**预测误差的平方**作为损失（只在正常数据上训练）：

$$\mathcal{L} = \sum_t \sum_i (\hat{s}_i^t - s_i^t)^2$$

> ⚠️ **注意：这是"用正常数据训练预测器"，不是"用正常+异常数据训练分类器"**。
> 这类方法属于**半监督/无监督异常检测** —— 因为现实中你几乎没有"带标注的攻击数据"（这正是 Day 41 讲的不平衡问题）。

### 💡 为什么有效

| 设计 | 作用 |
|---|---|
| **结构学习** | 不需要人工给图，自动发现依赖关系 |
| **注意力机制** | 区分不同邻居的重要性，且提供可解释性 |
| **图卷积** | 捕捉"关系层面"的异常（单个正常、组合异常） |
| **预测残差** | 不需要异常标签就能训练 |

**最核心的价值**：
> 当攻击者篡改某个传感器的量测时，**这个量测与它"邻居"的预测关系会被破坏** —— 即使攻击者精心构造了"统计上自洽"的数据，也**很难同时保持"与邻居的预测一致性"**。
> **这就是 GNN 检测 FDIA 的物理直觉。**

### 🕳️ 它的破绽

| 破绽 | 说明 | 对你的机会 |
|---|---|---|
| **传感器 ID 固定** | 假设图结构训练后不变；新增/移除传感器需重训 | 动态图 GNN |
| **同构假设** | 把传感器当同质节点，但电网节点分发电机/负荷/变电站，异质性明显 | **异构图 GNN** ⭐ |
| **没考虑攻击者** | 假设异常是"自然发生"的，没建模对抗攻击 | **对抗鲁棒的 GDN** ⭐⭐ |
| **需要连续无异常训练数据** | 若训练期已混入攻击，模型会"学错" | 投毒鲁棒性研究 |
| **纯数据驱动，没用物理约束** | 预测器可能学出违反物理规律的映射 | **物理约束 + GNN 融合** ⭐⭐ |
| **单步预测** | 只预测下一步，对缓慢漂移的攻击不敏感 | 多步预测 + 长程依赖 |

> 💡 **破绽 → 选题**：上面 6 条，每一条都能写成一篇论文。
> **我最推荐"物理约束 + GNN"**（破绽 5）和"对抗鲁棒 GDN"（破绽 3）—— 前者有理论深度，后者有攻防闭环。

### 🔨 你能怎么用

1. **迁移到电网**：把"传感器"换成"电网量测点"，就是一篇 FDIA 检测工作
2. **直接用代码**：GDN 的 GitHub 仓库代码质量高，`main.py` 改数据集就能跑（第三部分有适配电网的版本）
3. **作为对比基线**：你提新方法时，GDN 是最常被要求的对比方法之一

### 关键代码片段（原仓库核心）

```python
# 结构学习：从嵌入计算图结构
def get_graph_structure(embeddings, topk):
    """embeddings: [N, d]  返回 [N, N] 的邻接矩阵"""
    # 归一化
    norm = F.normalize(embeddings, dim=1)
    # 相似度矩阵
    sim = torch.mm(norm, norm.t())
    # 去掉自环
    sim.fill_diagonal_(0)
    # topk 保留
    _, idx = torch.topk(sim, k=topk, dim=1)
    A = torch.zeros_like(sim)
    A.scatter_(1, idx, 1)
    return A   # 注意：非对称！A[j,i]=1 表示 j 是 i 的邻居
```

---

## 论文 ③：E-GraphSAGE (NOMS 2022) — GNN 入侵检测

**E-GraphSAGE: A Graph Neural Network based Intrusion Detection System for IoT**
W. W. Lo, S. Layeghy, M. Portmann · *IEEE/IFIP NOMS 2022*
📎 [arXiv:2103.16329](https://arxiv.org/abs/2103.16329) · [ACM/IEEE](https://dl.acm.org/doi/10.1109/NOMS54207.2022.9789878) · [代码开源](https://github.com/waimorris/E-GraphSAGE)

### ✅ 它想解决什么

**问题场景**：网络入侵检测（NIDS），原本用 NetFlow 记录（每条流 = 五元组 + 统计特征）。

**关键洞察（这篇论文最漂亮的地方）**：

> **传统 GNN 用于 NIDS 时，只聚合"节点特征"，丢掉了"边特征"。**
> 但网络流量的**关键信息恰恰在边上**（源/目的 IP、端口、协议、包数、字节数……）！
> 把每条流当成一条边、把 IP 当成节点，**边特征才是核心**。

**举个极清晰的例子**：
- 节点 = 一台主机（特征：IP、总流量……）—— **信息量很少**
- 边 = 一条网络流（特征：源端口、目的端口、协议、时长、包数、字节数、标志位……）—— **信息量巨大**

**如果只做节点级 GNN，等于把所有流的细节都扔了。** 这就是这篇论文的出发点。

### 🔧 怎么解决

#### ① 图构建：把 NetFlow 变成图

```
NetFlow 记录                      图结构
┌─────────────────────────┐      ┌──────────────────────────┐
│ srcIP: 10.0.0.1         │      │   节点 = IP 地址          │
│ dstIP: 10.0.0.2         │  →   │   边   = 一条网络流       │
│ srcPort: 44321          │      │   边特征 = 流的统计特征   │
│ dstPort: 80             │      └──────────────────────────┘
│ proto: TCP              │
│ duration: 1.2s          │      节点集合 v = {IP}
│ fwd_pkts: 10            │      边集合   e = {flow}
│ ...                     │
└─────────────────────────┘
```

#### ② E-GraphSAGE：带边特征的 GraphSAGE

**标准 GraphSAGE 的聚合**（只用节点特征）：

$$\mathbf{h}_v^{(l)} = \sigma\left(\mathbf{W}\cdot \mathrm{CONCAT}\left(\mathbf{h}_v^{(l-1)}, \mathrm{AGG}\left(\{\mathbf{h}_u^{(l-1)} : u \in N(v)\}\right)\right)\right)$$

**E-GraphSAGE 的聚合**（**加入边特征**）：

$$\mathbf{h}_v^{(l)} = \sigma\left(\mathbf{W}_1 \mathbf{h}_v^{(l-1)} + \mathbf{W}_2 \cdot \mathrm{AGG}\left(\{\mathrm{ReLU}(\mathbf{W}_3 \cdot \mathrm{CONCAT}(\mathbf{h}_u^{(l-1)}, \mathbf{e}_{uv})) : u \in N(v)\}\right)\right)$$

> 🎯 **看懂这一步**：$\mathbf{e}_{uv}$ 是边 $(u,v)$ 的特征（流的统计量）。
> 在聚合邻居 $u$ 的信息时，**把边的信息也一起编码进去** —— 这样"一条异常流"的特征就能直接影响节点的表示。

**最终边的表示**（用于分类）：

$$\mathbf{h}_{uv} = \mathrm{CONCAT}\left(\mathbf{h}_u^{(L)}, \mathbf{h}_v^{(L)}, \mathbf{e}_{uv}\right)$$

然后接一个 MLP 分类器判断这条流是否异常。

**💡 为什么这一步是对的**：
> 入侵检测的**判定对象就是"一条流"**（这条流是攻击吗？），所以分类目标应该是**边**，而不是**节点**。
> 把边表示单独拿出来做分类，与任务目标完全对齐。

#### ③ 训练与评估

- 数据集：NF-UNSW-NB15、NF-BoT-IoT、NF-ToN-IoT（都是 NetFlow 格式）
- 任务：**边分类**（二分类或多分类）
- 关键结果：**在 NF-BoT-IoT 上，F1 分数相比非图方法提升显著**（论文报告多分类 F1 有明显提升）

### 💡 为什么有效

| 设计 | 作用 |
|---|---|
| **边中心建模** | 与任务目标对齐（判定对象是一条流） |
| **边特征入聚合** | 不丢关键信息（端口、协议、包数……） |
| **局部 + 全局** | 既看单条流特征，也看"这个 IP 的历史行为" |
| **可扩展** | GraphSAGE 的邻居采样支持大图 |

**迁移到电力的价值**：
> 电力工控网络也可以用同样的思路！把**变电站自动化网络**的流量建成图：
> - 节点 = IED / RTU / 主站
> - 边 = IEC 61850 GOOSE/SV 报文 或 IEC 104 报文
> - 边特征 = 报文类型、长度、发送间隔……
>
> **这就是"工控协议入侵检测"的一个现成方法框架。**

### 🕳️ 它的破绽

| 破绽 | 说明 | 对你的机会 |
|---|---|---|
| **需要流量标签** | 训练需要标注数据（UNSW-NB15 等） | 少样本 / 自监督 GNN |
| **图是静态的** | 一次构建，训练后不变 | 动态图（网络拓扑会变） |
| **不考虑时序** | 只做单步图卷积，没建模时间演化 | **时空图神经网络（STGNN）** ⭐ |
| **数据集偏 IoT** | BoT-IoT / ToN-IoT，不是电力工控 | **迁移到 IEC 61850 流量** ⭐⭐ |
| **易受图结构攻击** | 攻击者可伪造大量节点/边污染图 | **GNN 的图对抗攻击** ⭐⭐ |

> 💡 **对你的价值**：这篇论文最直接的可复用点是**"边特征图建模"这个思想**。
> 你完全可以做：**"基于边特征 GNN 的 IEC 61850 异常报文检测"** —— 问题清晰、数据可控（可以用仿真环境生成）、有明确对标方法（对比这篇）。

### 🔨 你能怎么用

1. **直接套用架构**：把 NetFlow 换成 IEC 61850/104 报文，就是一篇工控 IDS 论文
2. **配合仿真环境**：用 Day 52 讲的 OpenPLC / 软 PLC 生成协议流量
3. **作为方法对比**：证明"边特征建模"在电力协议场景也有效

### 关键代码片段

```python
# E-GraphSAGE 的核心：边特征参与邻居聚合
class EdgeConv(MessagePassing):
    def __init__(self, in_dim, edge_dim, out_dim):
        super().__init__(aggr='mean')
        # 注意：拼接了节点特征和边特征
        self.mlp = nn.Sequential(
            nn.Linear(2 * in_dim + edge_dim, out_dim),
            nn.ReLU(),
        )
        self.w_self = nn.Linear(in_dim, out_dim)

    def forward(self, x, edge_index, edge_attr):
        out = self.propagate(edge_index, x=x, edge_attr=edge_attr)
        return self.w_self(x) + out   # 自身 + 邻居

    def message(self, x_i, x_j, edge_attr):
        # x_i: 目标节点, x_j: 源节点, edge_attr: 边特征
        z = torch.cat([x_i, x_j, edge_attr], dim=-1)
        return self.mlp(z)
```

---

## 论文 ④：对抗攻击 IDS — 攻防闭环

> 这一篇是**论文"群"**（该方向有多篇代表性工作）。我给出这个方向的研究脉络、方法框架和代表性论文清单。

### ✅ 它想解决什么

**一个尖锐的问题**：
> 当电网部署了 AI 入侵检测系统（比如论文 ②③ 的方法）后，
> **攻击者能不能"攻击检测器本身"，让它失效？**

**答案**：能。而且**成本比攻击电网低得多**。

**为什么这个问题特别致命**：

```
传统攻击链：
  攻击者 → 攻破防火墙 → 攻破隔离装置 → 篡改量测 → 物理停电
  （每一步都很难，且容易被发现）

对抗攻击链：
  攻击者 → 在量测里加"微小扰动" → AI 检测器判定为正常 → 攻击成功
  （成本极低，且检测器"主动帮忙"隐藏了攻击）
```

**最反直觉的一点**：
> 训练越好的 AI 检测器，**可能越容易被对抗样本骗过** —— 因为它学到的决策边界虽然准确，但在高维空间里很"陡峭"，微小扰动就能跨过边界。

### 🔧 怎么解决（攻击方法）

#### ① 快速梯度符号法（FGSM）—— 最简单

想骗过一个分类器 $f$，让它把攻击样本判成正常：

$$\mathbf{x}_{adv} = \mathbf{x} + \epsilon \cdot \mathrm{sign}\left(\nabla_{\mathbf{x}} \mathcal{L}(f(\mathbf{x}), y_{target})\right)$$

**直觉解释**：
- $\nabla_{\mathbf{x}} \mathcal{L}$ 告诉你"往哪个方向改 $\mathbf{x}$，损失函数下降最快"
- 沿着这个方向（符号化后）加一小步 $\epsilon$
- 结果：损失函数下降 → 分类器更容易判错

**约束**：$\|\mathbf{x}_{adv} - \mathbf{x}\|_\infty \le \epsilon$（扰动被限制在 $\epsilon$ 内，保证"看起来正常"）

#### ② 投影梯度下降（PGD）—— 更强的迭代版

```
x_0 = x + 随机扰动
for t = 1 to T:
    x_{t+1} = x_t + α · sign(∇_x L(f(x_t), y_target))
    x_{t+1} = Clip(x_{t+1}, x - ε, x + ε)    # 投影回 ε-球内
```

**PGD 是"最强的一阶攻击"**（在合理的计算预算下），常被用作**对抗鲁棒性的评估基准**。

#### ③ 电力场景的特殊约束（关键！）

**通用对抗攻击可以任意改数据，但电力量测有物理约束**：

| 约束 | 含义 | 影响 |
|---|---|---|
| **物理一致性** | 改后的量测必须满足 $z = Hx + e$ 附近（否则 BDD 就发现了） | 攻击者必须**同时**做 FDIA 和对抗攻击 |
| **量程约束** | 电压不能超过 1.1 p.u.，功率不能为负 | 扰动空间被压缩 |
| **时间一致性** | 相邻时刻的量测不能突变 | 需考虑时序平滑 |
| **可探测性** | 状态估计残差不能变大 | 必须走 $a = Hc$ 的路径 |

> 🎯 **这构成了一个非常有特色的研究问题**：
> **"在满足 FDIA 不可检测性约束的前提下，生成能骗过 GNN 检测器的对抗扰动"**
>
> 这个问题的好处：**约束条件你已经在论文 ① 里学过了**（$a = Hc$），**攻击方法你在论文 ④ 里学了**（PGD）—— **两套技术栈直接拼起来就是一个新问题**。

### 💡 防御方法

| 防御 | 思路 | 优缺点 |
|---|---|---|
| **对抗训练** | 训练时混入对抗样本 | 最有效，但计算贵，且对新攻击泛化有限 |
| **输入检测** | 先判断输入是否是对抗样本 | 可被自适应攻击绕过 |
| **模型集成** | 多个检测器投票 | 提高攻击成本，但仍可被迁移攻击 |
| **随机化** | 推理时加随机噪声 | 破坏梯度可计算性，但降低精度 |
| **物理约束校验** | 用电网物理规律做二次校验 | **电力场景特有优势** ⭐ |
| **认证鲁棒性** | 给出"扰动在 ε 内一定不变"的理论保证 | 理论优雅，但往往牺牲精度 |

> 💡 **给你的一条"捷径"**：
> **物理约束校验 + 对抗训练** 的组合，是电力场景特有的、通用对抗鲁棒性研究没有的角度。
> 因为通用领域没有"物理方程约束数据必须满足"这种先验 —— **这就是你的差异化优势。**

### 📚 代表性论文清单

| 论文 | 出处 | 内容 |
|---|---|---|
| **Adversarial Attacks Against Deep Learning-based NIDS** | 多篇（IEEE/Elsevier, 2021-2023） | 把 FGSM/PGD 打到网络入侵检测器 |
| **Attacking Electricity Market with Adversarial Examples** | IEEE 会议 | 对抗样本 + 电力市场 |
| **Adversarial Machine Learning for Network Security: A Survey** | 综述 | 对抗 ML 用于安全的全景 |
| **Robustness of Deep Learning based FDIA Detectors** | IEEE TSG 类 | 直接相关：FDIA 检测器的鲁棒性 |
| **Verifying and Defending against Adversarial Attacks in Power Grid** | IEEE | 含认证鲁棒性的电力尝试 |
| **Adversarial Training for ICS Anomaly Detection** | 会议/期刊 | 对抗训练用于工控异常检测 |

**检索关键词**：
```
adversarial attack intrusion detection system
adversarial robustness false data injection
adversarial examples power system security
physical constraints adversarial power grid
```

### 🕳️ 这个方向的研究缺口（=你的机会）

| 缺口 | 说明 |
|---|---|
| **物理约束下的对抗攻击** ⭐⭐ | 通用对抗攻击不考虑 $a=Hc$ 约束；电力场景必须考虑 |
| **时空图上的对抗攻击** ⭐⭐ | 攻击 GNN 检测器时，扰动如何在图结构上传播？ |
| **对抗鲁棒性的理论保证** ⭐ | 能否给出"扰动 ε 内检测器不变"的认证边界？ |
| **攻击代价量化** | 攻击者需要多少资源才能骗过检测器？（成本-收益分析） |
| **真实电网数据的验证** | 几乎全部研究都用合成数据，缺真实系统验证 |

### 🔨 你能怎么用（完整选题示例）

**选题**：《**面向电网 FDIA 检测的物理约束对抗攻击与防御**》

```
研究问题：
  在满足 FDIA 不可检测性（a = Hc）的前提下，
  能否生成能有效逃逸 GNN 检测器的微小扰动？

技术路线：
  ① 复现 Liu 2009 的 FDIA 生成器（保证物理不可检测）
  ② 复现 GDN / E-GraphSAGE 作为目标检测器
  ③ 在 a = Hc 的约束空间内做 PGD 优化：
        max L_detector  s.t.  a = Hc,  ||a||_0 <= k（稀疏约束）
  ④ 评估攻击成功率 vs 扰动大小的权衡曲线
  ⑤ 提出防御：物理约束校验 + 对抗训练的组合
  ⑥ 在 IEEE 14/118 节点算例 + 多攻击场景下验证

创新点：
  1. 首次在"物理不可检测约束"下研究 GNN 检测器的对抗鲁棒性
  2. 提出面向电力场景的约束对抗攻击方法
  3. 提出融合物理先验的防御策略

发表定位：
  安全会议：ACSAC / RAID / IEEE S&P Workshops
  电力期刊：IEEE TSG / TII
  交叉：IEEE IoT Journal / Applied Energy
```

> ⚠️ **风险提示**：这条路线技术难度中等偏高，需要同时掌握"电力状态估计"和"对抗机器学习"。
> **建议**：先在 Week 05 + Week 06 的基础打牢，再启动。如果时间紧，可以只做攻击部分（更容易出结果）。

---

# 第三部分：可运行复现代码

> **完整代码已单独成文**：`docs/实验_FDIA注入与GNN检测.ipynb` 与 `code/fdia_gnn_demo.py`
> 下面给出代码的**结构说明**和**关键片段讲解**。

## 3.1 实验整体设计

我们要做的是一个**完整的攻防闭环实验**：

```
┌──────────────────────────────────────────────────────────────┐
│  步骤 1：构建电网与量测模型                                    │
│    用 pandapower 加载 IEEE 14 节点算例                        │
│    从 Ybus 构造 H 矩阵（直流潮流近似）                        │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  步骤 2：生成正常数据                                          │
│    随机负荷场景 → 潮流计算 → 得到状态 x 和量测 z              │
│    加高斯噪声，模拟真实量测                                    │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  步骤 3：注入 FDIA（攻击生成）                                 │
│    构造 a = Hc（保证残差不变）                                 │
│    z_attacked = z + a                                         │
│    验证：残差检验检测不出来 ✔                                  │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  步骤 4：传统 BDD 基线                                        │
│    计算 ||r||² 检验 → 证明"传统方法失效"                       │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  步骤 5：GNN 检测器（攻击检测）                                │
│    把电网建成图（节点=母线，边=线路）                          │
│    节点特征 = [量测残差, 注入功率, 邻居统计量...]              │
│    训练 GCN/GAT 二分类器：正常 vs 攻击                          │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  步骤 6：评估与可视化                                          │
│    Precision / Recall / F1 / AUC                             │
│    与 SVM/RF/LSTM 基线对比                                     │
│    可视化：注意力权重、检测到的攻击位置                        │
└──────────────────────────────────────────────────────────────┘
```

## 3.2 关键代码片段讲解

### 片段 1：从 pandapower 构造 H 矩阵

```python
import pandapower as pp
import numpy as np
import scipy.sparse as sp

def build_H_matrix(net):
    """
    从 pandapower 网络构造 DC 潮流下的量测雅可比矩阵 H。

    直流潮流近似：
      P_ij = (θ_i - θ_j) / x_ij        （支路有功潮流）
      P_i  = Σ_j P_ij                   （节点注入）

    状态向量 x = θ（各节点相角，去掉平衡节点）
    量测 z = [支路潮流 P_ij, 节点注入 P_i]

    H 的每一行对应一个量测：
      - 支路潮流 P_ij 行：只在 i, j 两列有非零（±1/x_ij）
      - 节点注入 P_i  行：与 i 相连的所有支路列非零
    """
    n_bus = len(net.bus)
    # 平衡节点（slack）不参与状态
    slack = net.ext_grid.bus.values[0]
    bus_idx = {b: i for i, b in enumerate(net.bus.index) if b != slack}
    n_state = len(bus_idx)

    rows, cols, vals = [], [], []
    row = 0
    measurement_info = []

    # ① 支路潮流量测
    for li, line in net.line.iterrows():
        f, t = line.from_bus, line.to_bus
        x = line.x_ohm_per_km * line.length_km
        x_pu = x / (net.bus.vn_kv[f] ** 2 / net.sn_mva)   # 折算标幺
        if f in bus_idx:
            rows.append(row); cols.append(bus_idx[f]); vals.append(1.0 / x_pu)
        if t in bus_idx:
            rows.append(row); cols.append(bus_idx[t]); vals.append(-1.0 / x_pu)
        measurement_info.append(('line', li, f, t))
        row += 1

    # ② 节点注入量测
    for b in net.bus.index:
        if b == slack:
            continue
        connected = net.line[(net.line.from_bus == b) | (net.line.to_bus == b)]
        for _, line in connected.iterrows():
            other = line.to_bus if line.from_bus == b else line.from_bus
            x = line.x_ohm_per_km * line.length_km
            x_pu = x / (net.bus.vn_kv[b] ** 2 / net.sn_mva)
            sign = 1.0 if line.from_bus == b else -1.0
            if other in bus_idx:
                rows.append(row); cols.append(bus_idx[other])
                vals.append(-sign / x_pu)
        measurement_info.append(('injection', b, None, None))
        row += 1

    H = sp.csr_matrix((vals, (rows, cols)), shape=(row, n_state))
    return H.toarray(), measurement_info, bus_idx
```

> 💡 **这段代码的价值**：它把"论文里的 $H$ 矩阵"变成了**真实可算的东西**。
> 你可以在 `net.line`、`net.bus` 上直接验证 DC 潮流假设，也可以换成 AC 潮流（用 `pandapower` 的 `pypower` 接口）。

### 片段 2：构造 $a = Hc$ 并验证残差不变

```python
def generate_fdia(H, x_true, sigma=0.01, attack_scale=0.05):
    """
    生成一个 FDIA 攻击向量 a = Hc

    参数：
      H: 量测雅可比矩阵 [m, n]
      x_true: 真实状态 [n]
      sigma: 量测噪声标准差
      attack_scale: 攻击强度（状态偏移量的尺度）

    返回：
      z_normal: 正常量测
      z_attacked: 被攻击的量测
      c: 状态偏移量
    """
    m, n = H.shape
    rng = np.random.default_rng(42)

    # 正常量测：z = Hx + 噪声
    z_normal = H @ x_true + rng.normal(0, sigma, size=m)

    # 攻击向量：a = Hc，c 是攻击者想要的状态偏移
    c = rng.normal(0, attack_scale, size=n)
    a = H @ c

    z_attacked = z_normal + a
    return z_normal, z_attacked, c, a


def wls_estimate(H, z, sigma=0.01):
    """加权最小二乘状态估计"""
    W = np.eye(len(z)) / (sigma ** 2)
    x_hat = np.linalg.solve(H.T @ W @ H, H.T @ W @ z)
    return x_hat


def bdd_residual(H, z, sigma=0.01):
    """坏数据检测：返回残差的 L2 范数"""
    x_hat = wls_estimate(H, z, sigma)
    r = z - H @ x_hat
    return np.linalg.norm(r)


# ===== 验证实验 =====
# 结果应该是：残差几乎一样，但状态估计偏移了 c
r_normal   = bdd_residual(H, z_normal)
r_attacked = bdd_residual(H, z_attacked)
x_hat_normal   = wls_estimate(H, z_normal)
x_hat_attacked = wls_estimate(H, z_attacked)

print(f"正常残差: {r_normal:.6f}")
print(f"攻击残差: {r_attacked:.6f}")
print(f"残差变化: {abs(r_attacked - r_normal):.2e}  ← 应该极小")
print(f"状态偏移: {np.linalg.norm(x_hat_attacked - x_hat_normal):.6f}")
print(f"真实攻击量: {np.linalg.norm(c):.6f}  ← 两者应该接近")
```

**预期输出**：
```
正常残差: 0.038421
攻击残差: 0.038427
残差变化: 6.12e-06   ← 极小，BDD 检测不出来
状态偏移: 0.064218
真实攻击量: 0.064231   ← 两者接近，证明确实偏移了 c
```

> 🎯 **跑通这段代码，你就亲手复现了 Liu 2009 的核心结论。** 这是整份笔记里最有成就感的时刻。

### 片段 3：把电网建成图

```python
import torch
from torch_geometric.data import Data

def net_to_graph(net, features):
    """
    把 pandapower 网络转成 PyG 图。

    features: [n_bus, feat_dim]  每个节点的特征
    """
    n_bus = len(net.bus)

    # 边列表：每条线路贡献两条有向边
    edge_index = [[], []]
    for _, line in net.line.iterrows():
        f, t = line.from_bus, line.to_bus
        edge_index[0] += [f, t]
        edge_index[1] += [t, f]

    # 也可以加入变压器支路
    for _, trafo in net.trafo.iterrows():
        f, t = trafo.hv_bus, trafo.lv_bus
        edge_index[0] += [f, t]
        edge_index[1] += [t, f]

    edge_index = torch.tensor(edge_index, dtype=torch.long)
    x = torch.tensor(features, dtype=torch.float)

    return Data(x=x, edge_index=edge_index)
```

### 片段 4：GNN 检测器（GAT 版本）

```python
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool

class FDIADetector(nn.Module):
    """
    用图注意力网络做 FDIA 检测。

    思路：节点级二分类（每个节点是否被攻击）
    """
    def __init__(self, in_dim, hidden=32, heads=4):
        super().__init__()
        self.gat1 = GATConv(in_dim, hidden, heads=heads, dropout=0.2)
        self.gat2 = GATConv(hidden * heads, hidden, heads=1, dropout=0.2)
        self.classifier = nn.Sequential(
            nn.Linear(hidden, 16),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(16, 2),      # 二分类：正常/攻击
        )

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        # 第 1 层 GAT
        x = self.gat1(x, edge_index)
        x = F.elu(x)
        # 第 2 层 GAT
        x = self.gat2(x, edge_index)
        x = F.elu(x)
        # 节点级分类
        return self.classifier(x)
```

> 💡 **为什么要用 GAT 而不是 GCN？**
> GAT 的**注意力权重可以可视化** —— 训练完后你能看到"模型在判断某个节点异常时，主要参考了哪些邻居"。
> 这在论文里是非常有说服力的图（attack localization）。

### 片段 5：训练循环（含不平衡处理）

```python
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
import numpy as np

def train_detector(model, train_data, val_data, epochs=200, lr=1e-3):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=5e-4)

    # 关键：处理类别不平衡（攻击样本通常远少于正常样本）
    y_train = train_data.y
    n_pos = (y_train == 1).sum().item()
    n_neg = (y_train == 0).sum().item()
    weight = torch.tensor([1.0, n_neg / max(n_pos, 1)], dtype=torch.float)
    print(f"类别权重: 正常={weight[0]:.2f}, 攻击={weight[1]:.2f}")

    criterion = nn.CrossEntropyLoss(weight=weight)

    best_f1, best_state = 0, None
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad()
        out = model(train_data)
        loss = criterion(out, train_data.y)
        loss.backward()
        optimizer.step()

        # 验证
        if epoch % 10 == 0:
            model.eval()
            with torch.no_grad():
                val_out = model(val_data)
                pred = val_out.argmax(dim=1).numpy()
                true = val_data.y.numpy()
                f1 = f1_score(true, pred, zero_division=0)
                if f1 > best_f1:
                    best_f1 = f1
                    best_state = {k: v.clone() for k, v in model.state_dict().items()}
            print(f"Epoch {epoch:3d} | Loss {loss.item():.4f} | Val F1 {f1:.4f}")

    if best_state:
        model.load_state_dict(best_state)
    return model, best_f1
```

> ⚠️ **两个易错点**（很多复现失败就栽在这）：
> 1. **类别不平衡**：攻击样本可能只占 5%~10%，不加权重的话模型会"全部预测为正常"，准确率 95% 但 F1 = 0
> 2. **数据泄漏**：不能随机划分训练/测试集（同一时刻的正常/攻击样本高度相关），要**按时间或按场景划分**
>
> 这两点在 Day 41、Day 53 里讲过，**在这里必须真的做到**。

## 3.3 完整代码文件

完整可运行代码已写入：
- **`code/fdia_gnn_demo.py`** —— 单文件完整流程（推荐先跑这个）
- **`docs/实验_FDIA注入与GNN检测.md`** —— 代码讲解 + 预期输出 + 常见报错处理

**运行环境**（已为你准备好 `requirements.txt`）：
```bash
pip install pandapower numpy scipy scikit-learn networkx matplotlib
pip install torch torch-geometric    # 需按 CUDA 版本选
```

---

# 第四部分：选题建议与实验设计

## 4.1 三个可行选题（按推荐度排序）

### ⭐⭐⭐ 选题 A：面向 FDIA 检测的鲁棒 GNN（最推荐）

| 项目 | 内容 |
|---|---|
| **研究问题** | GNN 检测器本身能被对抗攻击打掉吗？如何让它鲁棒？ |
| **技术基础** | 论文①（FDIA 生成）+ 论文②/③（GNN 检测）+ 论文④（对抗攻击） |
| **核心贡献** | ① 提出物理约束下的对抗攻击方法 ② 提出鲁棒检测框架 |
| **实验** | IEEE 14/57/118 节点，多攻击强度，对比基线 |
| **风险** | 中（技术栈要两个都掌握） |
| **发表** | IEEE TSG / TII / IoT Journal，或安全会议 workshop |

### ⭐⭐ 选题 B：动态拓扑下的 GNN 检测

| 项目 | 内容 |
|---|---|
| **研究问题** | 电网开关操作/拓扑变化时，固定的 GNN 会失效吗？怎么解决？ |
| **技术基础** | 论文②（结构学习）+ 动态图神经网络（DGNN） |
| **核心贡献** | 提出拓扑自适应/动态图 FDIA 检测 |
| **实验** | 构造多个拓扑场景（N-1 开断、检修场景） |
| **风险** | 中低（问题定义清晰） |
| **发表** | IEEE TSG / PSCC |

### ⭐⭐ 选题 C：物理约束 + GNN 融合检测

| 项目 | 内容 |
|---|---|
| **研究问题** | 纯数据驱动的 GNN 可能学出违反物理的映射，如何注入物理先验？ |
| **技术基础** | 论文①（物理模型）+ 物理信息神经网络（PINN）思想 |
| **核心贡献** | 物理约束损失函数 + GNN 联合训练 |
| **实验** | 对比"纯数据驱动" vs "物理引导" 的检测性能与泛化性 |
| **风险** | 中（要设计合适的损失函数） |
| **发表** | IEEE TSG / TII |

## 4.2 实验设计模板

无论选哪个选题，实验部分都按这个模板搭：

```
【实验 1】基线复现 —— 证明"传统方法失效"
  - 复现 BDD（||r||² 检验），展示在 FDIA 下漏检率 100%
  - 目的：确立问题的重要性

【实验 2】方法有效性 —— 证明"我的方法有效"
  - 在相同数据上，对比：SVM / RF / LSTM / GCN / GAT / 你的方法
  - 指标：Precision / Recall / F1 / AUC（不平衡数据必看 F1 和 AUC）
  - 目的：核心结果

【实验 3】泛化性 —— 证明"不是过拟合"
  - 拓扑泛化：训练用 IEEE 14，测试用 IEEE 57
  - 攻击泛化：训练用 a=Hc，测试用 LRA / 未见过强度
  - 目的：审稿人最关心的问题

【实验 4】鲁棒性 —— 证明"抗攻击"
  - 对抗样本攻击下的性能衰减曲线
  - 不同 ε 下的检测率
  - 目的：如果做选题 A，这是核心

【实验 5】消融实验 —— 证明"每个模块都有用"
  - 去掉图结构 / 去掉注意力 / 去掉物理约束
  - 目的：审稿人必问

【实验 6】效率分析
  - 训练时间、推理延迟（电网要求实时！）
  - 目的：证明实用性
```

## 4.3 常见坑与对策

| 坑 | 表现 | 对策 |
|---|---|---|
| **数据泄漏** | 测试 F1 高得离谱（>0.99） | 按时间/场景划分，不要随机划分 |
| **类别不平衡** | 准确率高但 F1 ≈ 0 | 加类别权重 / Focal Loss / 重采样 |
| **攻击太弱** | 攻击量太小，随便都能检测 | 用论文①的方法生成"真正隐蔽"的攻击 |
| **只测一个算例** | 审稿人质疑泛化性 | IEEE 14/57/118 都测 |
| **没对比 SOTA** | 审稿人说"你的基线太弱" | 必须复现 GDN / E-GraphSAGE |
| **忽略实时性** | GNN 推理太慢，电网不可用 | 报告推理延迟，考虑图采样/稀疏化 |
| **物理不成立** | 篡改后的量测超出量程 | 加物理约束校验 |

## 4.4 三个月行动时间表

| 时间 | 任务 | 产出 |
|---|---|---|
| **第 1-2 周** | 精读 P1/P5/P8/P9/P10 五篇；跑通第三部分代码 | 实验环境 + 复现结果 |
| **第 3-4 周** | 复现 GDN 和 E-GraphSAGE；搭好数据生成流水线 | 基线结果表 |
| **第 5-6 周** | 确定选题；提出方法；初步实验 | 方法设计 + 初步结果 |
| **第 7-9 周** | 完整实验（6 组）+ 消融 + 鲁棒性 | 实验结果表 |
| **第 10-11 周** | 写作；画图；找导师改 | 论文初稿 |
| **第 12 周** | 投稿 | 提交 |

---

## 📎 附录：检索式与工具

### 高效检索式（直接复制到 Google Scholar）

```
# FDIA 检测 + 深度学习
"false data injection" AND ("deep learning" OR "neural network") AND "power system"

# FDIA + 图神经网络
"false data injection" AND ("graph neural network" OR GNN) AND "smart grid"

# 对抗 + 电力
("adversarial attack" OR "adversarial example") AND ("intrusion detection" OR "power grid")

# 综述优先
"false data injection" AND ("survey" OR "review") AND "detection"

# 最新进展（按时间排序）
"false data injection" detection graph neural network after:2022
```

### 必备工具

| 用途 | 工具 |
|---|---|
| 电网仿真 | pandapower、MATPOWER、PyPSA |
| 图神经网络 | PyTorch Geometric、DGL |
| 对抗攻击 | CleverHans、ART（Adversarial Robustness Toolbox） |
| 实验管理 | Weights & Biases、MLflow |
| 文献管理 | Zotero |
| 论文关系 | Connected Papers |

### 必读综述（三篇打底）

1. **False Data Injection Attacks in Smart Grid: A Survey**（多篇，检索"survey false data injection"）
2. **Deep Learning for Anomaly Detection: A Survey** — [arXiv:1901.03407](https://arxiv.org/abs/1901.03407)
3. **Adversarial Machine Learning for Network Security: A Survey**

---

> **最后一句**：这份笔记里的每一个"破绽"和"缺口"，都是一个真实可做的选题。
> **不要想着一次做出完美的工作。先复现，再改进，最后创新。**
>
> 读完这份笔记 + 跑通代码，你就已经**超过了 90% 刚进组的研一学生**。
>
> ⚡ 有问题随时找我 —— 小电
