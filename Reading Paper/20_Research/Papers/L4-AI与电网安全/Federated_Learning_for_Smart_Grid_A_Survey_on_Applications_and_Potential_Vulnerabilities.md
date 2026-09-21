---
document_id: "arxiv-2409.10764"
arxiv_id: "2409.10764"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2409.10764"
title: "Federated Learning for Smart Grid: A Survey on Applications and Potential Vulnerabilities"
zh_title: "联邦学习用于智能电网：应用与潜在脆弱性综述"
authors: ["Zikai Zhang", "Suman Rath", "Jiahao Xu", "Tingsong Xiao"]
published: "2024-09-16"
venue: "ACM Transactions on Cyber-Physical Systems 2025；arXiv:2409.10764"
domain: "L4-AI与电网安全"
level: "L4"
reading_order: 28
difficulty: "入门+"
tags: ["论文笔记", "L4-AI与电网安全", "联邦学习", "隐私保护", "综述", "必读"]
quality_score: 10
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 028 | 联邦学习用于智能电网：应用与潜在脆弱性综述

> [!abstract] 一句话
> **第一篇专门研究"联邦学习 × 智能电网"的综述**：按"发电—输配—用电"三阶段梳理 FL 应用，同时系统梳理 FL 自身的脆弱性，还开源了一个攻防框架 **FedGridShield**。

## 为什么这是 L4 的"总纲"

理由：
1. **首篇专注 FL+SG 的综述**（作者自己强调了这个定位）
2. **双向视角**：既讲"用 FL 保护电网"，也讲"FL 自己怎么被攻击"
3. **按电力业务阶段组织** → 直接对应电力工程视角
4. **开源框架 FedGridShield** → 你可以直接拿来跑实验

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Federated Learning for Smart Grid: A Survey on Applications and Potential Vulnerabilities |
| **作者** | Zikai Zhang, Suman Rath, Jiahao Xu, Tingsong Xiao（美国克莱姆森大学等） |
| **发表** | ACM Transactions on Cyber-Physical Systems（2025 已接收） |
| **发布** | 2024-09-16 |
| **分类** | cs.LG |
| **链接** | [arXiv](https://arxiv.org/abs/2409.10764) \| [PDF](https://arxiv.org/pdf/2409.10764) |
| **开源框架** | FedGridShield（论文中提到，含 SOTA 攻防方法实现） |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2409.10764_fig1.png]]

![[2409.10764_fig2.png]]

![[2409.10764_fig3.png]]

![[2409.10764_fig4.png]]

![[2409.10764_fig5.png]]

---


## 这篇论文在讲什么（白话版）

### 为什么智能电网需要联邦学习

> 原文：*"The Smart Grid (SG) is a critical energy infrastructure that collects real-time electricity usage data to forecast future energy demands using information and communication technologies (ICT). Due to growing concerns about data security and privacy in SGs, federated learning (FL) has emerged as a promising training framework."*

**逻辑链**：
```
智能电网要采集实时用电数据 → 用于负荷预测
  → 但数据涉及隐私、且分散在各方
    → 联邦学习：不共享原始数据，只共享模型
      → 在"隐私、效率、精度"三者间取得平衡
```

> 原文：*"FL offers a balance between privacy, efficiency, and accuracy in SGs by enabling collaborative model training without sharing private data from IoT devices."*

### 论文的组织方式：按电力业务三阶段

| 阶段 | 联邦学习应用 | 典型任务 |
|---|---|---|
| **1. 发电（Generation）** | 分布式发电预测 | 风电/光伏出力预测 |
| **2. 输配电（Transmission & Distribution）** | 状态估计、故障检测、FDIA 检测 | 跨区域协同建模 |
| **3. 用电（Consumption）** | 负荷预测、需求响应、用户行为分析 | 保护用户隐私 |

> **这个三阶段划分很实用** —— 你可以直接用它来定位自己的研究方向。

### 核心贡献二：FL 的潜在脆弱性

论文明确指出：**FL 在电网落地时会引入新的脆弱性**。

**FL 的典型攻击面**（综合论文 + 公开知识）：

| 攻击类型 | 攻击方式 | 后果 |
|---|---|---|
| **投毒攻击（Poisoning）** | 恶意客户端上传带毒梯度 | 全局模型被污染 |
| **后门攻击（Backdoor）** | 植入特定触发器 | 模型在特定输入下失效 |
| **梯度泄露（Gradient Leakage）** | 从梯度反推训练数据 | 隐私保护失效 |
| **拜占庭攻击（Byzantine）** | 部分客户端任意作恶 | 聚合结果偏离 |
| **搭便车（Free-rider）** | 上传虚假/无效梯度 | 影响收敛，白嫖模型 |
| **推理攻击（Inference）** | 成员推断、属性推断 | 泄露用户信息 |
| **模型窃取** | 通过查询反推模型 | 知识产权泄露 |

> **小电提醒**：注意"**梯度泄露**"这一条 —— 它直接否定了"联邦学习 = 隐私安全"的朴素认知。
> **"不上传原始数据"≠"不泄露信息"**，这是理解 FL 安全的关键。

### 核心贡献三：SOTA 与实际落地的差距

> 原文：*"we discuss the gap between state-of-the-art (SOTA) FL research and its practical applications in SGs, and we propose future research directions."*

**论文指出了"研究"和"落地"之间的鸿沟** —— 这是很有价值的批判性视角。

### 核心贡献四：FedGridShield 开源框架

> 原文：*"we also introduce FedGridShield, an open-source framework featuring implementations of SOTA attack and defense methods."*

**开源了攻防方法的实现** → 你可以直接用来做实验。

### 论文的独特定位

> 原文：*"Unlike traditional surveys addressing security issues in centralized machine learning methods for SG systems, this survey is the first to specifically examine the applications and security concerns unique to FL-based SG systems."*

**第一篇专门研究"FL-based 智能电网系统"的应用与安全问题的综述。**

## 用网安的话说（小电解读）

> 这篇论文给了你一个**完整的研究闭环**。

**闭环结构**：
```
电网需要隐私保护
  → 用联邦学习
    → 但 FL 自己有安全问题
      → 需要"安全联邦学习"
        → 但安全机制带来开销
          → 需要"效率-隐私-安全"的权衡
```

**三个关键的权衡三角**：

| 三角 | 冲突 |
|---|---|
| **隐私 ↔ 精度** | 加差分隐私 → 精度下降 |
| **安全 ↔ 效率** | 加密（如 Paillier）→ 计算开销大 |
| **鲁棒 ↔ 可用** | 抗投毒聚合（如 Krum）→ 收敛变慢 |

**→ 这三个三角，每一个都是一个可研究的方向。**

**对你的具体机会**：

1. **"FL 在电力场景的适用性"**
   > 通用 FL 研究很多，但**电力场景的特殊性**（实时性、异构性、数据分布差异大）研究不足。
   > 例如：电网里不同区域的数据分布差异极大（非独立同分布 non-IID）→ FL 收敛困难 → 这是一个真问题。

2. **"FL 攻防的电力特化"**
   > 通用 FL 攻防研究很多，但**电力场景的物理约束**没被利用。
   > 例如：投毒梯度如果导致模型输出违反物理约束 → 可以被检测出来。
   > → **"物理约束增强的鲁棒联邦聚合"** 是一个新颖方向。

3. **"FedGridShield 的复现与改进"**
   > 有开源框架 → 你可以直接上手 → 提出改进 → 对比实验 → 一篇论文。

**与你实验室方向的完美对接**：
- **"AI与数据安全"** ← 直接对口（FL 安全）
- **"工业AI与智能体"** ← 分布式智能体协同
- **"入侵检测"** ← 联邦入侵检测

> **小电判断**：**这可能是对你最"友好"的一个方向** —— 因为 FL 是你实验室的强项领域，而"电力 + FL 安全"的交叉文献相对少，你有明显的"主场优势"。

## 读完后你应该能回答

- [ ] 为什么智能电网需要联邦学习？
- [ ] FL 在发电/输配/用电三个阶段分别有什么应用？
- [ ] 联邦学习有哪些典型攻击？为什么"不共享数据"不等于"隐私安全"？
- [ ] 联邦学习中的三个主要权衡三角是什么？
- [ ] FedGridShield 是什么？

## 局限性

- **综述性质**，具体算法细节需查阅原始论文。
- 对"FL 在电网的**实时性约束**"讨论可能不足（电网要求毫秒级，FL 训练/通信开销大）。
- 提出的未来方向较多，**优先级不明确**。
- FedGridShield 的实际可用性需自行验证。

## 和你的方向有什么关系

- **这是 L4 的核心入口**，也是与你实验室方向最契合的一篇。
- **直接选题（按推荐度）**：
  1. **面向电力 FDIA 检测的鲁棒联邦聚合**（抗投毒）
  2. **非独立同分布（non-IID）场景下的联邦负荷预测**
  3. **物理约束增强的 FL 安全机制**
  4. **FL 中的后门攻击与检测（电力场景特化）**
- **立刻可做的行动**：
  1. 找到 FedGridShield 仓库，跑通基线
  2. 选一个数据集（如 TAMU 智能电网数据集）
  3. 复现一个投毒攻击 + 一个防御方法

## 概念关联

- 核心概念：[[联邦学习]] · [[智能电网]] · [[虚假数据注入攻击(FDIA)]] · [[电力负荷预测]] · [[对抗样本攻击]]
- 前置阅读：[[20_Research/Papers/L2-电力系统基础/Optimal_Distributed_Control_of_Reactive_Power_via_ADMM|015 ADMM 分布式优化]]（结构同构，可对照）
- 应用实例：[[20_Research/Papers/L4-AI与电网安全/Detection_of_False_Data_Injection_Attacks_in_Smart_Grid_A_Secure_Federated_Deep_Learning_Approach|029 联邦深度学习检测 FDIA]]
- 检测背景：[[20_Research/Papers/L3-工控与电网安全/A_Survey_of_Machine_Learning_Methods_for_Detecting_False_Data_Injection_Attacks|022 FDIA 检测的机器学习方法综述]]
- 安全总纲：[[20_Research/Papers/L3-工控与电网安全/A_Comprehensive_Survey_on_the_Security_of_Smart_Grid|016 智能电网安全综合综述]]

## 原文摘要

> The Smart Grid (SG) is a critical energy infrastructure that collects real-time electricity usage data to forecast future energy demands using information and communication technologies (ICT). Due to growing concerns about data security and privacy in SGs, federated learning (FL) has emerged as a promising training framework. FL offers a balance between privacy, efficiency, and accuracy in SGs by enabling collaborative model training without sharing private data from IoT devices. In this survey, we thoroughly review recent advancements in designing FL-based SG systems across three stages: generation, transmission and distribution, and consumption. Additionally, we explore potential vulnerabilities that may arise when implementing FL in these stages. Furthermore, we discuss the gap between state-of-the-art (SOTA) FL research and its practical applications in SGs, and we propose future research directions. Unlike traditional surveys addressing security issues in centralized machine learning methods for SG systems, this survey is the first to specifically examine the applications and security concerns unique to FL-based SG systems. We also introduce FedGridShield, an open-source framework featuring implementations of SOTA attack and defense methods. Our aim is to inspire further research into applications and improvements in the robustness of FL-based SG systems.
