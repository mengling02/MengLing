---
document_id: "arxiv-2307.02049"
arxiv_id: "2307.02049"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2307.02049"
title: "Graph Neural Network-based Power Flow Model"
zh_title: "基于图神经网络的潮流计算模型"
authors: ["Mingjian Tuo", "Xingpeng Li", "Tianxia Zhao"]
published: "2023-07-05"
venue: "arXiv (eess.SY)"
domain: "L2-电力系统基础"
level: "L2"
reading_order: 10
difficulty: "入门+"
tags: ["论文笔记", "L2-电力系统基础", "潮流计算", "图神经网络", "AI应用"]
quality_score: 8
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 010 | 基于图神经网络的潮流计算模型

> [!abstract] 一句话
> **用 GNN 学潮流计算，比传统 DC 潮流更准，比 DNN/CNN 更好，而且快** —— 因为电网本身就是一张图。

## 为什么读它

这篇论文有三重价值：

1. **理解潮流计算**：论文把[[潮流计算]]讲清楚了（DC 潮流的局限、为什么需要更准的方法）
2. **理解 GNN 为什么适合电网**：这是 [[图神经网络]] 在电力领域最直观的应用
3. **理解"AI + 物理"的融合模式**：这是当前最主流的研究范式

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Graph Neural Network-based Power Flow Model |
| **作者** | Mingjian Tuo, Xingpeng Li, Tianxia Zhao |
| **发布** | 2023-07-05 |
| **分类** | eess.SY |
| **链接** | [arXiv](https://arxiv.org/abs/2307.02049) \| [PDF](https://arxiv.org/pdf/2307.02049) |
| **备注** | arXiv 管理员标注：与 arXiv:2112.08418 有文本重叠 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2307.02049_fig1.png]]

![[2307.02049_fig2.png]]

---


## 这篇论文在讲什么（白话版）

### 问题：DC 潮流不够准

**背景知识**（详见 [[潮流计算]]）：
- **AC 潮流**：精确，但需要迭代求解非线性方程，慢
- **DC 潮流**：线性近似（$P = B\theta$），快、稳，但**在部分线路上误差大**

**什么时候误差大？**
> 原文指出：当有**风电场等新能源**接入时（它们常常远离主网），关键线路的潮流结果不准确，而这些线路的精确潮流**对后续运行至关重要**。

**这就是问题**：为了快用了 DC 潮流，但关键线路需要准。

### 解决方案：用历史数据训练 GNN

思路：**既然物理模型难算，那就用数据学一个映射**。

```
输入：节点注入功率 P, Q（历史数据）
  ↓ GNN（利用电网拓扑做消息传递）
输出：线路潮流、电压幅值、相角
```

### 为什么是 GNN 而不是 DNN/CNN？

| 模型 | 问题 |
|---|---|
| **DNN（全连接）** | 把电网当成一个扁平的向量，**完全丢掉拓扑结构**；换个系统就得重训 |
| **CNN（卷积）** | 适合规则的网格（如图像），但**电网不是网格**，节点连接不规则 |
| **GNN** | 直接在图上做消息传递，**天然利用拓扑** → 更准、更可迁移 |

### 实验与结论

论文做了**四路对比**：
1. 提出的 **GNN 模型**
2. 传统 **DC 潮流**
3. **DNN**
4. **CNN**

**结论**：GNN 模型在测试系统上**精度更高、效率也高**。

## 关键公式

**GNN 的消息传递机制**：

$$h_v^{(k+1)} = \sigma\left(W^{(k)} \cdot \text{AGG}\left(\{h_u^{(k)} : u \in \mathcal{N}(v)\} \cup \{h_v^{(k)}\}\right)\right)$$

其中：
- $h_v^{(k)}$：节点 $v$ 在第 $k$ 层的特征（初始为节点注入功率）
- $\mathcal{N}(v)$：节点 $v$ 的邻居集合（**这就是电网拓扑**）
- $\text{AGG}$：聚合函数（求和/均值/最大值）
- $W^{(k)}$：可学习权重

**物理意义**：迭代 $k$ 轮后，每个节点"看到"了 $k$ 跳范围内的电网信息 —— 这与潮流的**物理传播范围**是对应的。

**DC 潮流的对照**：
$$P_{ij} = \frac{\theta_i - \theta_j}{x_{ij}}$$

即：线路潮流 = 两端相角差 ÷ 线路电抗。简单、线性，但忽略了无功和损耗。

## 用网安的话说（小电解读）

> 这篇论文对你有**三重意义**：

**1）它是"AI + 电力"的标准范式**
```
物理问题（潮流计算）
  → 传统方法有局限（DC 潮流不准）
    → 用数据驱动方法补足（GNN）
      → 用物理结构约束模型（图拓扑）
```
这个范式，你后面会在几乎所有 AI 类电力论文里看到。

**2）它暴露了新的攻击面**
GNN 潮流模型是一个**数据驱动的代理模型（surrogate）**。那么：
- **训练数据投毒**：篡改历史潮流数据 → 学出错误的模型
- **对抗样本**：微调输入功率 → 让 GNN 输出错误的线路潮流 → **调度员看到"线路正常"实际已过载**
- **拓扑扰动**：攻击者改变开关状态（真实的或伪造的）→ GNN 输入图结构变化 → 输出失真

**3）它给你一个"低成本仿真器"**
训练好的 GNN 潮流模型**比 AC 潮流快几个数量级**。
→ 对做**攻防仿真**的人（比如你），这意味着可以跑更多攻击场景。
→ **这本身就是一个可做的选题**：用 GNN 代理模型加速电网攻防仿真。

## 读完后你应该能回答

- [ ] DC 潮流和 AC 潮流的区别是什么？DC 潮流什么时候会不准？
- [ ] 为什么 GNN 比 DNN/CNN 更适合电力系统？
- [ ] 消息传递机制中，"邻居聚合"对应电网里的什么物理过程？
- [ ] 一个数据驱动的潮流模型，可能被怎样攻击？

## 局限性

- **纯性能导向**，完全没有考虑安全性、鲁棒性、对抗性 —— 这是整个方向的普遍问题，也是你的机会。
- 数据驱动方法依赖**历史数据的覆盖度**：遇到训练分布外的工况（如极端故障），泛化性存疑。
- 未讨论**拓扑变化**（开关操作）时的模型适应性问题。
- arXiv 管理员标注与作者另一篇论文有文本重叠，引用时建议核对。

## 和你的方向有什么关系

- **直接选题**：
  1. **GNN 潮流模型的对抗鲁棒性评估**（攻击者能否用微小输入扰动欺骗它？）
  2. **训练数据投毒对电网代理模型的影响**
  3. **用 GNN 代理模型加速攻防仿真**（工程价值高）
- **技术储备**：GNN 是你实验室"工业AI与智能体"方向的核心技术之一，这篇给你一个电力场景的落地案例。
- 与 [[对抗样本攻击]] 直接相关 —— 把图像领域的对抗攻击思路搬到电网图结构上，是很有前景的方向。

## 概念关联

- 核心概念：[[潮流计算]] · [[图神经网络]] · [[对抗样本攻击]] · [[状态估计]]
- 前置阅读：[[20_Research/Papers/L2-电力系统基础/Roles_of_Dynamic_State_Estimation_in_Power_System_Modeling_Monitoring_and_Operation|008]]
- 后续阅读：[[20_Research/Papers/L4-AI与电网安全/State_Estimation_in_Electric_Power_Systems_Leveraging_Graph_Neural_Networks|033 用 GNN 做状态估计]]
- 攻击视角：[[20_Research/Papers/L4-AI与电网安全/Exploiting_Vulnerabilities_of_Load_Forecasting_Through_Adversarial_Attacks|030 通过对抗攻击利用负荷预测的脆弱性]]

## 原文摘要

> Power flow analysis plays a crucial role in examining the electricity flow within a power system network. By performing power flow calculations, the system's steady-state variables, including voltage magnitude, phase angle at each bus, active/reactive power flow across branches, can be determined. While the widely used DC power flow model offers speed and robustness, it may yield inaccurate line flow results for certain transmission lines. This issue becomes more critical when dealing with renewable energy sources such as wind farms, which are often located far from the main grid. Obtaining precise line flow results for these critical lines is vital for next operations. To address these challenges, data-driven approaches leverage historical grid profiles. In this paper, a graph neural network (GNN) model is trained using historical power system data to predict power flow outcomes. The GNN model enables rapid estimation of line flows. A comprehensive performance analysis is conducted, comparing the proposed GNN-based power flow model with the traditional DC power flow model, as well as deep neural network (DNN) and convolutional neural network (CNN). The results on test systems demonstrate that the proposed GNN-based power flow model provides more accurate solutions with high efficiency comparing to benchmark models.
