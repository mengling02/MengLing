---
document_id: "arxiv-2302.12168"
arxiv_id: "2302.12168"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2302.12168"
title: "A comparative assessment of deep learning models for day-ahead load forecasting: Investigating key accuracy drivers"
zh_title: "日负荷预测的深度学习模型比较评估：关键精度驱动因素探究"
authors: ["Sotiris Pelekis", "Ioannis-Konstantinos Seisopoulos", "Evangelos Spiliotis", "Theodosios Pountridis", "Evangelos Karakolis", "Spiros Mouzakitis", "Dimitris Askounis"]
published: "2023-02-23"
venue: "Sustainable Energy, Grids and Networks, 2023；arXiv:2302.12168"
domain: "L2-电力系统基础"
level: "L2"
reading_order: 12
difficulty: "入门"
tags: ["论文笔记", "L2-电力系统基础", "负荷预测", "深度学习", "模型对比"]
quality_score: 8
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 012 | 日负荷预测的深度学习模型比较评估

> [!abstract] 一句话
> 把 5 种主流深度学习模型（MLP / LSTM / N-BEATS / TCN / TFT）放在同一个日负荷预测任务上公平对比，结论有点反直觉：**结构最简单的 MLP 表现排第二，而 N-BEATS 最好**。

## 为什么读它

这是你**最容易上手的一篇 AI + 电力论文**：

- 任务就是**时间序列预测**（和你熟悉的领域高度重合）
- 数据是公开的（葡萄牙全国负荷 + 天气）
- 结论有实用价值（告诉你该用哪个模型）
- **完全没考虑安全** → 留给你发挥的空间很大

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | A comparative assessment of deep learning models for day-ahead load forecasting: Investigating key accuracy drivers |
| **作者** | Sotiris Pelekis 等 7 人（希腊雅典国立技术大学等） |
| **发表** | Sustainable Energy, Grids and Networks, 2023 |
| **分类** | cs.LG |
| **关键词** | STLF, Deep Learning, Ensemble, N-BEATS, Temporal Convolution, Forecasting Accuracy |
| **链接** | [arXiv](https://arxiv.org/abs/2302.12168) \| [PDF](https://arxiv.org/pdf/2302.12168) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2302.12168_fig1.png]]

![[2302.12168_fig2.png]]

![[2302.12168_fig3.png]]

![[2302.12168_fig4.png]]

![[2302.12168_fig5.png]]

![[2302.12168_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 问题：短期负荷预测（STLF）很难

> 原文：*"the non-linearity and non-stationarity of electricity demand as well as its dependency on various external factors renders STLF a challenging task."*

三个难点：
1. **非线性**：负荷和影响因素的关系不是线性的
2. **非平稳**：统计特性随时间变化（季节、趋势、疫情等）
3. **依赖外部因素**：天气、节假日、经济活动

### 方法：5 个模型同台竞技

| 模型 | 全称 | 特点 |
|---|---|---|
| **MLP** | Multi-Layer Perceptron | 最基础的全连接网络 |
| **LSTM** | Long Short-Term Memory | 经典循环网络，处理时序 |
| **N-BEATS** | Neural Basis Expansion Analysis for Time Series | 专为时序设计的纯 MLP 堆叠结构 |
| **TCN** | Temporal Convolutional Network | 用因果卷积处理时序 |
| **TFT** | Temporal Fusion Transformer | 带注意力机制的高级结构 |

### 实验设置

- **数据**：葡萄牙全国净聚合负荷（national net aggregated load）
- **任务**：日前（day-ahead）预测
- **额外分析**：识别影响负荷的外部因素，并分析它们对各模型精度的影响

### 结论（三个关键发现）

1. **N-BEATS 稳定胜出** —— 在所有对比中表现最好
2. **MLP 排第二** —— 这提供了"**简单前馈网络优于复杂架构**"的证据
3. **关键精度驱动因素**：**一天中的小时（hour of day）** 和 **温度（temperature）** 是最重要的特征

> 第 2 点很有启发性：**在负荷预测这种任务上，特征工程比模型复杂度更重要**。

## 用网安的话说（小电解读）

> 这篇论文对你而言，是一个**理想的"攻击靶场"**。

**为什么？**
- 模型清楚（5 个公开实现）
- 数据清楚（公开数据）
- 评价指标清楚（预测精度）
- **完全没有安全性分析** → 你可以直接在这个基础上加一章

**可以做的攻击实验（建议真的做）**：

| 攻击 | 怎么做 | 预期效果 |
|---|---|---|
| **数据投毒** | 在训练数据里注入偏移（如把某类日子的负荷整体调低 10%） | 模型系统性低估峰值 |
| **对抗样本** | 对输入特征（温度、小时）做微小扰动 | 预测值显著偏离 |
| **输入篡改** | 直接改输入（模拟量测被劫持） | 见 [[20_Research/Papers/L4-AI与电网安全/Exploiting_Vulnerabilities_of_Load_Forecasting_Through_Adversarial_Attacks\|030]] |
| **模型窃取** | 通过 API 查询反推模型 | 为后续攻击提供信息 |

**物理后果链**（这是电网安全论文必须写的）：
```
负荷预测低估峰值
  → 调度安排的备用容量不足
    → 高峰时段功率缺额
      → 频率下降
        → 低频减载 / 停电
```

**论文没有做这件事，你做了，就是一篇文章。**

## 读完后你应该能回答

- [ ] 短期负荷预测的三个主要难点是什么？
- [ ] N-BEATS 为什么能胜出？（提示：它是纯 MLP 的堆叠，但专门为时序设计）
- [ ] 为什么"简单模型打败复杂模型"在这个任务上成立？
- [ ] 负荷预测的误差会通过什么链条传导到物理后果？

## 局限性

- **单一数据集**（仅葡萄牙全国负荷），结论的普适性需要更多验证。
- 只做了**日前预测**，未涉及超短期（分钟级）和多步预测。
- 未考虑**极端场景**（极端天气、突发事件、疫情），泛化性存疑。
- 未涉及**概率预测**（只给点预测，不给不确定性区间）—— 而调度更需要区间。
- **完全没有安全性分析**。

## 和你的方向有什么关系

- **最容易落地的第一个实验**：有公开数据、公开模型、清晰指标。
- **直接选题**：
  1. **负荷预测模型的对抗鲁棒性评估**（对 5 个模型都测一遍，做对比 → 很自然的论文）
  2. **数据投毒的影响量化**（不同投毒比例 → 精度下降曲线 → 物理后果）
  3. **检测投毒/对抗输入**（防御侧）
- 与你实验室方向对接：**"AI与数据安全"**（模型安全）、**"假消息检测"**（虚假数据识别）、**"工业AI"**（预测模型）。
- 与 [[联邦学习]] 结合：分布式负荷预测中的隐私与安全问题。

## 概念关联

- 核心概念：[[电力负荷预测]] · [[对抗样本攻击]] · [[联邦学习]] · [[电力需求响应]]
- 后续阅读：[[20_Research/Papers/L4-AI与电网安全/Exploiting_Vulnerabilities_of_Load_Forecasting_Through_Adversarial_Attacks|030 通过对抗攻击利用负荷预测的脆弱性（必读）]]
- 相关方向：[[20_Research/Papers/L4-AI与电网安全/Federated_Learning_for_Smart_Grid_A_Survey_on_Applications_and_Potential_Vulnerabilities|028 联邦学习用于智能电网综述]]

## 原文摘要

> Short-term load forecasting (STLF) is vital for the effective and economic operation of power grids and energy markets. However, the non-linearity and non-stationarity of electricity demand as well as its dependency on various external factors renders STLF a challenging task. To that end, several deep learning models have been proposed in the literature for STLF, reporting promising results. In order to evaluate the accuracy of said models in day-ahead forecasting settings, in this paper we focus on the national net aggregated STLF of Portugal and conduct a comparative study considering a set of indicative, well-established deep autoregressive models, namely multi-layer perceptrons (MLP), long short-term memory networks (LSTM), neural basis expansion coefficient analysis (N-BEATS), temporal convolutional networks (TCN), and temporal fusion transformers (TFT). Moreover, we identify factors that significantly affect the demand and investigate their impact on the accuracy of each model. Our results suggest that N-BEATS consistently outperforms the rest of the examined models. MLP follows, providing further evidence towards the use of feed-forward networks over relatively more sophisticated architectures. Finally, certain calendar and weather features like the hour of the day and the temperature are identified as key accuracy drivers, providing insights regarding the forecasting approach that should be used per case.
