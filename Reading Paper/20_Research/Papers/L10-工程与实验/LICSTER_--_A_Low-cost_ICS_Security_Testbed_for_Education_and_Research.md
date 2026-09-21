---
document_id: "arxiv-1910.00303"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/1910.00303"
arxiv_id: "1910.00303"
title: "LICSTER -- A Low-cost ICS Security Testbed for Education and Research"
authors: ["Felix Sauer", "Matthias Niedermaier", "Susanne Kießling", "Dominik Merli"]
published: "2019-10-01"
venue: "arXiv preprint"
domain: "L10-工程与实验"
level: "L10"
reading_order: 91
difficulty: "入门"
lang: "en"
tags: ["电网安全", "L10-工程与实验", "测试床", "ICS安全", "低成本"]
quality_score: 9
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 091 | LICSTER：面向教育与研究的低成本 ICS 安全测试床

> [!abstract] 一句话
> 花约 500 欧元（约 4000 元人民币）就能搭出一套带真实物理过程的开源 ICS 测试床，全部材料开源提供——**这是本专题里对你最"能上手"的一篇**。

## 为什么读它

前面 090 讲的是数字孪生的顶层框架，落不了地。这篇直接给你一个**具体报价、具体物料、开源发布**的方案。

它在整个 L10 专题里的角色是"**最小可行测试床**"。后面 092（水处理 SCADA 测试床）、094（变电站 CPS 测试床）、098（DNP3 + 真实 RTAC 硬件）都是更大更贵的方案；LICSTER 证明了一件事：**入门 ICS 安全实验不需要几十万的设备**。

对研一学生来说，"能不能自己搭得起"往往比"这个平台有多先进"更重要。这篇就是回答这个问题的。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | LICSTER -- A Low-cost ICS Security Testbed for Education and Research |
| 作者 | Felix Sauer, Matthias Niedermaier, Susanne Kießling, Dominik Merli |
| 发表 | arXiv preprint, 2019-10-01 |
| 链接 | [arXiv](https://arxiv.org/abs/1910.00303) |
| 类型 | arXiv 预印本 |
| 难度 | 入门 |
| 关键词 | ICS 安全测试床、低成本、开源、教学、动手实验 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[1910.00303_fig1.png]]

![[1910.00303_fig2.png]]

![[1910.00303_fig3.png]]

![[1910.00303_fig4.png]]

![[1910.00303_fig5.png]]

![[1910.00303_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：工控系统正在变成"联网设备"，但没人敢在上面做实验

先说 ICS（Industrial Control Systems，工业控制系统）。**它是一类用来控制物理过程的计算机系统**——水厂控制水泵和阀门、电网控制断路器和变压器、汽车厂控制装配线。这些东西平时没人注意，但它们一旦停摆，城市就断水断电。

论文指出的趋势是：随着数字化推进，这些系统为了支持**远程控制和监控**，正在变得越来越联网。好处是运维方便，坏处是——**攻击面（attack surface）显著变大**。原本封闭在厂区里的系统现在有了网络接口，攻击者就有了入口。

那怎么让它们更安全？答案是**做研究**。但研究有个现实困难，论文原文说得很直白：**"difficult to conduct on productive systems, since these often have to operate twenty-four-seven"**——生产系统 7×24 小时不能停，你不可能在上面做渗透测试和攻击复现。

所以必须用测试床。但论文指出当时的两难：

- **真实测试床**：贵。工业级 PLC、RTU、HMI 加真实物理过程，成本极高；
- **纯仿真测试床**：便宜，但**没有真实物理过程（no real-world physical process）**——你攻击一个虚拟的水箱，水位不会真的变化，攻击的物理后果完全体现不出来。

**这就是 LICSTER 要填的坑：既要真实物理过程，又要便宜。**

### 方法：500 欧元的开源 ICS 测试床

论文的贡献就是一个叫 **LICSTER** 的测试床（名字本身是 Low-cost ICS Security Testbed 的缩写，论文标题也是这么展开的）。

它的核心设计目标是三条：

1. **低成本**：论文明确给出的数字是**约 500 欧元**（约 500 Euro）。摘要中这是唯一给出的价格数字，没有给出物料清单明细和各项单价。
2. **开源**：论文提供**所有必要的材料（all necessary material）**，让研究者能快速开始 ICS 黑客实验。
3. **面向教学与研究**：重点在于让人**动手（hands-on experience）**，而不是看论文。

论文强调的定位是"**with the focus on low-cost and open-source for education and research**"——低成本 + 开源，服务于教育和研究。

**摘要没有给出的关键信息**（不要臆造）：
- 具体用了什么型号的 PLC/控制器（摘要未给出）
- 具体控制的是什么物理过程（摘要未给出）
- 用了哪些工业协议（摘要未给出）
- 开源代码的仓库地址（摘要只说"提供所有必要材料"，未给出链接）

要落地搭建，必须去读原文正文和它的开源物料清单。

### 结果与结论

论文的结论是：**约 500 欧元就能让研究者和学生获得 ICS 安全的动手经验**，而且所有材料都提供出来了，可以"快速开始 ICS 黑客（quickly start ICS hacking）"。

摘要中**没有给出任何实验数据、攻击案例结果或性能指标**。这篇是典型的**平台/工具类论文**——它的"结果"就是平台本身可用、可复现。

## 关键公式（小白版）

这篇以平台设计为主，没有需要展开的核心公式。它的技术路线是：

1. **论证需求**：生产系统不能做实验 → 需要测试床；真实测试床太贵、纯仿真无物理过程 → 需要"便宜且带真实物理过程"的方案；
2. **设计并搭建**：用低成本硬件 + 开源软件组成一套可运行的 ICS 环境，成本控制在约 500 欧元；
3. **开放物料**：把搭建所需的全部材料公开，让别人能复制。

## 用网安的话说（小电解读）

**LICSTER ≈ 一个 4000 块钱能搭起来的工控靶场。**你在学校搭过 Web 靶场（DVWA、Pikachu 那种），LICSTER 就是工控版：**它的价值不在"高级"，在于"你今晚就能下单，下周就能开打"。**

具体对接你熟悉的东西：

- **"真实物理过程"这一层，相当于靶场里的"有状态服务"。**纯仿真测试床就像你只跑了一个返回固定 JSON 的 mock 接口——你改请求参数，后端状态不变，攻击效果看不出来。LICSTER 加了真实物理过程，等于后端真的会写数据库，你注入的数据会真的改变系统状态。**这对评测"攻击的物理后果"是决定性的。**
- **成本 500 欧 ≈ 你实验室一台中端服务器的钱。**这意味着它可以作为**个人课题的起步平台**，不用排队等实验室的大设备。
- **"开源 + 提供全部材料"是它最大的学术价值**。工控安全领域一个长期痛点是**实验不可复现**——各家论文用各家的测试床，数据不可比。LICSTER 把物料开放，等于给了你一个**可以和你师弟用同一套环境**的基准。

**可迁移的选题**：

1. **在 LICSTER 上复现已知 ICS 攻击并做检测**——因为平台开源、成本低，这是最容易跑通的一条路；
2. **给 LICSTER 补数据集**——这类教学测试床通常**不附带标注数据集**（摘要中也未提及任何数据集），而数据集正是这个领域最缺的资源。**"基于低成本测试床的 ICS 攻击流量数据集构建"**是低风险高价值的选题；
3. **横向对比多个低成本测试床的保真度**——LICSTER vs 102 那篇的软件仿真测试床，量化"物理过程的有无"对检测算法评测结论的影响。

## 读完后你应该能回答

- [ ] 为什么不能在真实的工控系统上做安全实验？
- [ ] 纯仿真测试床缺了什么关键要素？为什么这会影响研究结论？
- [ ] LICSTER 的成本大约是多少？它为什么强调"开源"？
- [ ] LICSTER 和 092 那篇水处理 SCADA 测试床，定位上有什么不同？
- [ ] 如果要用 LICSTER 做研究，你还缺什么（提示：数据）？

## 局限性

- **摘要信息量很小**：没有给出硬件型号、物理过程类型、使用的协议、代码仓库地址。**仅凭摘要无法复现搭建**，必须读原文。
- **2019 年的工作**，此后低成本硬件和开源 ICS 仿真生态（如基于 Docker 的方案）发展很快，方案可能已不是最优选择。
- **面向教学定位**：这类平台通常**规模小、攻击场景有限**，适合入门和教学，**未必足以支撑需要大规模数据的 ML 检测研究**。
- 论文没有讨论**测试床本身的保真度量化**（"多像真实 ICS"），也没有给出与其他测试床的对照评估。
- **500 欧元的成本未说明是否包含全部外设与软件授权**，摘要中只有一个总价数字，明细未知。

## 和你的方向有什么关系

- **这是你"最快能动手"的一篇**。如果实验室暂时没有大测试床，LICSTER 可以作为个人起步环境。
- **直接选题（按推荐度排序）**：
  1. **基于低成本测试床构建 ICS 攻击数据集**——这是领域刚需，且和你"入侵检测"方向完全对口；
  2. **在 LICSTER 上评测现有 IDS 方法**，检验"实验室里 99% 的检测率"在真实物理过程下还剩多少（呼应 L3 的"虚假安全感"主题）；
  3. **攻击注入工具开发**——把攻击脚本工程化，作为靶场组件。
- **和你实验室方向的对接**：**"入侵检测"**（直接对口）、**"工业AI与智能体"**（测试床可作为智能体训练与评测环境）。

## 概念关联

[[工控安全测试床与数据集]] · [[SCADA系统]] · [[Modbus协议安全]] · [[IEC 62443]]

## 原文摘要

> Unnoticed by most people, Industrial Control Systems (ICSs) control entire productions and critical infrastructures such as water distribution, smart grid and automotive manufacturing. Due to the ongoing digitalization, these systems are becoming more and more connected in order to enable remote control and monitoring. However, this shift bears significant risks, namely a larger attack surface, which can be exploited by attackers. In order to make these systems more secure, it takes research, which is, however, difficult to conduct on productive systems, since these often have to operate twenty-four-seven. Testbeds are mostly very expensive or based on simulation with no real-world physical process. In this paper, we introduce LICSTER, an open-source low-cost ICS testbed, which enables researchers and students to get hands-on experience with industrial security for about 500 Euro. We provide all necessary material to quickly start ICS hacking, with the focus on low-cost and open-source for education and research.
