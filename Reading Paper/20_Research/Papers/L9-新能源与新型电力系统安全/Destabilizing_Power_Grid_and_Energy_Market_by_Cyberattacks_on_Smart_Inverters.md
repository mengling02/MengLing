---
document_id: "arxiv-2505.14175"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2505.14175"
arxiv_id: "2505.14175"
title: "Destabilizing Power Grid and Energy Market by Cyberattacks on Smart Inverters"
authors: ["Xiangyu Hui", "Samuel Karumba", "Sid Chi-Kin Chau", "Mohiuddin Ahmed"]
published: "2025-05-20"
venue: "arXiv preprint"
domain: "L9-新能源与新型电力系统安全"
level: "L9"
reading_order: 79
difficulty: "进阶"
lang: "en"
tags: ["电网安全", "L9-新能源与新型电力系统安全", "智能逆变器", "电力市场", "协同攻击"]
quality_score: 9
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 079 | 用对智能逆变器的网络攻击搞乱电网与能源市场

> [!abstract] 一句话
> 论文用澳大利亚真实电力市场数据回答了一个关键问题：大规模攻击智能逆变器，真的能搞垮电网吗？答案是——**要精心策划才行，而且需要的逆变器比例低得惊人**。

## 为什么读它

这是 L9 专题里**最"务实"的一篇攻击评估论文**。

前面 078 篇告诉你"逆变器是软件定义设备，有攻击面"。这篇不满足于此，它要回答一个更硬的问题：

> **如果攻击者真的动手，规模要多大才有效？电网的现有安全机制能不能扛住？**

它的价值有三层：

1. **它是"可行性评估"，不是"漏洞演示"**。很多攻击论文只能证明"理论上可以"，这篇用的是**真实电力市场数据**，做的是**量级判断**——这比单点漏洞更有决策价值。
2. **它同时打了电网和电力市场**。这是很少见的——大多数论文只关心"电灯会不会灭"，这篇还关心"电价会不会崩"。
3. **它的结论很反直觉**：论文发现**相对低比例的分布式光伏就足以发动有影响的协同攻击**。这意味着防御方不能靠"新能源渗透率还不高，先不管"来拖延。

读完它，你会对"新能源把电网变脆了"这条主线有一个**量化的、带对抗视角的**理解。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | Destabilizing Power Grid and Energy Market by Cyberattacks on Smart Inverters |
| 作者 | Xiangyu Hui, Samuel Karumba, Sid Chi-Kin Chau, Mohiuddin Ahmed |
| 发表 | arXiv preprint, 2025-05-20 |
| 链接 | [arXiv:2505.14175](https://arxiv.org/abs/2505.14175) |
| 类型 | arXiv 预印本（实证评估研究） |
| 难度 | 进阶 |
| 关键词 | 智能逆变器、分布式光伏、电力市场、协同攻击、电网稳定性 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2505.14175_fig1.png]]

![[2505.14175_fig2.png]]

![[2505.14175_fig3.png]]

![[2505.14175_fig4.png]]

![[2505.14175_fig5.jpeg]]

![[2505.14175_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 为什么现在必须认真对待这件事

论文开篇给了三个理由，说明"逆变器被攻击"已经从理论担忧变成了现实威胁：

1. **已经有真实漏洞和攻击事件被记录在案**（well-documented vulnerabilities and attack incidents）。也就是说，这不是假设——逆变器的漏洞是公开的、被利用过的。
2. **逆变器设备寿命很长**。一台逆变器装上去要用十几年，甚至二十年。这意味着**它出厂时的安全水平，会被锁定十几年**。今天不安全的设备，十年后还在网里跑。这和 IT 设备"三年一换"的节奏完全不同。
3. **用户根本不关心合规**（users' oblivion of cybersecurity compliance），而且**缺乏网络监管框架**（lack of cyber regulatory frameworks）。

第三点特别值得注意：**分布式光伏的业主是普通家庭和企业，不是电力公司**。他们没有动力、也没有能力去维护逆变器的安全。而监管上，这些小设备又处在"电网公司管不着、网信部门管不过来"的灰色地带。这造成了一个**巨大的、无人负责的攻击面**。

论文由此提出核心研究问题：

> 如果对智能逆变器的网络攻击被**大规模地协同发起**，它是否真的会对电网和能源市场造成**广域不稳定**？

注意"协同（orchestrated）"这个词——它不是问"攻击一台逆变器会怎样"，而是问"**同时攻击很多台，并且精心选择时机和对象**会怎样"。

### 方法：用真实市场数据 + 实际的事故应对机制

论文的研究方法是这篇的亮点：

- **数据**：使用**澳大利亚电力市场（electricity market）的真实数据**。澳大利亚是全球分布式光伏渗透率最高的地区之一（屋顶光伏极普及），所以它是研究这个问题的天然实验场。
- **机制**：结合**实际的事故应对机制（practical contingency mechanisms）**的知识。也就是说，论文不是凭空假设电网会怎么反应，而是按照电网实际运行中应对"意外事故"的流程来建模。

"事故应对机制"这个概念需要解释一下：电网运行中，调度中心预先准备了一套"如果发生 X 事故，就执行 Y 措施"的预案（比如切负荷、启动备用机组、解列）。论文把攻击放在这个框架里评估——**如果攻击让系统进入某种状态，现有的预案能不能救回来？**

这个思路非常关键，因为它把攻击评估从"物理破坏"提升到了"**对抗性利用既有防御机制**"的层面。

### 三个核心发现

论文的三个结论，每一个都值得单独记住：

**发现一：破坏是可能的，但需要精心策划和协同。**

> 尽管对智能逆变器的网络攻击存在扰乱电网的可能性，但其影响**只有在仔细规划和协同下才会显著**。

这看起来像是个"好消息"（随便打打没用），但实际上是**坏消息**：它意味着电网的天然鲁棒性能够吸收**无意的、随机的**扰动，但对**有意的、最优化的**攻击没有抵抗力。攻防不对称——防御方要防住所有情况，攻击方只需要找到一种最优组合。

**发现二：电网能扛住"意外事故"，但扛不住"聪明攻击者"。**

> 电网能确保一定的电力系统安全性以在**无意的事故（inadvertent contingency）**中存活，但**不足以防御能够在对抗性方式下协同攻击的狡猾攻击者**。

这是全篇最重要的一句话。翻译成大白话：

**电网的 N-1 安全准则（即"任何单一元件故障都不应导致系统崩溃"）是为"随机故障"设计的，不是为"恶意攻击"设计的。** 随机故障不会挑时机、不会选最脆弱的组合、不会配合市场周期。而攻击者会。

这和 IT 安全的类比非常直接：**容错（fault tolerance）不等于抗攻击（attack resilience）**。一个能容忍随机硬件故障的分布式系统，未必能容忍一个知道系统内部结构的拜占庭节点。

**发现三：需要的渗透率低得惊人。**

> 对澳大利亚电网的数据分析还显示，**相对较低比例的分布式光伏**就足以对电网发动有影响力的协同攻击。

论文**没有在摘要里给出具体数值**（摘要未给出具体数值），只说了"relatively low percentage"。但这个定性结论本身已经很震撼了：它意味着"新能源渗透率还不高"**不能**作为推迟安全建设的理由。

### 结论与建议

论文最后说，它的研究为"高分布式光伏渗透率地区"的防御策略提供了洞见。核心含义是：**这些地区需要重新设计防御策略，把"对抗性攻击"作为一类独立的威胁来建模**，而不是继续沿用为随机故障设计的机制。

## 关键公式（小白版）

这篇以数据分析和实证评估为主，摘要中没有给出需要展开的核心公式。

它的技术路线是：**真实市场数据 → 结合实际事故应对机制建模 → 协同攻击场景构造 → 评估电网与市场的失稳程度 → 给出防御启示**。属于"实证评估"类研究，核心贡献在于结论而非公式。

如果你需要理解背后的数学，最相关的是 078 篇里给出的**转子摆动方程**——攻击逆变器影响的就是其中的 $\Delta P_e$ 项（功率缺额），而"低渗透率就足够"这个结论，本质上说的是"在惯量已经很低的系统里，不需要太大的功率缺额就能造成危险"。

## 用网安的话说（小电解读）

**这篇论文的思维方式和渗透测试里的"红队评估"完全一致，值得你把它当作方法论范本来读。**

对齐到你的知识体系：

- **它的核心命题 = "漏洞存在 ≠ 系统可被攻陷"**。这正是渗透测试和红队评估的区别。单点漏洞（逆变器不加密、弱认证）是"漏洞"，但真正要评估的是**"把漏洞组合起来、在正确时机使用，能不能达成目标"**。论文做的就是后者。你做渗透测试时写的"攻击链（kill chain）"就是同一件事。

- **"协同攻击" ≈ 分布式协同攻击（coordinated attack）**。论文说的 orchestrated attack 有明确的三要素：
  - **多目标同时**（大量逆变器一起动）
  - **精心选择对象**（不是随便挑，而是挑对系统影响最大的）
  - **配合时机**（比如配合负荷高峰、配合市场出清时刻）
  
  这和你熟悉的多阶段 APT 攻击逻辑一模一样：**侦察 → 选点 → 等待时机 → 协同触发**。

- **"电网能抗意外但不抗恶意" ≈ 容错系统不抗拜占庭攻击**。这是一个非常深刻的普适结论，不限于电力。**任何按"随机故障"设计的冗余机制，在对抗性攻击面前都会失效**，因为攻击者可以专门制造"多个冗余同时失效"的场景。你的选题可以从这个角度切入：**把电力系统的 N-1 准则扩展到"对抗性 N-k"**。

- **"低渗透率就够" ≈ 攻击者只需要找到系统的关键少数**。这本质上是一个**影响力最大化（influence maximization）**问题——和社交网络里"选哪几个节点传播谣言最有效"是同一个数学问题。第 080 篇正是从这个角度做的（最优攻击集选择）。

- **可迁移的选题**：
  1. **面向电力市场的攻击建模**：论文同时打了物理电网和市场，但市场侧的分析相对粗。**"攻击如何通过操纵逆变器出力影响电价"** 是可以深挖的。
  2. **对抗性场景生成**：论文的结论依赖"精心策划"，那能不能用**强化学习训练一个攻击策略**，自动找出最有效的攻击组合？这是一个典型的 AI + 安全的交叉题，直接对接你的方向。

## 读完后你应该能回答

- [ ] 论文认为智能逆变器面临的三个加剧因素是什么？为什么"设备寿命长"是个安全问题？
- [ ] 论文用什么数据和什么机制来做评估？为什么用澳大利亚的数据？
- [ ] "电网能扛住无意事故但扛不住协同攻击"这句话背后的逻辑是什么？为什么容错不等于抗攻击？
- [ ] 论文关于"所需渗透率"的结论是什么？它意味着什么？
- [ ] 为什么"用户不关心合规"和"缺乏监管框架"会让问题更严重？

## 局限性

- **摘要未给出具体数值**。论文只说"相对较低比例"，没有在摘要中披露具体的渗透率阈值、影响范围或仿真规模。要判断这个结论有多强，必须读全文。
- **地域依赖强**。结论基于**澳大利亚**的电力市场数据和事故应对机制。澳大利亚电网的特点（高光伏渗透、相对孤立的同步电网、市场机制）与中国、欧洲、北美差异都很大，**结论不能直接外推**。
- **"攻击可实现性"被抽象掉了**。论文评估的是"如果攻击者能控制 N 台逆变器，会发生什么"，但对**攻击者如何真正拿下这些逆变器**（是漏洞利用？供应链？弱口令？）着墨不多。也就是说，它评估的是**影响**，不是**可行性链路**。
- **模型简化的风险**。用市场数据 + 事故机制做评估，必然要简化电网的动态模型（比如惯量、保护动作、机组响应）。简化到什么程度会改变结论，摘要里看不出来。
- **"协同"的假设很强**。论文假设攻击者能做到精确同步、精确选点。现实中大规模协同攻击本身就有技术难度（需要 C2 基础设施、需要同步机制）。这个假设放宽后结论会弱多少，是个开放问题。

## 和你的方向有什么关系

- **这是你理解"攻击效果评估"方法论的最佳中文入口**（虽然是英文论文）：它示范了如何从"漏洞"走到"影响"，这个思维对你的研究设计很有用。
- **最推荐的选题**：
  1. **用强化学习自动搜索最优攻击策略**。论文的结论依赖"精心策划"，而"找最优策略"正是强化学习擅长的事。**"基于 RL 的逆变器协同攻击策略生成"** 是一个方法上成熟、场景上新颖的题目。
  2. **对抗性 N-k 安全评估**：把传统电力 N-1/N-k 准则改造成"面向最优攻击者的 k 台设备失效"评估框架。这是一个偏理论但很扎实的方向。
  3. **影响力度量**：论文的核心问题是"选哪些逆变器攻击最有效"，这是图上的影响力最大化问题。如果你对图神经网络/图算法有兴趣，可以做成"基于 GNN 的电网关键节点识别"。
- **和你实验室方向的对接**：这篇是典型的"AI + 安全 + 工控"三合一场景，天然契合"工业 AI 与安全"实验室定位。它也是很好的**数据集/测试床切入点**——论文用的是市场数据，你可以考虑用仿真平台（如 ACTIVSg、IEEE 标准系统）复现并扩展。
- **地域上**：中国分布式光伏发展很快，山东等省份的户用光伏装机量已经很大。论文的结论对这类地区有直接的参考价值——**"低渗透率就足够"意味着分布式光伏大省需要更早建立安全评估能力**。

## 概念关联

[[逆变器与电力电子安全]] · [[电力信息物理系统(CPS)]] · [[电力系统稳定性]] · [[高级持续性威胁(APT)]] · [[智能电网]]

## 原文摘要

> Cyberattacks on smart inverters and distributed PV are becoming an imminent threat, because of the recent well-documented vulnerabilities and attack incidents. Particularly, the long lifespan of inverter devices, users' oblivion of cybersecurity compliance, and the lack of cyber regulatory frameworks exacerbate the prospect of cyberattacks on smart inverters. As a result, this raises a question -- "do cyberattacks on smart inverters, if orchestrated on a large scale, pose a genuine threat of wide-scale instability to the power grid and energy market"? This paper provides a realistic assessment on the plausibility and impacts of wide-scale power instability caused by cyberattacks on smart inverters. We conduct an in-depth study based on the electricity market data of Australia and the knowledge of practical contingency mechanisms. Our key findings reveal: (1) Despite the possibility of disruption to the grid by cyberattacks on smart inverters, the impact is only significant under careful planning and orchestration. (2) While the grid can assure certain power system security to survive inadvertent contingency events, it is insufficient to defend against savvy attackers who can orchestrate attacks in an adversarial manner. Our data analysis of Australia's electricity grid also reveals that a relatively low percentage of distributed PV would be sufficient to launch an impactful concerted attack on the grid. Our study casts insights on robust strategies for defending the grid in the presence of cyberattacks for places with high penetration of distributed PV.
