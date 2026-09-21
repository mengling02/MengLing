---
document_id: "arxiv-2008.06926"
arxiv_id: "2008.06926"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2008.06926"
title: "A Survey of Machine Learning Methods for Detecting False Data Injection Attacks in Power Systems"
zh_title: "电力系统虚假数据注入攻击检测的机器学习方法综述"
authors: ["Ali Sayghe", "Yaodan Hu", "Ioannis Zografopoulos", "XiaoRui Liu", "Raj Gautam Dutta", "Yier Jin", "Charalambos Konstantinou"]
published: "2020-08-16"
venue: "arXiv (eess.SY)"
domain: "L3-工控与电网安全"
level: "L3"
reading_order: 22
difficulty: "入门+"
tags: ["论文笔记", "L3-工控与电网安全", "FDIA检测", "机器学习", "综述", "必读"]
quality_score: 10
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 022 | 电力系统虚假数据注入攻击检测的机器学习方法综述

> [!abstract] 一句话
> **FDIA 检测的 ML 方法大全**：从传统 BDD 的局限讲起，系统梳理各类机器学习检测方法，是"防御侧"最完整的一篇综述。

## 为什么这是"防御侧"的核心文献

前面几篇讲"怎么攻击"（[[20_Research/Papers/L3-工控与电网安全/Comprehensive_Survey_and_Taxonomies_of_False_Injection_Attacks_in_Smart_Grid|021]]），这篇讲**"怎么检测"**。

对你（网安 + 入侵检测背景）来说，**这篇的技术栈你最熟悉** —— 它讲的都是分类、异常检测、特征工程，正是你的主场。

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | A Survey of Machine Learning Methods for Detecting False Data Injection Attacks in Power Systems |
| **作者** | Ali Sayghe, Yaodan Hu, Ioannis Zografopoulos, XiaoRui Liu, Raj Gautam Dutta, Yier Jin, Charalambos Konstantinou（佛罗里达州立大学、中佛罗里达大学等） |
| **发布** | 2020-08-16 |
| **分类** | eess.SY |
| **类型** | 综述 |
| **链接** | [arXiv](https://arxiv.org/abs/2008.06926) \| [PDF](https://arxiv.org/pdf/2008.06926) |

> **小电注**：作者团队里 **Yier Jin** 是硬件安全与 IoT 安全领域的知名学者，说明这个方向吸引了跨领域的安全研究者。

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2008.06926_fig1.png]]

![[2008.06926_fig2.png]]

![[2008.06926_fig3.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：FDIA 的完整攻击链（论文讲得很清楚）

> 原文：*"Adversaries can successfully perform FDIAs in order to manipulate the power system State Estimation (SE) by compromising sensors or modifying system data."*

**关键链条**：
```
攻击者 → 攻陷传感器 / 篡改系统数据
  → 操纵状态估计（SE）
    → EMS 得到错误的状态
      → 错误决策
```

### 为什么传统 BDD 不够用

> 原文：*"FDIAs can bypass BDD modules to inject malicious data vectors into a subset of measurements without being detected, and thus manipulate the results of the SE process."*

**FDIA 能绕过 BDD 模块**，注入恶意数据而不被检测 —— 这就是经典结论（见 [[不良数据检测与状态估计防御]]）。

**BDD 的定位**（原文）：SE 流程里包含 BDD 算法，用来消除量测误差（**比如传感器故障**）。
> **注意这个措辞**："in case of sensor failures" —— BDD 本来是设计来对付**随机故障**的，不是对付**恶意攻击**的。
> **这就是问题的根源**：用"故障检测"的思路去做"攻击检测"，天然不够。

### 为什么用机器学习

> 原文：*"data-driven solutions based on machine learning algorithms have been widely adopted for detecting malicious manipulation of sensor data due to their fast execution times and accurate results."*

两个理由：**执行快（fast execution times）** + **结果准（accurate results）**。

### 论文覆盖的 ML 方法（分类整理）

论文综述了当时最前沿的 ML 检测方法，大致可分为：

| 类别 | 方法 | 特点 |
|---|---|---|
| **监督学习** | SVM、决策树、随机森林、KNN、MLP | 需要标注数据；准确率高但难泛化到未知攻击 |
| **无监督学习** | 自编码器（AE）、PCA、聚类、One-Class SVM | 只需正常数据；适合未知攻击检测 |
| **深度学习** | CNN、LSTM、GAN、深度自编码器 | 自动特征提取；需要大量数据 |
| **集成学习** | Bagging、Boosting、Stacking | 提升鲁棒性 |
| **半监督** | 少量标注 + 大量未标注 | 缓解标注稀缺 |

**常用特征**：
- 原始量测量 $z$
- 状态估计残差 $r = z - H\hat{x}$
- 量测变化率 $\Delta z$
- 物理导出的特征（功率不平衡量）

## 用网安的话说（小电解读）

> 这篇论文对你来说，是**"把 IT 入侵检测迁移到电力量测数据"的操作手册**。

**迁移映射表**：

| IT 入侵检测 | 电网 FDIA 检测 | 差异 |
|---|---|---|
| 网络流量特征 | **量测量 $z$ + 残差 $r$** | 电网数据有物理结构 |
| 攻击样本标注 | **极少**（真实攻击数据稀缺） | 更依赖无监督 |
| 类别不平衡 | **更严重**（攻击样本 <1%） | 需要特殊处理 |
| 检测延迟容忍 | **毫秒级要求**（不能拖慢实时控制） | 约束更紧 |
| 误报代价 | 分析师被打扰 | **可能误切线路** |
| 对抗鲁棒性 | 已有研究 | **电网场景研究少** |

**关键技术洞察**：

1. **"特征工程"是胜负关键**
   > 在电网里，**物理导出的特征（残差、功率不平衡）比原始量测更有效**。
   > 因为攻击者可以改量测值，但**很难让物理关系自洽**（除非他掌握完整拓扑）。
   > → **"物理信息特征工程"是电网检测的独特优势。**

2. **无监督方法的价值被低估**
   - 真实攻击样本稀缺 → 监督学习在现实中难落地
   - **自编码器、One-Class SVM 这类"只学正常行为"的方法更实用**
   - 但会面对"正常行为本身有噪声"的问题

3. **这篇论文的隐含警告**
   > 论文提到 ML 方法"准确率高"，但**没有讨论这些方法在未知攻击上的表现**。
   > 而下一篇 [[20_Research/Papers/L3-工控与电网安全/A_False_Sense_of_Security_Revisiting_the_State_of_Machine_Learning-Based_Industrial_Intrusion_Detection|026]] 正是打了这个脸：**未知攻击检测率会暴跌到 3.2%~14.7%**。
   > **两篇对照读，你会看到这个领域的"真实水位"。**

## 读完后你应该能回答

- [ ] 为什么传统 BDD 无法检测 FDIA？
- [ ] 为什么 BDD 原本是设计来对付"传感器故障"而不是"攻击"的？
- [ ] FDIA 检测常用的特征有哪些？
- [ ] 监督学习和无监督学习在 FDIA 检测中各自的优缺点是什么？

## 局限性

- **2020 年的综述**，未包含 Transformer、图神经网络、联邦学习等新方法。
- **没有讨论对抗鲁棒性**（检测器本身被攻击会怎样）—— 这是明显的缺口。
- 对各类方法的**实验对比不充分**（不同论文用不同数据集，无法横向比较）。
- 对**实时性约束**（能否满足调度毫秒级要求）讨论不足。

## 和你的方向有什么关系

- **这是你最可能"直接上手"的方向**：技术栈（分类/异常检测）与你的背景高度重合。
- **直接选题（按推荐度）**：
  1. **对抗鲁棒的 FDIA 检测**（论文没做，是缺口）
  2. **物理信息增强的检测特征工程**
  3. **跨系统泛化**（在 IEEE 14 训练，在 IEEE 118 测试）
  4. **未知攻击检测**（对接 [[20_Research/Papers/L3-工控与电网安全/A_False_Sense_of_Security_Revisiting_the_State_of_Machine_Learning-Based_Industrial_Intrusion_Detection|026]] 揭示的问题）
- 与实验室方向对接：**"入侵检测"**（核心对口）、**"AI与数据安全"**（模型安全）、**"工业AI"**（工业场景 ML）。

## 概念关联

- 核心概念：[[虚假数据注入攻击(FDIA)]] · [[不良数据检测与状态估计防御]] · [[入侵检测系统(IDS)]] · [[状态估计]] · [[工控安全测试床与数据集]]
- 攻击侧：[[20_Research/Papers/L3-工控与电网安全/Comprehensive_Survey_and_Taxonomies_of_False_Injection_Attacks_in_Smart_Grid|021 FDIA 综合综述]] · [[20_Research/Papers/L3-工控与电网安全/Vulnerability_Analysis_and_Consequences_of_False_Data_Injection_Attack_on_Power_System_State_Estimation|024 FDIA 脆弱性分析]]
- 防御侧：[[20_Research/Papers/L3-工控与电网安全/Graphical_Methods_for_Defense_Against_False-data_Injection_Attacks|025 图方法防御 FDIA]]
- **必读对照**：[[20_Research/Papers/L3-工控与电网安全/A_False_Sense_of_Security_Revisiting_the_State_of_Machine_Learning-Based_Industrial_Intrusion_Detection|026 机器学习工控入侵检测的"虚假安全感"]]
- AI 方法延伸：[[20_Research/Papers/L4-AI与电网安全/Detection_of_False_Data_Injection_Attacks_in_Smart_Grid_A_Secure_Federated_Deep_Learning_Approach|029 联邦深度学习检测 FDIA]] · [[20_Research/Papers/L4-AI与电网安全/State_Estimation_in_Electric_Power_Systems_Leveraging_Graph_Neural_Networks|033 用 GNN 做状态估计]]

## 原文摘要

> Over the last decade, the number of cyberattacks targeting power systems and causing physical and economic damages has increased rapidly. Among them, False Data Injection Attacks (FDIAs) is a class of cyberattacks against power grid monitoring systems. Adversaries can successfully perform FDIAs in order to manipulate the power system State Estimation (SE) by compromising sensors or modifying system data. SE is an essential process performed by the Energy Management System (EMS) towards estimating unknown state variables based on system redundant measurements and network topology. SE routines include Bad Data Detection (BDD) algorithms to eliminate errors from the acquired measurements, e.g., in case of sensor failures. FDIAs can bypass BDD modules to inject malicious data vectors into a subset of measurements without being detected, and thus manipulate the results of the SE process. In order to overcome the limitations of traditional residual-based BDD approaches, data-driven solutions based on machine learning algorithms have been widely adopted for detecting malicious manipulation of sensor data due to their fast execution times and accurate results. This paper provides a comprehensive review of the most up-to-date machine learning methods for detecting FDIAs against power system SE algorithms.
