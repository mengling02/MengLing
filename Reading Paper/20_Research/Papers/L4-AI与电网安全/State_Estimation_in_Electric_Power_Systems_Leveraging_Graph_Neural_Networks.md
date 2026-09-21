---
document_id: "arxiv-2201.04056"
arxiv_id: "2201.04056"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2201.04056"
title: "State Estimation in Electric Power Systems Leveraging Graph Neural Networks"
zh_title: "利用图神经网络进行电力系统状态估计"
authors: ["Ognjen Kundacina", "Mirsad Cosovic", "Dejan Vukobratovic"]
published: "2022-01-11"
venue: "2022 17th International Conference on Probabilistic Methods Applied to Power Systems (PMAPS)；arXiv:2201.04056"
domain: "L4-AI与电网安全"
level: "L4"
reading_order: 33
difficulty: "进阶"
tags: ["论文笔记", "L4-AI与电网安全", "图神经网络", "状态估计", "PMU"]
quality_score: 8
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 033 | 利用图神经网络进行电力系统状态估计

> [!abstract] 一句话
> 用 GNN 学"PMU 量测 → 状态"的映射，训练数据由传统线性状态估计求解器自动标注，实现**快速且准确**的状态估计。

## 为什么读它

这篇和 [[20_Research/Papers/L2-电力系统基础/Graph_Neural_Network-based_Power_Flow_Model|010]] 是一对：

| | 010（潮流） | 033（状态估计） |
|---|---|---|
| 任务 | 已知注入功率 → 算线路潮流 | 已知量测 → 算状态 |
| 方向 | 正向（仿真） | 反向（估计） |
| 方法 | GNN | GNN |

**读完这两篇，你就理解了"GNN 在电力系统里能干什么"。**

而且这篇特别讨论了**缺失数据敏感性** —— 这和安全问题（数据可用性攻击）直接相关。

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | State Estimation in Electric Power Systems Leveraging Graph Neural Networks |
| **作者** | Ognjen Kundacina, Mirsad Cosovic, Dejan Vukobratovic（塞尔维亚诺维萨德大学） |
| **发表** | 2022 17th International Conference on Probabilistic Methods Applied to Power Systems (PMAPS) |
| **发布** | 2022-01-11（6 页，6 图，会议论文） |
| **分类** | cs.LG |
| **链接** | [arXiv](https://arxiv.org/abs/2201.04056) \| [PDF](https://arxiv.org/pdf/2201.04056) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2201.04056_fig1.png]]

![[2201.04056_fig2.png]]

![[2201.04056_fig3.png]]

![[2201.04056_fig4.png]]

![[2201.04056_fig5.png]]

![[2201.04056_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 问题：PMU 采样快，但传统 SE 求解器慢

> 原文：*"Because phasor measurement units (PMUs) are increasingly being used in transmission power systems, there is a need for a fast SE solver that can take advantage of high sampling rates of PMUs."*

**矛盾**：
- PMU 采样率很高（每秒几十次甚至更多）
- 传统状态估计求解器（WLS 迭代）**计算慢**
- → **无法跟上 PMU 的采样速度** → 浪费了 PMU 的高采样率优势

**这就是这篇论文要解决的问题**：**做一个"快"的状态估计器**。

### 方法：GNN 学习"量测 → 状态"映射

> 原文：*"This paper proposes training a graph neural network (GNN) to learn the estimates given the PMU voltage and current measurements as inputs, with the intent of obtaining fast and accurate predictions during the evaluation phase."*

**输入**：PMU 的**电压和电流量测**
**输出**：**状态估计值**（复电压）
**目标**：**推理阶段又快又准**

### 训练数据怎么来？—— 合成数据 + 传统求解器标注

> 原文：*"GNN is trained using synthetic datasets, created by randomly sampling sets of measurements in the power system and labelling them with a solution obtained using a linear SE with PMUs solver."*

**这是一个很聪明的设计**：
```
随机采样量测配置
  → 用传统线性 SE 求解器算出"标准答案"
    → 作为标签训练 GNN
      → 推理时 GNN 直接输出结果（快！）
```

> **小电解读**：这叫做 **"知识蒸馏 / 代理模型（surrogate model）"**。
> 用慢但精确的传统方法生成标签，训练一个快模型来替代它。
> **这是"AI 加速科学计算"的标准范式**，你在很多领域都会看到。

### 关键发现：对缺失数据的敏感性

> 原文：*"The presented results display the accuracy of GNN predictions in various test scenarios and tackle the sensitivity of the predictions to the missing input data."*

**论文专门研究了"输入数据缺失时预测的准确性"** —— 这一点很重要（见下文）。

## 用网安的话说（小电解读）

> 这篇论文有两个对你特别有价值的点。

**价值一：它是"AI 替代传统求解器"的范式案例**

这个范式的一般形式：
```
传统方法：精确但慢
  → 用传统方法生成训练数据
    → 训练 AI 代理模型
      → 推理时用 AI（快）
        → 定期用传统方法校准（保精度）
```

**攻击视角**：**代理模型是一个新的攻击面**。
- 攻击者不需要攻破传统求解器（它可能很难攻破）
- 只需要攻击 **AI 代理模型**（对抗样本、投毒）
- → **"AI 化"实际上扩大了攻击面**

**价值二：缺失数据敏感性 → 数据可用性攻击**

论文研究"输入数据缺失时预测精度如何变化"。**从安全角度看**：
> **攻击者可以通过"删除数据"来攻击系统**（而不是篡改数据）。
> - 传统 SE：量测缺失 → 可观测性下降 → 但也可能仍可解
> - GNN：训练时没见过缺失模式 → **精度可能急剧下降**

**这就把 [[20_Research/Papers/L3-工控与电网安全/A_Taxonomy_of_Data_Attacks_in_Power_Systems|023 数据攻击分类学]] 里提到的"数据丢弃（dropped）"攻击具体化了**：
> **"面向 AI 状态估计器的数据可用性攻击"** —— 一个很新颖的方向。
> 论文研究了"缺失数据的影响"，但**没有从攻击者视角研究"如何最优地删除数据以最大化破坏"**。

**三个可延伸的方向**：

| 方向 | 说明 |
|---|---|
| **数据可用性攻击** | 最优删除哪些量测能让 GNN 估计误差最大？ |
| **对抗鲁棒性** | 对 PMU 量测加微小扰动 → 估计偏移 |
| **缺失数据鲁棒性** | 训练时随机 mask，提升对数据缺失的鲁棒性（防御） |

## 读完后你应该能回答

- [ ] 为什么 PMU 的普及要求"快速状态估计器"？
- [ ] 论文如何获得训练数据？（合成 + 传统求解器标注）
- [ ] 这种"代理模型"范式的优点和风险分别是什么？
- [ ] 为什么"数据缺失"对 GNN 状态估计是个威胁？

## 局限性

- **会议论文，篇幅短**（6 页），实验规模有限。
- 只用了**线性 SE** 生成标签，未涉及非线性场景。
- 未讨论**拓扑变化**时的泛化能力。
- **完全没有安全分析**（但讨论了缺失数据敏感性，算是一个间接的鲁棒性分析）。
- 未与其他 AI 方法（如 DNN、Transformer）做充分对比。

## 和你的方向有什么关系

- **这是"AI 替代传统算法"的入门案例**，帮你理解这个范式的机会与风险。
- **直接选题（推荐度）**：
  1. **面向 AI 状态估计器的数据可用性攻击**（新颖，论文间接提到但未做）
  2. **对抗鲁棒的 GNN 状态估计**（加对抗训练 / 物理约束）
  3. **缺失数据下的鲁棒状态估计**（防御侧）
- **技术储备**：GNN + 状态估计 + 代理模型 —— 三样都是热门技能。
- 与实验室方向对接：**"AI与数据安全"**（模型安全）、**"工业AI"**（AI 加速仿真）、**"入侵检测"**（异常量测识别）。

## 概念关联

- 核心概念：[[图神经网络]] · [[状态估计]] · [[虚假数据注入攻击(FDIA)]] · [[对抗样本攻击]] · [[工控安全测试床与数据集]]
- 前置阅读：[[20_Research/Papers/L2-电力系统基础/Graph_Neural_Network-based_Power_Flow_Model|010 基于 GNN 的潮流模型]] · [[20_Research/Papers/L2-电力系统基础/Roles_of_Dynamic_State_Estimation_in_Power_System_Modeling_Monitoring_and_Operation|008 动态状态估计的作用]]
- 攻击对照：[[20_Research/Papers/L3-工控与电网安全/Vulnerability_Analysis_and_Consequences_of_False_Data_Injection_Attack_on_Power_System_State_Estimation|024 FDIA 脆弱性分析]]
- 分类框架：[[20_Research/Papers/L3-工控与电网安全/A_Taxonomy_of_Data_Attacks_in_Power_Systems|023 电力系统数据攻击分类学]]（数据丢弃 vs 篡改）

## 原文摘要

> The goal of the state estimation (SE) algorithm is to estimate complex bus voltages as state variables based on the available set of measurements in the power system. Because phasor measurement units (PMUs) are increasingly being used in transmission power systems, there is a need for a fast SE solver that can take advantage of high sampling rates of PMUs. This paper proposes training a graph neural network (GNN) to learn the estimates given the PMU voltage and current measurements as inputs, with the intent of obtaining fast and accurate predictions during the evaluation phase. GNN is trained using synthetic datasets, created by randomly sampling sets of measurements in the power system and labelling them with a solution obtained using a linear SE with PMUs solver. The presented results display the accuracy of GNN predictions in various test scenarios and tackle the sensitivity of the predictions to the missing input data.
