---
document_id: "arxiv-2305.08037"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2305.08037"
arxiv_id: "2305.08037"
title: "ChargeX: Exploring State Switching Attack on Electric Vehicle Charging Systems"
authors: ["Ce Zhou", "Qiben Yan", "Zhiyuan Yu", "Eshan Dixit", "Ning Zhang", "Huacheng Zeng", "Alireza Safdari Ghanhdari"]
published: "2023-05-14"
venue: "arXiv preprint"
domain: "L9-新能源与新型电力系统安全"
level: "L9"
reading_order: 86
difficulty: "入门+"
lang: "en"
tags: ["电网安全", "L9-新能源与新型电力系统安全", "电动汽车充电安全", "硬件攻击", "协议状态机"]
quality_score: 9
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 086 | ChargeX：探索针对电动汽车充电系统的状态切换攻击

> [!abstract] 一句话
> 车和桩之间那根充电线上的控制信号**完全没有真实性保护**——加一块小电路就能伪造它，让没在充电的车"假装在充电"，甚至把充电桩搞宕机。

## 为什么读它

**这是 L9 专题里最"硬"的一篇——真刀真枪的硬件攻击。**

前面 084、085 讲的是协议层和系统层的问题，都是"分析"和"综述"。这篇不一样：作者**做出了攻击硬件、在真实公共充电站和家用充电器上做了实验，还在一辆特斯拉 Model 3 上验证了攻击**。

它的价值：

1. **它证明了"协议设计缺陷"可以变成"物理世界里的真实攻击"**。这是从理论到实证的关键一步，比纯分析论文有说服力得多。
2. **它的攻击手法非常"网安"**：利用协议状态机的设计缺陷、缺乏真实性保护、状态转换无授权校验。这些概念你全懂。
3. **它的攻击后果直接**：让充电桩宕机（DoS）、扰乱充电计划、损害电池。**这是能直接影响用户和电网的攻击。**

如果你想知道"电力安全的攻击论文长什么样"，这篇是最好的样板。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | ChargeX: Exploring State Switching Attack on Electric Vehicle Charging Systems |
| 作者 | Ce Zhou, Qiben Yan, Zhiyuan Yu 等 |
| 发表 | arXiv preprint, 2023-05-14 |
| 链接 | [arXiv:2305.08037](https://arxiv.org/abs/2305.08037) |
| 类型 | arXiv 预印本（攻击实证研究） |
| 难度 | 入门+ |
| 关键词 | 电动汽车充电、SAE J1772、状态切换攻击、硬件攻击电路、拒绝服务（DoS） |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2305.08037_fig1.png]]

![[2305.08037_fig2.png]]

![[2305.08037_fig3.png]]

![[2305.08037_fig4.png]]

![[2305.08037_fig5.png]]

![[2305.08037_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：充电基础设施是电动汽车普及的关键

论文开篇的逻辑很直白：

- 电动汽车（EV）是应对环境和能源危机的有前景的方案之一。
- 而电动汽车能否广泛普及，**关键在于充电基础设施是否普及**——包括**私人/家用充电器**和**公共/商业充电站**两类。
- **然而，电动汽车充电的安全性还没有被彻底研究（has not been thoroughly investigated）。**

最后这句话就是论文的立足点：**充电桩铺得飞快，但安全研究严重滞后。**

### 核心发现：SAE J1772 协议缺乏真实性保护

论文做了两件事：

**第一件：研究充电器（chargers）和电动汽车（EVs）之间的通信机制。**

**第二件：发现了 SAE J1772 充电控制协议中缺乏真实性保护（lack of protection on the authenticity）。**

先解释 **SAE J1772** 是什么。

SAE J1772 是北美（也是国际上广泛采用）的电动汽车充电接口标准。它规定了：

- **物理接口**：充电枪的形状、引脚定义。除了大功率的电力引脚，还有几根**信号引脚**。
- **控制导引（Control Pilot, CP）信号**：这是最关键的部分。充电枪和车之间通过一根低压信号线，用**PWM（脉宽调制）信号**来通信。

**PWM 信号怎么工作？** 简单说，充电桩通过改变 PWM 的**占空比（duty cycle）** 来告诉车"我最多能给你多少电流"。车则通过改变信号线上的**电压电平**来告诉桩"我现在的状态"（未连接、已连接、准备充电、正在充电、有故障等）。

**这套机制的核心缺陷是：它只是一个"信号"，没有任何加密、没有任何认证、没有任何完整性校验。**

论文的发现就是：**SAE J1772 的充电控制协议在真实性（authenticity）上完全没有保护**。

**用网安的话说**：这相当于一个**没有任何认证的应用层协议**——你只要能在物理上接触到信号线，就能伪造任意指令。**它甚至不是"弱认证"，而是"零认证"。**

### 攻击：ChargeX

基于这个发现，论文提出了一类新的攻击：**ChargeX**。

**攻击目标**：操纵充电器（chargers）的**充电状态（charging states）** 或**充电速率（charging rates）**。

**攻击目的（三选一或组合）**：

1. **扰乱充电计划（disrupting the charging schedules）**：让车在你不需要的时候充电，或者不充电。
2. **造成拒绝服务（DoS, Denial of Service）**：让充电桩宕机或无法正常使用。
3. **降低电池性能（degrading the battery performance）**：不当的充放电状态切换会损害电池寿命。

**攻击手段：插入一个硬件攻击电路（hardware attack circuit）来策略性地修改充电控制信号。**

这是这篇论文最"硬"的地方。论文不是通过软件漏洞攻击，而是**做了一块物理电路，串接或并接在充电控制信号线上，用来篡改 CP 信号**。

**为什么用硬件？** 因为 CP 信号是**物理层的模拟/PWM 信号**，不是网络协议包。你没法"发个恶意数据包"来篡改它——你必须在物理上介入这根线。

**攻击的物理可行性**：作者能在真实充电站和家用充电器上部署这个电路，说明这个攻击**不是理论上的，是物理可实现的**。这也意味着攻击者需要**物理接触**（比如插一个恶意适配器，或者改装充电枪）。

### 攻击系统的设计与实现

论文做的工作包括：

1. **设计并实现了多个攻击系统（multiple attack systems）**。也就是说，不是只有一个攻击，而是一整套。
2. **在实验环境中评估**：
   - 一个**公共充电站（public charging station）**
   - 两个**家用充电器（home chargers）**
   - 使用**模拟的车辆负载（simulated vehicle load）**
3. **广泛的实验证明攻击的有效性和泛化性（effectiveness and generalization）**：在不同的充电器类型上都能成功，说明这个缺陷是**协议层面的，不是某个厂商的实现问题**。

**"泛化性"这个点很重要**：如果攻击只对某一个品牌的充电桩有效，那可以说是个别厂商的 bug。但论文证明它**跨多种充电器类型都有效**，说明这是 **SAE J1772 协议本身的设计缺陷**——**所有符合该标准的设备都有这个漏洞**。

### 关键攻击演示

论文演示了一个非常直观的攻击效果：

> **ChargeX 可以强制电动汽车的充电状态从"待机（stand by）"切换到"充电（charging）"，即使车辆并不处于充电状态。**

这个攻击为什么严重？想一下：

- 你以为车没在充电，实际上它在充电——**电费账单会莫名其妙地涨**。
- 如果你已经拔枪了，但系统认为还在充电——**状态不一致会导致计费错误、设备保护误动作**。
- 如果大量车被强制进入充电状态——**配电网会突然多出一大堆负荷**，可能造成过载。这直接呼应第 087 篇的负载改变攻击。

论文还做了进一步的验证：

> **我们在一辆特斯拉 Model 3 车辆上验证了攻击，以证明 ChargeX 的破坏性影响。**

在真实车型（而且是主流车型）上验证，这是论文说服力的关键。

### 结论

论文的结论很直接：

> **如果部署，ChargeX 可能会显著摧毁人们对电动汽车充电基础设施的信任（may significantly demolish people's trust in the EV charging infrastructure）。**

这句话点出了这类攻击的真正危害——**不完全是物理破坏，而是信任崩塌**。如果用户担心自己的车会被偷偷充电、被损坏、或者充电桩会被攻击宕机，他们就不敢用电动汽车。**对关键基础设施的攻击，信任损失往往比物理损失更难修复。**

## 关键公式（小白版）

这篇以硬件实验为主，摘要中没有给出需要展开的核心公式。

不过有一个概念值得量化理解，因为它是整个攻击的技术基础——**PWM 占空比与可用电流的关系**。

在 SAE J1772 中，充电桩通过 CP 信号线的 PWM 占空比 $D$ 告诉车辆可用电流上限：

$$I_{\text{avail}} = D \times 0.6 \quad (\text{单位：A，} D \text{ 以百分比计})$$

符号解释：

- $I_{\text{avail}}$：充电桩声明能提供的最大电流（安培）。
- $D$：PWM 信号的**占空比**（duty cycle），即高电平时间占整个周期的比例，以百分比表示。
- $0.6$：标准规定的换算系数（1% 占空比对应 0.6 A）。

**这个公式在说什么**：充电桩用**一个占空比数字**来传递"我能给你多大电流"这个关键信息。**占空比是模拟量，没有任何加密和认证。**

攻击者只要篡改这个占空比，就能：
- **调高** → 让车按更大电流充电（可能超过线路承受能力，造成过载或设备损坏）
- **调低** → 让车充得很慢（变相 DoS）
- **伪造整个状态序列** → 让车和桩的状态机错位（ChargeX 的核心手法）

（注：这是 SAE J1772 标准中控制导引机制的通用原理，论文摘要未给出具体数值。具体的电流上限换算关系请以标准原文为准。）

## 用网安的话说（小电解读）

**这篇论文是你最熟悉的攻击模式在电力场景的完整重现——而且做成了硬件实证，非常值得精读。**

逐条对齐：

- **"缺乏真实性保护" = 零认证协议**。这在 IT 里对应的是：
  - **早期 Modbus/TCP**：无认证、无加密，任何能连上的人都能读写寄存器。
  - **早期 SNMP（v1/v2c）**：明文 community string，本质是"口令当密码用"。
  - **CAN 总线**：车载网络里所有报文都是广播的，没有发送者认证——**任何接入 CAN 的节点都能伪造刹车、加速信号**。
  
  SAE J1772 的 CP 信号就是同一类东西：**一个物理层信号，传递关键控制信息，但没有任何发送者身份验证**。

- **"状态切换攻击" ≈ 利用协议状态机的设计缺陷**。这是最精准的类比，也是你该记住的术语。这类攻击的本质是：
  - 协议定义了一组**状态**（未连接 → 已连接 → 准备 → 充电 → 完成）和**状态转换条件**。
  - 但**状态转换请求没有授权校验**——只要发出正确的信号，状态就切换，不管发出者是谁。
  - 攻击者可以**跳过中间状态**、**强制切换**、**保持某个状态不放**。
  
  这在 IT 里对应什么？
  - **TCP 状态机攻击**：比如 SYN flood 让连接处于半开状态。
  - **认证状态绕过**：跳过认证直接进入已认证状态。
  - **SIP/SS7 状态机攻击**：伪造信令让呼叫状态错乱。
  - **支付协议的状态重放**：重复提交同一个交易状态。
  
  **共同特征：协议把"状态转换"当成一个单纯的信号事件，而不是一个需要授权的操作。** 这是一个跨领域的普适设计缺陷。

- **"硬件攻击电路" ≈ 物理层攻击 / 中间人适配器**。这类攻击在你熟悉的领域也有对应：
  - **USB Rubber Ducky**：伪装成键盘的 USB 设备。
  - **恶意充电线（O.MG Cable）**：看起来是普通数据线，内置了攻击芯片。
  - **硬件植入（hardware implant）**：在设备里植入芯片。
  
  **ChargeX 的攻击电路和这些是同一类：在物理链路中插入一个主动篡改信号的装置。** 区别是它篡改的不是数据包，而是**模拟/PWM 信号**。

- **"泛化性" ≈ 协议级漏洞 vs 实现级漏洞**。论文强调攻击跨多种充电器有效，这是一个非常重要的区分：
  - **实现级漏洞**：某个厂商代码写错了 → 打补丁就行。
  - **协议级漏洞**：标准本身设计有问题 → **所有实现都有问题，打补丁解决不了，必须改协议**。
  
  **协议级漏洞的修复成本高几个数量级**——因为全球有数百万台设备已经部署了。这就是为什么第 084 篇强调 OCPP 2.0 才引入安全机制、第 085 篇强调"密码敏捷性"。**在这类长寿命、大规模部署的基础设施里，"事后补救"极其困难，安全必须前置设计。**

- **可迁移的选题**：
  1. **协议状态机的形式化建模与漏洞搜索**：把 SAE J1772（或 OCPP、ISO 15118）的状态机形式化建模，用模型检验（model checking）自动搜索非法状态转换路径。这是你的协议安全技能的直接应用。
  2. **充电协议异常的检测**：ChargeX 篡改了物理信号，但**它必然导致充电行为在时序上出现异常**（比如状态转换的时间分布、充电电流的变化模式）。**用 ML 检测这类物理层攻击** 是一个很自然的题目，而且论文本身没做检测。
  3. **更大范围的协议安全普查**：SAE J1772 的问题可能也存在于其他充电标准（中国国标 GB/T、欧洲 IEC 61851、日本 CHAdeMO）。**对比不同标准的真实性保护机制** 是一个扎实的综述型题目。

## 读完后你应该能回答

- [ ] SAE J1772 是什么？它规定了什么？控制导引（CP）信号是干什么用的？
- [ ] 论文发现 SAE J1772 的核心安全缺陷是什么？为什么这个缺陷是"协议级"而不是"实现级"？
- [ ] ChargeX 攻击的三个目标分别是什么？
- [ ] 论文为什么用硬件攻击电路而不是软件方式？这说明攻击者需要什么前提条件？
- [ ] "强制从待机切换到充电"这个攻击会造成什么实际后果？
- [ ] 为什么论文说 ChargeX 会"摧毁人们对充电基础设施的信任"？

## 局限性

- **攻击需要物理接触**。ChargeX 需要插入硬件攻击电路，这意味着攻击者必须**物理接触充电桩或充电枪**（比如安装一个恶意适配器，或者改装设备）。这大幅提高了攻击门槛，也限制了攻击规模——你不可能给全国几十万个充电桩都装电路。**论文没有讨论攻击的规模化路径。**
- **未讨论检测与防御**。论文完全站在攻击者视角，虽然给出了"这是协议缺陷"的诊断，但没有提出任何检测或缓解方案。这是一个明显的空白（也是你的机会）。
- **实验环境的限制**。公共充电站的测试使用了**模拟的车辆负载（simulated vehicle load）**，而不是真实车辆。只有特斯拉 Model 3 那部分是真实车辆验证。实验覆盖的场景范围有限。
- **对电池损害的量化不足**。论文声称会"降低电池性能"，但摘要没有给出具体的损害程度、时间尺度或可复现的测试数据。
- **未讨论中国标准**。论文针对的是 SAE J1772（北美标准）。中国的 GB/T 27930（车桩通信协议）和 GB/T 18487（传导充电系统）是另一套体系，安全性如何、是否存在类似问题，论文没有涉及。**这本身就是一个现成的研究方向。**
- **时间因素**。论文是 2023 年 5 月的。此后 SAE J1772 标准是否有修订、厂商是否加了缓解措施，摘要中没有信息。

## 和你的方向有什么关系

- **这是 L9 里"最像攻击论文"的一篇**，也是你做攻击类研究时的模板：**发现协议缺陷 → 设计攻击 → 硬件实现 → 真实设备验证 → 讨论影响**。这套结构可以直接搬到你要研究的任何协议上。
- **最推荐的选题**：
  1. **国标充电协议的安全性分析**（最推荐，且几乎是空白）。中国的 GB/T 27930 和 GB/T 18487 是强制标准，覆盖国内所有充电桩。**它们是否存在类似 SAE J1772 的真实性缺陷？** 这个题目：
     - 实际意义强（涉及国内数百万充电桩）
     - 技术门槛可控（协议分析是你的本行）
     - 竞争少（国内外对国标充电协议安全的研究远少于 OCPP/SAE J1772）
  2. **充电状态异常检测**：论文没做检测。用 ML 检测"状态转换时序异常"（比如充电状态切换过于频繁、充电电流曲线异常）是一个很自然的补充工作。
  3. **协议状态机的形式化验证**：用模型检验工具自动找出非法状态转换路径，可以做成一个通用方法论，适用于多种充电协议。
- **和你实验室方向的对接**：
  - **"程序逆向"** → 充电桩固件分析、协议实现逆向、寻找额外的软件层漏洞
  - **"协议安全"** → 国标充电协议分析、状态机形式化验证
  - **"AI 与数据安全"** → 充电行为异常检测、物理层攻击的 ML 检测
  - **"工业 AI 与智能体"** → 硬件在环（HIL）测试床、攻击自动化
- **一个实操提醒**：涉及硬件攻击的实验要特别注意**安全和法律边界**。建议在实验室环境下用隔离的测试设备，不要对生产环境的充电桩做测试。中国对关键信息基础设施有严格的保护要求，未授权的测试可能触犯法律。

## 概念关联

[[电动汽车充电安全]] · [[拒绝服务攻击(DoS)]] · [[电力信息物理系统(CPS)]] · [[零信任架构]] · [[硬件在环仿真(HIL)]]

## 原文摘要

> Electric Vehicle (EV) has become one of the promising solutions to the ever-evolving environmental and energy crisis. The key to the wide adoption of EVs is a pervasive charging infrastructure, composed of both private/home chargers and public/commercial charging stations. The security of EV charging, however, has not been thoroughly investigated. This paper investigates the communication mechanisms between the chargers and EVs, and exposes the lack of protection on the authenticity in the SAE J1772 charging control protocol. To showcase our discoveries, we propose a new class of attacks, ChargeX, which aims to manipulate the charging states or charging rates of EV chargers with the goal of disrupting the charging schedules, causing a denial of service (DoS), or degrading the battery performance. ChargeX inserts a hardware attack circuit to strategically modify the charging control signals. We design and implement multiple attack systems, and evaluate the attacks on a public charging station and two home chargers using a simulated vehicle load in the lab environment. Extensive experiments on different types of chargers demonstrate the effectiveness and generalization of ChargeX. Specifically, we demonstrate that ChargeX can force the switching of an EV's charging state from ``stand by" to ``charging", even when the vehicle is not in the charging state. We further validate the attacks on a Tesla Model 3 vehicle to demonstrate the disruptive impacts of ChargeX. If deployed, ChargeX may significantly demolish people's trust in the EV charging infrastructure.
