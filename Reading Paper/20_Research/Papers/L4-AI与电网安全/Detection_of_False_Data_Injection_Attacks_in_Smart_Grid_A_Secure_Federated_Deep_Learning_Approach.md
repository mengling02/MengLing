---
document_id: "arxiv-2209.00778"
arxiv_id: "2209.00778"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2209.00778"
title: "Detection of False Data Injection Attacks in Smart Grid: A Secure Federated Deep Learning Approach"
zh_title: "智能电网虚假数据注入攻击检测：一种安全联邦深度学习方法"
authors: ["Yang Li", "Xinhao Wei", "Yuanzheng Li", "Zhaoyang Dong", "Mohammad Shahidehpour"]
published: "2022-09-02"
venue: "IEEE Transactions on Smart Grid 13 (2022) 4862-4872；arXiv:2209.00778"
domain: "L4-AI与电网安全"
level: "L4"
reading_order: 29
difficulty: "进阶"
tags: ["论文笔记", "L4-AI与电网安全", "联邦学习", "FDIA检测", "Transformer", "同态加密"]
quality_score: 9
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 029 | 智能电网虚假数据注入攻击检测：一种安全联邦深度学习方法

> [!abstract] 一句话
> **Transformer（检测器）+ 联邦学习（隐私）+ Paillier 同态加密（安全）三件套**：在 IEEE 14/118 节点系统上验证，既保护隐私又检测 FDIA。

## 为什么读它

这是 L4 的**技术实例**：把 [[20_Research/Papers/L4-AI与电网安全/Federated_Learning_for_Smart_Grid_A_Survey_on_Applications_and_Potential_Vulnerabilities|028]] 讲的方向真正实现出来。

价值：
- **发表在 IEEE Transactions on Smart Grid**（电力领域顶刊）→ 质量保证
- **三个技术的组合很典型** → 你可以学到"怎么把多个技术拼成一篇论文"
- **作者阵容强**（Mohammad Shahidehpour 是电力系统领域的高被引学者）
- 有明确的**数据集和对比基线** → 便于复现

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Detection of False Data Injection Attacks in Smart Grid: A Secure Federated Deep Learning Approach |
| **作者** | Yang Li, Xinhao Wei, Yuanzheng Li, Zhaoyang Dong, Mohammad Shahidehpour（东南大学、新南威尔士大学、伊利诺伊理工等） |
| **发表** | IEEE Transactions on Smart Grid, 13 (2022) 4862-4872 |
| **发布** | 2022-09-02 |
| **分类** | cs.CR |
| **链接** | [arXiv](https://arxiv.org/abs/2209.00778) \| [PDF](https://arxiv.org/pdf/2209.00778) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2209.00778_fig1.png]]

![[2209.00778_fig2.png]]

![[2209.00778_fig3.png]]

![[2209.00778_fig4.png]]

![[2209.00778_fig5.png]]

![[2209.00778_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 出发点：FDIA 检测中的隐私盲区

> 原文：*"However, so far little attention has been paid to privacy preservation issues in the detection of FDIAs in smart grid."*

**问题**：大家都在研究"怎么检测 FDIA"，但**没人关注"检测过程中的隐私问题"**。

**为什么会有隐私问题？**
- FDIA 检测需要**跨区域的数据**（攻击可能跨区域协同）
- 但数据属于不同电力公司，**不能直接共享**（商业机密 + 用户隐私）
- → 需要**联邦学习**

### 方法：三个技术的组合

**1）Transformer 作为检测器**

> 原文：*"The Transformer, as a detector deployed in edge nodes, delves deep into the connection between individual electrical quantities by using its multi-head self-attention mechanism."*

**Transformer 的多头自注意力机制**能捕捉**各电气量之间的关联**：
- 电压、电流、功率之间的物理关联
- 跨节点的空间关联
- 时间上的演化关联

> **小电解读**：这是很聪明的设计 —— FDIA 攻击会破坏电气量之间的**关联模式**（因为攻击者要满足 $a = Hc$ 的约束，往往会留下关联上的破绽）。Transformer 的注意力机制正好擅长捕捉这种关联。

**2）联邦学习框架**

> 原文：*"By using federated learning framework, our approach utilizes the data from all nodes to collaboratively train a detection model while preserving data privacy by keeping the data locally during training."*

**数据留在本地**，只共享模型参数 → 保护隐私。

**3）Paillier 同态加密**

> 原文：*"To improve the security of federated learning, a secure federated learning scheme is designed by combing Paillier cryptosystem with federated learning."*

**为什么联邦学习还不够安全？**
因为**梯度本身会泄露信息**（见 [[20_Research/Papers/L4-AI与电网安全/Federated_Learning_for_Smart_Grid_A_Survey_on_Applications_and_Potential_Vulnerabilities|028]] 里的"梯度泄露"攻击）。

**Paillier 同态加密**：允许**在密文上直接计算** → 服务器可以在**看不到明文梯度**的情况下聚合。

> **加法同态**：$\text{Enc}(a) \cdot \text{Enc}(b) = \text{Enc}(a + b)$
> → 服务器把密文梯度相加，解密后得到梯度之和，但**从未见过任何单个客户端的梯度**。

### 实验

| 项目 | 内容 |
|---|---|
| **测试系统** | IEEE 14 节点、IEEE 118 节点 |
| **结论** | 论文声明方法的**有效性和优越性**得到验证 |

## 用网安的话说（小电解读）

> 这篇论文是**"隐私增强技术（PET）+ AI 检测"的标准模板**，你可以拆解学习。

**三件套的作用分工**：

```
Transformer  → 解决"检测精度"问题（算法层）
联邦学习      → 解决"数据不出域"问题（架构层）
Paillier 加密 → 解决"梯度泄露"问题（密码学层）
```

**这个分层思路很重要**：**每一层解决一个维度的问题**。
你以后设计系统时，可以问：**"我这一层解决什么问题？还有什么没解决？"**

**论文没有解决什么（你的机会）**：

| 未解决的问题 | 说明 |
|---|---|
| **投毒攻击** | Paillier 保护了梯度机密性，但**不防投毒**（恶意客户端可以上传"合法加密的恶意梯度"） |
| **计算开销** | 同态加密**计算代价高**，电网要求实时 → 这是硬约束 |
| **通信开销** | Transformer 参数量大 → 联邦通信负担重 |
| **非独立同分布** | 不同区域数据分布差异大 → FL 收敛困难 |
| **对抗鲁棒性** | Transformer 检测器本身可能被[[对抗样本攻击]] |
| **物理约束未利用** | 检测器是纯数据驱动的，没用物理模型 |

> **最后一条尤其值得注意**：论文用 Transformer 学"电气量之间的关联"，但**没有显式地使用物理方程**。
> → **"物理信息增强的联邦 FDIA 检测"** 是一个自然的改进方向。

**另一个观察**：
> 论文的**安全设计是"加法式"的**（Transformer + FL + 加密）。
> 但**安全性不是加法**：FL 引入了新攻击面，加密引入了新开销。
> → **"端到端的安全分析"比"堆叠安全组件"更重要** —— 这是你可以指出的问题。

## 读完后你应该能回答

- [ ] 为什么 FDIA 检测需要联邦学习？
- [ ] 为什么联邦学习还需要额外的加密（Paillier）？
- [ ] 同态加密的"加法同态"性质在联邦聚合中怎么用？
- [ ] Transformer 为什么适合做 FDIA 检测？
- [ ] 这个方案还有哪些未解决的安全问题？

## 局限性

- **未考虑投毒攻击**（同态加密只保护机密性，不保护完整性/可用性）。
- **计算和通信开销大**（Transformer + 同态加密），与电网实时性要求存在张力。
- 实验在 **IEEE 标准系统**上（14/118 节点），未验证真实电网规模的可行性。
- **未做对抗鲁棒性评估**（检测器被对抗样本攻击会怎样？）。
- 未考虑**非独立同分布（non-IID）**数据场景。

## 和你的方向有什么关系

- **这是"隐私保护 + AI 检测"的标准范例**，你可以照此结构设计自己的方案。
- **直接选题（改进这篇）**：
  1. **抗投毒的安全联邦 FDIA 检测**（补上最大缺口）
  2. **轻量级同态加密 / 安全多方计算**（降低开销）
  3. **物理信息增强的联邦检测**（用物理约束提升精度和鲁棒性）
  4. **对抗鲁棒的联邦 FDIA 检测器**
- **技术储备**：Transformer、联邦学习、同态加密 —— 这三样都是你实验室"AI与数据安全"方向的核心技术。
- **写作启示**：注意论文的**"三件套"叙事结构** —— 每个技术解决一个明确问题。这是好论文的常见写法。

## 概念关联

- 核心概念：[[联邦学习]] · [[虚假数据注入攻击(FDIA)]] · [[入侵检测系统(IDS)]] · [[对抗样本攻击]] · [[状态估计]]
- 前置阅读：[[20_Research/Papers/L4-AI与电网安全/Federated_Learning_for_Smart_Grid_A_Survey_on_Applications_and_Potential_Vulnerabilities|028 联邦学习用于智能电网综述]]
- 检测背景：[[20_Research/Papers/L3-工控与电网安全/A_Survey_of_Machine_Learning_Methods_for_Detecting_False_Data_Injection_Attacks|022 FDIA 检测的机器学习方法综述]]
- 后续阅读：[[20_Research/Papers/L4-AI与电网安全/Adversarial_Attacks_on_Time-Series_Intrusion_Detection_for_Industrial_Control_Systems|031 针对时序入侵检测的对抗攻击]]

## 原文摘要

> As an important cyber-physical system (CPS), smart grid is highly vulnerable to cyber attacks. Amongst various types of attacks, false data injection attack (FDIA) proves to be one of the top-priority cyber-related issues and has received increasing attention in recent years. However, so far little attention has been paid to privacy preservation issues in the detection of FDIAs in smart grid. Inspired by federated learning, a FDIA detection method based on secure federated deep learning is proposed in this paper by combining Transformer, federated learning and Paillier cryptosystem. The Transformer, as a detector deployed in edge nodes, delves deep into the connection between individual electrical quantities by using its multi-head self-attention mechanism. By using federated learning framework, our approach utilizes the data from all nodes to collaboratively train a detection model while preserving data privacy by keeping the data locally during training. To improve the security of federated learning, a secure federated learning scheme is designed by combing Paillier cryptosystem with federated learning. Through extensive experiments on the IEEE 14-bus and 118-bus test systems, the effectiveness and superiority of the proposed method is verifed.
