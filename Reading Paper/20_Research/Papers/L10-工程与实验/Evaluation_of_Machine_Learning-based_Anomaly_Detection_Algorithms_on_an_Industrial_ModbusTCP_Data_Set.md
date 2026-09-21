---
document_id: "arxiv-1905.11757"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/1905.11757"
arxiv_id: "1905.11757"
title: "Evaluation of Machine Learning-based Anomaly Detection Algorithms on an Industrial Modbus/TCP Data Set"
authors: ["Simon Duque Anton", "Suneetha Kanoor", "Daniel Fraunholz", "Hans Dieter Schotten"]
published: "2019-05-28"
venue: "arXiv preprint"
domain: "L10-工程与实验"
level: "L10"
reading_order: 99
difficulty: "入门"
lang: "en"
tags: ["电网安全", "L10-工程与实验", "Modbus", "异常检测", "数据集"]
quality_score: 8
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 099 | 在工业 Modbus/TCP 数据集上评估基于机器学习的异常检测算法

> [!abstract] 一句话
> 在一个**合成生成的（synthetic）** Modbus/TCP 通信数据集上跑四种机器学习算法做异常检测，结论是 SVM 和 k-NN 表现较好，k-means 聚类不理想——**注意：这个数据集是合成的，不是真实工控网络抓包**。

## 为什么读它

这是 L10 专题里**最"轻量"的一篇**——没有测试床、没有硬件、没有真实攻击，就是**在一个数据集上跑算法做对比**。

**它的价值恰恰在于简单**：如果你现在就想动手做点实验，这是**门槛最低的起点**。你不需要买 PLC、不需要搭物理过程，下载数据、跑四个 sklearn 模型、写个对比表，就是一篇论文的骨架。

但它也是一篇**需要带着批判眼光读的论文**，因为它暴露了工控 ML 检测研究里的几个典型问题：**合成数据、任务过于简单、结论表述有矛盾**。**读懂它的局限，比读懂它的方法更有价值**——这些局限正是你可以改进的地方。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | Evaluation of Machine Learning-based Anomaly Detection Algorithms on an Industrial Modbus/TCP Data Set |
| 作者 | Simon Duque Anton, Suneetha Kanoor, Daniel Fraunholz, Hans Dieter Schotten |
| 发表 | arXiv preprint, 2019-05-28 |
| 链接 | [arXiv](https://arxiv.org/abs/1905.11757) |
| 类型 | arXiv 预印本 |
| 难度 | 入门 |
| 关键词 | Modbus/TCP、工业物联网、异常检测、机器学习、合成数据集 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[1905.11757_fig1.png]]

![[1905.11757_fig2.png]]

![[1905.11757_fig3.png]]

![[1905.11757_fig4.png]]

![[1905.11757_fig5.png]]

![[1905.11757_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：IT 协议跑进了工厂，把 IT 的攻击面也带进来了

论文的背景逻辑非常清晰，是工控安全领域最经典的一段论证：

1. **工业物联网（IIoT）的趋势**：原本用于家庭和办公环境的通信技术，被引入到工业应用中；
2. **为什么会被引入**：商用现货产品（commercial off-the-shelf products）加上统一且成熟的通信协议，让这套技术**易于集成和使用**；而且相比经典工业控制，**生产率提高了**，因为系统更容易管理、搭建和配置；
3. **代价是什么**：论文原话是 "**most attack surfaces of home and office environments are introduced into industrial applications as well**"——**家庭和办公环境的大部分攻击面，也同样被引入了工业应用**；
4. **而工业应用的问题**：**"which usually have very few security mechanisms in place"**——**通常几乎没有安全机制**。

> **这段话你可以直接背下来当开题报告背景。** 它精准概括了工控安全的根本矛盾：**为了便利性采用了 IT 技术栈，却没有同步采用 IT 的安全实践。** 结果是"IT 的攻击手法 + OT 的无防护环境"。

论文也承认，过去几年已经有若干技术被研究来解决这个问题（"several technologies tackling that issue have been researched"）——**这篇论文就是其中之一，它选择了机器学习异常检测这条路。**

### 主角：Modbus/TCP

**Modbus** 是工业界最广泛使用的通信协议之一，**Modbus/TCP** 是它在以太网上的版本（把 Modbus 报文封装进 TCP）。

> **用你熟悉的话说**：Modbus 是工业界的"明文 HTTP"——**没有认证、没有加密、没有完整性校验**。它的功能码（function code）就是简单的数字（读线圈、写寄存器等），报文结构极其简单。
>
> **攻击者的视角**：这简直是最好的靶子。你只要能连上 502 端口，就能读走所有传感器数据，也能直接写寄存器控制执行机构。**没有任何机制能阻止你。**

### 方法：合成数据集 + 四种算法

**关键前提：数据集是合成生成的**

论文明确说，它用的是 **"a synthetically generated data set of Modbus/TCP communication of a fictitious industrial scenario"**——**一个虚构工业场景的、合成生成的 Modbus/TCP 通信数据集**。

**这一点非常重要，必须说清楚**：

- 它**不是**真实工控网络抓的包；
- 它**不是**那个著名的公开"Modbus/TCP 数据集"（如有些论文使用的真实抓包数据）；
- 它是**论文自己生成的**——"虚构工业场景"意味着拓扑、设备、流量模式都是设计出来的。

论文还指出合成数据带来的一个直接好处：**"Due to the synthetic data set, supervised learning is possible."**——因为是合成数据，**所以监督学习是可行的**。

**这句话的潜台词值得琢磨**：真实工控场景下，**攻击样本极其稀缺，标注成本极高**，监督学习往往做不了。合成数据解决了标注问题，但代价是——**数据分布未必反映真实系统**。

**四种算法**

论文使用了四种机器学习算法做异常检测：

| 算法 | 英文 | 类型 |
|---|---|---|
| 支持向量机 | Support Vector Machine (SVM) | 监督学习 |
| 随机森林 | Random Forest | 监督学习（集成） |
| k 近邻 | k-nearest neighbour (k-NN) | 监督学习（惰性） |
| k 均值聚类 | k-means clustering | 无监督学习 |

论文称它们为"**基于机器学习的异常检测算法（machine learning-based anomaly detection algorithms）**"，任务是"**在数据集中找出恶意流量（find malicious traffic）**"。

### 结果与结论

论文的结论原文是：

> "**Support Vector Machine and k-nearest neighbour perform well with different data sets, while k-nearest neighbour and k-means clustering do not perform satisfactorily.**"

**这里有一个明显的表述矛盾，必须指出来**：这句话里 **k-NN 同时出现在"表现好"和"表现不好"两组里**。

这几乎可以肯定是**原文摘要的笔误**——从常理推断，作者想说的很可能是"**SVM 和随机森林表现好，k-NN 和 k-means 表现不理想**"，或者是"**SVM 和 k-NN 表现好，k-means 表现不理想**"。**但摘要原文就是这样写的，我无法确定作者的真实意图。**

**摘要中还没有给出的关键信息**（不要臆造）：
- 数据集的具体规模（多少条记录、多少特征）
- 各类算法的准确率、精确率、召回率、F1（**一个数字都没有**）
- "different data sets" 指的是哪几个数据集（摘要只说"不同的数据集"，未说明来源和数量）
- 攻击类型（论文未说明注入的是什么攻击）
- 数据集是否公开（摘要未提及）

**特别警告：这篇摘要里没有任何性能数字，不要编造任何准确率。**

### 结论的意义

抛开表述矛盾，论文的核心结论是：**在合成 Modbus/TCP 数据集上，部分机器学习算法能有效识别恶意流量，但另一些（聚类类）效果不佳。**

对做检测的人来说，这条结论其实符合直觉：**有监督方法（有标签可用）通常优于无监督方法**，尤其是在数据是合成的、标签是完备的情况下。

## 关键公式（小白版）

这篇以实验对比为主，没有需要展开的核心公式。它的技术路线是一条极简的流水线：

```
合成生成 Modbus/TCP 通信数据集（虚构工业场景）
        ↓  标注（因为合成，所以有完整标签）
        ↓
四种算法分别训练/检测
   SVM | Random Forest | k-NN | k-means
        ↓
   对比检测效果 → SVM 类表现较好，k-means 不理想
```

## 用网安的话说（小电解读）

**这篇论文 ≈ "在自造数据集上跑 sklearn 四件套"**。你要做的事和它几乎一模一样，只是可以做得更好。

**为什么这篇论文值得你花时间——它踩的坑你可以避开：**

1. **"合成数据"是这个领域最大的争议点。**
   论文直说数据是合成的，**这是一个诚实的做法**（很多论文用了合成数据却写得像真实数据）。但你要清楚：**在合成数据上跑出高准确率，几乎没有说服力**——因为合成数据的攻击模式往往太"干净"，和正常流量的区别太明显。
   **这直接对应你在 L3 读过的"虚假安全感"主题**：模型在干净数据上 99%，上线就崩。
   **你的机会**：在真实抓包数据（或至少是带真实噪声的数据）上重做这个实验，看结论是否还成立。

2. **"因为合成所以能做监督学习"——这句话反过来读更有价值。**
   真实工控场景的问题是**标签稀缺**。所以：
   - **无监督 / 半监督 / 自监督**方法才是更现实的方向；
   - **合成数据 + 域适应**（合成数据训练，真实数据测试）是一个非常有前景的方向；
   - **数据增强 / 生成式模型造攻击样本**（GAN、扩散模型）也是热门。

3. **Modbus 的检测特征其实很特别。**
   Modbus/TCP 的报文结构简单到可以**逐字段枚举**：事务标识、协议标识、长度、单元标识、功能码、数据。**这意味着可以做"协议语义检测"**——比如"某个 IP 平时只发功能码 3（读保持寄存器），突然发了功能码 16（写多个寄存器）"，这就是异常。**这是比统计异常检测更精确的路线**（呼应 097 那篇的语义规则 IDS 思路）。

4. **k-means 效果差是有原因的，而且这个原因有研究价值。**
   k-means 在异常检测里的典型问题是：**它假设簇是球形的、且它本质上是聚类不是分类**——它会把少量攻击样本"吸收"进正常簇里（因为攻击样本太少，不构成独立的簇）。**"工控场景下极不平衡数据对无监督检测的影响"**是一个可以做实证研究的问题。

**可迁移的选题**：

1. **在真实 Modbus/TCP 抓包数据上重做这个对比实验**——验证合成数据结论的可迁移性，**这是一个很好的"复现 + 打脸"型论文**；
2. **Modbus 协议语义型异常检测**——基于功能码序列、读写权限的规则+学习混合方法；
3. **面向极端类别不平衡的工控异常检测**——把 k-means 失败的原因讲清楚，并给出解法；
4. **合成数据质量评估**——怎么衡量"合成流量像不像真实流量"？这本身就是一个可发论文的评测问题。

## 读完后你应该能回答

- [ ] 为什么 IT 协议进入工业场景会带来安全风险？
- [ ] Modbus/TCP 为什么容易成为攻击目标？它缺哪些安全机制？
- [ ] 论文用的数据集是真实的还是合成的？这会影响结论的可信度吗？
- [ ] "因为数据是合成的，所以监督学习可行"——这句话隐含了真实场景的什么问题？
- [ ] 论文摘要里关于 k-NN 的表述有什么矛盾？

## 局限性

- **摘要存在明显矛盾**：k-NN 同时被列入"表现好"和"表现不好"两组，**摘要的结论表述不可靠，必须读原文核实**。
- **数据集是合成生成的**，且基于"虚构工业场景"。**攻击模式可能过于规则、与正常流量区分度太高，导致检测任务被人为简化。** 论文未讨论合成数据与真实流量的差异。
- **摘要零量化结果**：没有数据集规模、没有准确率、没有 F1、没有误报率。**无法评估方法实际效果，也无法与其他工作对比。**
- **数据集是否公开未说明**。如果不公开，这篇论文对社区的价值就大打折扣（**数据集本身才是最有价值的产出**）。
- **只对比了四种传统算法**，没有深度学习、没有考虑对抗攻击、没有考虑类别不平衡的处理。
- **"different data sets"表述模糊**：摘要提到"在不同数据集上表现"，但没有说明是几个数据集、来自哪里，**无法判断结论的泛化性**。
- **2019 年的工作**，Modbus 安全检测领域此后有大量新方法，**这篇只能当基线，不能当前沿**。

## 和你的方向有什么关系

- **这是 L10 里"最轻量、最容易复现"的一篇**——如果你想快速上手做实验，从这篇的流程开始最合适。
- **直接选题（按推荐度排序）**：
  1. **真实数据 vs 合成数据的检测效果对比研究**——直接针对这篇的最大软肋，**问题陈述清晰、实验可控、结论有价值**；
  2. **Modbus 协议语义型检测方法**（功能码序列 + 权限模型），对接 097 的语义 IDS 思路；
  3. **极端不平衡下的工控异常检测**（论文的 k-means 失败提供了一个现成的反面案例）；
  4. **工业协议数据集质量评估框架**。
- **和你实验室方向的对接**：**"入侵检测"**（直接对口，且 Modbus 数据集易获取）、**"AI与数据安全"**（合成数据质量、类别不平衡、标注可信度）。

## 概念关联

[[Modbus协议安全]] · [[电力系统异常检测]] · [[工控安全测试床与数据集]] · [[SCADA系统]]

## 原文摘要

> In the context of the Industrial Internet of Things, communication technology, originally used in home and office environments, is introduced into industrial applications. Commercial off-the-shelf products, as well as unified and well-established communication protocols make this technology easy to integrate and use. Furthermore, productivity is increased in comparison to classic industrial control by making systems easier to manage, set up and configure. Unfortunately, most attack surfaces of home and office environments are introduced into industrial applications as well, which usually have very few security mechanisms in place. Over the last years, several technologies tackling that issue have been researched. In this work, machine learning-based anomaly detection algorithms are employed to find malicious traffic in a synthetically generated data set of Modbus/TCP communication of a fictitious industrial scenario. The applied algorithms are Support Vector Machine (SVM), Random Forest, k-nearest neighbour and k-means clustering. Due to the synthetic data set, supervised learning is possible. Support Vector Machine and k-nearest neighbour perform well with different data sets, while k-nearest neighbour and k-means clustering do not perform satisfactorily.
