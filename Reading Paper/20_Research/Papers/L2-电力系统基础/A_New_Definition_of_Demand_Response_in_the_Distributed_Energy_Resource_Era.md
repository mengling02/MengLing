---
document_id: "arxiv-2410.18768"
arxiv_id: "2410.18768"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2410.18768"
title: "A New Definition of Demand Response in the Distributed Energy Resource Era"
zh_title: "分布式能源时代对需求响应的新定义"
authors: ["Johanna L. Mathieu", "Gregor Verbič", "Thomas Morstyn", "Mads Almassalkhi", "Kyri Baker", "Julio Braslavsky", "Kenneth Bruninx", "Yury Dvorkin", "et al."]
published: "2024-10-24"
venue: "arXiv (eess.SY)"
domain: "L2-电力系统基础"
level: "L2"
reading_order: 13
difficulty: "入门"
tags: ["论文笔记", "L2-电力系统基础", "需求响应", "分布式能源", "综述与定义"]
quality_score: 8
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 013 | 分布式能源时代对需求响应的新定义

> [!abstract] 一句话
> 13 位学者联合指出：**"需求响应"这个用了 100 年的老概念，定义已经乱了**。在分布式能源（DER）时代，必须重新定义，否则研究无法比较、政策无法落地。

## 为什么读它

这篇论文很特别：**它不是提出算法，而是提出"定义"**。

对研一学生的价值：
- 理解**学术概念是怎么演进的**（定义 → 研究 → 定义失效 → 重新定义）
- 需求响应是"新型电力系统"的关键机制，你迟早要碰
- 作者的**研究议程（research agenda）**部分，直接给出了"哪些问题还没解决" → **天然的选题清单**

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | A New Definition of Demand Response in the Distributed Energy Resource Era |
| **作者** | Johanna L. Mathieu, Gregor Verbič, Thomas Morstyn, Mads Almassalkhi, Kyri Baker, Julio Braslavsky, Kenneth Bruninx, Yury Dvorkin 等（13 位作者，横跨欧美多所高校） |
| **发布** | 2024-10-24 |
| **分类** | eess.SY |
| **类型** | 立场/定义类论文（Position Paper） |
| **链接** | [arXiv](https://arxiv.org/abs/2410.18768) \| [PDF](https://arxiv.org/pdf/2410.18768) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2410.18768_fig1.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：需求响应"火了 30 年"，但定义混乱

> 原文：*"we have seen an explosion of research on demand response and demand-side technologies in the past 30 years, coinciding with the shift towards liberalized/deregulated electricity markets and efforts to decarbonize the power sector."*

需求响应的概念**从最早的电力系统就存在**，但过去 30 年研究爆炸式增长，原因有两个：
1. 电力市场自由化/去管制化
2. 电力行业脱碳

### 新的范式转变：从集中式到分布式

> 原文：*"Now we are also seeing a shift towards more distributed/decentralized electric systems; we have entered the era of 'distributed energy resources,' which require new grid management, operational, and control strategies."*

**变化**：
- 以前：集中式大电厂 + 被动用户
- 现在：**海量分布式资源（DER）** + 主动用户（prosumer，产消者）

**DER 包括**：屋顶光伏、家用储能、电动车、可控负荷（空调、热水器、热泵）……

**问题**：这些资源**既是负荷也是电源**，且由不同主体控制 —— 传统的"需求响应"定义（用户削减负荷）已经不适用了。

### 论文的四个动作

1. **梳理现有定义**（survey existing definitions）
2. **指出缺陷**（highlight their shortcomings）
3. **提出新定义**（propose a new definition）
4. **说明新定义的价值**，并给出**研究议程 + 障碍与使能因素**

### 新定义的意义

论文主张：新定义能让研究者更好地**利用这个"巨大的资源"**来实现：
- **经济目标**（降低用能成本）
- **技术目标**（维持电网稳定）
- **环境目标**（促进新能源消纳）
- **社会目标**（公平、可及性）

## 用网安的话说（小电解读）

> 这篇论文表面上和"安全"无关，但它给了你**两个重要的东西**：

**1）一个清晰的"新型电力系统"运行图景**

理解需求响应，你才能理解：
- 为什么"海量终端接入"是必然趋势 → 为什么攻击面必然扩大
- 为什么传统"物理隔离"策略难以为继 → 见 [[电力监控系统安全防护体系]]

**2）一个"研究议程"= 选题清单**

论文最后列出的**障碍（barriers）与使能因素（enablers）**，每一条背后都藏着安全问题：

| 需求响应的使能条件 | 对应的安全风险 |
|---|---|
| 需要用户实时数据 | **隐私泄露**（用电曲线可反推生活作息） |
| 需要通信与控制通道 | **中间人攻击、指令篡改** |
| 需要价格/激励信号 | **虚假信号注入**（假消息！） |
| 需要聚合商（aggregator） | **单点失效、聚合商被攻破 → 大规模负荷同时动作** |
| 需要计量与结算 | **计量数据欺诈**（骗取补偿） |

**一个很有特色的选题**：
> **"需求响应中的虚假信号检测"** —— 这正好对接你实验室的"**假消息检测**"方向！
> 需求响应本质上是"**用价格信号协调海量设备**"，那么"**伪造价格信号**"就是一种"电力系统中的假消息"。这个交叉点很新颖，且文献不多。

**另一个思路**：
> **大规模协同攻击**：如果攻击者控制了 10 万台可控负荷（空调、热水器、充电桩），能否**同步启停**制造人为的功率振荡？
> 这类"**通过海量终端制造物理扰动**"的攻击，在物联网安全里是理论问题，在电网里是**真实威胁**。

## 读完后你应该能回答

- [ ] 什么是"分布式能源（DER）"？它和传统负荷有什么不同？
- [ ] 为什么旧的需求响应定义在 DER 时代失效了？
- [ ] 需求响应系统有哪些环节可能被攻击？
- [ ] "聚合商"在需求响应中扮演什么角色？它的安全风险是什么？

## 局限性

- 这是**立场/定义类论文**，不含实验、算法或数据 → 不能指望从中学到技术方法。
- 新定义是否能被学术界接受，还需要时间检验。
- 对**安全性**几乎零讨论（只在"使能因素"里间接涉及）。
- 主要面向欧美电力市场语境，中国电力市场结构不同（以中长期交易为主），需注意适配性。

## 和你的方向有什么关系

- **理解"新型电力系统"的商业与机制层面**：技术之外，你还需要懂"电是怎么交易的"，这直接影响攻击动机。
- **直接选题**：
  1. **需求响应中的信号伪造与检测**（对接"假消息检测"方向）
  2. **聚合商（aggregator）被攻破的后果建模**
  3. **海量可控负荷的协同攻击与防御**
- 与 [[联邦学习]] 结合：分布式资源的数据聚合天然需要隐私保护技术。
- 与 [[对抗样本攻击]] 结合：价格预测模型也会被对抗攻击。

## 概念关联

- 核心概念：[[电力需求响应]] · [[智能电网]] · [[电力负荷预测]] · [[联邦学习]]
- 前置阅读：[[20_Research/Papers/L2-电力系统基础/A_comparative_assessment_of_deep_learning_models_for_day-ahead_load_forecasting|012 深度学习负荷预测模型比较]]
- 后续阅读：[[20_Research/Papers/L4-AI与电网安全/Federated_Learning_for_Smart_Grid_A_Survey_on_Applications_and_Potential_Vulnerabilities|028 联邦学习用于智能电网综述]]
- 体系视角：[[20_Research/Papers/L1-零基础起步/新型电力系统信息物理安全防护体系研究|002]]

## 原文摘要

> Demand response is a concept that has been around since the very first electric power systems. However, we have seen an explosion of research on demand response and demand-side technologies in the past 30 years, coinciding with the shift towards liberalized/deregulated electricity markets and efforts to decarbonize the power sector. Now we are also seeing a shift towards more distributed/decentralized electric systems; we have entered the era of "distributed energy resources," which require new grid management, operational, and control strategies. Given this paradigm shift, we argue that the concept of demand response needs to be revisited, and more carefully/consistently defined to enable us to better utilize this massive resource for economic, technical, environmental, and societal aims. In this paper, we survey existing demand response definitions, highlight their shortcomings, propose a new definition, and describe how this new definition enables us to more effectively harness the value of demand response in modern power systems. We conclude with a demand response research agenda informed by a discussion of demand response barriers and enablers.
