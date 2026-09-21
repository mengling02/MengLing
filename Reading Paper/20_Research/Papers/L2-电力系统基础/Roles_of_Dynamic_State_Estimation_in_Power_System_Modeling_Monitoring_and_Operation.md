---
document_id: "arxiv-2005.05380"
arxiv_id: "2005.05380"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2005.05380"
title: "Roles of Dynamic State Estimation in Power System Modeling, Monitoring and Operation"
zh_title: "动态状态估计在电力系统建模、监测与运行中的作用"
authors: ["Junbo Zhao", "Marcos Netto", "Zhenyu Huang", "Samson Shenglong Yu", "Antonio Gomez-Exposito", "Shaobu Wang", "Innocent Kamwa", "Shahrokh Akhlaghi", "et al."]
published: "2020-05-11"
venue: "arXiv (eess.SP)；IEEE 电力系统领域综述性文章"
domain: "L2-电力系统基础"
level: "L2"
reading_order: 8
difficulty: "入门"
tags: ["论文笔记", "L2-电力系统基础", "状态估计", "动态状态估计", "综述"]
quality_score: 9
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 008 | 动态状态估计在电力系统建模、监测与运行中的作用

> [!abstract] 一句话
> **静态状态估计告诉你"电网现在是什么样"，动态状态估计告诉你"电网正在往哪走"** —— 它是从"看照片"到"看视频"的升级。

## 为什么从这篇开始 L2

前面 L1 建立了"电网会被攻击"的世界观，但从这一篇起，你要理解**电网自己是怎么运行的**。
[[状态估计]] 是电网运行的核心环节，也是 [[虚假数据注入攻击(FDIA)]] 的攻击目标 —— 所以它是**承上启下的枢纽**。

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Roles of Dynamic State Estimation in Power System Modeling, Monitoring and Operation |
| **作者** | Junbo Zhao, Marcos Netto, Zhenyu Huang, Samson Shenglong Yu, Antonio Gomez-Exposito, Shaobu Wang, Innocent Kamwa, Shahrokh Akhlaghi 等（16 位作者，IEEE 电力系统状态估计领域的主力研究者） |
| **发布** | 2020-05-11 |
| **分类** | eess.SP（信号处理）/ 电力系统 |
| **类型** | 综述与展望 |
| **链接** | [arXiv](https://arxiv.org/abs/2005.05380) \| [PDF](https://arxiv.org/pdf/2005.05380) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2005.05380_fig1.png]]

![[2005.05380_fig2.png]]

![[2005.05380_fig3.png]]

![[2005.05380_fig4.png]]

![[2005.05380_fig5.png]]

![[2005.05380_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：三个驱动力推动 DSE 成为热点

原文点出三个原因：

1. **缺乏精确的模型** —— 电网越来越复杂（尤其是电力电子设备），传统模型不够准
2. **快速采样、时间同步的量测越来越多** —— PMU（相量测量单元）提供了毫秒级的同步数据
3. **计算与通信能力提升** —— 算得起、传得动

### 静态 vs 动态：核心区别

| 维度 | 静态状态估计（SSE） | 动态状态估计（DSE） |
|---|---|---|
| **假设** | 系统处于稳态，各时刻独立 | 系统状态随时间演化 |
| **数学模型** | $z = h(x) + e$ | $x_{k+1} = f(x_k) + w_k$，$z_k = h(x_k) + v_k$ |
| **时间尺度** | 分钟级（SCADA 刷新周期） | **毫秒~秒级**（PMU 采样） |
| **算法** | 加权最小二乘（WLS） | **卡尔曼滤波**（EKF / UKF / EnKF） |
| **能干什么** | 知道当前运行点 | **预测**、跟踪机电暂态、检测振荡 |
| **数据需求** | SCADA/RTU 量测 | PMU 同步相量 + 动态模型 |

### 论文的三个视角

**1）建模（Modeling）**
DSE 需要**发电机/变流器的动态模型**（转子运动方程、励磁系统、调速器）。
→ 模型不准，估计就不准。这是 DSE 最大的痛点。

**2）监测（Monitoring）**
- 跟踪发电机转子角、转速、内电势等**无法直接量测**的内部状态
- 检测**低频振荡**（inter-area oscillation）
- 用于**事件检测与分类**

**3）运行（Operation）**
- **时间关键型应用**：紧急控制、广域阻尼控制
- 提升系统的**鲁棒性与韧性**

### 面向未来：同步机 → 电力电子变流器

论文特别讨论了从"同步发电机主导"到"**电力电子接口电源主导**"的转变：
- 变流器没有物理转子 → 传统的转子运动方程失效
- 需要**新的动态模型**和**新的估计方法**（虚拟同步机、构网型控制等）

## 关键公式（小白版）

**动态状态估计的标准形式**：

$$\begin{cases} x_{k+1} = f(x_k, u_k) + w_k & \text{(状态方程：系统怎么演化)} \\ z_k = h(x_k) + v_k & \text{(量测方程：我们看到什么)} \end{cases}$$

其中 $w_k \sim \mathcal{N}(0, Q)$ 是过程噪声，$v_k \sim \mathcal{N}(0, R)$ 是量测噪声。

**卡尔曼滤波的直觉**：

$$\hat{x}_k = \underbrace{\hat{x}_k^-}_{\text{预测值}} + K_k \underbrace{(z_k - h(\hat{x}_k^-))}_{\text{新息（残差）}}$$

> **一句话理解**：先按物理模型预测，再用实际量测修正。$K$ 决定"更相信模型还是更相信量测"。

**这正是安全研究的切入点**：如果攻击者能操纵 $z_k$，他就能操纵 $\hat{x}_k$。

## 用网安的话说（小电解读）

> DSE 相当于一个**带物理模型的实时状态跟踪器（类似粒子滤波/目标跟踪）**。

- **它和静态 SE 的安全含义不同**：
  - 攻击静态 SE：污染某一时刻的"快照"
  - 攻击动态 SE：**持续污染跟踪过程**，可以让估计值**逐渐偏离**真实轨迹而不被发现 → 更隐蔽、更危险
- **攻击面更多**：
  - 量测 $z$（FDIA 经典路径）
  - 模型参数（如篡改发电机惯性常数 $M$、阻尼系数 $D$）
  - 状态转移函数 $f$（篡改控制逻辑）
- **检测难度更大**：因为 DSE 本身就在处理噪声和不确定性，"异常"的边界更模糊。

**对研一学生的意义**：
- 这是"**AI/信号处理 + 电力物理**"的交叉点 —— 卡尔曼滤波、粒子滤波、深度学习估计器都是你的技术储备。
- **选题启发**：**面向 DSE 的隐蔽攻击与检测**，比静态 SE 场景的工作少得多，有空间。

## 读完后你应该能回答

- [ ] 静态状态估计和动态状态估计的根本区别是什么？
- [ ] 为什么 PMU 的出现推动了 DSE 的发展？
- [ ] DSE 在"时间关键型应用"中扮演什么角色？
- [ ] 高比例电力电子设备给 DSE 带来了什么新挑战？

## 局限性

- **综述性质**，重在讲"角色"和"方向"，具体算法实现与实验对比不深入。
- 面向的是**输电系统 + 大机组**场景，配电系统（量测稀疏、拓扑多变）的 DSE 讨论较少。
- **未涉及安全性（攻击）视角** —— 这恰恰是留给你的空间。

## 和你的方向有什么关系

- **技术迁移点**：卡尔曼滤波 → 你在信号处理/状态估计上的能力可以直接复用。
- **选题方向**：
  1. **DSE 场景下的 FDIA 攻击构造与检测**（相比静态 SE 更少人做）
  2. **模型参数攻击**（篡改惯性常数等物理参数）—— 很有新意
  3. **用深度学习加速 DSE**（如 PINN、Transformer 替代卡尔曼滤波）并评估其安全性
- 与实验室方向对接：**"工业AI与智能体"**（AI 替代传统估计器）、**"AI与数据安全"**（数据完整性）。

## 概念关联

- 核心概念：[[状态估计]] · [[虚假数据注入攻击(FDIA)]] · [[电力系统稳定性]] · [[工控安全测试床与数据集]]
- 前置阅读：[[20_Research/Papers/L1-零基础起步/面向电力信息物理系统的虚假数据注入攻击研究综述|003]]
- 后续阅读：[[20_Research/Papers/L2-电力系统基础/Power_System_Dynamic_State_Estimation_Using_Extended_and_Unscented_Kalman_Filters|009 用 EKF/UKF 做动态状态估计]]（理论 → 实操）
- 攻击视角：[[20_Research/Papers/L3-工控与电网安全/Vulnerability_Analysis_and_Consequences_of_False_Data_Injection_Attack_on_Power_System_State_Estimation|024 FDIA 脆弱性分析]]
- AI 方法：[[20_Research/Papers/L4-AI与电网安全/State_Estimation_in_Electric_Power_Systems_Leveraging_Graph_Neural_Networks|033 用 GNN 做状态估计]]

## 原文摘要

> Power system dynamic state estimation (DSE) remains an active research area. This is driven by the absence of accurate models, the increasing availability of fast-sampled, time-synchronized measurements, and the advances in the capability, scalability, and affordability of computing and communications. This paper discusses the advantages of DSE as compared to static state estimation, and the implementation differences between the two, including the measurement configuration, modeling framework and support software features. The important roles of DSE are discussed from modeling, monitoring and operation aspects for today's synchronous machine dominated systems and the future power electronics-interfaced generation systems. Several examples are presented to demonstrate the benefits of DSE on enhancing the operational robustness and resilience of 21st century power system through time critical applications. Future research directions are identified and discussed, paving the way for developing the next generation of energy management systems.
