---
document_id: "arxiv-2407.00681"
arxiv_id: "2407.00681"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2407.00681"
title: "Safe Reinforcement Learning for Power System Control: A Review"
zh_title: "面向电力系统控制的安全强化学习：综述"
authors: ["Peipei Yu", "Zhenyi Wang", "Hongcai Zhang", "Yonghua Song"]
published: "2024-06-30"
venue: "arXiv (eess.SY)"
domain: "L4-AI与电网安全"
level: "L4"
reading_order: 32
difficulty: "入门+"
tags: ["论文笔记", "L4-AI与电网安全", "强化学习", "安全RL", "控制", "综述"]
quality_score: 9
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 032 | 面向电力系统控制的安全强化学习：综述

> [!abstract] 一句话
> **强化学习能学出很好的控制策略，但它在训练时会"乱试"** —— 而电网里"乱试"等于停电。这篇综述系统梳理了 Safe RL 的方法，以及如何把它们用到频率调节、电压控制、能量管理上。

## 为什么读它

三个理由：

1. **RL 是当前最热的 AI 方法**，而电网是它最有价值的应用场景之一
2. **"安全"是 RL 落地的最大障碍** —— 这篇把这个核心矛盾讲清楚了
3. **与你的方向直接相关**：你实验室有"工业AI与智能体"，RL 是智能体的核心方法

而且这篇的作者包括 **Yonghua Song（宋永华）**，电力系统领域的国际知名学者。

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Safe Reinforcement Learning for Power System Control: A Review |
| **作者** | Peipei Yu, Zhenyi Wang, Hongcai Zhang, Yonghua Song（澳门大学、清华大学等） |
| **发布** | 2024-06-30 |
| **分类** | eess.SY |
| **链接** | [arXiv](https://arxiv.org/abs/2407.00681) \| [PDF](https://arxiv.org/pdf/2407.00681) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2407.00681_fig1.png]]

![[2407.00681_fig2.png]]

![[2407.00681_fig3.jpg]]

![[2407.00681_fig4.png]]

![[2407.00681_fig5.png]]

![[2407.00681_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：新能源让控制变难

> 原文：*"The large-scale integration of intermittent renewable energy resources introduces increased uncertainty and volatility to the supply side of power systems, thereby complicating system operation and control."*

**间歇性新能源 → 供给侧不确定性和波动性增加 → 运行控制变复杂**。

### 为什么用强化学习

> 原文：*"data-driven approaches, particularly reinforcement learning (RL), have shown significant promise in addressing complex control challenges in power systems, because RL can learn from interactive feedback without needing prior knowledge of the system model."*

**RL 的优势**：**不需要系统模型的先验知识，通过与环境的交互反馈学习**。

**这对电力系统很重要**：
- 新型电力系统里，**精确模型越来越难建立**（电力电子设备行为复杂）
- 传统基于模型的控制方法失效
- → RL 可以"从数据中直接学策略"

### 核心矛盾：训练需要"试错"，但电网不能"试错"

> 原文：*"the training process of model-free RL methods relies heavily on random decisions for exploration, which may result in 'bad' decisions that violate critical safety constraints and lead to catastrophic control outcomes."*

**这是全文最关键的一段**：

```
RL 需要"探索（exploration）" → 即随机尝试各种动作
  → 会产生"坏决策"
    → 违反安全约束
      → 灾难性后果（停电、设备损坏）
```

> 原文：*"Due to the inability of RL methods to theoretically ensure decision safety in power systems, directly deploying traditional RL algorithms in the real world is deemed unacceptable."*

**"直接部署传统 RL 算法在现实世界是不可接受的"** —— 这句话很重。

### 论文内容：Safe RL 方法 + 电力应用

**论文的两部分**：

**1）Safe RL 技术综述**（state-of-the-art safe RL techniques）

**2）如何应用到电力系统控制问题**：
- **频率调节（frequency regulation）**
- **电压控制（voltage control）**
- **能量管理（energy management）**

**3）关键挑战与未来方向**：
- 收敛性与最优性（convergence and optimality）
- 训练效率（training efficiency）
- 普适性（universality）
- 实际部署（real-world deployment）

## 关键方法（Safe RL 的几条技术路线）

综合论文 + 领域公开知识：

| 方法 | 思路 | 在电网的应用 |
|---|---|---|
| **约束 MDP（CMDP）** | 把安全要求写成约束，用拉格朗日法求解 | 电压/频率约束 |
| **Lyapunov 方法** | 构造能量函数，保证稳定性 | 暂态稳定控制 |
| **安全层 / 盾牌（Shield）** | 动作执行前过一遍安全校验 | 任何控制场景 |
| **模型预测控制 + RL（MPC+RL）** | MPC 保证安全，RL 优化性能 | 经济调度 |
| **模仿学习预热** | 先用专家数据训练，再 RL 微调 | 减少危险探索 |
| **安全探索（Safe Exploration）** | 限制探索空间在安全集内 | 训练阶段 |
| **多智能体安全 RL** | 协调多个智能体，避免冲突 | 分布式控制 |

## 用网安的话说（小电解读）

> 这篇论文对你有**双重价值**：既是"AI 应用"知识，也是"攻击面"知识。

**第一层：AI 应用视角**

RL 在电网的三个典型应用：
```
频率调节：状态=频率偏差，动作=调机组出力，奖励=−频率偏差
电压控制：状态=各节点电压，动作=调无功，奖励=−电压偏差−损耗
能量管理：状态=负荷/电价/储能SOC，动作=充放电，奖励=−成本
```

**第二层：安全视角（更重要）**

> **RL 智能体本身就是一个新的攻击目标。**

| 攻击点 | 攻击方式 | 后果 |
|---|---|---|
| **观测（state）** | 篡改传感器 → 智能体看到错误状态 | 错误决策 |
| **奖励（reward）** | 篡改奖励信号 → 智能体学错策略 | 训练出危险策略 |
| **动作（action）** | 中间人篡改控制指令 | 直接危害 |
| **训练数据** | 数据投毒 | 后门策略 |
| **对抗扰动** | 对状态加微小扰动 → 策略偏移 | 见 [[对抗样本攻击]] |

> **"奖励投毒（Reward Poisoning）"** 是 RL 特有的、非常有意思的攻击面：
> 攻击者在训练阶段篡改奖励函数，让智能体学出一个"平时正常、特定情况下灾难"的策略 —— 类似**后门攻击**。

**第三层：一个漂亮的选题结构**

> **"RL 智能体在电网控制中的对抗鲁棒性"**
> - RL 智能体正在被引入电网控制（趋势）
> - RL 有对抗脆弱性（已知）
> - 但"电网 RL 智能体的对抗攻击与防御"研究很少
> - → **这是一个时机很好的选题**

**还有一个有趣的悖论**：
> 论文关注"RL 如何保证安全"（Safety）
> 但很少关注"RL 如何被攻击"（Security）
> **Safety ≠ Security**：
> - Safety：系统不出意外（随机故障、模型误差）
> - Security：系统不被恶意攻击（对抗性）
> → **"从 Safety 到 Security 的延伸"** 是一个自然的研究缺口。

## 读完后你应该能回答

- [ ] 为什么强化学习适合电力系统控制？
- [ ] 为什么"直接部署传统 RL"在电网里不可接受？
- [ ] Safe RL 的主要技术路线有哪些？
- [ ] RL 智能体本身有哪些可被攻击的点？
- [ ] "Safety"和"Security"在电网 RL 场景下的区别是什么？

## 局限性

- **综述性质**，具体算法实现需查阅原始论文。
- 侧重"安全（Safety）"，对"安全（Security，即对抗攻击）"讨论较少。
- 电力应用集中在**频率/电压/能量管理**三个场景，其他场景（如保护、市场）覆盖不足。
- 对**多智能体**场景的安全问题讨论有限。
- 论文提到"实际部署"，但真实电网的 RL 部署案例仍然极少。

## 和你的方向有什么关系

- **这是"工业AI与智能体"方向的核心文献**：RL + 电力控制 + 安全。
- **直接选题（按推荐度）**：
  1. **电网 RL 智能体的对抗攻击与防御**（缺口明显）
  2. **奖励投毒攻击**（RL 特有，新颖）
  3. **Safe RL 与 Secure RL 的统一框架**（理论价值高）
  4. **多智能体 RL 在电网攻防博弈中的应用**（对接 [[移动目标防御(MTD)]]）
- **可用环境**：`PowerGridworld`、`Andes_gym`、`Gym-ANM`（论文可能提到，也可自行搜索）
- **注意**：这条路线**技术门槛较高**（需要 RL + 电力双重知识），但**竞争相对少**，适合想做硬核工作的同学。

> [!tip] 小电的判断
> 如果你想做"AI + 电网"里**技术含量高、竞争少**的方向，**RL 安全**是一个好选择。
> 理由：RL 本身门槛高 → 会做的人少 → 加上电网领域知识 → 门槛更高 → 竞争更少。
> 代价是**学习曲线陡峭**，建议在 L1-L3 打好基础后再进入。

## 概念关联

- 核心概念：[[强化学习]] · [[电力系统稳定性]] · [[对抗样本攻击]] · [[移动目标防御(MTD)]] · [[大语言模型(LLM)]]
- 前置阅读：[[20_Research/Papers/L2-电力系统基础/Impact_of_Low_Rotational_Inertia_on_Power_System_Stability_and_Operation|011 低惯量对电力系统稳定性的影响]]
- 应用场景：[[20_Research/Papers/L2-电力系统基础/Optimal_Distributed_Control_of_Reactive_Power_via_ADMM|015 无功功率分布式优化]]
- 智能体方向：[[20_Research/Papers/L2-电力系统基础/ML_applications_for_electricity_market_agent-based_models|014 电力市场智能体建模中的机器学习应用]]
- 前沿延伸：[[20_Research/Papers/L5-前沿-LLM与智能体/GAIA_A_Large_Language_Model_for_Advanced_Power_Dispatch|035 GAIA：面向高级调度的 LLM]]

## 原文摘要

> The large-scale integration of intermittent renewable energy resources introduces increased uncertainty and volatility to the supply side of power systems, thereby complicating system operation and control. Recently, data-driven approaches, particularly reinforcement learning (RL), have shown significant promise in addressing complex control challenges in power systems, because RL can learn from interactive feedback without needing prior knowledge of the system model. However, the training process of model-free RL methods relies heavily on random decisions for exploration, which may result in "bad" decisions that violate critical safety constraints and lead to catastrophic control outcomes. Due to the inability of RL methods to theoretically ensure decision safety in power systems, directly deploying traditional RL algorithms in the real world is deemed unacceptable. Consequently, the safety issue in RL applications, known as safe RL, has garnered considerable attention in recent years, leading to numerous important developments. This paper provides a comprehensive review of the state-of-the-art safe RL techniques and discusses how these techniques can be applied to power system control problems such as frequency regulation, voltage control, and energy management. We then present discussions on key challenges and future research directions, related to convergence and optimality, training efficiency, universality, and real-world deployment.
