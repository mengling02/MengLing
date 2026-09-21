---
document_id: "arxiv-1706.09303"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/1706.09303"
arxiv_id: "1706.09303"
title: "Stealthy Deception Attacks Against SCADA Systems"
authors: ["Amit Kleinmann", "Ori Amichay", "Avishai Wool", "David Tenenbaum", "Ofer Bar", "Leonid Lev"]
published: "2017-06-28"
venue: "arXiv preprint"
domain: "L6-攻击技术专题"
level: "L6"
reading_order: 42
difficulty: "入门+"
lang: "en"
tags: ["电网安全", "L6-攻击技术专题", "SCADA", "语义攻击", "工控安全测试床"]
quality_score: 9
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 042 | 针对 SCADA 系统的隐蔽欺骗攻击

> [!abstract] 一句话
> 劫持 HMI 和 PLC 之间的通信，让操作员看到假的画面、并按假画面操作，而所有流量特征（大小、时序、命令序列、数值）全部合法——任何基于流量或状态的异常检测都发现不了。

## 为什么读它

这篇是 L6 专题里**最"网安味"的一篇**，也是最能让你找到亲切感的一篇。

原因很简单：它攻击的不是数学，而是**人**。

前面 039–041 讨论的都是"篡改数据让算法算错"。这篇换了个思路：**数据可以是真的，画面可以是假的；甚至画面是真的，操作员发出的指令的语义可以被反转。** 论文明确说，这类攻击是"完全隐蔽的（totally stealthy）"，因为：

- 报文大小不变
- 报文时序不变
- 命令序列不变
- ICS 的状态值全部保持合法

也就是说，**所有已知的检测维度都被绕过了**。

而且这篇的实验条件相当硬：在**当地电力公司的测试实验室**里，用**真实 HMI 和真实 PLC**，中间隔着**商用级防火墙**，攻击依然成功，并且把系统带到了**停电和可能设备损坏**的状态。

对网安背景的你来说，这篇的价值在于：它把"**语义层攻击**"这个概念在工控场景里讲得极清楚，而这个概念你在 Web 安全、协议安全里早就熟悉了。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | Stealthy Deception Attacks Against SCADA Systems |
| 作者 | Amit Kleinmann, Ori Amichay, Avishai Wool, 等 6 人 |
| 发表 | arXiv preprint, 2017-06-28 |
| 链接 | [arXiv:1706.09303](https://arxiv.org/abs/1706.09303) |
| 类型 | arXiv 预印本（攻击方法 + 真实测试床验证） |
| 难度 | 入门+ |
| 关键词 | SCADA、会话劫持、语义攻击、异常检测绕过、ICS 攻击描述语言 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[1706.09303_fig1.png]]

![[1706.09303_fig2.png]]

![[1706.09303_fig3.png]]

![[1706.09303_fig4.png]]

![[1706.09303_fig5.png]]

![[1706.09303_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：SCADA 系统与它现有的防护思路

先补概念。**SCADA（Supervisory Control and Data Acquisition，数据采集与监视控制系统）**是工控系统的"总控台"。它由三部分构成：

- **HMI（Human Machine Interface，人机界面）**：操作员面前的屏幕，显示工业过程的当前状态，操作员在上面点击按钮下发控制命令。
- **PLC（Programmable Logic Controller，可编程逻辑控制器）**：直接连接物理设备的控制器，接收 HMI 的指令去操作阀门、开关、电机。
- **通信链路**：HMI 和 PLC 之间的网络，跑的是工控协议（如 Modbus、DNP3、IEC 61850 等）。

因为 SCADA 协议在设计时主要考虑实时性和可靠性，**安全机制普遍很弱**——很多协议没有认证、没有加密、没有完整性保护。所以论文开篇就说：SCADA 协议容易受到**会话劫持（session hijacking）**这类网络攻击。

面对这个威胁，学术界和工业界提出两类异常检测方法：

1. **基于元数据的网络异常检测**：看报文的**大小（message sizes）**、**时序（timing）**、**命令序列（command sequence）**。比如"这个 PLC 平时每 100ms 收一条命令，现在突然收到 1000 条"就是异常。
2. **基于物理过程状态值的检测**：看 ICS 的**状态值**是否合理。比如"水泵转速 200% 额定值"就是异常。

**本文的定位就是：这两类检测都发现不了我这类攻击。**

### 攻击的核心思想：让"显示"和"实际"脱钩

论文提出的是一类**语义网络攻击（semantic network-based attacks）**。步骤是这样的：

**第一步：劫持通信通道。** 攻击者先拿下 HMI 和 PLC 之间的通信（通过会话劫持或中间人）。这一步是前提，不是本文的创新。

**第二步：让 HMI 显示假的过程视图。** 关键在这里——攻击者不改变 PLC 的实际行为，而是**拦截 PLC 返回给 HMI 的报文，把它们替换成伪造的"一切正常"的数据**。

于是操作员看到的是：所有参数都在正常范围内，设备运行平稳。而实际上，物理过程可能已经在往危险的方向走了。

**第三步：欺骗操作员做手动操作。** 因为操作员看到的是假象，他会基于这个假象做判断。比如他看到"某条线路过载"，于是手动去切负荷；或者他看到"温度正常"，于是不去干预一个实际上正在升温的设备。

**这一步是整个攻击的精髓**：攻击者不需要自己发出任何恶意指令，**让操作员自己动手就够了**。操作员的每一条指令在系统看来都是合法的、由授权人员发出的，因为**它确实是合法人员发出的**。

### 最狠的一招：反转语义

论文里"最先进的攻击（most advanced attack）"还多做了一件事：

> **篡改操作员操作所产生的报文，反转它们的语义含义，同时让 HMI 显示一个与操作员意图一致的视图。**

这句话信息量很大，拆开看：

- 操作员想**打开**一个开关，他在 HMI 上点了"打开"。
- 攻击者拦截了这条报文，把它改成"关闭"再发给 PLC。
- 同时，攻击者让 HMI 显示"开关已打开"——**和操作员的意图一致**。

结果：操作员以为自己做了一件事，实际系统做的是**相反**的事。而且操作员看到的画面是"我做对了"，所以他不会怀疑，也不会重复操作。

这个手法在网安里有个精准的对应物：**UI 欺骗（UI redressing）**，或者更贴切的——**交易篡改（transaction tampering）**，比如某些银行木马做的事：用户在网银上看到"转账 100 元给张三"，实际提交的是"转账 10000 元给李四"，而页面显示的是用户以为的那笔。

### 为什么它完全隐蔽

论文给出了"完全隐蔽"的四条理由，每一条都对应一种检测维度：

| 检测维度 | 攻击后状态 | 为什么检测不到 |
|---|---|---|
| 报文大小 | 不变 | 替换的报文和原报文长度一致 |
| 报文时序 | 不变 | 不额外注入报文，只替换内容 |
| 命令序列 | 不变 | 不新增命令，只反转已有命令的语义 |
| ICS 状态值 | 合法 | 物理过程本身没有被"设定"成异常值，异常是操作员操作导致的自然结果 |

**核心洞察**：传统异常检测找的是"**偏离正常模式的流量或数值**"。而本文的攻击**没有偏离任何模式**——它只是在正确的时刻，把语义反过来了。**流量层看，这是一段完美的正常通信。**

### 实现：IAML 和实时评估工具

论文不只是提出思路，还实现了工具：

- 开发了一个**实时安全评估工具**，能够**同时操纵与多个 PLC 的通信**，并让 HMI 显示一个**系统级的、前后一致的假视图**。

这里"同时"和"一致"很关键。如果只骗一个 PLC，操作员可能会发现"HMI 上的总功率和分项功率对不上"。攻击者必须让所有被操纵的 PLC 的数据**互相自洽**，才能骗过有经验的操作员。这是一个工程上的难点。

- 工具通过**报文操纵规则**来配置，规则用一种作者自己设计的语言编写：**ICS Attack Markup Language（IAML，工控攻击标记语言）**。论文认为这个语言本身可能具有独立的价值（may be of independent interest）——因为它把"怎么改报文"变成了可描述、可复用、可批量部署的规则。

**IAML 的思路你肯定熟悉**：它和 Snort 规则、YARA 规则、Suricata 规则是同一个范式——用声明式的规则描述"匹配什么、做什么"。只不过 Snort 是**检测**规则，IAML 是**攻击**规则。

### 结果

论文在**当地电力公司的测试实验室**里，针对**真实的 HMI 和真实的 PLC**（中间隔着**商用级防火墙**）测试了多个攻击场景。结论是：

> 所有的语义攻击都**成功骗过了操作员**，并把系统带到了**停电（blackout）和可能设备损坏（possible equipment damage）**的状态。

**摘要未给出**具体的测试次数、成功率百分比、参与的操作员人数、以及攻击耗时等量化数据。

## 关键公式（小白版）

这篇以实验和系统实现为主，**没有需要展开的核心公式。**

它的技术路线可以概括成一条"报文变换链"：

$$\text{HMI} \xleftarrow{\;\text{伪造视图}\;}\; \boxed{\text{攻击者}}\; \xrightarrow{\;\text{语义反转}\;}\; \text{PLC} \quad \text{s.t.} \quad \begin{cases} \text{size} = \text{size}_{\text{orig}} \\ \text{timing} = \text{timing}_{\text{orig}} \\ \text{seq} = \text{seq}_{\text{orig}} \end{cases}$$

用白话解释这条链：

- 攻击者站在 HMI 和 PLC 之间（中间人位置）。
- **往 PLC 方向**：把操作员的命令**语义反转**（开→关，增→减）后转发。
- **往 HMI 方向**：把 PLC 的真实状态**替换成**符合操作员预期的假状态。
- **约束条件**：报文大小、时序、命令序列全部保持和原始通信一致——这就是"隐蔽"的定义。

## 用网安的话说（小电解读）

这篇论文的核心可以浓缩成一句话：**它绕过的不是检测算法，而是检测的维度。**

**它对应你熟悉的哪个攻击手法？** 主要是三个叠加：

1. **中间人攻击（MitM）+ 会话劫持**——这是前提，负责拿到通信通道。你在 ARP 欺骗、DNS 劫持、TLS 剥离里都见过这个位置。
2. **语义级攻击（Semantic Attack）**——这是核心创新。你在 Web 安全里见过太多：**HTTP 请求走私（request smuggling）**就是利用前后端对同一段字节流解析方式不同，让"合法的字节"产生"非法的语义"；**反序列化攻击**是让"合法的序列化数据"触发"任意的代码执行"。本文做的是同一件事：**让合法的 SCADA 报文承载反转的语义**。
3. **UI 欺骗 / 显示欺骗**——攻击者控制的不是过程，而是操作员对过程的**认知**。这对应钓鱼里的"伪造登录页"、银行木马里的"伪造交易确认页"。

**它和 IT 场景有什么异同？**

相同点：攻击链的骨架完全一样——**拿到中间人位置 → 篡改内容 → 保持外观不变**。这是所有"隐蔽篡改"类攻击的通用模板。

不同点在于**检测的可能性**。在 IT 场景里，你还有一层兜底：**端到端的密码学完整性保护**（TLS、签名）。报文被改了，MAC 校验就过不了。但工控协议（Modbus、DNP3 早期版本）**普遍缺少这层保护**，所以"改内容而不留痕迹"在这里是可以做到的。这解释了为什么工控安全里"协议加固"（如 IEC 62351、[[IEC 62443]]）这么重要。

另一个不同点是**攻击的终点不同**。IT 攻击的终点通常是数据泄露或权限获取；这里攻击的终点是**物理世界的停电和设备损坏**，而且**中间还站着一个被欺骗的人**。这一点非常特殊——**防御方不是只有机器，还有操作员**，而操作员是可以用"信息"来操纵的。

**迁移到你的研究，可以怎么切入？**

1. **把"语义一致性"做成检测特征**。既然攻击者要维持 HMI 显示的"系统级自洽"，那么**跨设备的一致性校验**就是一个可攻击的检测点。攻击者让多个 PLC 的数据互相自洽是需要成本的（论文的工具专门做了这件事），这个成本可以被防御方利用——**检测"过于一致"的数据**（现实中总有噪声和轻微不同步，完美一致本身就是异常）。这是一个很有意思的反直觉检测思路。
2. **用 LLM/Agent 做语义级检测**。传统 IDS 看的是字节和统计特征，看不懂"这条命令在业务上意味着什么"。而 LLM 恰好擅长理解语义。**"用大模型检测工控命令的语义异常"** 是一个直接对接你实验室"大语言模型"方向、且文献里还很空白的选题。注意：这同时也引入了提示注入风险（见 L8）。
3. **把 IAML 当成攻击生成 DSL 来研究**。这个语言的设计本身可以分析——规则的表达能力边界在哪？能否自动生成规则？能否用强化学习自动搜索最优攻击规则序列？（这条线可以接 048 那篇 RL 发现攻击的论文。）

## 读完后你应该能回答

- [ ] SCADA 系统的三个组成部分各自是什么角色？
- [ ] 为什么基于报文元数据（大小、时序、命令序列）的异常检测对这类攻击无效？
- [ ] 攻击者如何做到"反转操作员指令的语义"而不被操作员发现？
- [ ] 为什么让 HMI 显示"系统级一致"的假视图是攻击成功的关键？
- [ ] IAML 的设计思路和 Snort 规则有什么共同点？

## 局限性

- **前提条件较强**：攻击者必须先完成对 HMI-PLC 通信通道的劫持。论文把这一步当成既有能力，没有讨论劫持本身的难度。
- **依赖操作员的"配合"**：攻击效果的一部分来自操作员按假画面行动。如果操作员有独立的核查手段（比如现场巡检、独立仪表），攻击可能失效。论文没有讨论这种场景。
- **测试床规模有限**：在电力公司的实验室里做，但实验室环境无法完全复现真实变电站的复杂度和操作流程。
- **摘要缺少量化数据**：只说"成功骗过操作员"，没有说明样本量（多少次试验、多少位操作员），因此"成功率"的可信度无法评估。
- **未提出防御方案**：论文是纯攻击视角，没有给出"如何检测这类攻击"的方法，实用性偏攻击侧。
- **IAML 的适用性依赖协议细节**：论文没有在摘要中说明支持哪些工控协议、以及协议升级（如加认证）后是否依然有效。

## 和你的方向有什么关系

- **这篇是你最可能做出成果的论文之一**，因为它和你已有的技能栈重合度最高（协议分析、中间人、语义攻击）。
- **三个具体选题**：
  1. **语义级异常检测**：用序列模型或 LLM 对工控命令流做语义建模，检测"语法合法但语义矛盾"的指令序列。这是本文防御侧的空白，而且直接命中"AI与数据安全"和"大语言模型"两个方向。
  2. **跨设备一致性检测**：利用攻击者"必须维持全局自洽"这一约束，设计检测器找出"过于一致"或"自洽得可疑"的数据模式。
  3. **攻击自动化**：把本文的 IAML 规则替换成 RL 或 LLM 自动生成的攻击策略，研究"攻击规划"的自动化边界。这条线可以接 048。
- **实验资源**：工控测试床（如 GRFICS、小型 PLC 实验平台）是可行的，学院如果有工控安全实验室更好；没有的话，用 Modbus 模拟器 + Mininet 也能搭出简化版本（050 那篇就用了 Mininet）。
- **注意**：这类研究涉及真实工控攻击技术，做实验时务必在隔离环境、且需有明确的授权/教学用途说明。

## 概念关联

[[SCADA系统]] · [[隐蔽性攻击(Stealthy Attack)]] · [[Modbus协议安全]] · [[工控安全测试床与数据集]] · [[入侵检测系统(IDS)]]

## 原文摘要

> SCADA protocols for Industrial Control Systems (ICS) are vulnerable to network attacks such as session hijacking. Hence, research focuses on network anomaly detection based on meta--data (message sizes, timing, command sequence), or on the state values of the physical process. In this work we present a class of semantic network-based attacks against SCADA systems that are undetectable by the above mentioned anomaly detection. After hijacking the communication channels between the Human Machine Interface (HMI) and Programmable Logic Controllers (PLCs), our attacks cause the HMI to present a fake view of the industrial process, deceiving the human operator into taking manual actions. Our most advanced attack also manipulates the messages generated by the operator's actions, reversing their semantic meaning while causing the HMI to present a view that is consistent with the attempted human actions. The attacks are totaly stealthy because the message sizes and timing, the command sequences, and the data values of the ICS's state all remain legitimate. We implemented and tested several attack scenarios in the test lab of our local electric company, against a real HMI and real PLCs, separated by a commercial-grade firewall. We developed a real-time security assessment tool, that can simultaneously manipulate the communication to multiple PLCs and cause the HMI to display a coherent system--wide fake view. Our tool is configured with message-manipulating rules written in an ICS Attack Markup Language (IAML) we designed, which may be of independent interest. Our semantic attacks all successfully fooled the operator and brought the system to states of blackout and possible equipment damage.
