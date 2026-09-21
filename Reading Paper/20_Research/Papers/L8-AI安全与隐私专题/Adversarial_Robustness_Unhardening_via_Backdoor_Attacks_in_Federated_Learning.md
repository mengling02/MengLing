---
document_id: "arxiv-2310.11594"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2310.11594"
arxiv_id: "2310.11594"
title: "Adversarial Robustness Unhardening via Backdoor Attacks in Federated Learning"
authors: ["Taejin Kim", "Jiarui Li", "Shubhranshu Singh", "Nikhil Madaan", "Carlee Joe-Wong"]
published: "2023-10-17"
venue: "arXiv preprint"
domain: "L8-AI安全与隐私专题"
level: "L8"
reading_order: 69
difficulty: "进阶"
lang: "en"
tags: ["电网安全", "L8-AI安全与隐私专题", "联邦学习", "后门攻击", "对抗训练", "鲁棒聚合"]
quality_score: 8
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 069 | 通过联邦学习中的后门攻击实现"对抗鲁棒性软化"

> [!abstract] 一句话
> 对抗训练本来是用来防对抗样本的，但这篇论文发现：攻击者可以反过来利用后门攻击**故意把模型的对抗鲁棒性"软化"**，让它对更多对抗样本都变得脆弱，甚至能绕过鲁棒聚合防御。

## 为什么读它

- **这篇论文的思路非常"反直觉"，是很好的选题思路范本**：一般人想的是"后门攻击的目标是让模型在特定输入上误分类"；这篇论文想的是"**后门攻击能不能被用来削弱模型的其他防御能力**"。攻击目标从"让模型答错"变成了"让模型变脆"——这是攻击目标层面的创新，而不是攻击手段层面的创新。
- 它把两个原本分开研究的领域**接在了一起**：**对抗训练**（防御对抗样本）和**后门攻击**（联邦学习投毒的一种）。你如果只读一个方向的论文，很难想到这种交叉。
- 它的结论对你理解电力场景的威胁模型很重要：**电网里的 AI 检测器如果用了对抗训练（比如 072 就在用），那么它可能反而给攻击者开了一扇新门。**
- 建议读法：重点看它怎么定义 ARU 的攻击目标，以及它为什么能绕过鲁棒聚合防御（这一点是全篇最反直觉的）。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | Adversarial Robustness Unhardening via Backdoor Attacks in Federated Learning（通过联邦学习中的后门攻击实现对抗鲁棒性软化） |
| 作者 | Taejin Kim, Jiarui Li, Shubhranshu Singh, Nikhil Madaan, Carlee Joe-Wong（CMU 等） |
| 发表 | arXiv preprint, 2023-10-17 |
| 链接 | [arXiv](https://arxiv.org/abs/2310.11594) |
| 类型 | arXiv 预印本 |
| 难度 | 进阶 |
| 关键词 | 联邦学习、后门攻击、对抗训练、对抗鲁棒性软化（ARU）、鲁棒聚合、逃逸攻击 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2310.11594_fig1.png]]

![[2310.11594_fig2.png]]

![[2310.11594_fig3.png]]

![[2310.11594_fig4.png]]

![[2310.11594_fig5.png]]

![[2310.11594_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：联邦学习的两类安全威胁

论文开头复述了一个你早就熟的张力：联邦学习（Federated Learning, FL）让各方在不共享数据的前提下协同训练模型，但**它也带来了新的安全问题**，具体是两类：

- **投毒攻击（Poisoning Attack）与后门攻击（Backdoor Attack）**：恶意参与方在训练过程中**注入被污染的数据**（更准确地说，在联邦学习里是注入被污染的**模型更新**），让全局模型学坏。后门攻击的特点是：模型在正常输入上表现正常，只在**带触发器（trigger）的输入**上出错——非常隐蔽。
- **逃逸攻击（Evasion Attack）**：训练阶段不动手脚，只在**测试阶段**对输入做微小扰动，诱导模型误分类。这就是你熟悉的**对抗样本**。

这两类攻击对应的防御也不同：

- 对付投毒/后门，用**鲁棒聚合（robust aggregation）**——服务器在聚合时不简单求平均，而是先剔除"看起来可疑"的客户端更新（Krum、Trimmed Mean、Median 这类方法）。
- 对付逃逸攻击，用**对抗训练（Adversarial Training）**——训练时主动把对抗样本喂给模型，让它"见过世面"，从而在测试时更抗扰动。

### 核心洞察：两种防御之间的裂缝

论文的研究切入点就是：**对抗训练（防逃逸）和后门攻击（投毒的一种）在联邦学习里相遇时会发生什么？**

这里有一个关键逻辑：

> **对抗训练会把模型的决策边界"磨平"**——为了在对抗样本附近保持预测稳定，模型必须变得"平滑"。
> **而攻击者恰恰可以利用这一点**：如果我能通过后门机制**操纵模型的平滑程度**，我就不是在"攻击某个具体样本"，而是在**系统性地削弱模型对所有对抗样本的抵抗力**。

于是论文提出了 **ARU（Adversarial Robustness Unhardening，对抗鲁棒性软化）**。注意这个词的构词：正常叫 **hardening**（加固），ARU 就是**反向的加固**——不是让模型更鲁棒，而是让它更不鲁棒。

### 方法：ARU 怎么工作

**攻击者的设定**：联邦学习的一小部分客户端是**对抗客户端（adversarial clients）**，他们在联邦训练过程中参与，目标是**故意削弱模型的鲁棒性**。

**攻击的效果**：模型在训练完成后，会对**更广泛范围的逃逸攻击**变得脆弱（susceptible to a broader range of evasion attacks）。注意这里是"更广泛范围"，不是"某个特定触发器"——**这是 ARU 与传统后门攻击的本质区别**：

| | 传统后门攻击 | ARU |
|---|---|---|
| 攻击目标 | 让模型在**带触发器的特定输入**上出错 | 让模型**整体对抗鲁棒性下降** |
| 攻击的"精度" | 精确、有针对性 | 弥散、面向全局 |
| 检测难度 | 可以扫描触发器 | 更隐蔽，因为没有明显的"后门样本" |
| 攻击者的收益 | 攻破特定样本 | 后续可任意发动逃逸攻击 |

**论文做的大量实验**，评估了 ARU 对两件事的影响：

1. 对**对抗训练**的影响——即"我用了对抗训练，还扛不扛得住"；
2. 对**现有的抗投毒/抗后门鲁棒聚合防御**的影响——即"我用了 Krum/Trimmed Mean 这类防御，还扛不扛得住"。

### 结论（两个都是"坏消息"）

论文的结果是两个负面结论：

1. **ARU 可以显著削弱对抗训练的效果**。也就是说，你花了计算代价做对抗训练，但攻击者用 ARU 可以把它"白做"。
2. **使用 ARU 的攻击者甚至可以绕过鲁棒聚合防御**——而这类防御通常能够中和投毒攻击和后门攻击。

第 2 点是最反直觉的。原因是：**鲁棒聚合防御的判据是"这个更新离大多数更新有多远"**（离群点检测思路）。而 ARU 的攻击目标不是让模型输出错，而是让模型变"平滑"——这种更新在参数空间里**可能并不离群**，反而看起来"很正常"。于是基于距离/统计的鲁棒聚合**看不到异常**。

## 关键公式（小白版）

论文摘要没有给出公式。理解 ARU，需要先看**对抗训练**的标准形式（这是该领域的通用形式，不是本文摘要给出的）：

$$\min_{\theta}\ \mathbb{E}_{(x,y)\sim \mathcal{D}}\left[\ \max_{\|\delta\|_{p}\le \epsilon}\ \ell\big(f_{\theta}(x+\delta),\, y\big)\ \right]$$

符号解释：

- $\theta$ —— 模型参数。
- $(x, y)$ —— 训练样本与标签。
- $\delta$ —— 加在输入上的**扰动**（对抗扰动）。
- $\|\delta\|_p \le \epsilon$ —— 扰动被限制在一个小范围内（$p$ 通常取 2 或 $\infty$，$\epsilon$ 是扰动预算）。
- $\ell(\cdot,\cdot)$ —— 损失函数。
- 内层 $\max$ —— 攻击者视角：**找到让损失最大的那个扰动**（即最强的对抗样本）。
- 外层 $\min$ —— 防御者视角：**调整模型参数，让这个最坏情况下的损失最小**。

**一句话白话**：对抗训练就是"**我先把最难的情况找出来，然后专门练它**"。这也是它代价高的原因——每一步都要先解一个内层优化问题。

**ARU 的做法，可以理解为把这个内层目标反过来用**：攻击者不是让模型在扰动下"损失最小"，而是通过后门机制**让模型在扰动下损失更大**——即**主动破坏那个外层 $\min$ 的效果**。

> 注意：ARU 的具体数学形式（如何把后门目标写成对鲁棒性的削弱）**摘要中没有给出**，上面只是帮助你理解对抗训练与 ARU 关系的通用框架，具体公式请查原文。

## 用网安的话说（小电解读）

**这篇论文对应你非常熟的一个攻防范式：让防御机制本身成为攻击面。**

**对照表**：

| 你熟悉的 | ARU |
|---|---|
| 安全加固（hardening） | 反向操作：软化（unhardening） |
| 让杀软失效（而不是绕过某个具体病毒） | 让模型的对抗鲁棒性整体失效（而不是绕过某个具体样本） |
| 防御规避（Defense Evasion） | **削弱防御**，而非绕过防御——这是更彻底的一步 |
| 后门作为"武器" | 后门作为"**削弱其他防御的工具**" |

**这个区分很重要，值得你记住：**

- **绕过防御**：防御还在，但我找到了它的盲区。防御能力没有变化。
- **削弱防御**：我主动让防御能力下降。之后再攻击就轻松了。

ARU 属于后者，而且它用的是**训练阶段的投毒能力**去削弱**推理阶段的鲁棒性**。这是一次"跨阶段"的攻击——**训练阶段的攻击者影响了测试阶段的防御属性**。

**攻击面在哪**：在**联邦学习的参与方**上。攻击者不需要攻破服务器、不需要窃听链路，只需要**成为一个小比例的客户端**，然后在本地训练时做手脚。这个门槛非常低——任何开放参与的联邦学习系统都天然满足。

**为什么能绕过鲁棒聚合（这是最关键的一点）**：

鲁棒聚合（Krum、Trimmed Mean 等）的假设是"**恶意更新的数值分布与诚实更新显著不同**"。它本质上是一个**离群点检测器**。

而 ARU 的更新不是"数值异常"，而是"**方向异常**"——它把模型往"更不平滑"的方向推。这个方向的偏移量可能很小，**在数值上完全不离群**，但在功能上（对鲁棒性的影响）是致命的。

> **这和你熟悉的"低慢小"攻击（Low and Slow Attack）是同一个道理**：单次行为看起来完全正常，只有长期累积才显现恶意效果。鲁棒聚合是"逐轮看"的，看不出跨轮累积的效应。

**如果要迁移到你的研究**：

1. **面向电网 AI 检测器的"防御削弱"攻击**——电网里大量检测器（FDIA 检测、异常检测）都在用对抗训练或数据增强来提升鲁棒性（072 就是）。**ARU 的思路能不能搬过去？** 这是一个几乎没人做过的方向，而且和你的"AI与数据安全"方向完美契合。
2. **物理约束能不能作为检测 ARU 的抓手**——电网有一个 ARU 在图像领域没有的东西：**物理规律**。一个被"软化"的负荷预测模型可能在某些物理约束上表现出异常。这可能是电力场景独有的防御思路。
3. **ARU 在去中心化联邦学习（068）中的变体**——没有中心聚合器，鲁棒聚合本身就不存在，ARU 会更难防。

## 读完后你应该能回答

- [ ] 后门攻击和逃逸攻击分别发生在训练的哪个阶段？分别对应什么防御？
- [ ] 什么是 ARU？它和传统后门攻击的目标有什么本质区别？
- [ ] 为什么 ARU 能绕过鲁棒聚合防御？鲁棒聚合的隐含假设是什么？
- [ ] 对抗训练为什么可以被"削弱"？它的代价是什么？
- [ ] 为什么说 ARU 是一种"跨阶段"攻击？

## 局限性

- **纯通用方法，没有任何电力场景**：论文在通用联邦学习数据集上验证，没有涉及负荷、量测、状态估计等电力数据。迁移到电力场景需要重新验证——**这也正是空白所在**。
- **摘要未给出任何具体数值**：只说 ARU"可以显著削弱"对抗训练、"甚至可以绕过"鲁棒聚合，**没有给出鲁棒性下降的幅度、攻击者比例、攻击成功率等数字**。要评估攻击的实际威胁程度必须查原文。
- **攻击者假设偏强**：攻击者需要能控制一部分客户端，且这些客户端的本地训练过程完全不受监控。现实中如果联邦学习平台对客户端做验证，攻击难度会上升。
- **没有提出防御**：论文是纯攻击论文，没有给出针对 ARU 的检测或缓解方案（论文只"评估"了现有防御的失效情况）。**这是一个明确的后续工作空间。**
- **"软化"的度量方式依赖具体的鲁棒性评估指标**（比如特定 ε 下的对抗准确率），换一个指标结论可能不同，论文摘要没有说明它用了哪些指标。

## 和你的方向有什么关系

- **这是本专题里"攻击思路创新"最强的一篇**，非常适合作为你构思选题的方法论范本：**不要只想着"用什么新方法攻击"，要想"攻击能不能改变模型的某种属性"。**
- **直接选题（按推荐度）**：
  1. **电力 AI 检测器的对抗鲁棒性软化攻击**——把 ARU 迁移到 FDIA 检测器/负荷预测模型上，验证"攻击者能否让检测器整体变脆"。**迁移成本低、创新点明确、结论直接可用。**
  2. **检测 ARU 的物理约束方法**——电力场景独有，属于"用领域知识做防御"。
  3. **ARU 与鲁棒聚合的攻防博弈分析**——从博弈论角度刻画"聚合方能不能通过调整判据来发现方向异常"。
- **与实验室方向的对接**："AI与数据安全"直接对口（模型鲁棒性、投毒）；"入侵检测"对应"检测器自身的鲁棒性"；"工业AI与智能体"对应联邦智能体协同中的恶意节点。

## 概念关联

[[后门攻击]] · [[对抗样本攻击]] · [[联邦学习攻击与防御]] · [[联邦学习]] · [[数据投毒攻击]]

## 原文摘要

> The delicate equilibrium between user privacy and the ability to unleash the potential of distributed data is an important concern. Federated learning, which enables the training of collaborative models without sharing of data, has emerged as a privacy-centric solution. This approach brings forth security challenges, notably poisoning and backdoor attacks where malicious entities inject corrupted data into the training process, as well as evasion attacks that aim to induce misclassifications at test time. Our research investigates the intersection of adversarial training, a common defense method against evasion attacks, and backdoor attacks within federated learning. We introduce Adversarial Robustness Unhardening (ARU), which is employed by a subset of adversarial clients to intentionally undermine model robustness during federated training, rendering models susceptible to a broader range of evasion attacks. We present extensive experiments evaluating ARU's impact on adversarial training and existing robust aggregation defenses against poisoning and backdoor attacks. Our results show that ARU can substantially undermine adversarial training's ability to harden models against test-time evasion attacks, and that adversaries employing ARU can even evade robust aggregation defenses that often neutralize poisoning or backdoor attacks.
