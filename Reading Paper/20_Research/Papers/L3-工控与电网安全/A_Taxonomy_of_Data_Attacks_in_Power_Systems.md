---
document_id: "arxiv-2002.11011"
arxiv_id: "2002.11011"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2002.11011"
title: "A Taxonomy of Data Attacks in Power Systems"
zh_title: "电力系统数据攻击的分类学"
authors: ["Sagnik Basumallik"]
published: "2020-02-25"
venue: "arXiv (eess.SY)"
domain: "L3-工控与电网安全"
level: "L3"
reading_order: 23
difficulty: "入门+"
tags: ["论文笔记", "L3-工控与电网安全", "攻击分类学", "数据攻击", "数学建模"]
quality_score: 9
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 023 | 电力系统数据攻击的分类学

> [!abstract] 一句话
> 把 **19 种攻击模型**按"稳态控制 / 暂态与辅助控制 / 变电站控制 / 负荷控制"四大类整理，每一类都给出**数学攻击模型** —— 这是一篇"攻击建模工具箱"。

## 为什么读它

和 [[20_Research/Papers/L3-工控与电网安全/Comprehensive_Survey_and_Taxonomies_of_False_Injection_Attacks_in_Smart_Grid|021]] 相比，这篇的特点：

- **按"被攻击的控制环节"分类**（而非按攻击者能力）→ 更贴近**电网工程视角**
- **给出数学攻击模型** → 你可以直接拿来复现
- **单作者论文**，结构紧凑（更像是作者的博士研究综述）

**它回答了一个关键问题**：**电网里到底有哪些"控制回路"，每一个都可以被攻击。**

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | A Taxonomy of Data Attacks in Power Systems |
| **作者** | Sagnik Basumallik |
| **发布** | 2020-02-25 |
| **分类** | eess.SY |
| **链接** | [arXiv](https://arxiv.org/abs/2002.11011) \| [PDF](https://arxiv.org/pdf/2002.11011) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2002.11011_fig1.jpg]]

![[2002.11011_fig2.png]]

![[2002.11011_fig3.jpg]]

---


## 这篇论文在讲什么（白话版）

### 出发点：电力是所有行业的底座

> 原文：*"In a macro-economic system, all major sectors: agriculture, extraction of natural resources, manufacturing, construction, transport, communication and health services, are dependent on a reliable supply of electricity."*

**农业、采矿、制造、建筑、交通、通信、医疗 —— 全都依赖可靠供电。**

> 原文：*"Targeted attacks on power networks can lead to disruption in operations, causing significant economic and social losses."*

**定向攻击 → 运行中断 → 重大经济与社会损失。**

### 攻击的入口：时间关键型数据

> 原文：*"When cyber networks in power system are compromised, time-critical data can be dropped and modified, which can impede real time operations and decision making."*

**两种破坏方式**：
- **丢弃（dropped）** → 破坏**可用性**
- **篡改（modified）** → 破坏**完整性**

> **注意**：大多数 FDIA 论文只讲"篡改"。**"丢弃"（数据可用性攻击）是一个被相对忽视的方向**。

### 核心贡献：四类攻击分类（19 种攻击模型）

论文把 19 种攻击模型按**被攻击的运行/控制模块**分为四类：

| 类别 | 攻击对象 | 代表攻击 | 后果 |
|---|---|---|---|
| **1. 稳态控制（Steady State Control）** | 状态估计、最优潮流、经济调度 | FDIA、负载重分配攻击 | 调度决策错误 |
| **2. 暂态与辅助控制（Transient & Auxiliary Control）** | AGC（自动发电控制）、PSS（电力系统稳定器）、励磁控制 | 控制回路 FDIA | 频率/功角失稳 |
| **3. 变电站控制（Substation Control）** | 继电保护、断路器控制、IEC 61850 | GOOSE 伪造、保护定值篡改 | 保护误动/拒动 |
| **4. 负荷控制（Load Control）** | 需求响应、负荷管理、智能电表 | 虚假负荷信号、电表数据篡改 | 负荷振荡、经济欺诈 |

**每类都给出"综合的数学攻击模型综述"** —— 这是论文最实用的部分。

### 论文目标

> 原文：*"The goal is to provide a theoretically balanced approach to cyber attacks and their impacts on the reliable functioning of the electric grid."*

**提供"理论上平衡的"攻击及其影响分析方法** —— 即不只讲攻击，也讲影响。

## 用网安的话说（小电解读）

> 这篇论文给你一张**"电网攻击面地图"**，按控制回路划分。

**为什么这个分类方式比"按攻击者能力"更实用？**

因为它直接对应**工程上的责任划分**：
- 稳态控制 → 调度中心负责
- 暂态控制 → 稳定控制装置负责
- 变电站控制 → 保护班组负责
- 负荷控制 → 营销/需求侧负责

→ 你的研究如果要落地，必须明确"**我保护的是哪个环节、由谁运维**"。

**四类攻击的"技术难度-后果严重度"矩阵**（小电整理）：

| 类别 | 攻击难度 | 后果严重度 | 研究热度 |
|---|---|---|---|
| **稳态控制** | 中（需拓扑知识） | 中（决策错误，有缓冲） | **极高（最卷）** |
| **暂态与辅助控制** | 高（需控制理论） | **高（直接失稳）** | 中 |
| **变电站控制** | 中（协议无认证） | **极高（保护误动）** | 中 |
| **负荷控制** | 低（终端多、防护弱） | 中（经济+局部） | 低 |

**给你的选题建议**：

> **"高后果 + 中低研究热度"的格子最值得进**：
> - **暂态与辅助控制攻击**（后果最严重，研究相对少）
> - **变电站控制攻击**（IEC 61850 场景，工程价值高）
> - **负荷控制攻击**（终端多、易实施，且有"假消息"特色）

**特别提醒——"数据丢弃"这个被忽视的方向**：
> 论文明确提到数据可以被"dropped"（丢弃）。
> 在电力系统里，**让数据"消失"可能比"篡改"更有效**：
> - 让某些量测消失 → 状态估计**不可观（unobservable）** → 系统失去态势感知
> - 让控制指令丢失 → 执行机构不动作
> → **"可用性攻击在电力系统中的作用"** 是一个相对空白且有价值的方向。

## 读完后你应该能回答

- [ ] 电力系统有哪四类可被攻击的控制环节？
- [ ] 为什么"数据丢弃"和"数据篡改"同样重要？
- [ ] 哪些控制环节的攻击后果最严重？
- [ ] 为什么"按控制环节分类"比"按攻击者能力分类"更贴近工程？

## 局限性

- **单作者综述**，覆盖面可能不如团队综述全面。
- **2020 年**的工作，未包含新型电力系统（高比例新能源、虚拟电厂）带来的新控制环节。
- 数学模型的**符号体系可能与主流论文不一致**，对照时需注意。
- 未涉及 AI/ML 检测方法。

## 和你的方向有什么关系

- **这是你的"攻击面地图"**：帮你系统性地理解"电网有哪些地方可以打"。
- **直接选题**：
  1. **暂态/辅助控制回路的攻击检测**（高后果、相对空白）
  2. **数据可用性攻击**（让状态估计不可观）与防御
  3. **变电站控制层的攻击检测**（IEC 61850 GOOSE/SV 异常检测）
  4. **负荷控制层攻击**（对接"假消息检测"方向）
- **写作价值**：论文的**四类分类框架**可以直接用于你论文的"威胁模型"章节。

## 概念关联

- 核心概念：[[虚假数据注入攻击(FDIA)]] · [[状态估计]] · [[电力系统稳定性]] · [[IEC 61850]] · [[电力需求响应]]
- 分类学对照：[[20_Research/Papers/L3-工控与电网安全/Comprehensive_Survey_and_Taxonomies_of_False_Injection_Attacks_in_Smart_Grid|021 FDIA 综合综述（按攻击者能力分类）]]
- 攻击构造：[[20_Research/Papers/L3-工控与电网安全/Vulnerability_Analysis_and_Consequences_of_False_Data_Injection_Attack_on_Power_System_State_Estimation|024 FDIA 脆弱性分析]]
- 防御：[[20_Research/Papers/L3-工控与电网安全/A_Survey_of_Machine_Learning_Methods_for_Detecting_False_Data_Injection_Attacks|022 FDIA 检测的机器学习方法综述]]

## 原文摘要

> In a macro-economic system, all major sectors: agriculture, extraction of natural resources, manufacturing, construction, transport, communication and health services, are dependent on a reliable supply of electricity. Targeted attacks on power networks can lead to disruption in operations, causing significant economic and social losses. When cyber networks in power system are compromised, time-critical data can be dropped and modified, which can impede real time operations and decision making. This paper tracks the progress of research in power system cyber security over the last decade and presents a taxonomy of data attacks. Nineteen different attack models against major operation and control blocks are classified into four areas: steady state control, transient and auxiliary control, substation control and load control. For each class, a comprehensive review of mathematical attack models is presented. The goal is to provide a theoretically balanced approach to cyber attacks and their impacts on the reliable functioning of the electric grid.
