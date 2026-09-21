---
document_id: "arxiv-2101.05965"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2101.05965"
arxiv_id: "2101.05965"
title: "Real-time Power System Simulation with Hardware Devices through DNP3 in Cyber-Physical Testbed"
authors: ["Hao Huang", "C. Matthew Davis", "Katherine R. Davis"]
published: "2021-01-15"
venue: "arXiv preprint"
domain: "L10-工程与实验"
level: "L10"
reading_order: 98
difficulty: "入门+"
lang: "en"
tags: ["电网安全", "L10-工程与实验", "DNP3", "硬件在环", "SCADA"]
quality_score: 8
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 098 | 在信息物理测试床中通过 DNP3 与硬件设备进行实时电力系统仿真

> [!abstract] 一句话
> 把电力系统动态仿真软件和**真实的工业 RTAC 硬件**用 **DNP3 协议**接起来，在 **2000 节点的德州合成电网**上跑通了数据采集与控制——这就是典型的**硬件在环（HIL）**方案。

## 为什么读它

前面几篇测试床（091、092、094）都是"局部过程"——一个储水罐、一个变电站间隔。这篇的格局不一样：**它把整个大规模电网的实时仿真，接到了真实工业硬件上。**

这在工程上有个专门的名字：**HIL（Hardware-in-the-Loop，硬件在环）**。核心思想是：

> **虚拟电网 + 真实控制器。**
> 电力系统的物理过程用仿真软件算（因为真电网不能拿来试），但**控制侧用真实的工业设备**（因为控制器的行为、时延、协议实现细节，仿真是仿不出来的）。

这对安全研究意义重大：**只有用真实硬件，攻击的真实效果才能体现出来。** 你在仿真里攻击一个假的 RTAC，和在真实 RTAC 上攻击，能发现的问题完全不是一个量级。

而且这篇论文的规模数据是 L10 专题里**少数几个明确给出数字的**：**2000 节点的德州合成电网（2000-bus Texas synthetic grid）**。这个规模在学术研究里算是相当大的。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | Real-time Power System Simulation with Hardware Devices through DNP3 in Cyber-Physical Testbed |
| 作者 | Hao Huang, C. Matthew Davis, Katherine R. Davis |
| 发表 | arXiv preprint, 2021-01-15 |
| 链接 | [arXiv](https://arxiv.org/abs/2101.05965) |
| 类型 | arXiv 预印本 |
| 难度 | 入门+ |
| 关键词 | DNP3、SCADA、实时仿真、RTAC、硬件在环、德州合成电网 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2101.05965_fig1.png]]

![[2101.05965_fig2.png]]

![[2101.05965_fig3.png]]

![[2101.05965_fig4.jpg]]

![[2101.05965_fig5.jpg]]

![[2101.05965_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：电网依赖通信，而 DNP3 是通信的主角之一

论文开篇的观察是：**现代电网依赖通信系统来完成数据采集、可视化与控制**（"Modern power grids are dependent on communication systems for data collection, visualization, and control"）。

这句话看着平淡，但它是整个"信息物理安全"的根基：**通信断了或通信被篡改，物理电网就会失控。**这就是为什么研究"通信网络安全 → 电力系统数据采集 → 工业硬件"三者的依赖关系很重要。

主角是 **DNP3（Distributed Network Protocol 3，分布式网络协议第 3 版）**。

> **DNP3 是什么**：它是**电力系统中 SCADA 系统常用的通信协议**，让控制系统的软件和硬件能够互相通信。论文原话：**"Distributed Network Protocol 3 (DNP3) is commonly used in supervisory control and data acquisition (SCADA) systems in power systems to allow control system software and hardware to communicate."**
>
> **用你熟悉的话说**：DNP3 是电力行业的"专有 Modbus 升级版"。相比 Modbus，它更复杂、更可靠（支持时间戳、事件缓冲、主动上报），也因此**攻击面更大**。它主要在**主站（Master）与从站（Outstation/RTU）之间**通信——主站是调度中心的服务器，从站是变电站里的 RTU（远程终端单元）。

论文强调的研究动机是：**要研究"通信网络安全、电力系统数据采集、工业硬件"之间的依赖关系，就必须让通信能力与实时电力系统仿真打通。**

### 问题：仿真软件和真实硬件之间缺一座桥

你可以在 MATPOWER 里算潮流，也可以在真实 RTAC 上跑控制逻辑，但**这两者之间没有天然通道**。仿真软件不知道 DNP3 协议，真实 RTAC 不知道仿真世界里发生了什么。

论文要做的就是**把这座桥架起来**。

### 方法：给仿真包加 DNP3 功能，对接真实 RTAC

论文的贡献是：

**1）把电力系统动态仿真包的新功能集成进 CPS 电力系统测试床**

论文原文说，他们 "present the integration of new functionality of a power systems dynamic simulation package into our cyber-physical power system testbed"。也就是说，**给仿真软件扩展了新功能**，让它**支持通过 DNP3 进行实时电力系统数据传输**。

**摘要中没有说明是哪个仿真包**（不要臆造。可能是某个开源的动态仿真工具，但摘要未给出名称）。

**2）与真实工业 RTAC 硬件对接**

论文明确说这个能力是 **"demonstrated with an industrial real-time automation controller (RTAC)"**——用一个**工业级实时自动化控制器（RTAC）** 来演示。

> **RTAC 是什么**：Real-Time Automation Controller，实时自动化控制器。它是工业界真实在用的设备（通常用于变电站自动化），扮演类似 RTU/网关的角色——**它从设备采集数据，执行控制逻辑，并通过协议（如 DNP3、IEC 61850）和上层通信。**
>
> **用你熟悉的话说**：RTAC ≈ 工业界的"可编程网关 + 边缘控制器"。它既是攻击目标（攻陷它就能下发假控制命令），也是防御的关键节点（可以在这里做流量过滤和认证）。

**3）用 DNP3 实现大规模电网的监视与控制**

论文展示了**在真实设备上使用和配置 DNP3**，通过 DNP3 通信**实现对大规模合成电网的电力系统监视与控制**。

### 结果：2000 节点德州合成电网

论文的演示案例是：**在软件和硬件上，用 2000 节点的德州合成电网（2000-bus Texas synthetic grid）实现 DNP3 数据采集与控制的一个示例（exemplar）**。

**这是 L10 专题里明确给出的最大的电网规模数字。** 2000 节点在电力系统研究里属于大规模（对比：经典 IEEE 118 节点系统只有 118 个节点）。

**摘要中没有给出的关键信息**（不要臆造）：
- 仿真包的具体名称（摘要只说 "a power systems dynamic simulation package"）
- RTAC 的品牌型号（摘要只说 "industrial real-time automation controller (RTAC)"）
- 采样/更新频率、时延指标（摘要未给出）
- 测试床的其他硬件组成（摘要未给出）
- 是否开源（摘要未提及）

### 结论

论文证明了：**可以在一套 CPS 测试床里，用 DNP3 把实时电力系统仿真和真实工业硬件连通，并在 2000 节点规模上完成数据采集与控制。** 这为研究"通信安全 → 数据采集 → 物理后果"这条因果链提供了实验基础。

## 关键公式（小白版）

这篇以系统集成与工程实现为主，没有需要展开的核心公式。它的技术路线是：

```
┌─────────────────────┐          ┌──────────────────┐
│  电力系统动态仿真包   │          │   工业 RTAC 硬件   │
│ （实时求解 2000 节点 │  DNP3    │ （真实控制器，     │
│   德州合成电网）      │ ◄──────► │   真实协议栈）     │
└─────────────────────┘  网络     └──────────────────┘
        虚拟电网                          真实设备
              ↑
       这就是"硬件在环（HIL）"
```

**一句话概括**：让虚拟的 2000 节点电网和真实的工业控制器用 DNP3 对话。

## 用网安的话说（小电解读）

**HIL ≈ 半实物仿真：真实控制器 + 虚拟电网。**这个思路你在网安里其实见过——比如做 IoT 安全研究时，用固件模拟器跑真实固件（**那也是一种 HIL**：真实软件 + 虚拟硬件）。这里反过来：**真实硬件 + 虚拟物理过程。**

**为什么安全研究必须用 HIL**：

1. **只有真实设备才有真实的协议实现缺陷。**仿真出来的 DNP3 协议栈，是"理想实现"——不会有缓冲区溢出、不会有状态机错误、不会有厂商自定义扩展的漏洞。**真实 RTAC 才有这些，而这些恰恰是攻击者最爱的入口。**
2. **只有真实设备才有真实的时序行为。**响应延迟、超时重传、并发处理能力——这些决定了攻击能否成功、防御能否来得及。**仿真里这些数字都是假的。**
3. **DNP3 本身就是一个大攻击面。**它的设计年代早，**原生不带认证**（IEEE 1815 后来才加了 Secure Authentication，但部署率很低）。这和 Modbus 的问题一样：**明文、无认证、无完整性保护**。攻击者能做的：
   - **窃听**：直接看到所有量测数据；
   - **篡改**：修改报文里的量测值（类似 FDIA）；
   - **重放**：重放旧的合法命令；
   - **伪造**：直接冒充主站下发控制命令（**这是最危险的——可以直接操作断路器**）。

**可迁移的选题**：

1. **DNP3 攻击的检测**——尤其是**基于时序和状态机的检测**：DNP3 有明确的状态机（主从轮询模式），偏离状态机的行为就是异常。**这比纯统计异常检测更精确，误报率更低。**
2. **HIL 环境下的攻击效果量化**——"攻击者篡改一个量测值，在 2000 节点电网上会导致多大的物理偏差？"这类"从网络到物理"的因果链研究很有价值。
3. **RTAC 这类边缘控制器的安全加固**——它就是工业界的"边缘节点"，可以借鉴 IT 界的 EDR/零信任思路。
4. **DNP3 的模糊测试**——真实设备 + 真实协议栈 = 挖漏洞的天然靶场。**这是纯网安的活，你完全能做。**

## 读完后你应该能回答

- [ ] 什么是 DNP3？它在电力 SCADA 系统里扮演什么角色？
- [ ] 什么是 HIL（硬件在环）？为什么安全研究需要它？
- [ ] RTAC 是什么设备？它为什么既是攻击目标又是防御节点？
- [ ] 论文用的是什么规模的电网？这个规模在学术研究中算什么水平？
- [ ] 为什么"用真实硬件"比"纯仿真"对安全研究更重要？

## 局限性

- **摘要缺少关键工程细节**：仿真包名称、RTAC 型号、更新频率、时延数据全都没有。**仅凭摘要无法复现。**
- **规模虽大但场景单一**：2000 节点是拓扑规模，但论文只演示了"数据采集与控制的一个示例"，**没有说明在多种运行工况或攻击场景下的表现**。
- **没有涉及安全**：论文本身是**平台建设**工作，**没有做攻击实验、没有做检测评估**。它提供的是"能力"，不是"结论"。（这既是局限，也是机会——**平台建好了，安全研究还没做**。）
- **摘要未提及是否开源**，可复现性存疑。
- **HIL 的固有局限**：仿真电网再大也是仿真，**它不含真实的保护装置动作逻辑、不含真实的物理惯性**。论文摘要未讨论仿真与真实系统之间的偏差。
- **DNP3 版本未说明**：是否启用了 Secure Authentication（安全认证）未提及——这直接决定了攻击的难易程度。

## 和你的方向有什么关系

- **这是 L10 里"平台建设"路线的一篇**，和 096 Auto-SGCR（靶场自动化）、094（变电站测试床）互补：**096 解决"怎么快速搭"，098 解决"怎么接真实硬件"。**
- **直接选题（按推荐度排序）**：
  1. **DNP3 协议状态机异常检测**——利用协议本身的结构化特征做检测，比通用异常检测更精确，且**DNP3 的数据集比 IEC 61850 更容易获取**；
  2. **DNP3 模糊测试与漏洞挖掘**——真实设备 + 真实协议栈，纯网安技能可直接施展，**且工业协议实现漏洞是长期热点**；
  3. **HIL 环境下的"网络攻击 → 物理后果"量化研究**——这类研究需要平台，而你读这篇就是为了知道平台怎么来。
- **和你实验室方向的对接**：**"入侵检测"**（协议级检测）、**"程序逆向"**（RTAC 固件分析、DNP3 协议栈逆向）、**"工业AI与智能体"**（HIL 环境可作为智能体训练平台）。

## 概念关联

[[硬件在环仿真(HIL)]] · [[SCADA系统]] · [[工控安全测试床与数据集]] · [[电力信息物理系统(CPS)]]

## 原文摘要

> Modern power grids are dependent on communication systems for data collection, visualization, and control. Distributed Network Protocol 3 (DNP3) is commonly used in supervisory control and data acquisition (SCADA) systems in power systems to allow control system software and hardware to communicate. To study the dependencies between communication network security, power system data collection, and industrial hardware, it is important to enable communication capabilities with real-time power system simulation. In this paper, we present the integration of new functionality of a power systems dynamic simulation package into our cyber-physical power system testbed that supports real-time power system data transfer using DNP3, demonstrated with an industrial real-time automation controller (RTAC). The usage and configuration of DNP3 with real-world equipment in to achieve power system monitoring and control of a large-scale synthetic electric grid via this DNP3 communication is presented. Then, an exemplar of DNP3 data collection and control is achieved in software and hardware using the 2000-bus Texas synthetic grid.
