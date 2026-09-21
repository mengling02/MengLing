---
document_id: "arxiv-1809.02609"
arxiv_id: "1809.02609"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/1809.02609"
title: "Cyber-Security in Smart Grid: Survey and Challenges"
zh_title: "智能电网网络安全：综述与挑战"
authors: ["Zakaria El Mrabet", "Hassan El Ghazi", "Naima Kaabouch", "Hamid El Ghazi"]
published: "2018-08-31"
venue: "Computers and Electrical Engineering, Vol. 67, Elsevier, 2018；arXiv:1809.02609"
domain: "L3-工控与电网安全"
level: "L3"
reading_order: 17
difficulty: "入门"
tags: ["论文笔记", "L3-工控与电网安全", "智能电网安全", "综述", "安全需求"]
quality_score: 8
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 017 | 智能电网网络安全：综述与挑战

> [!abstract] 一句话
> 一篇**批评性**综述：指出前人研究"只用 CIA 三性分类攻击，漏掉了问责性（accountability）"，且防御方案"各自为政，缺乏全局视角"，然后提出了一套整体安全策略。

## 为什么读它

和 [[20_Research/Papers/L3-工控与电网安全/A_Comprehensive_Survey_on_the_Security_of_Smart_Grid|016]] 相比，这篇更**"有观点"**：

- 它**批评**了现有研究的两个通病
- 它提出了一套**分层的安全策略**
- 它教你**怎么用"安全需求"作为分析框架** —— 这是你写论文时做分类的标准工具

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Cyber-Security in Smart Grid: Survey and Challenges |
| **作者** | Zakaria El Mrabet, Hassan El Ghazi, Naima Kaabouch, Hamid El Ghazi |
| **发表** | Computers and Electrical Engineering, Vol. 67, Elsevier, 2018 |
| **分类** | cs.CR |
| **链接** | [arXiv](https://arxiv.org/abs/1809.02609) \| [PDF](https://arxiv.org/pdf/1809.02609) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[1809.02609_fig1.png]]

![[1809.02609_fig2.png]]

![[1809.02609_fig3.png]]

![[1809.02609_fig4.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：智能电网的两面性

> 原文：*"Smart grid uses the power of information technology to intelligently deliver energy to customers by using a two-way communication, and wisely meet the environmental requirements by facilitating the integration of green technologies."*

正面：**双向通信 + 绿色能源接入** → 更智能、更环保

> 原文：*"Because communication has been incorporated into the electrical power with its inherent weaknesses, it has exposed the system to numerous risks."*

负面：**通信被引入电力系统，也就把通信固有的脆弱性带进来了**。

### 对现有研究的两个批评（本文的核心观点）

**批评一：攻击分类不完整**

> 原文：*"most of them classified attacks based on confidentiality, integrity, and availability, and they excluded attacks which compromise other security criteria such as accountability."*

现有研究只用 **CIA 三性**（机密性/完整性/可用性）分类攻击，**漏掉了问责性（accountability）**。

**这一点很值得你记住**。在电网场景里，**问责性**尤其重要：
- 事故后必须能**溯源**（谁在什么时候做了什么）
- 没有审计日志 → 无法归因 → 无法改进
- 对应 [[20_Research/Papers/L1-零基础起步/电力监控系统安全防护规定|005 电力监控系统安全防护规定]] 里"保护现场以便调查和溯源取证"的要求

**批评二：防御方案缺乏全局视角**

> 原文：*"the existed security countermeasures focus on countering some specific attacks or protecting some specific components, but there is no global approach which combines these solutions to secure the entire system."*

现有方案都是"打补丁"：防某个攻击、护某个组件，**没有全局统一方案**。

### 论文的贡献

1. **回顾安全需求**（security requirements）—— 扩展了 CIA，加入问责性等
2. **深入分析重要网络攻击** —— 诊断潜在脆弱性与影响
3. **提出一套网络安全策略** —— 应对入侵、反制攻击、部署对策
4. **给出未来研究方向**

## 用网安的话说（小电解读）

> 这篇论文给你一个**实用的分析框架**：**用"安全需求"作为分类维度**。

**扩展的 CIA 模型**（电网版）：

| 安全需求 | 含义 | 在电网里的具体表现 | 攻击例子 |
|---|---|---|---|
| **机密性（C）** | 数据不泄露 | 用户用电数据、拓扑信息保密 | 窃取用电数据推断用户行为 |
| **完整性（I）** | 数据不被篡改 | 量测、控制指令准确 | **[[虚假数据注入攻击(FDIA)]]** |
| **可用性（A）** | 系统随时可用 | 电网持续供电 | DoS/DDoS 攻击通信网络 |
| **问责性（Accountability）** | 行为可追溯 | 审计日志、操作留痕 | 日志篡改、身份伪造 |
| **认证（Authentication）** | 身份可信 | 设备/用户身份验证 | 伪造设备身份接入 |
| **不可否认性（Non-repudiation）** | 行为不可抵赖 | 交易、指令的不可抵赖 | 事后否认发过指令 |
| **授权（Authorization）** | 权限受控 | 最小权限原则 | 越权操作 |

**这个框架的实用价值**：
> 当你读一篇攻击论文时，问自己："**它破坏了哪个安全需求？**"
> 当你设计一个防御方案时，问自己："**我保护了哪个安全需求？有没有遗漏？**"

**特别提醒**：在电网里，**优先级是 A > I > C**（可用性最重要）。
这与 IT 的 C > I > A **完全相反**，是电网安全的根本特征。

**为什么？**
- IT：数据泄露 → 声誉损失、罚款
- 电网：**停电 → 物理事故、人身伤害**

**"问责性"在电网里的特殊地位**：
- 电网是**关键信息基础设施**，任何事件都要能溯源
- 攻击者往往在得手后会**擦除日志**（如乌克兰事件里的 KillDisk）
- 所以"日志的完整性保护"本身就是一个研究方向

## 读完后你应该能回答

- [ ] 智能电网为什么天然带来安全风险？
- [ ] 除了 CIA，还有哪些安全需求在电网里很重要？
- [ ] 为什么电网的安全优先级是 A > I > C？
- [ ] "问责性"在电网安全中为什么重要？

## 局限性

- **2018 年的综述**，未覆盖此后的新技术（LLM、对抗 ML、联邦学习在电网的应用）。
- 提出的"安全策略"偏**框架性**，缺乏量化评估和实验验证。
- 对**中国电力体系**（安全分区、物理隔离）的讨论较少，主要面向欧美语境。
- 与 [[20_Research/Papers/L3-工控与电网安全/A_Comprehensive_Survey_on_the_Security_of_Smart_Grid|016]] 相比，技术细节和分类深度略浅。

## 和你的方向有什么关系

- **实用工具**：**"扩展 CIA"框架**是你以后分析任何安全问题的通用工具，写论文的"分类维度"就用它。
- **直接选题**：
  1. **问责性/审计日志的完整性保护**（相对冷门，有空间）
  2. **面向多安全需求的联合检测**（不只检测完整性破坏）
- **阅读策略**：和 [[20_Research/Papers/L3-工控与电网安全/A_Comprehensive_Survey_on_the_Security_of_Smart_Grid|016]] 对照读 —— 016 是 2024 年的"全景"，017 是 2018 年的"框架"，能看出 6 年间研究重心的迁移。

## 概念关联

- 核心概念：[[智能电网]] · [[电力信息物理系统(CPS)]] · [[虚假数据注入攻击(FDIA)]] · [[电力监控系统安全防护体系]]
- 对照阅读：[[20_Research/Papers/L3-工控与电网安全/A_Comprehensive_Survey_on_the_Security_of_Smart_Grid|016 智能电网安全综合综述（2024）]]
- 后续阅读：[[20_Research/Papers/L3-工控与电网安全/Architecture_and_Security_of_SCADA_Systems_A_Review|018 SCADA 系统架构与安全综述]]
- 攻击分类：[[20_Research/Papers/L3-工控与电网安全/A_Taxonomy_of_Data_Attacks_in_Power_Systems|023 电力系统数据攻击分类学]]

## 原文摘要

> Smart grid uses the power of information technology to intelligently deliver energy to customers by using a two-way communication, and wisely meet the environmental requirements by facilitating the integration of green technologies. Although smart grid addresses several problems of the traditional grid, it faces a number of security challenges. Because communication has been incorporated into the electrical power with its inherent weaknesses, it has exposed the system to numerous risks. Several research papers have discussed these problems. However, most of them classified attacks based on confidentiality, integrity, and availability, and they excluded attacks which compromise other security criteria such as accountability. In addition, the existed security countermeasures focus on countering some specific attacks or protecting some specific components, but there is no global approach which combines these solutions to secure the entire system. The purpose of this paper is to provide a comprehensive overview of the relevant published works. First, we review the security requirements. Then, we investigate in depth a number of important cyber-attacks in smart grid to diagnose the potential vulnerabilities along with their impact. In addition, we proposed a cyber security strategy as a solution to address breaches, counter attacks, and deploy appropriate countermeasures. Finally, we provide some future research directions.
