---
document_id: "arxiv-2206.02196"
arxiv_id: "2206.02196"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2206.02196"
title: "Machine learning applications for electricity market agent-based models: A systematic literature review"
zh_title: "机器学习在电力市场智能体模型中的应用：系统性文献综述"
authors: ["Alexander J. M. Kell", "Stephen McGough", "Matthew Forshaw"]
published: "2022-06-05"
venue: "arXiv (cs.MA)"
domain: "L2-电力系统基础"
level: "L2"
reading_order: 14
difficulty: "入门"
tags: ["论文笔记", "L2-电力系统基础", "电力市场", "智能体建模", "系统性综述"]
quality_score: 8
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 014 | 机器学习在电力市场智能体模型中的应用：系统性文献综述

> [!abstract] 一句话
> 系统梳理了 2016–2021 年 **55 篇**用机器学习做电力市场智能体仿真的论文，发现研究**高度集中在竞价策略**上，还有大量"长尾"方向没人做。

## 为什么读它

这篇论文给你**两个稀缺的东西**：

1. **一个完整的研究地图**：55 篇论文的分布 → 哪些方向卷、哪些方向空
2. **"智能体（Agent）"在电力领域的落地图景** → 直接对接你实验室的"工业AI与智能体"方向

而且它教了你一个**方法论**：**系统性文献综述（SLR）怎么写** —— 你研一很可能要写综述，这是很好的范本。

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Machine learning applications for electricity market agent-based models: A systematic literature review |
| **作者** | Alexander J. M. Kell, Stephen McGough, Matthew Forshaw（英国纽卡斯尔大学） |
| **发布** | 2022-06-05 |
| **分类** | cs.MA（多智能体系统） |
| **类型** | 系统性文献综述（Systematic Literature Review） |
| **范围** | 2016–2021 年发表的 **55 篇**论文 |
| **链接** | [arXiv](https://arxiv.org/abs/2206.02196) \| [PDF](https://arxiv.org/pdf/2206.02196) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2206.02196_fig1.png]]

![[2206.02196_fig2.png]]

![[2206.02196_fig3.png]]

![[2206.02196_fig4.png]]

![[2206.02196_fig5.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：为什么用"智能体仿真"研究电力市场

> 原文：*"the electricity market is made up of many different variables and data inputs. These variables and data inputs behave in sometimes unpredictable ways which can not be predicted a-priori."*

电力市场的特点：
- 变量极多（价格、负荷、天气、政策、燃料成本……）
- 参与者众多且**会互相博弈**（发电商、售电公司、用户、聚合商）
- 行为**不可先验预测**（人会策略性报价、会学习）

**传统方法**（如均衡模型）假设参与者理性且信息完全 —— 与现实不符。

**智能体建模（ABM）**：让每个参与者变成一个"智能体"，各自有策略，互相博弈 → **涌现出市场行为**。

**ML 的作用**：给智能体装上"大脑" —— 让它能学习、能预测、能自适应。

### 方法：系统性文献综述

论文的 SLR 流程（值得学习）：
1. 定义研究问题
2. 检索策略（数据库、关键词）
3. 筛选标准（纳入/排除）
4. 数据提取
5. 综合与分类

**最终纳入 55 篇（2016–2021）**

### 核心发现

**1）研究高度聚集（clustering）**

> 原文：*"research clusters around popular topics, such as bidding strategies."*

**竞价策略（bidding strategies）** 是最热的方向 —— 大量论文都在研究"智能体如何学习最优报价"。

**2）存在长尾（long tail）**

> 原文：*"there exists a long-tail of different research applications that could benefit from the high intensity research from the more investigated applications."*

意思是：**热门方向的研究方法，可以迁移到大量尚未被充分研究的应用上**。

**这直接就是选题建议**：找一条"长尾"应用，用成熟方法（如 RL 竞价）改造它。

## 用网安的话说（小电解读）

> 这篇论文对你有三层价值：

**1）智能体（Agent）= 你实验室的核心方向**

"工业AI与智能体" —— 而电力市场仿真正是**多智能体系统（MAS）**的经典应用场景。
```
每个发电商 = 一个 RL 智能体
每个用户 = 一个 RL 智能体
市场出清 = 环境（environment）
奖励 = 利润
```
→ 这是一个**天然的 MARL（多智能体强化学习）环境**。

**2）安全视角的空白（你的机会）**

电力市场仿真里，"智能体"如果被**对手控制**会怎样？
- **市场操纵（Market Manipulation）**：某个智能体学会"合谋抬价"
- **虚假报价**：智能体提交虚假容量 → 见"假消息检测"
- **数据投毒**：污染其他智能体的观测数据 → 让对手做出错误决策
- **对抗性 RL**：对手用 RL 学习"如何攻击我的策略"

> **"电力市场中的对抗性多智能体博弈"** —— 这是一个很有前景且文献稀少的方向。

**3）方法论价值**

SLR 的写作流程（检索 → 筛选 → 提取 → 分类 → 综合）是你**研一写综述论文的标准模板**。这篇论文本身就是个范本。

## 读完后你应该能回答

- [ ] 什么是智能体建模（ABM）？它比传统市场模型好在哪？
- [ ] 为什么电力市场适合用多智能体仿真？
- [ ] 论文发现研究集中在哪个方向？"长尾"意味着什么机会？
- [ ] 系统性文献综述（SLR）的基本流程是什么？

## 局限性

- **只覆盖 2016–2021 年**，未包含 2022 年后的工作（尤其是 LLM 智能体的爆发）。
- 综述性质，**不含原创实验**。
- 对**安全性/对抗性**几乎没有讨论 —— 因为当时的文献里确实很少。
- 电力市场建模本身有争议：仿真结果与真实市场行为的偏差难以验证。

## 和你的方向有什么关系

- **最直接的对接**：**"工业AI与智能体"** —— 这篇论文给你一个完整的电力场景多智能体图景。
- **可直接使用的开源环境**：搜索 `PowerGridworld`、`Andes_gym`、`Gym-ANM` 等电力 RL 环境。
- **选题方向**：
  1. **电力市场中的对抗性多智能体强化学习**（智能体攻防博弈）
  2. **LLM 智能体在电力市场中的行为与安全**（2024+ 的新方向，见 [[大语言模型(LLM)]]）
  3. **虚假报价检测**（对接"假消息检测"方向）
- **注意**：这条路线偏"经济/市场"，与"物理安全"距离较远。如果你更喜欢硬核的物理安全，可以把这篇当"视野拓展"，重点放在 L3/L4。

## 概念关联

- 核心概念：[[电力需求响应]] · [[强化学习]] · [[大语言模型(LLM)]] · [[智能电网]]
- 前置阅读：[[20_Research/Papers/L2-电力系统基础/A_New_Definition_of_Demand_Response_in_the_Distributed_Energy_Resource_Era|013 需求响应新定义]]
- 后续阅读：[[20_Research/Papers/L4-AI与电网安全/Safe_Reinforcement_Learning_for_Power_System_Control_A_Review|032 安全强化学习用于电力系统控制综述]]
- 前沿方向：[[20_Research/Papers/L5-前沿-LLM与智能体/GAIA_A_Large_Language_Model_for_Advanced_Power_Dispatch|035 GAIA：面向高级调度的 LLM]]

## 原文摘要

> The electricity market has a vital role to play in the decarbonisation of the energy system. However, the electricity market is made up of many different variables and data inputs. These variables and data inputs behave in sometimes unpredictable ways which can not be predicted a-priori. It has therefore been suggested that agent-based simulations are used to better understand the dynamics of the electricity market. Agent-based models provide the opportunity to integrate machine learning and artificial intelligence to add intelligence, make better forecasts and control the power market in better and more efficient ways. In this systematic literature review, we review 55 papers published between 2016 and 2021 which focus on machine learning applied to agent-based electricity market models. We find that research clusters around popular topics, such as bidding strategies. However, there exists a long-tail of different research applications that could benefit from the high intensity research from the more investigated applications.
