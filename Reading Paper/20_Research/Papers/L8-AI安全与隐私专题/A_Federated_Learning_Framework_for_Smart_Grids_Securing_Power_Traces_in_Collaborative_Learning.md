---
document_id: "arxiv-2103.11870"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2103.11870"
arxiv_id: "2103.11870"
title: "A Federated Learning Framework for Smart Grids: Securing Power Traces in Collaborative Learning"
authors: ["Haizhou Liu", "Xuan Zhang", "Xinwei Shen", "Hongbin Sun"]
published: "2021-03-22"
venue: "arXiv preprint"
domain: "L8-AI安全与隐私专题"
level: "L8"
reading_order: 66
difficulty: "入门+"
lang: "en"
tags: ["电网安全", "L8-AI安全与隐私专题", "联邦学习", "智能电网", "同态加密", "隐私保护"]
quality_score: 8
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 066 | 面向智能电网的联邦学习框架：在协同学习中保护用电轨迹

> [!abstract] 一句话
> 把联邦学习真正落到电网业务上的一份"框架设计文档"：横向联邦解决"数据分散在不同变电站"，纵向联邦解决"数据分散在不同机构"，再用 Paillier 同态加密把参数传输也保护起来。

## 为什么读它

- 064 是中文综述，讲的是"联邦学习能用在电力哪些地方"；这篇是**较早把"横向/纵向两类联邦怎么在电网里落地"讲清楚的英文工程论文**，两者搭配读，一个给地图、一个给施工图。
- 它回答了一个很具体的问题：**电力数据不只是"分散在样本维度"，还分散在"特征维度"**。例如电力公司只有用电量，移动运营商只有人口流动数据——这两类数据对同一批用户做联合建模，就是纵向联邦。这个场景比"多台电表联合训练"复杂得多。
- 它是**把密码学工具（同态加密）引入电力联邦学习的早期代表**，后面的 067（差分隐私）、076（DP + 安全聚合）可以对照着看：**保护手段从"密码学"到"噪声注入"的演化路线**。
- 建议读法：重点看它怎么定义横向/纵向两种场景的数据分布，以及 Paillier 加密在其中的作用位置。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | A Federated Learning Framework for Smart Grids: Securing Power Traces in Collaborative Learning（面向智能电网的联邦学习框架：在协同学习中保护用电轨迹） |
| 作者 | Haizhou Liu, Xuan Zhang, Xinwei Shen, Hongbin Sun（清华大学等） |
| 发表 | arXiv preprint, 2021-03-22 |
| 链接 | [arXiv](https://arxiv.org/abs/2103.11870) |
| 类型 | arXiv 预印本 |
| 难度 | 入门+ |
| 关键词 | 联邦学习框架、用电轨迹保护、横向联邦、纵向联邦、Paillier 同态加密 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2103.11870_fig1.jpg]]

![[2103.11870_fig2.jpg]]

![[2103.11870_fig3.png]]

![[2103.11870_fig4.png]]

![[2103.11870_fig5.png]]

![[2103.11870_fig6.jpg]]

---


## 这篇论文在讲什么（白话版）

### 背景：电网的数据困局

论文的出发点和 064 一样，但用了很具体的例子：

- **用电量数据**分散在城市里成千上万个**变电站**（transformer station）手里；
- **人口流动数据**（是预测用电量的重要指标）掌握在**移动通信运营商**手里。

这些数据对做大数据分析非常有价值，但**直接共享会同时损害三方利益**：企业的商业利益、个人的隐私、甚至国家安全。

论文的动机很直接：**能不能在不共享原始数据的前提下，让这些数据"联合起来发挥作用"？** 答案借用了 Google 的联邦学习方案。

### 方法：两种联邦，对应两种数据分散方式

论文的核心贡献是给出了一个**面向电网的联邦学习框架**，并且明确区分两种场景：

**（1）横向联邦学习（Horizontal FL）—— 数据在样本空间分散**

适用条件：各参与方**拥有相同的特征字段**，只是记录的**对象不同**。

电力例子：十个不同的变电站，每家都有"某台区在某个时刻的有功功率、无功功率、电压"这些字段，但记录的是不同台区。把它们联合起来训练负荷预测模型，就是横向联邦。

**（2）纵向联邦学习（Vertical FL）—— 数据在特征空间分散**

适用条件：各参与方**记录的是同一批对象**，但**字段不同**。

电力例子：电网公司有"某用户的用电曲线"，移动运营商有"该用户的人口流动特征"。两者对同一批用户做联合建模，字段不重叠，这就是纵向联邦。论文明确指出这类场景的设计难度更高，因为它需要**样本对齐（sample alignment）**——双方得先在不泄露各自数据的前提下，找出"哪些记录是同一个人"。

### 关键组件：Paillier 加密

框架在参数交换环节引入了 **Paillier 加密**（一种加法同态加密）。它的作用是：**让服务器能在密文上做加法，却看不到明文参数**。

论文的案例研究结论是：在采用恰当加密方案（如 Paillier）的前提下，通过该框架构建的机器学习模型是**无损的（lossless）、隐私保护的（privacy-preserving）、有效的（effective）**。

> **"lossless"（无损）这个词很关键**：它意味着加密没有损失模型精度——这是同态加密相对差分隐私的最大优势。代价是计算开销。

### 展望：联邦学习在电网的其他落点

论文最后讨论了联邦学习在智能电网其他环节的前景：

- **电动汽车（Electric Vehicles）**——充电行为数据分散在车企、充电桩运营商、电网之间；
- **分布式发电/用电（Distributed Generation/Consumption）**——海量屋顶光伏、储能设备的数据归属分散；
- **综合能源系统（Integrated Energy Systems）**——电、气、热多能耦合，数据分属不同能源企业。

## 关键公式（小白版）

论文摘要没有给出公式，但它的技术核心是 **Paillier 同态加密的加法同态性质**。这是该加密方案的通用性质（不是本文提出的）：

$$E(a) \cdot E(b) \bmod n^{2} = E\big((a+b) \bmod n\big)$$

符号解释：

- $a, b$ —— 两个明文数值（例如两个客户端上传的模型参数分量）。
- $E(\cdot)$ —— Paillier 加密函数。
- $n$ —— 公钥的一部分（两个大素数的乘积），$n^2$ 是模数。
- $E(a) \cdot E(b) \bmod n^2$ —— 两个**密文**相乘后再取模。

**一句话白话**：两个密文相乘，等于"把明文加起来再加密"。所以服务器可以在**完全不知道明文是多少**的情况下，把一堆客户端上传的参数加起来（正好是 FedAvg 需要做的加权求和），然后把结果密文发给客户端解密。

**代价**：密文长度远大于明文（Paillier 的密文通常是明文的两倍比特数），加解密和密文运算的计算开销也很大。**这是"安全 ↔ 效率"权衡的经典体现**，在电网这种要求实时响应的场景里尤其要命。

## 用网安的话说（小电解读）

**这篇论文本质上是"用密码学手段把联邦学习协议做成端到端加密"。**

你在网安课上学过的对照点：

| 概念 | 在这篇论文里 |
|---|---|
| 同态加密（Homomorphic Encryption） | Paillier，支持加法同态，用于参数聚合 |
| 安全多方计算（MPC） | 纵向联邦的样本对齐环节本质上是一个 PSI（隐私集合求交）问题 |
| 端到端加密 | 服务器全程只接触密文，是"零知识"式的聚合 |
| 差分隐私 | **论文没用**——它选了"精确但慢"的路线，而不是"快但加噪声"的路线 |

**这是一个很重要的技术路线分叉，你要记住：**

- **密码学路线（本文）**：精确、无损、无精度损失，但**计算和通信开销大**，且**不抵抗投毒/后门**（加密只保证"服务器看不到明文"，不保证"客户端上传的东西是干净的"）。
- **噪声注入路线（067、076）**：便宜、快，但**损失精度**，且隐私强度依赖隐私预算 ε 的取值。

**两条路线各自的攻击面也不同**：

- 密码学路线怕**协议层攻击**——比如纵向联邦里的样本对齐过程本身就是攻击面（攻击者可以通过反复查询推断出对方有哪些样本，这类攻击叫"标签泄露/隐私泄露"）。
- 噪声注入路线怕**参数层攻击**——比如后门攻击（069、070），噪声对后门几乎无效，因为后门是"有结构"的信号，不是随机扰动。

**如果要迁移到你的研究**：本文的框架没有考虑**恶意客户端**。一个很自然的选题是：**在 Paillier 加密的联邦聚合里，怎么检测投毒客户端？** 难点在于——服务器只能看到密文，**传统的"看梯度分布找异常"的防御方法在密文上直接失效**。这个"密文域下的鲁棒聚合"是一个真实的开放问题，而且和你实验室的"AI与数据安全"方向严丝合缝。

## 读完后你应该能回答

- [ ] 横向联邦和纵向联邦的区别是什么？电网里各对应什么数据场景？
- [ ] 纵向联邦为什么需要"样本对齐"？这会带来什么新的隐私风险？
- [ ] Paillier 加密的加法同态性质是什么？它为什么正好适合 FedAvg 的聚合步骤？
- [ ] 论文说模型是"lossless"的，这是什么意思？代价是什么？
- [ ] 为什么"参数加密"不能防御投毒攻击？

## 局限性

- **威胁模型很弱**：只防御"服务器偷看参数"，没有考虑恶意客户端、投毒、后门。论文自己也没有声称能防这些。
- **加密开销未被充分讨论**：摘要说结果是"有效的"，但**没有给出任何具体的性能数字**（耗时、通信量），读者无法判断它能不能满足电网的实时性要求。
- **纵向联邦部分偏概念化**：样本对齐的具体协议、对齐过程中的隐私泄露风险，摘要层面没有交代。
- **案例研究的规模与数据来源不明**：摘要只说"case studies show"，没有说明用的是真实电网数据还是仿真数据。
- 论文是 2021 年的工作，此后纵向联邦的隐私保护协议已有大量进展（如基于差分隐私的 PSI），本文的协议设计相对早期。

## 和你的方向有什么关系

- **这是一篇"工程框架"论文，适合作为你进入电力联邦学习的第一篇英文文献**（难度入门+，不需要电力专业知识就能读懂主要思想）。
- **直接选题（按推荐度）**：
  1. **密文域下的鲁棒联邦聚合**——在 Paillier 加密条件下检测投毒/后门客户端。这是本文与 069/070 之间的空白，**价值高、难度中等**。
  2. **纵向联邦在电力场景的样本对齐隐私评估**——电网公司与运营商做纵向联邦时，对齐协议本身会泄露什么。
  3. **同态加密 vs 差分隐私的电力场景对比实验**——用同一批负荷数据，比较两条路线的精度、隐私、开销三个维度。这是"综述+实验"型工作，上手快。
- **与实验室方向的对接**："AI与数据安全"直接对口（密码学 + 联邦学习）；"工业AI与智能体"对应多主体协同建模。

## 概念关联

[[联邦学习]] · [[智能电网]] · [[电力负荷预测]] · [[联邦学习攻击与防御]] · [[电动汽车充电安全]]

## 原文摘要

> With the deployment of smart sensors and advancements in communication technologies, big data analytics have become vastly popular in the smart grid domain, informing stakeholders of the best power utilization strategy. However, these power-related data are stored and owned by different parties. For example, power consumption data are stored in numerous transformer stations across cities; mobility data of the population, which are important indicators of power consumption, are held by mobile companies. Direct data sharing might compromise party benefits, individual privacy and even national security. Inspired by the federated learning scheme from Google AI, we propose a federated learning framework for smart grids, which enables collaborative learning of power consumption patterns without leaking individual power traces. Horizontal federated learning is employed when data are scattered in the sample space; vertical federated learning, on the other hand, is designed for the case with data scattered in the feature space. Case studies show that, with proper encryption schemes such as Paillier encryption, the machine learning models constructed from the proposed framework are lossless, privacy-preserving and effective. Finally, the promising future of federated learning in other facets of the smart grid is discussed, including electric vehicles, distributed generation/consumption and integrated energy systems.
