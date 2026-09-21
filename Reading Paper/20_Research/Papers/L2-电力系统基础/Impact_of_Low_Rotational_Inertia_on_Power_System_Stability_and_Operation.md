---
document_id: "arxiv-1312.6435"
arxiv_id: "1312.6435"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/1312.6435"
title: "Impact of Low Rotational Inertia on Power System Stability and Operation"
zh_title: "低转动惯量对电力系统稳定性与运行的影响"
authors: ["Andreas Ulbig", "Theodor S. Borsche", "Göran Andersson"]
published: "2013-12-22"
venue: "IFAC World Congress 2014 (Cape Town)；arXiv:1312.6435"
domain: "L2-电力系统基础"
level: "L2"
reading_order: 11
difficulty: "入门"
tags: ["论文笔记", "L2-电力系统基础", "稳定性", "惯量", "新能源", "经典论文"]
quality_score: 9
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 011 | 低转动惯量对电力系统稳定性与运行的影响

> [!abstract] 一句话
> **风电光伏把"旋转的飞轮"赶出了电网，电网变得越来越"轻"** —— 惯量下降导致频率变化更快、控制更难。这是"新型电力系统"最核心的物理挑战之一。

## 为什么读它

- **它讲的是"新型电力系统"的根本矛盾**，而且讲得**极其清楚**（瑞典 KTH 团队，2013 年提出，至今仍是经典引用）
- **不需要高深数学**：核心是几个物理直觉 + 一个简化的频率响应模型
- **理解它，你才能理解为什么"新能源并网"会带来安全问题** —— 攻击者可以利用低惯量这个脆弱性放大攻击效果

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Impact of Low Rotational Inertia on Power System Stability and Operation |
| **作者** | Andreas Ulbig, Theodor S. Borsche, Göran Andersson（瑞典皇家理工学院 KTH） |
| **发表** | IFAC World Congress 2014, Cape Town（2013-12-22 上传 arXiv） |
| **分类** | math.OC |
| **类型** | 会议论文（经典高引） |
| **链接** | [arXiv](https://arxiv.org/abs/1312.6435) \| [PDF](https://arxiv.org/pdf/1312.6435) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[1312.6435_fig1.png]]

![[1312.6435_fig2.png]]

![[1312.6435_fig3.png]]

![[1312.6435_fig4.png]]

![[1312.6435_fig5.png]]

![[1312.6435_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 核心物理：什么是"惯量"

传统电网里，**同步发电机的转子有巨大的旋转质量**。当功率突然不平衡（比如一台机组跳闸），这些转子会**自动释放/吸收动能**来抵抗频率变化。

这就是**转动惯量**，物理上写作：

$$E_{kin} = \frac{1}{2} J \omega^2$$

**直觉**：像一个大飞轮。你推它一下，它不会立刻变速；负载突变时，它能"顶住"。

### 问题：新能源没有惯量

> 原文：*"RES units, notably inverter-connected wind turbines and PV that as such do not provide rotational inertia, are effectively displacing conventional generators and their rotating machinery."*

风电、光伏通过**电力电子变流器（inverter）**并网，**没有旋转质量** → **不提供惯量**。

而它们正在**替代**传统同步发电机 → **系统总惯量持续下降**。

### 后果：频率变化更快

> 原文：*"Frequency dynamics are faster in power systems with low rotational inertia, making frequency control and power system operation more challenging."*

**频率动态更快** → 意味着：
- 从扰动到频率越限的时间**更短**
- 留给保护和控制动作的**时间窗口更小**
- 传统频率控制策略（基于慢动态设计）**可能来不及**

论文的关键判断：**"传统假设"失效了**

> *"The traditional assumption that grid inertia is sufficiently high with only small variations over time is thus not valid for power systems with high RES shares."*

传统电力系统分析里有一个隐含假设：**"系统惯量足够大，且随时间变化很小"**。
高比例新能源场景下，这个假设**不再成立**。

## 关键公式（频率动态）

**系统频率的摇摆方程（Swing Equation）**：

$$M \frac{d\Delta f}{dt} = \Delta P_m - \Delta P_e - D \Delta f$$

其中：
- $M = \frac{2H}{f_0}$：惯量常数（$H$ 是惯性时间常数，单位秒）
- $\Delta f$：频率偏差
- $\Delta P_m - \Delta P_e$：机械功率与电磁功率的不平衡（**扰动源**）
- $D$：阻尼系数

**关键结论（初始频率变化率 RoCoF）**：

$$\left.\frac{df}{dt}\right|_{t=0^+} = \frac{\Delta P}{M}$$

> **惯量 $M$ 越小，初始频率变化率 RoCoF 越大** → 频率"掉得更快"。

这就是低惯量问题的数学本质，也是所有后续研究（虚拟惯量、快速频率响应）的理论基础。

## 用网安的话说（小电解读）

> 这篇论文对你有两个层面的价值：

**1）物理层面的理解**

你要理解：**电网的"抗扰动能力"是有物理上限的**。
- 高惯量 = 系统"皮实"，扰动后慢慢恢复
- 低惯量 = 系统"脆弱"，扰动后迅速恶化

**2）安全层面的启示（这是关键）**

> **低惯量让攻击的"性价比"变高了。**

为什么？
- 攻击者的目标是**制造频率失稳**。
- 在高惯量系统里，要制造失稳需要很大的功率冲击 → 难。
- 在低惯量系统里，**同样的功率冲击会造成更大的频率跌落** → 攻击更容易成功。

**具体的攻击路径**：
- 篡改 AGC（自动发电控制）指令 → 让调频机组反向动作
- 伪造频率量测 → 让控制系统误判 → 错误响应
- 大规模协同控制分布式资源（如光伏逆变器）→ 人为制造功率振荡

→ 这些都指向 [[虚假数据注入攻击(FDIA)]] 与 **控制层攻击**。

**一个很好的选题方向**：
> **"低惯量电网下的攻击影响量化"** —— 同样一个 FDIA，在不同惯量水平下造成的后果差异有多大？这个问题目前研究不多，且直接对应"新型电力系统"这个国家战略方向。

## 读完后你应该能回答

- [ ] 什么是转动惯量？为什么它对电网频率稳定重要？
- [ ] 为什么风电光伏"不提供惯量"？
- [ ] 惯量下降会带来什么后果？（提示：RoCoF）
- [ ] 论文说"传统假设失效"，具体指哪个假设？
- [ ] 从攻击者角度，低惯量系统为什么更"好打"？

## 局限性

- 2013 年的论文，**未覆盖**此后发展的具体技术方案（虚拟同步机、构网型变流器、快速频率响应等）。
- 主要是**概念性分析 + 简化模型**，未做大规模系统的详细仿真验证。
- 论文有勘误说明（"Flaws in Table I corrected"），引用数据时建议核对最新版本。
- **没有安全视角** —— 完全是运行与控制视角。

## 和你的方向有什么关系

- **理解"新型电力系统"的最佳入口**：你会反复看到"惯量""一次调频""虚拟惯量"这些词，这篇讲得最清楚。
- **直接选题**：
  1. **低惯量电网下网络攻击的影响量化**（跨领域，新颖）
  2. **虚拟惯量控制的安全性**（虚拟惯量是软件实现的 → 可被攻击！）
  3. **频率控制回路的 FDIA 检测**
- 与你实验室方向对接：**"工业AI与智能体"**（用 AI 做惯量估计/频率预测）、**"AI与数据安全"**（控制指令完整性）。
- 注意：**"虚拟惯量是软件定义的"** 这句话很关键 —— 传统惯量是物理的（攻击不了），虚拟惯量是代码的（**可以攻击**）。这是一个很好的洞察点。

## 概念关联

- 核心概念：[[电力系统稳定性]] · [[电力信息物理系统(CPS)]] · [[虚假数据注入攻击(FDIA)]] · [[智能电网]]
- 前置阅读：[[20_Research/Papers/L2-电力系统基础/Roles_of_Dynamic_State_Estimation_in_Power_System_Modeling_Monitoring_and_Operation|008]]
- 后续阅读：[[20_Research/Papers/L4-AI与电网安全/Safe_Reinforcement_Learning_for_Power_System_Control_A_Review|032 安全强化学习用于电力系统控制综述]]
- 体系视角：[[20_Research/Papers/L1-零基础起步/新型电力系统信息物理安全防护体系研究|002]]

## 原文摘要

> Large-scale deployment of RES has led to significant generation shares of variable RES in power systems worldwide. RES units, notably inverter-connected wind turbines and PV that as such do not provide rotational inertia, are effectively displacing conventional generators and their rotating machinery. The traditional assumption that grid inertia is sufficiently high with only small variations over time is thus not valid for power systems with high RES shares. This has implications for frequency dynamics and power system stability and operation. Frequency dynamics are faster in power systems with low rotational inertia, making frequency control and power system operation more challenging. This paper investigates the impact of low rotational inertia on power system stability and operation, contributes new analysis insights and offers mitigation options for low inertia impacts.
