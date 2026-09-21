---
document_id: "arxiv-2012.06069"
arxiv_id: "2012.06069"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2012.06069"
title: "Power System Dynamic State Estimation Using Extended and Unscented Kalman Filters"
zh_title: "使用扩展卡尔曼滤波（EKF）与无迹卡尔曼滤波（UKF）的电力系统动态状态估计"
authors: ["Narayan Bhusal", "Mukesh Gautam"]
published: "2020-12-11"
venue: "arXiv (eess.SY)"
domain: "L2-电力系统基础"
level: "L2"
reading_order: 9
difficulty: "入门+"
tags: ["论文笔记", "L2-电力系统基础", "卡尔曼滤波", "状态估计", "可复现代码"]
quality_score: 8
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 009 | 使用 EKF 与 UKF 的电力系统动态状态估计

> [!abstract] 一句话
> **把卡尔曼滤波真正跑在电力系统上的一篇"能上手"的论文**：作者用 EKF 和 UKF 在 WECC 9 节点和 New England 39 节点系统上做了状态估计，而且**代码开源在 GitHub**。

## 为什么读它

上一篇（[[20_Research/Papers/L2-电力系统基础/Roles_of_Dynamic_State_Estimation_in_Power_System_Modeling_Monitoring_and_Operation|008]]）讲了 DSE "为什么重要"，这一篇告诉你 **"怎么算"**。

对研一学生的价值：
- **篇幅短、门槛低**（arXiv 工作稿，不是顶刊长文）
- **代码开源** → 你可以直接跑起来，改参数，看效果
- **两个标准测试系统**（WECC 3机9节点、New England 10机39节点）→ 后续你读的所有论文都会用到这些系统

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Power System Dynamic State Estimation Using Extended and Unscented Kalman Filters |
| **作者** | Narayan Bhusal, Mukesh Gautam |
| **发布** | 2020-12-11 |
| **分类** | eess.SY（系统与控制） |
| **类型** | 技术报告 / 工作稿（作者说明会持续更新更多方法） |
| **链接** | [arXiv](https://arxiv.org/abs/2012.06069) \| [PDF](https://arxiv.org/pdf/2012.06069) |
| **代码** | 论文声明所有源码（牛顿-拉夫逊潮流、导纳矩阵、EKF、UKF）公开在 GitHub |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2012.06069_fig1.png]]

![[2012.06069_fig2.png]]

![[2012.06069_fig3.png]]

![[2012.06069_fig4.png]]

![[2012.06069_fig5.png]]

![[2012.06069_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 问题：量测永远有噪声

即使有 PMU 这样的高精度设备，量测**仍然有噪声**（原文：*"these measurements are still not completely free from the measurement noises"*）。

所以要**滤波** —— 从带噪声的量测中恢复真实的系统动态。

### 两个滤波器：EKF vs UKF

**扩展卡尔曼滤波（EKF）**

思路：系统是非线性的，那我就**在每一步做线性化**（泰勒展开取一阶项）。

$$x_{k+1} \approx f(\hat{x}_k) + F_k (x_k - \hat{x}_k), \quad F_k = \left.\frac{\partial f}{\partial x}\right|_{\hat{x}_k}$$

- 优点：计算快、实现简单、工业界广泛使用
- 缺点：**强非线性时线性化误差大**，可能发散；需要计算雅可比矩阵

**无迹卡尔曼滤波（UKF）**

思路：**不做线性化**。而是选一组"sigma 点"，让它们通过真实的非线性函数，再用变换后的点统计出均值和协方差（**无迹变换**）。

- 优点：**非线性场景下精度更高**，不需要雅可比矩阵
- 缺点：计算量稍大（需要传播 $2n+1$ 个 sigma 点）

### 实验设置

| 项目 | 内容 |
|---|---|
| **测试系统** | WECC 3机9节点；New England 10机39节点 |
| **估计目标** | 发电机动态状态（转子角、转速等） |
| **结论** | UKF 和 EKF **都能准确估计**电力系统动态；论文给出了两者的对比性能 |

## 关键公式

**卡尔曼滤波的通用两步结构**：

**预测步（时间更新）**：
$$\hat{x}_k^- = f(\hat{x}_{k-1}), \quad P_k^- = F_{k-1} P_{k-1} F_{k-1}^T + Q$$

**更新步（量测更新）**：
$$K_k = P_k^- H_k^T (H_k P_k^- H_k^T + R)^{-1}$$
$$\hat{x}_k = \hat{x}_k^- + K_k (z_k - h(\hat{x}_k^-)), \quad P_k = (I - K_k H_k) P_k^-$$

> **直觉**：$K_k$ 是"卡尔曼增益"，它自动权衡"信模型"还是"信量测"：
> - 量测噪声 $R$ 大 → $K$ 小 → 更相信模型预测
> - 过程噪声 $Q$ 大 → $K$ 大 → 更相信量测

**这就是攻击者的切入点**：如果你能同时污染 $z_k$ 并让 $R$ 看起来合理，滤波器会**心甘情愿地跟着你走**。

## 用网安的话说（小电解读）

> 这篇论文对你最大的价值是：**它是一个可动手的起点**。

**你可以直接做的实验（建议真的做一次）**：

1. 把代码跑起来，在 WECC 9 节点系统上复现 EKF/UKF 的估计效果
2. **注入虚假数据**：手动给某个量测加一个偏置，看估计值怎么偏
3. **测试检测能力**：算新息（残差）$z_k - h(\hat{x}_k^-)$，看能不能发现异常
4. **构造隐蔽攻击**：调整注入量，让它刚好不触发残差阈值 → **你就在复现 FDIA 了**

> 这四步做完，你对 FDIA 的理解会从"读过论文"变成"亲手打过"。

**技术对比的启示**：
- UKF 比 EKF 精度高，但**在安全场景下，精度高不等于安全** —— 一个更精确的估计器可能对攻击更敏感（因为攻击引起的偏差更容易被检测），也可能因为更"自信"而更容易被带偏。这本身就是一个可研究的点。

## 读完后你应该能回答

- [ ] EKF 和 UKF 的核心区别是什么？各自适合什么场景？
- [ ] 卡尔曼增益 $K$ 的物理含义是什么？
- [ ] 为什么说"过程噪声 $Q$ 和量测噪声 $R$"的设定会影响估计结果？
- [ ] 从攻击者角度，污染卡尔曼滤波有哪些路径？

## 局限性

- 这是**技术报告性质的工作稿**，不是正式发表的期刊论文，**实验规模和深度有限**。
- 只对比了 EKF 和 UKF，未涉及更现代的 EnKF（集合卡尔曼滤波）、粒子滤波、以及基于学习的方法（作者说后续会更新）。
- 测试系统规模小（9 节点、39 节点），未验证大规模系统的可扩展性。
- **完全没有安全视角** —— 这对你反而是好事（留了空间）。

## 和你的方向有什么关系

- **这是你最好的"第一个实验"**：代码开源、系统标准、问题清晰。
- **可延伸的选题**：
  1. **EKF/UKF 在 FDIA 下的鲁棒性对比**（谁更抗攻击？）
  2. **用神经网络替代卡尔曼滤波**，并评估其对抗鲁棒性
  3. **自适应 $Q/R$ 估计**用于攻击检测（攻击会导致噪声统计异常）
- 与你实验室方向对接：**"入侵检测"**（残差即异常信号）、**"AI与数据安全"**（滤波器的数据完整性）。

## 概念关联

- 核心概念：[[状态估计]] · [[虚假数据注入攻击(FDIA)]] · [[不良数据检测与状态估计防御]] · [[工控安全测试床与数据集]]
- 前置阅读：[[20_Research/Papers/L2-电力系统基础/Roles_of_Dynamic_State_Estimation_in_Power_System_Modeling_Monitoring_and_Operation|008]]
- 后续阅读：[[20_Research/Papers/L3-工控与电网安全/Vulnerability_Analysis_and_Consequences_of_False_Data_Injection_Attack_on_Power_System_State_Estimation|024 FDIA 脆弱性分析]]
- 相关方法：[[20_Research/Papers/L4-AI与电网安全/State_Estimation_in_Electric_Power_Systems_Leveraging_Graph_Neural_Networks|033 用 GNN 做状态估计]]

## 原文摘要

> Accurate estimation of power system dynamics is very important for the enhancement of power system reliability, resilience, security, and stability of power system. With the increasing integration of inverter-based distributed energy resources, the knowledge of power system dynamics has become more necessary and critical than ever before for proper control and operation of the power system. Although recent advancement of measurement devices and the transmission technologies have reduced the measurement and transmission error significantly, these measurements are still not completely free from the measurement noises. Therefore, the noisy measurements need to be filtered to obtain the accurate power system operating dynamics. In this work, the power system dynamic states are estimated using extended Kalman filter (EKF) and unscented Kalman filter (UKF). We have performed case studies on Western Electricity Coordinating Council (WECC)'s 3-machine 9-bus system and New England 10-machine 39-bus. The results show that the UKF and EKF can accurately estimate the power system dynamics. The comparative performance of EKF and UKF for the tested case is also provided. Other Kalman filtering techniques alongwith the machine learning-based estimator will be updated in this report soon. All the sources code including Newton Raphson power flow, admittance matrix calculation, EKF calculation, and UKF calculation are publicly available in Github.

> [!tip] 动手任务
> 找到论文提到的 GitHub 仓库（可在 arXiv 页面或论文正文中查找链接），把代码跑起来。
> 然后尝试：**给某个量测注入一个恒定偏置，观察估计误差随时间的变化。**
> 这个简单的实验，就是 FDIA 研究的最小可复现单元。
