---
document_id: "arxiv-2506.19302"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2506.19302"
arxiv_id: "2506.19302"
title: "Adversarial Attacks on Deep Learning-Based False Data Injection Detection in Differential Relays"
authors: ["Ahmad Mohammad Saber", "Aditi Maheshwari", "Amr Youssef", "Deepa Kundur"]
published: "2025-06-24"
venue: "arXiv preprint"
domain: "L8-AI安全与隐私专题"
level: "L8"
reading_order: 72
difficulty: "进阶"
lang: "en"
tags: ["电网安全", "L8-AI安全与隐私专题", "对抗样本", "差动保护", "虚假数据注入攻击", "对抗训练"]
quality_score: 8
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 072 | 针对差动继电器中基于深度学习的虚假数据注入检测的对抗攻击

> [!abstract] 一句话
> 线路电流差动继电器用深度学习来判断"电流差是故障还是被注入的假数据"；这篇论文用 FGSM 构造微小扰动，让检测器把攻击误判成真实故障，**直接触发继电器跳闸**——部分模型攻击成功率超过 99.7%。

## 为什么读它

- **这是本专题里"物理后果最严重"的一篇。** 前面几篇的攻击后果是"模型出错"；这篇的攻击后果是**继电器跳闸**——也就是**真实世界里的停电**。它把"AI 模型被对抗样本骗了"和"电网设备误动作"之间的因果链条完整地连了起来。
- **它用的是最经典的攻击方法（FGSM），但打的是最"硬"的场景（保护装置）。** 这一点很有教学价值：**你不需要发明新攻击，把成熟攻击用到没被验证过的场景里，本身就是一篇有价值的论文**——而且这类工作的实验结论通常很惊人（99.7% 成功率）。
- **它同时给出了防御（对抗训练）并验证了防御有效**，是一篇结构完整的"攻击—防御"论文，适合作为你写第一篇论文的模板。
- **它和 071 是姊妹篇**：071 打的是调度中心的 FDIA 定位检测器（多标签），这篇打的是变电站里的差动继电器检测器（二分类）。两篇对照，你能看清"同一个攻击思路在不同电力环节的落地差异"。
- 建议读法：先搞清楚"差动保护是什么"，再看攻击为什么能把 FDIA 伪装成"真实故障"。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | Adversarial Attacks on Deep Learning-Based False Data Injection Detection in Differential Relays（针对差动继电器中基于深度学习的虚假数据注入检测的对抗攻击） |
| 作者 | Ahmad Mohammad Saber, Aditi Maheshwari, Amr Youssef, Deepa Kundur（多伦多大学等） |
| 发表 | arXiv preprint, 2025-06-24 |
| 链接 | [arXiv](https://arxiv.org/abs/2506.19302) |
| 类型 | arXiv 预印本 |
| 难度 | 进阶 |
| 关键词 | 对抗样本、FGSM、线路电流差动继电器、FDIA 检测、对抗训练、误跳闸 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2506.19302_fig1.png]]

![[2506.19302_fig2.png]]

![[2506.19302_fig3.png]]

![[2506.19302_fig4.jpeg]]

![[2506.19302_fig5.jpeg]]

![[2506.19302_fig6.jpg]]

---


## 这篇论文在讲什么（白话版）

### 背景知识一：什么是差动继电器（这是读懂本文的前提）

**线路电流差动继电器（Line Current Differential Relay, LCDR）** 是输电线路的主保护装置。它的原理非常好懂：

> **一条线路的两端各装一个电流互感器，正常情况下，"流入的电流"应该等于"流出的电流"（电流守恒）。如果两端的电流差超过阈值，说明电流"漏"出去了——那就意味着线路上发生了故障（比如短路到地），继电器立刻动作，断开线路（这叫"跳闸 trip"）。**

**这个原理为什么依赖通信？** 因为线路两端可能相距几十上百公里，一端的电流值必须**通过通信链路传给另一端**才能做比较。这就是所谓的**远程量测（remote measurements）**。

**于是攻击面出现了**：如果攻击者能篡改这条通信链路上的远程量测值，就能**伪造出一个"电流不平衡"的假象**，让继电器误以为发生了故障——**然后跳闸**。

### 背景知识二：深度学习被引入来做 FDIA 检测

问题在于：**"电流不平衡"既可能是真实故障，也可能是攻击者注入的假数据（FDIA）**。继电器必须区分这两种情况：

- 如果是**真实故障** → 应该跳闸（保护线路）；
- 如果是**FDIA 攻击** → 不应该跳闸（否则攻击者就得逞了）。

论文指出，**基于深度学习的方案（Deep Learning-based Schemes, DLSs）** 已经被大量用于这个检测任务，因为它们能从电流波形里学到"故障"和"攻击"的细微差异。

**这里有一个隐含的对抗关系，值得你注意**：

> 传统上，**攻击者的目标是"让继电器不跳闸"**（让保护失效，好让真实的物理攻击得逞）。
> **而这篇论文的攻击目标恰恰相反——让继电器"错误地跳闸"（误动）。**

**为什么"误跳闸"也是攻击目标？** 因为**电网是一个强耦合系统**。一条关键线路无故跳闸，会导致潮流重新分布，可能引发连锁过载，最终演变成**大停电**。所以"误跳闸"是一种典型的**可用性攻击（Availability Attack）**——不需要破坏任何设备，只要让保护装置自己"打自己"就行。

### 方法：用 FGSM 构造对抗 FDIA

论文提出的攻击框架使用 **FGSM（Fast Gradient Sign Method，快速梯度符号法）**。

**FGSM 是什么？** 它是对抗样本领域最经典、最简单的方法。核心思想是：**沿着损失函数的梯度方向，把输入往"让模型判断错"的方向推一小步。**

**论文的攻击怎么做的**：对 **LCDR 的远程量测（remote measurements）** 引入**微小的扰动（small perturbations）**，利用 DLS 模型的脆弱性，达到两个效果：

1. **把 FDIA 误分类为"合法故障"**——检测器认为这是真实的物理故障，而不是攻击；
2. **同时触发 LCDR 跳闸**——继电器基于这个错误判断执行了保护动作。

**这两个效果合起来，就是攻击的完整杀伤链**：

```
篡改远程量测（加微小扰动）
  → 深度学习检测器被欺骗，判定为"真实故障"
    → 继电器执行跳闸
      → 线路断开，潮流重分布
        → 潜在的连锁故障 / 大停电
```

### 实验：测了四类模型，全都很脆弱

论文评估了**多个深度学习模型**在对抗条件下的鲁棒性，包括：

- **多层感知机（Multi-Layer Perceptron, MLP）**
- **卷积神经网络（Convolutional Neural Network, CNN）**
- **长短期记忆网络（Long Short-Term Memory, LSTM）**
- **残差网络（Residual Network, ResNet）**

**结论**（这是摘要给出的唯一数值）：

> 这些模型在正常情况下表现都很好（"perform well"），但它们**对对抗攻击表现出高度的脆弱性（high degrees of vulnerability）**。**对其中一些模型，对抗攻击成功率超过 99.7%。**

**99.7% 意味着什么？** 意味着攻击者几乎可以**确定地**触发误跳闸。这不是"偶尔能成功"，而是"想打就打"。论文用这个数字说明：**当前部署的基于深度学习的 FDIA 检测方案，在对抗攻击面前几乎是纸糊的。**

### 防御：对抗训练

论文提出的防御是**对抗训练（Adversarial Training）**——作为一种**主动防御机制（proactive defense mechanism）**。做法是：在训练阶段就把对抗样本喂给模型，让它"见过"这类攻击。

**结论**：对抗训练**显著增强了模型抵抗对抗 FDIA 的能力**，而且**没有牺牲故障检测的准确率**（without compromising fault detection accuracy）。

> **"没有牺牲精度"这一点很关键**——回忆 070（CRFL）的代价分析：可证明鲁棒方法通常会掉精度。而这篇论文报告对抗训练在这个场景下**不掉精度**，这是一个相当正面的结果。不过要注意：**对抗训练通常只对"训练时见过的攻击类型"有效**，面对新攻击（比如不同 $\epsilon$、不同方法）时鲁棒性会下降——这是对抗训练领域的已知问题，论文摘要没有讨论。

## 关键公式（小白版）

论文明确使用了 **FGSM**，这是对抗样本领域的标准公式：

$$x_{\text{adv}} \;=\; x \;+\; \epsilon \cdot \mathrm{sign}\Big(\nabla_{x}\, J\big(\theta,\ x,\ y\big)\Big)$$

符号解释：

- $x$ —— 原始输入（这里是 LCDR 的远程量测数据）。
- $y$ —— 真实标签（"故障"还是"攻击"）。
- $\theta$ —— 检测模型的参数。
- $J(\theta, x, y)$ —— 损失函数，衡量模型预测与真实标签的差距。
- $\nabla_x J$ —— 损失对**输入**的梯度（注意：不是对参数求导，是对输入求导）。
- $\mathrm{sign}(\cdot)$ —— 符号函数，把梯度变成 $+1$ 或 $-1$，只保留方向、丢掉大小。
- $\epsilon$ —— 扰动幅度上限（步长）。
- $x_{\text{adv}}$ —— 生成的对抗样本。

**一句话白话**：

> **看看"输入往哪个方向变，模型的损失会变大"，然后沿着那个方向走一小步。** 走多少由 $\epsilon$ 决定。

**为什么 FGSM 这么"便宜"？** 因为它只需要**一次**梯度计算——这也是它叫 "Fast"（快速）的原因。相比之下，迭代式的攻击（如 PGD，跑很多步）成功率更高但更慢。**论文选 FGSM，说明它想强调的是"攻击成本极低就能造成严重后果"。**

**注意**：论文的扰动加在**远程量测**上，而不是加在原始电流波形上。这意味着攻击者只需要能篡改通信链路上传输的数值——**攻击面在通信层，不在物理层**。

## 用网安的话说（小电解读）

**这篇论文是你最熟悉的东西，换了一个最要命的场景。**

**对照表**：

| 你熟悉的 | 这篇论文里的 |
|---|---|
| FGSM 对抗样本（图像分类） | FGSM 对抗样本（差动保护量测） |
| 让分类器把"停止标志"识别成"限速标志" | 让检测器把"攻击"识别成"真实故障" |
| 误报 / 假阳性（False Positive） | **误跳闸**（保护误动） |
| 可用性攻击（DoS） | **通过欺骗保护装置实现的可用性攻击** |
| 对抗训练防御 | 对抗训练防御（同样有"只防见过的攻击"的局限） |

**这篇论文最值得你记住的三个点：**

**第一，攻击目标是"反向"的。**

在图像对抗样本里，攻击者的目标通常是**让模型漏检**（把恶意样本判成正常）。而在这里，攻击者的目标是**让模型误报**——把"攻击"判成"故障"，从而**触发一个物理动作（跳闸）**。

> **"误报"从"麻烦"升级成了"武器"。** 这是电力场景特有的——因为模型的下游不是"给人看的结果"，而是"直接驱动物理设备的指令"。**这个"AI 决策直接连到物理执行器"的结构，是工控/电力 AI 安全和普通 IT AI 安全最本质的差异。**

**第二，攻击门槛极低，后果极严重。**

FGSM 是 2014 年就提出的方法，实现只需要几行代码。而它能达到 99.7% 的成功率，后果是**一条输电线路被无故断开**。这个"低成本—高后果"的组合，是论文强调"紧迫性"的原因。

**第三，"对抗训练有效"这个结论要打个问号。**

论文说对抗训练显著提升了鲁棒性且不牺牲精度，这是好消息。但你在网安里学过：**对抗训练是针对特定攻击分布的防御**。它相当于"用已知攻击样本做的特征工程"——**对训练时没见过的攻击（不同的 $\epsilon$、不同的范数、不同算法）效果会明显下降**。论文摘要没有说明它测试的泛化范围。

> **这正好是一个选题点**：**差动继电器检测器的对抗训练，能不能抵抗自适应攻击（adaptive attack）？** 自适应攻击是指"攻击者知道防御方法后专门设计来绕过它的攻击"。这是对抗鲁棒性评估的黄金标准，而这篇论文没有做。

**攻击面在哪（值得单独说）**：

- **不在变电站的物理设备上**，而在**线路两端的通信链路**上——远程量测是通过通信网传的，篡改它不需要接触任何一次设备。
- 这一点与 IT 场景高度相似：**你不需要攻破服务器，只需要在传输环节做手脚**。这也解释了为什么电力 CPS 安全里"通信安全"和"物理安全"必须一起考虑。
- **和 071 的差异**：071 攻击的是调度中心的检测器（影响的是"决策"），这篇攻击的是保护装置（影响的是"动作"）。**前者影响人，后者直接影响电。** 后者的时间尺度更紧（保护动作是毫秒级），这也意味着防御的可计算预算更小。

**如果要迁移到你的研究**：

1. **自适应对抗攻击评估**——把论文的防御（对抗训练）当作已知条件，设计能绕过它的自适应攻击。这是对抗鲁棒性评估的标准做法，工作量可控，结论明确。
2. **对抗训练的电力场景泛化性**——在不同拓扑、不同故障类型、不同 $\epsilon$ 下测试对抗训练的鲁棒性边界。这是一个偏实验的工作，很适合作为第一篇论文。
3. **实时性约束下的鲁棒检测**——保护装置要求毫秒级响应，很多高级防御（如 070 的平滑分类器需要几百次前向）根本跑不动。**"如何在毫秒级预算内做对抗鲁棒检测"是一个真实且有价值的工程问题。**
4. **物理一致性校验作为防御**——对抗扰动虽然能骗过深度学习模型，但它可能违反某些物理规律（比如电流波形的高频特征、功率平衡）。**用物理规律做"第二道防线"**，是一个电力场景独有的防御思路。

## 读完后你应该能回答

- [ ] 线路电流差动继电器（LCDR）的工作原理是什么？为什么它依赖通信？
- [ ] 为什么"篡改远程量测"能让继电器误跳闸？这会造成什么后果？
- [ ] FGSM 的公式是什么？为什么它被称为"快速"？
- [ ] 论文测了哪几类深度学习模型？它们的脆弱程度如何？
- [ ] 论文提出的防御是什么？它可能有什么局限？
- [ ] 为什么说"AI 检测器的下游直接连着物理执行器"是电力 AI 安全的本质特点？

## 局限性

- **摘要只给了一个数字（99.7%）**：没有说明是哪个模型达到的、在什么 $\epsilon$ 下、用什么数据集、测试系统是哪个（IEEE 测试系统还是仿真线路）。**没有这些信息，读者无法判断这个 99.7% 的可比性。**
- **只用了 FGSM 一种攻击方法**：FGSM 是单步攻击，成功率通常低于 PGD 等迭代攻击。用更弱的攻击都能达到 99.7%，说明模型的脆弱性很严重；但反过来，论文没有给出"更强攻击能到什么程度"的上界。
- **对抗训练的鲁棒性未做自适应评估**：论文没有测试"知道防御方法的攻击者"能否绕过对抗训练。这是对抗鲁棒性评估的标准要求，缺失会高估防御的有效性。
- **"不牺牲故障检测准确率"缺少细节**：是在什么数据分布下测的？正常样本和故障样本的比例是多少？如果故障样本占比很低，准确率这个指标本身就不敏感。
- **威胁模型假设偏强**：攻击者需要能实时篡改 LCDR 的远程量测，并且需要知道模型的梯度（FGSM 需要 $\nabla_x J$，即白盒访问）。**黑盒场景下攻击是否仍然有效，摘要没有回答**——这是一个重要的实践问题。
- **实验环境与真实保护的差距**：论文没有说明实验是在硬件在环（HIL）平台还是纯仿真上做的。真实保护装置有滤波、采样、时延等工程细节，可能影响攻击的可行性。

## 和你的方向有什么关系

- **这是"AI 安全方法迁移到电力场景"的教科书式范例**：成熟的攻击（FGSM）+ 未被验证的关键场景（差动保护）+ 完整的攻防实验。**你的第一篇论文完全可以照这个结构写。**
- **直接选题（按推荐度）**：
  1. **自适应对抗攻击与鲁棒性评估**——针对对抗训练后的检测器设计绕过攻击。这是对抗鲁棒性领域的标准动作，方法成熟、上手快。
  2. **物理约束增强的对抗检测**——把电流波形、功率平衡等物理规律作为第二道防线，检测"物理上不合理"的对抗扰动。**这是电力场景独有的思路。**
  3. **毫秒级实时约束下的鲁棒保护算法**——解决"高级防御跑不动"的工程问题。
  4. **跨场景迁移研究**——把 FGSM 攻击从差动继电器迁移到其他保护装置（距离保护、母线保护）或其他电网 AI 任务（状态估计、负荷预测），做系统性的脆弱性评估。
- **与实验室方向的对接**："AI与数据安全"直接对口（对抗样本）；"入侵检测"对应"FDIA 检测器"；"工业AI与智能体"对应保护装置的智能决策。

## 概念关联

[[虚假数据注入攻击(FDIA)]] · [[对抗样本攻击]] · [[深度学习检测方法]] · [[电力系统稳定性]] · [[入侵检测系统(IDS)]]

## 原文摘要

> The application of Deep Learning-based Schemes (DLSs) for detecting False Data Injection Attacks (FDIAs) in smart grids has attracted significant attention. This paper demonstrates that adversarial attacks, carefully crafted FDIAs, can evade existing DLSs used for FDIA detection in Line Current Differential Relays (LCDRs). We propose a novel adversarial attack framework, utilizing the Fast Gradient Sign Method, which exploits DLS vulnerabilities by introducing small perturbations to LCDR remote measurements, leading to misclassification of the FDIA as a legitimate fault while also triggering the LCDR to trip. We evaluate the robustness of multiple deep learning models, including multi-layer perceptrons, convolutional neural networks, long short-term memory networks, and residual networks, under adversarial conditions. Our experimental results demonstrate that while these models perform well, they exhibit high degrees of vulnerability to adversarial attacks. For some models, the adversarial attack success rate exceeds 99.7%. To address this threat, we introduce adversarial training as a proactive defense mechanism, significantly enhancing the models' ability to withstand adversarial FDIAs without compromising fault detection accuracy. Our results highlight the significant threat posed by adversarial attacks to DLS-based FDIA detection, underscore the necessity for robust cybersecurity measures in smart grids, and emphasize the effectiveness of adversarial training in enhancing model robustness against adversarial FDIAs.
