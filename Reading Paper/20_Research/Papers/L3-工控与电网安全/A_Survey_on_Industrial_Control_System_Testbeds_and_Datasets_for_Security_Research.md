---
document_id: "arxiv-2102.05631"
arxiv_id: "2102.05631"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2102.05631"
title: "A Survey on Industrial Control System Testbeds and Datasets for Security Research"
zh_title: "面向安全研究的工业控制系统测试床与数据集综述"
authors: ["Mauro Conti", "Denis Donadel", "Federico Turrin"]
published: "2021-02-10"
venue: "arXiv (cs.CR)"
domain: "L3-工控与电网安全"
level: "L3"
reading_order: 20
difficulty: "入门"
tags: ["论文笔记", "L3-工控与电网安全", "测试床", "数据集", "实验基础", "必读"]
quality_score: 10
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 020 | 面向安全研究的工业控制系统测试床与数据集综述

> [!abstract] 一句话
> **做 ICS 安全研究，第一件事是"数据从哪来、实验在哪跑"** —— 这篇综述把所有公开测试床和数据集盘点了一遍，还给出了每个数据集上表现最好的 IDS 算法，等于**直接给你一份"基线对照表"**。

## 为什么这篇对你极其重要

你研一要发论文，**最大的现实障碍不是算法，是数据**。
这篇论文解决的正是这个问题：

1. **列出所有可用的测试床和数据集** → 你不用自己从零搭
2. **给出每个数据集上的 SOTA 基线** → 你的方法只要比它好就能发
3. **指出设计挑战与最佳实践** → 避免踩坑

> **小电强烈建议**：读完这篇后，**立刻选一个数据集下载下来**。

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | A Survey on Industrial Control System Testbeds and Datasets for Security Research |
| **作者** | Mauro Conti, Denis Donadel, Federico Turrin（意大利帕多瓦大学，Conti 组是安全领域知名团队） |
| **发布** | 2021-02-10 |
| **分类** | cs.CR |
| **链接** | [arXiv](https://arxiv.org/abs/2102.05631) \| [PDF](https://arxiv.org/pdf/2102.05631) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2102.05631_fig1.jpg]]

![[2102.05631_fig2.jpg]]

![[2102.05631_fig3.jpg]]

![[2102.05631_fig4.jpg]]

![[2102.05631_fig5.png]]

![[2102.05631_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 问题：ML 需要数据，但 ICS 数据稀缺

> 原文：*"these algorithms require a testing platform and a considerable amount of data to be trained and tested accurately."*

机器学习检测算法需要**大量数据**训练。但 ICS 场景下：
- 真实系统**不能拿来做实验**（核电站、化工厂、电网）
- 真实攻击样本**极其稀少**
- 数据涉及**商业机密和安全敏感**

**解决方案**：**测试床（testbed）** = 缩小的 ICS 或仿真环境 → 在测试床上复现攻击 → 收集数据 → 共享给社区。

### 论文的三块内容

**1）ICS 基础综述**
- 架构设计（现场层/控制层/监控层）
- 使用的设备（PLC、RTU、HMI、传感器）
- 实现的安全协议

**2）测试床与数据集盘点（核心贡献）**

论文收集、对比、描述了文献中的测试床和数据集，并给出：
- **关键挑战**（收集数据时要注意什么）
- **设计指南**（搭建测试床时的最佳实践）
- **每个数据集上表现最好的 IDS 算法** → **创建了 SOTA 基线**

**3）建议与最佳实践**

> 原文：*"we report advice and good practices on the development, the choice, and the utilization of testbeds, datasets, and IDSs."*

### 知名的 ICS 测试床与数据集（结合公开知识补充）

| 名称 | 类型 | 说明 |
|---|---|---|
| **SWaT**（Secure Water Treatment） | 物理测试床 | 新加坡 iTrust 的水处理系统，最著名的 ICS 数据集之一 |
| **WADI** | 物理测试床 | iTrust 的配水系统，SWaT 的扩展 |
| **EPIC** | 物理测试床 | iTrust 的电力基础设施测试床 |
| **Mississippi State / ORNL** | 电力数据集 | 电力系统网络攻击数据集 |
| **TAMU（Texas A&M）** | 电力数据集 | 智能电网 FDIA、继电器攻击等，ML 检测常用 |
| **ICSSIM** | 仿真框架 | 用 Docker 容器搭建 ICS 仿真测试床 |
| **EPICTWIN** | 数字孪生 | 电力数字孪生，用于安全测试与教育 |
| **PowerCyber / PowerCyber-ISU** | 电力测试床 | 电力 CPS 攻防测试床 |
| **MINICPS** | 仿真框架 | 基于 Python 的 CPS 仿真 |
| **SUTD / iTrust** | 多个 | 见 iTrust 官网 |
| **IEEE 14/30/57/118/300 节点** | 标准测试系统 | **不是数据集**，是标准电网拓扑（几乎所有电力论文都用） |

> **注意区分**：
> - **测试床（testbed）**：可运行的物理/仿真系统 → 用来**做实验**
> - **数据集（dataset）**：录制的数据 → 用来**训练/测试算法**
> - **标准测试系统（如 IEEE 118）**：拓扑定义 → 用来**建模**

## 用网安的话说（小电解读）

> 这篇论文是你的**"实验基础设施选型指南"**。

**给你的行动清单**：

**第一步：选一个数据集**
| 如果你想做… | 推荐数据集 |
|---|---|
| 电力系统攻击检测 | **TAMU 智能电网数据集**（FDIA、继电器攻击） |
| 通用 ICS 入侵检测 | **SWaT / WADI**（最成熟，论文最多，便于对比） |
| 工业协议流量分析 | Modbus/DNP3 抓包数据集 |
| 电力 CPS 攻击影响 | Mississippi State / ORNL 数据集 |

**第二步：选一个仿真环境**
| 需求 | 工具 |
|---|---|
| 电力潮流/最优潮流 | **MATPOWER / pandapower** |
| 电力动态仿真 | **ANDES** |
| 强化学习电网环境 | **PowerGridworld / Gym-ANM / andes_gym** |
| ICS 网络仿真 | **ICSSIM（Docker）** |
| 联合仿真 | **GridLAB-D + ns-3**、**EPICTWIN** |

**第三步：建立基线**
> 论文给出了**每个数据集上最好的 IDS 算法** → 你的方法必须超过它，或者说明为什么不同维度更好。

**关键洞察**：

1. **"有基线"是发论文的前提**
   > 为什么这个领域论文质量参差？因为**没有统一基准**。
   > 你在 A 数据集上做，他在 B 数据集上做，检测率 99% vs 95%，无法比较。
   > → **"统一基准评测"本身就是一篇好论文**。

2. **数据稀缺 = 你的机会**
   - 真实攻击样本少 → **合成攻击数据**（用 GAN/扩散模型生成）
   - 类别不平衡 → **少样本学习、异常检测**
   - 环境差异大 → **域适应、迁移学习**

3. **注意"物理可行性"**
   > 在电网数据集上做攻击注入，**必须满足物理约束**（不能出现负功率）。
   > 很多论文忽略了这一点 → 数据不真实 → 见 [[20_Research/Papers/L3-工控与电网安全/A_False_Sense_of_Security_Revisiting_the_State_of_Machine_Learning-Based_Industrial_Intrusion_Detection|026 "虚假安全感"]]

## 读完后你应该能回答

- [ ] 测试床（testbed）和数据集（dataset）有什么区别？
- [ ] 为什么 ICS 安全研究必须依赖测试床？
- [ ] 有哪些知名的 ICS 安全数据集？分别适合什么任务？
- [ ] 为什么"缺乏统一基准"是当前研究的问题？

## 局限性

- **2021 年的综述**，此后新增的数据集（如更细粒度的电力攻击数据）未覆盖。
- 测试床描述偏**定性**，缺乏统一的"保真度"量化指标。
- 数据集对比主要看"是否可用"，对其**物理真实性**评估不足。
- 未深入讨论**数据集的隐私与合规问题**（真实电网数据受严格管制）。

## 和你的方向有什么关系

- **这是你"开始做实验"的第一篇必读**。读完后立刻行动：下载数据集 + 跑通基线。
- **直接选题（低风险高产出）**：
  1. **在现有数据集上提出更好的检测方法**（有基线可对比）
  2. **跨数据集的泛化性研究**（A 数据集训练，B 数据集测试 → 域适应）
  3. **数据集质量评估框架**（评估现有数据集的物理真实性）
  4. **合成更真实的攻击数据**（生成模型 + 物理约束）
- **与你实验室方向的对接**：**"入侵检测"**（直接对口）、**"AI与数据安全"**（数据质量与投毒）。

## 概念关联

- 核心概念：[[工控安全测试床与数据集]] · [[入侵检测系统(IDS)]] · [[SCADA系统]] · [[虚假数据注入攻击(FDIA)]]
- 前置阅读：[[20_Research/Papers/L3-工控与电网安全/Architecture_and_Security_of_SCADA_Systems_A_Review|018 SCADA 系统架构与安全综述]]
- 后续阅读：[[20_Research/Papers/L3-工控与电网安全/A_False_Sense_of_Security_Revisiting_the_State_of_Machine_Learning-Based_Industrial_Intrusion_Detection|026 机器学习工控入侵检测的"虚假安全感"]]
- 攻击建模：[[20_Research/Papers/L3-工控与电网安全/Vulnerability_Analysis_and_Consequences_of_False_Data_Injection_Attack_on_Power_System_State_Estimation|024 FDIA 脆弱性分析]]

## 原文摘要

> The increasing digitization and interconnection of legacy Industrial Control Systems (ICSs) open new vulnerability surfaces, exposing such systems to malicious attackers. Furthermore, since ICSs are often employed in critical infrastructures (e.g., nuclear plants) and manufacturing companies (e.g., chemical industries), attacks can lead to devastating physical damages. In dealing with this security requirement, the research community focuses on developing new security mechanisms such as Intrusion Detection Systems (IDSs), facilitated by leveraging modern machine learning techniques. However, these algorithms require a testing platform and a considerable amount of data to be trained and tested accurately. To satisfy this prerequisite, Academia, Industry, and Government are increasingly proposing testbed (i.e., scaled-down versions of ICSs or simulations) to test the performances of the IDSs. Furthermore, to enable researchers to cross-validate security systems (e.g., security-by-design concepts or anomaly detectors), several datasets have been collected from testbeds and shared with the community. In this paper, we provide a deep and comprehensive overview of ICSs, presenting the architecture design, the employed devices, and the security protocols implemented. We then collect, compare, and describe testbeds and datasets in the literature, highlighting key challenges and design guidelines to keep in mind in the design phases. Furthermore, we enrich our work by reporting the best performing IDS algorithms tested on every dataset to create a baseline in state of the art for this field. Finally, driven by knowledge accumulated during this survey's development, we report advice and good practices on the development, the choice, and the utilization of testbeds, datasets, and IDSs.

> [!tip] 行动建议
> **本周末任务**：选一个数据集（推荐 SWaT 或 TAMU），下载下来，用最简单的算法（如 Isolation Forest 或 Autoencoder）跑一个基线。
> **跑通了，你就正式"入门"了。**
