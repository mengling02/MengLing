---
document_id: "arxiv-2103.10594"
arxiv_id: "2103.10594"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2103.10594"
title: "Comprehensive Survey and Taxonomies of False Injection Attacks in Smart Grid: Attack Models, Targets, and Impacts"
zh_title: "智能电网虚假数据注入攻击的综合综述与分类：攻击模型、目标与影响"
authors: ["Haftu Tasew Reda", "Adnan Anwar", "Abdun Mahmood"]
published: "2021-03-19"
venue: "Renewable and Sustainable Energy Reviews, Vol. 163, July 2022, 112423；arXiv:2103.10594"
domain: "L3-工控与电网安全"
level: "L3"
reading_order: 21
difficulty: "入门+"
tags: ["论文笔记", "L3-工控与电网安全", "虚假数据注入", "FDIA", "分类体系", "必读"]
quality_score: 10
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 021 | 智能电网虚假数据注入攻击的综合综述与分类

> [!abstract] 一句话
> **FDIA 领域最系统的分类学论文**：按"对抗模型（adversarial models）→ 攻击目标（attack targets）→ 影响（impacts）"三条线，把整个 FDIA 研究空间切得清清楚楚。

## 为什么这是 FDIA 方向的"必读核心"

[[20_Research/Papers/L1-零基础起步/面向电力信息物理系统的虚假数据注入攻击研究综述|003]] 是中文入门，这篇是**英文的体系化版本**，而且：

- 发表在 **Renewable and Sustainable Energy Reviews**（影响因子很高的能源类期刊）→ 说明这个方向受能源领域认可
- **分类学（taxonomies）** 做得很细 → 你可以直接拿来做**文献综述的分类框架**
- 明确指出了现有研究的**技术局限**和**未来方向** → 选题清单

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Comprehensive Survey and Taxonomies of False Injection Attacks in Smart Grid: Attack Models, Targets, and Impacts |
| **作者** | Haftu Tasew Reda, Adnan Anwar, Abdun Mahmood（澳大利亚迪肯大学） |
| **发表** | Renewable and Sustainable Energy Reviews, Vol. 163, July 2022, 112423 |
| **arXiv** | 2021-03-19 上传（24 页双栏，基于 IEEE Transactions 文章准备） |
| **链接** | [arXiv](https://arxiv.org/abs/2103.10594) \| [PDF](https://arxiv.org/pdf/2103.10594) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2103.10594_fig1.png]]

![[2103.10594_fig2.png]]

![[2103.10594_fig3.png]]

![[2103.10594_fig4.png]]

![[2103.10594_fig5.png]]

![[2103.10594_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：智能电网的"融合代价"

> 原文：*"Smart Grid has rapidly transformed the centrally controlled power system into a massively interconnected cyber-physical system that benefits from the revolutions happening in the communications (e.g. 5G) and the growing proliferation of the Internet of Things devices (such as smart metres and intelligent electronic devices)."*

**演进链条**：
```
集中控制电力系统
  → 深度互联的信息物理系统（5G + 海量 IoT）
    → 效率提升、竞争力增强
      → 但引入了大量脆弱性 → 数据可用性、完整性、机密性被破坏
```

### FDIA 的定位

> 原文：*"Recently, false data injection (FDI) has become one of the most critical cyberattacks, and appears to be a focal point of interest for both research and industry."*

**"最关键的工控攻击之一，学术界和工业界共同关注的焦点"**。

### 论文的三大分类维度（核心贡献）

论文明确说关注三点：

**1）对抗模型（Adversarial Models）**

即"攻击者具备什么能力"：

| 维度 | 类型 | 说明 |
|---|---|---|
| **知识水平** | 完全信息 / 部分信息 / 盲攻击 | 是否知道拓扑 $H$ |
| **资源能力** | 单点 / 多点；有限/无限预算 | 能改几个量测 |
| **访问方式** | 直接物理访问 / 远程网络访问 | 攻击路径 |
| **目标导向** | 随机 / 定向 | 是否针对特定状态量 |
| **隐蔽性** | 严格隐蔽 / 近似隐蔽 / 非隐蔽 | 是否触发 BDD |

**2）攻击目标（Attack Targets）**

| 目标 | 说明 |
|---|---|
| **状态估计** | 最经典的目标 |
| **负荷预测** | 影响调度决策 |
| **自动发电控制（AGC）** | 影响频率 |
| **经济调度 / 市场** | 影响经济性 |
| **保护系统** | 影响可靠性 |
| **广域监测（PMU）** | 影响态势感知 |
| **分布式能源/微网控制** | 新型目标 |

**3）影响（Impacts）**

| 层级 | 影响 |
|---|---|
| **数据层** | 状态估计偏差、错误告警 |
| **控制层** | 错误控制动作 |
| **物理层** | 设备过载、电压越限、频率偏差 |
| **系统层** | 失稳、连锁故障、大面积停电 |
| **经济层** | 市场操纵、经济损失 |

### 论文的结论：技术局限 + 未来方向

> 原文：*"a range of technical limitations of existing false data attack research is identified, and a number of future research directions is recommended."*

## 用网安的话说（小电解读）

> 这篇论文的分类学，可以直接当你的**"论文索引系统"**。

**给你的实用工具：三维定位法**

当你读任何一篇 FDIA 论文时，问自己三个问题：

```
1. 它假设攻击者知道什么？  → 对抗模型
2. 它攻击哪个环节？        → 攻击目标
3. 它关心什么后果？        → 影响层级
```

**这个框架的威力**：你会发现**大量论文挤在同一个格子里**：
- 完全信息 + 状态估计 + 数据层影响 → **最卷的区域**
- 部分信息 + 分布式能源控制 + 物理层影响 → **相对空白**

**"填格子"就是选题策略**：找一个格子，看看里面有没有人。

**几个特别值得注意的空白（综合论文的局限分析 + 公开知识）**：

| 空白方向 | 为什么空白 | 机会 |
|---|---|---|
| **部分信息 + 拓扑时变** | 数学难度大 | 用学习方法估计 $H$ |
| **FDIA + 新能源**（逆变器控制） | 新场景，模型复杂 | 直接对接"新型电力系统" |
| **FDIA 的经济影响量化** | 跨学科 | 需要市场建模能力 |
| **FDIA 与物理约束的博弈** | 需要精确物理模型 | 物理信息 ML |
| **隐蔽性 vs 破坏性的权衡** | 需要多目标优化 | 帕累托前沿分析 |

**一个重要提醒**：
> 论文提到 FDI 攻击"**同时**破坏数据可用性、完整性、机密性"。
> 但传统 FDIA 主要破坏**完整性**。**破坏可用性的 FDIA**（如选择性丢弃数据，让状态估计不可观）是一个相对新颖的角度。

## 读完后你应该能回答

- [ ] FDIA 的"对抗模型"可以从哪些维度刻画？
- [ ] FDIA 能攻击哪些目标？除了状态估计还有哪些？
- [ ] FDIA 的影响可以分为哪几个层级？
- [ ] 如何用"三维定位法"快速判断一篇 FDIA 论文的位置？

## 局限性

- **综述性质**，具体攻击构造的数学细节需查阅原始论文。
- 分类框架虽然系统，但**各类之间仍有交叉**（一篇论文可能同时属于多个类别）。
- 对**防御方法**的梳理不如攻击部分细致（防御可看 [[20_Research/Papers/L3-工控与电网安全/A_Survey_of_Machine_Learning_Methods_for_Detecting_False_Data_Injection_Attacks|022]]）。
- 未涉及 LLM、扩散模型等 2022 年后的新方法。

## 和你的方向有什么关系

- **这是你写 FDIA 相关论文时的"分类学基础"**：论文的 Related Work 部分可以按这三个维度组织。
- **直接选题（按推荐度）**：
  1. **部分信息/盲 FDIA 在新型电力系统场景下的攻击构造**
  2. **FDIA 对分布式能源控制的攻击与检测**（新场景）
  3. **多阶段协同 FDIA**（呼应 [[20_Research/Papers/L3-工控与电网安全/A_Comprehensive_Survey_on_the_Security_of_Smart_Grid|016]] 提到的协同攻击）
- 与实验室方向对接：**"AI与数据安全"**（数据完整性）、**"入侵检测"**（异常检测）。

## 概念关联

- 核心概念：[[虚假数据注入攻击(FDIA)]] · [[状态估计]] · [[不良数据检测与状态估计防御]] · [[智能电网]] · [[电力负荷预测]]
- 中文前置：[[20_Research/Papers/L1-零基础起步/面向电力信息物理系统的虚假数据注入攻击研究综述|003]]
- 攻击构造：[[20_Research/Papers/L3-工控与电网安全/Vulnerability_Analysis_and_Consequences_of_False_Data_Injection_Attack_on_Power_System_State_Estimation|024 FDIA 脆弱性分析]]
- 防御方法：[[20_Research/Papers/L3-工控与电网安全/A_Survey_of_Machine_Learning_Methods_for_Detecting_False_Data_Injection_Attacks|022 FDIA 检测的机器学习方法综述]] · [[20_Research/Papers/L3-工控与电网安全/Graphical_Methods_for_Defense_Against_False-data_Injection_Attacks|025 图方法防御 FDIA]]
- 分类学对照：[[20_Research/Papers/L3-工控与电网安全/A_Taxonomy_of_Data_Attacks_in_Power_Systems|023 电力系统数据攻击分类学]]

## 原文摘要

> Smart Grid has rapidly transformed the centrally controlled power system into a massively interconnected cyber-physical system that benefits from the revolutions happening in the communications (e.g. 5G) and the growing proliferation of the Internet of Things devices (such as smart metres and intelligent electronic devices). While the convergence of a significant number of cyber-physical elements has enabled the Smart Grid to be far more efficient and competitive in addressing the growing global energy challenges, it has also introduced a large number of vulnerabilities culminating in violations of data availability, integrity, and confidentiality. Recently, false data injection (FDI) has become one of the most critical cyberattacks, and appears to be a focal point of interest for both research and industry. To this end, this paper presents a comprehensive review in the recent advances of the FDI attacks, with particular emphasis on 1) adversarial models, 2) attack targets, and 3) impacts in the Smart Grid infrastructure. This review paper aims to provide a thorough understanding of the incumbent threats affecting the entire spectrum of the Smart Grid. Related literature are analysed and compared in terms of their theoretical and practical implications to the Smart Grid cybersecurity. In conclusion, a range of technical limitations of existing false data attack research is identified, and a number of future research directions is recommended.
