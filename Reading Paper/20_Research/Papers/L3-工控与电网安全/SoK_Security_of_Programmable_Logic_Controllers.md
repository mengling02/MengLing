---
document_id: "arxiv-2403.00280"
arxiv_id: "2403.00280"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2403.00280"
title: "SoK: Security of Programmable Logic Controllers"
zh_title: "SoK：可编程逻辑控制器的安全"
authors: ["Efrén López-Morales", "Ulysse Planta", "Carlos Rubio-Medrano", "Ali Abbasi", "Alvaro A. Cardenas"]
published: "2024-03-01"
venue: "USENIX Security Symposium (33rd)；arXiv:2403.00280"
domain: "L3-工控与电网安全"
level: "L3"
reading_order: 27
difficulty: "入门+"
tags: ["论文笔记", "L3-工控与电网安全", "PLC", "SoK", "顶会论文"]
quality_score: 10
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 027 | SoK：可编程逻辑控制器的安全

> [!abstract] 一句话
> **USENIX Security 顶会论文**：系统化梳理（SoK）过去 17 年 PLC 安全研究，提出新的 PLC/ICS 威胁分类学，并指出"如果被忽视可能导致灾难性攻击"的研究空白。

## 为什么读它

- **发表在美国 USENIX Security**（安全领域四大顶会之一）→ **质量保证**
- **SoK（Systematization of Knowledge）** 是一种特殊的论文类型：**不做新实验，而是把已有知识系统化**
- **PLC 是 OT 安全的核心**：它是连接"信息世界"和"物理世界"的那个点（论文原话）
- 提出了**新的威胁分类学** → 你可以直接用于自己的威胁建模

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | SoK: Security of Programmable Logic Controllers |
| **作者** | Efrén López-Morales, Ulysse Planta, Carlos Rubio-Medrano, Ali Abbasi, Alvaro A. Cardenas（德州农工大学、俄勒冈州立大学等） |
| **发表** | 第 33 届 USENIX Security Symposium（2024） |
| **发布** | 2024-03-01（arXiv 扩展版：25 页，13 图） |
| **链接** | [arXiv](https://arxiv.org/abs/2403.00280) \| [PDF](https://arxiv.org/pdf/2403.00280) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2403.00280_fig1.png]]

![[2403.00280_fig2.png]]

![[2403.00280_fig3.png]]

![[2403.00280_fig4.jpeg]]

---


## 这篇论文在讲什么（白话版）

### 背景：PLC 为什么是关键目标

> 原文：*"Billions of people rely on essential utility and manufacturing infrastructures such as water treatment plants, energy management, and food production. Our dependence on reliable infrastructures makes them valuable targets for cyberattacks."*

**数十亿人依赖水处理、能源管理、食品生产等基础设施 → 它们是有价值的攻击目标。**

> 原文：*"One of the prime targets for adversaries attacking physical infrastructures are Programmable Logic Controllers (PLCs) because they connect the cyber and physical worlds."*

**PLC 是首要目标，因为它连接了"信息世界"和"物理世界"。**

> **小电点评**：这句话是整个 OT 安全的核心。PLC 就是那个"数字指令变成物理动作"的转换点。
> 攻下 PLC = 可以直接控制物理世界。

### 什么是 SoK 论文

**Systematization of Knowledge（知识系统化）**：
- 不是提出新方法
- 而是**把某个领域已有的知识重新组织、分类、批判**
- 价值在于：**给后来者一张清晰的地图** + **指出真正的空白**

> 在顶会发表 SoK 是**很难的**（因为要有独到洞察），所以这篇的质量可信度高。

### 论文的贡献

**1）深入分析 PLC 攻击与防御**

**2）发现 17 年研究的趋势**
> 原文：*"we discover trends in the security of PLCs from the last 17 years of research"*

**3）提出新的 PLC/ICS 威胁分类学**
> 原文：*"We introduce a novel threat taxonomy for PLCs and Industrial Control Systems (ICS)."*

**4）指出研究空白**
> 原文：*"we identify and point out research gaps that, if left ignored, could lead to new catastrophic attacks against critical infrastructures."*

**"如果被忽视，可能导致新的灾难性攻击"** —— 这是很强的措辞，说明作者认为这些空白很危险。

## 用网安的话说（小电解读）

> 这篇论文给你的价值，是**"PLC 安全的全景图 + 空白清单"**。

**PLC 安全的攻击面（综合论文内容 + 公开知识）**：

| 层面 | 攻击点 | 例子 |
|---|---|---|
| **固件层** | 固件篡改、后门 | 固件逆向、植入恶意逻辑 |
| **逻辑层** | 控制逻辑篡改（Ladder Logic / ST） | 修改梯形图，让设备异常动作 |
| **通信层** | 协议攻击（Modbus/DNP3/Profinet） | 伪造指令、重放 |
| **工程软件层** | 工程站被攻破 | 通过工程师站下载恶意逻辑 |
| **物理层** | 侧信道、物理接触 | 功耗分析、直接接线 |
| **供应链** | 厂商固件/库被污染 | 出厂即带后门 |

**"逻辑层攻击"特别值得注意**：
> 传统 IT 安全关注"代码漏洞"，但 PLC 的攻击可以是**"合法的逻辑修改"**。
> 攻击者不需要利用漏洞 —— 他有工程师站权限，**正常下载一份恶意梯形图**就行。
> → **这对应 [[20_Research/Papers/L1-零基础起步/乌克兰电网攻击事件复盘|007 乌克兰事件]] 里"用合法凭据做非法事"的思路。**
> → **基于行为的检测**（而非签名检测）在这里是必需的。

**论文指出的"研究空白"（你的机会）**：

虽然论文具体列举的空白需要读原文，但结合领域现状，常见的空白包括：

| 空白 | 说明 |
|---|---|
| **PLC 固件安全** | 固件分析、完整性验证，厂商封闭、研究困难 |
| **逻辑层异常检测** | 检测"合法但恶意"的逻辑，非常难 |
| **物理-逻辑一致性校验** | 用物理过程验证 PLC 逻辑是否被篡改 |
| **实时性约束下的安全** | PLC 扫描周期毫秒级，安全机制不能拖慢 |
| **老旧 PLC 的改造** | 大量在役设备无法升级 |
| **跨厂商的统一安全框架** | 各厂商私有协议、私有工具链 |

**对你最直接的启发**：
> **"用物理过程的一致性来检测 PLC 逻辑篡改"** —— 这是一个很有前景的方向。
> 因为攻击者可以改逻辑、可以伪造通信，但**很难让物理过程自洽**（除非他完全理解工艺流程）。

## 读完后你应该能回答

- [ ] 为什么 PLC 是 OT 攻击的首要目标？
- [ ] PLC 的攻击面有哪些层面？
- [ ] 什么是 SoK 论文？它的价值在哪？
- [ ] 为什么"逻辑层攻击"特别难检测？
- [ ] 物理一致性校验为什么能帮助检测 PLC 攻击？

## 局限性

- **SoK 性质**，不提供新方法或实验数据。
- 面向 PLC 通用场景，**电力系统特有的问题**（如 IEC 61850、保护装置）讨论有限。
- 论文的威胁分类学虽新，但**是否被社区广泛接受还需时间**。
- 17 年的研究跨度，早期工作的技术细节可能与现代 PLC 差异较大。

## 和你的方向有什么关系

- **这是 OT 安全的"高质量入口"**：顶会论文，视野和严谨性都有保证。
- **直接选题**：
  1. **PLC 逻辑层的异常检测**（难，但价值高）
  2. **物理-逻辑一致性校验**（电力场景的独特优势）
  3. **PLC 固件完整性验证**（工程价值高）
  4. **面向电力保护装置的类似 SoK**（如果你想要一篇高影响力综述）
- **写作启示**：**SoK/综述类论文**是建立学术影响力的高效方式 —— 引这篇论文的人，都会看到你的工作。
- 与实验室方向对接：**"程序逆向"**（PLC 固件逆向！这是你实验室的明确方向）、**"入侵检测"**、**"工业AI与智能体"**。

> [!tip] 小电的观察
> 你实验室有**"程序逆向"**方向。PLC 固件逆向正好是**逆向工程 + 工控安全**的交叉点，而且文献相对少。
> 这是一个和你实验室方向**高度契合**的选题切入点。

## 概念关联

- 核心概念：[[SCADA系统]] · [[入侵检测系统(IDS)]] · [[IEC 61850]] · [[工控安全测试床与数据集]] · [[电力信息物理系统(CPS)]]
- 前置阅读：[[20_Research/Papers/L3-工控与电网安全/Architecture_and_Security_of_SCADA_Systems_A_Review|018 SCADA 系统架构与安全综述]] · [[20_Research/Papers/L3-工控与电网安全/Network_Security_in_the_Industrial_Control_System_A_Survey|019 ICS 网络安全综述]]
- 对照阅读：[[20_Research/Papers/L3-工控与电网安全/A_False_Sense_of_Security_Revisiting_the_State_of_Machine_Learning-Based_Industrial_Intrusion_Detection|026 机器学习工控入侵检测的"虚假安全感"]]
- 攻击案例：[[20_Research/Papers/L1-零基础起步/乌克兰电网攻击事件复盘|007 乌克兰电网攻击事件复盘]]

## 原文摘要

> Billions of people rely on essential utility and manufacturing infrastructures such as water treatment plants, energy management, and food production. Our dependence on reliable infrastructures makes them valuable targets for cyberattacks. One of the prime targets for adversaries attacking physical infrastructures are Programmable Logic Controllers (PLCs) because they connect the cyber and physical worlds. In this study, we conduct the first comprehensive systematization of knowledge that explores the security of PLCs: We present an in-depth analysis of PLC attacks and defenses and discover trends in the security of PLCs from the last 17 years of research. We introduce a novel threat taxonomy for PLCs and Industrial Control Systems (ICS). Finally, we identify and point out research gaps that, if left ignored, could lead to new catastrophic attacks against critical infrastructures.
