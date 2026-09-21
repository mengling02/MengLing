---
document_id: "arxiv-2507.18249"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2507.18249"
arxiv_id: "2507.18249"
title: "Auto-SGCR: Automated Generation of Smart Grid Cyber Range Using IEC 61850 Standard Models"
authors: ["Muhammad M. Roomi", "S. M. Suhail Hussain", "Ee-Chien Chang", "David M. Nicol", "Daisuke Mashima"]
published: "2025-07-24"
venue: "arXiv preprint"
domain: "L10-工程与实验"
level: "L10"
reading_order: 96
difficulty: "进阶"
lang: "en"
tags: ["电网安全", "L10-工程与实验", "网络靶场", "自动化生成", "IEC 61850"]
quality_score: 9
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 096 | Auto-SGCR：用 IEC 61850 标准模型自动生成智能电网网络靶场

> [!abstract] 一句话
> 定义了一门 XML 建模语言 SG-ML（内含 IEC 61850 的 SCL 配置），再写一套工具链把它**自动实例化成一个能跑的智能电网靶场**——靶场从"一次性手工定制"变成"可共享、可修改、可复现的模型文件"，而且**工具链和示例模型已开源**。

## 为什么读它

这是 L10 专题里**工程含量最高、也最接近你"造靶场"需求**的一篇。

前面几篇测试床的共同问题是：**每一个都是"一次性、专有系统（one-off, proprietary system）"**。论文原文把这个痛点列得很清楚——现有智能电网靶场**在可配置性（configurability）、可访问性（accessibility）、可移植性（portability）、可复现性（reproducibility）上都受限**。

**这句话你可能有强烈共鸣**：实验室搭靶场最痛的就是"搭一次用一次"——换个场景就得重搭，别人还复现不了你的环境，论文里的实验别人永远重现不出来。

Auto-SGCR 的解法很"程序员"：**把靶场定义抽象成一个模型文件**。模型文件可以 git 管理、可以分享、可以改一行参数就换一个拓扑。**这本质上就是"靶场即代码（Cyber Range as Code）"。**

而且它**开源**（工具链 + 示例 SG-ML 模型）。这是本专题里少数明确说了开源的项目之一。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | Auto-SGCR: Automated Generation of Smart Grid Cyber Range Using IEC 61850 Standard Models |
| 作者 | Muhammad M. Roomi, S. M. Suhail Hussain, Ee-Chien Chang, David M. Nicol, Daisuke Mashima |
| 发表 | arXiv preprint, 2025-07-24 |
| 链接 | [arXiv](https://arxiv.org/abs/2507.18249) |
| 类型 | arXiv 预印本 |
| 难度 | 进阶 |
| 关键词 | 智能电网网络靶场、自动化生成、SG-ML、IEC 61850、SCL、开源工具链 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2507.18249_fig1.png]]

![[2507.18249_fig2.png]]

![[2507.18249_fig3.png]]

![[2507.18249_fig4.jpg]]

![[2507.18249_fig5.jpg]]

![[2507.18249_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：为什么电网需要"网络靶场"

先解释 **网络靶场（cyber range）**。你熟悉 CTF 平台和攻防演练环境——**靶场就是一套隔离的、可安全地打攻击的仿真环境**。和普通测试床的区别在于，靶场更强调"**完整可运行**"和"**可反复使用**"。

论文开篇的逻辑链是这样的：

1. **电网数字化让它越来越容易受网络攻击**（digitalization of power grids have made them increasingly susceptible to cyber-attacks）；
2. 所以**迭代式的网络安全测试是不可或缺的**（iterative cybersecurity testing is indispensable），用来对抗不断出现的新攻击向量，并确保关键基础设施的可依赖性；
3. 这些测试还能用来**评估安全配置、评估防御措施对各种攻击向量的有效性、以及训练防守方专家**；
4. **但生产环境不可能用来做这些实验**（"it is often infeasible to conduct such experiments and training using production environment"）；
5. 所以**需要高保真度的网络靶场（high-fidelity cyber range）**。

**"缩小研究与生产环境之间的差距（narrows the gap between academic research and production environment）"**——这句话是论文的核心动机。**学术论文里的攻击在真实电网上到底成不成立？** 靶场保真度越高，这个问题的答案越可靠。

### 问题：造靶场太难、太贵、太不可复现

论文把造靶场的困难列成了三条：

**1）需要跨领域的专业知识**
> "the design and implementation of cyber range requires extensive domain knowledge of physical and cyber aspect of the infrastructure"

你要同时懂**电力系统的物理侧**（潮流、保护、动态）和**信息侧**（协议、网络、软件）。**这个"跨领域"要求恰恰是大多数研究者的痛点**——做安全的不懂电力，做电力的不懂安全。这也是**你现在的处境**，只不过你是从安全侧切入。

**2）搭建与维护成本高**
> "costs incurred for setup and maintenance of cyber range are significant"

**3）现有靶场是"一次性、专有"的，不可配置、不可访问、不可移植、不可复现**
> "most existing smart grid cyber ranges are designed as a one-off, proprietary system, and are limited in terms of configurability, accessibility, portability, and reproducibility"

**这四条限制（4 个 -ity）是整篇论文要打的靶子。**

### 方法：SG-ML + 工具链

Auto-SGCR 的方案分两步：

**第一步：定义 SG-ML（Smart Grid Modeling Language，智能电网建模语言）**

论文定义了一门 **XML 为基础、对人和机器都友好（human-/machine-friendly）** 的建模语言，叫 **SG-ML**。它的关键特性是**"incorporates IEC 61850 System Configuration Language files"**——**把 IEC 61850 的 SCL（系统配置语言）文件整合进来**。

> **这一步为什么关键**：回忆 095 那篇 Subs-BOM——它也是拿 IEC 61850 的 SCD 文件做数据源。**这两篇论文走的是同一条路：IEC 61850 的配置文件是电力行业的"事实标准资产描述"，复用它，就等于免费获得了"真实变电站的配置数据"。**
>
> **用你熟悉的话说**：这相当于用一份标准的 Docker Compose 文件来描述整个靶场——拓扑、设备、连接关系全在里面，`docker compose up` 就起来。

**第二步：开发工具链（toolchain）**

论文开发了一套工具链，功能是：**解析 SG-ML 模型文件 → 自动实例化一个功能完整的智能电网网络靶场**（parse SG-ML model files and automatically instantiate a functional smart grid cyber range）。

**"自动实例化"是核心**。这意味着：**模型文件是"声明式"的，工具链负责把它变成实际运行的靶场。**你不需要手工配每一台设备。

**第三步（隐含但很重要）：模型可共享、可修改**

论文明确说：**"The developed SG-ML models can be easily shared and/or modified to reproduce or customize for any cyber range."**——开发出来的 SG-ML 模型可以轻松地分享或修改，以复现或定制任意靶场。

**这正是解决了"可复现性"问题**：以后发论文，把 SG-ML 模型文件作为附件一起提交，别人就能一键复现你的实验环境。**这在学术上意义重大**——工控安全领域长期被诟病"实验不可复现"。

### 验证与开放

- **案例研究（case studies）**：论文用**大规模变电站模型（large-scale substation models）** 演示了 Auto-SGCR 的应用；
- **开源**：论文明确说"**The toolchain along with example SG-ML models have been open-sourced.**"——工具链和示例 SG-ML 模型已经开源。

**摘要中没有给出的关键信息**（不要臆造）：
- SG-ML 的具体语法结构、支持哪些 IEC 61850 逻辑节点（摘要未给出）
- 开源仓库的地址（摘要未给出 URL）
- 靶场实例化后跑在什么平台（容器？虚拟机？真实硬件？摘要未给出）
- "大规模"具体是多少个变电站/多少个 IED（摘要未给出）
- 实例化耗时、资源占用（摘要未给出）

**特别警告**：论文说"large-scale substation models"，但**具体规模摘要里没有数字，不要臆造。**

### 结论

Auto-SGCR 证明了：**用标准化的建模语言 + 自动化工具链，可以把智能电网靶场的构建从"手工定制的一次性工程"变成"可声明、可分享、可复现的模型驱动过程"**。

## 关键公式（小白版）

这篇以系统设计与工具实现为主，没有需要展开的核心公式。它的技术路线可以画成一条"模型驱动"的流水线：

```
IEC 61850 SCL 文件（真实变电站的标准配置描述）
        +
   自定义的 SG-ML 建模语言（XML）
        ↓
   SG-ML 模型文件（可 git 管理、可分享、可 diff）
        ↓  工具链解析
   自动实例化
        ↓
   可运行的智能电网网络靶场
```

**一句话概括**：把"搭靶场"从"手工作业"变成"写配置文件"。

## 用网安的话说（小电解读）

**Auto-SGCR ≈ 用 Docker Compose / Terraform 的思路造工控靶场。**这个类比非常贴切：

| Auto-SGCR 的概念 | 你熟悉的对应物 |
|---|---|
| SG-ML 模型文件 | Docker Compose YAML / Terraform HCL |
| 工具链（解析 + 实例化） | `docker compose up` / `terraform apply` |
| IEC 61850 SCL 文件 | 现成的镜像描述 / 基础设施清单 |
| 可分享、可复现的靶场 | 把 compose 文件提交到 git，别人一键复现 |

**几个关键洞察**：

1. **"靶场即代码"直接解决了科研的可复现性危机。**
   工控安全领域一个长期问题是：**论文里的测试床没人能复现，实验结论无法验证**。Auto-SGCR 的思路是——**把环境也变成论文的一部分（artifact）**。这和你现在看到的 `note_path` 自动插图机制是同一种工程思维的产物。

2. **复用 IEC 61850 SCL 是"站在巨人肩膀上"**。
   为什么能自动生成？因为**变电站的配置信息本来就标准化了**。这是电力行业相比其他工控行业（比如化工、制造，各家协议五花八门）的独特优势。**做电网安全靶场，你有一个别的 ICS 领域没有的便利条件。**

3. **"跨领域知识要求高"这一条，恰恰是你的定位**。
   论文把它列为困难，但**对你来说是机会**：你网安功底在，缺的只是电力侧知识——**而这个知识可以通过读靶场定义文件（SCL/SG-ML）快速补齐**。**"能读懂 SCL 文件"本身就是一项稀缺技能。**

4. **论文的空白 = 你的选题**：
   - **SG-ML 只描述"结构"，不描述"攻击"**——能不能把攻击场景也模型化？（Attack as Code）
   - **保真度未量化**——自动生成的靶场和真实变电站差多少？
   - **没有中国体系适配**——SG-ML 里没有中国电力监控系统"安全分区、网络专用、横向隔离、纵向认证"的建模能力。

**可迁移的选题**：

1. **"攻击即代码"（Attack as Code）**：扩展 SG-ML，把攻击脚本、攻击时序也纳入模型，实现"一条命令复现一篇论文的攻击实验"；
2. **靶场保真度评估框架**：量化自动生成靶场与真实系统的偏差；
3. **面向中国电力监控体系的靶场自动生成**（把"横向隔离装置""纵向加密认证装置"建模进去）；
4. **SG-ML 模型的模糊测试**：模型文件本身就是输入，畸形模型会不会让工具链崩掉/生成错误靶场？**这是纯网安视角，几乎没人做。**

## 读完后你应该能回答

- [ ] 什么是网络靶场？它和测试床的区别在哪？
- [ ] 现有智能电网靶场的四个限制是什么（四个 -ity）？
- [ ] SG-ML 是什么？它为什么要整合 IEC 61850 的 SCL 文件？
- [ ] Auto-SGCR 的"自动实例化"意味着什么？为什么它能提升可复现性？
- [ ] 论文开源了什么？

## 局限性

- **摘要未给出任何量化指标**：没有实例化耗时、资源占用、支持的规模上限。**无法判断工具链在"大规模"场景下是否真的可用。**
- **案例研究只有"大规模变电站模型"**，摘要未说明具体规模和场景多样性。
- **保真度（fidelity）未被量化**：论文强调"high-fidelity cyber range is vital"，但摘要未给出任何保真度评估方法或结果。**自动生成的靶场到底多像真实变电站，是个悬而未决的问题。**
- **SG-ML 是一门新语言，生态为零**：没有社区、没有工具、没有文档，学习成本由使用者承担。相比之下，直接用现成的编排工具（如容器编排）可能更实用。摘要未讨论为什么必须自造一门语言。
- **只覆盖 IEC 61850 体系**：对其他电力协议（DNP3、Modbus）和其他环节（配电网、新能源场站）的适用性未知。
- **开源代码的维护持续性未知**（摘要未给出仓库地址，无法评估活跃度）。

## 和你的方向有什么关系

- **这是你"自建靶场"最直接的技术参考**，而且开源，可以直接下载研究。
- **直接选题（按推荐度排序）**：
  1. **攻击即代码（Attack as Code）**——把攻击场景纳入 SG-ML 之类的模型语言，实现攻击实验的完全可复现。**这是论文最明显的空白，且工程量适中，非常适合硕士课题**；
  2. **靶场保真度量化框架**——对接你在 L3 读到的"缺乏统一基准"问题；
  3. **靶场定义文件的安全性**——模型文件/SCL 文件的解析器漏洞、恶意模型注入，**纯网安视角，几乎无人涉足**；
  4. **面向中国电力监控系统防护体系的靶场建模扩展**。
- **和你实验室方向的对接**：**"入侵检测"**（靶场是 IDS 评测平台）、**"工业AI与智能体"**（靶场可作为智能体训练环境）、**"程序逆向"**（解析 SCL/SG-ML 二进制或文本格式，做解析器安全分析）。

## 概念关联

[[IEC 61850]] · [[工控安全测试床与数据集]] · [[数字孪生]] · [[智能电网]]

## 原文摘要

> Digitalization of power grids have made them increasingly susceptible to cyber-attacks in the past decade. Iterative cybersecurity testing is indispensable to counter emerging attack vectors and to ensure dependability of critical infrastructure. Furthermore, these can be used to evaluate cybersecurity configuration, effectiveness of the cybersecurity measures against various attack vectors, as well as to train smart grid cybersecurity experts defending the system. Enabling extensive experiments narrows the gap between academic research and production environment. A high-fidelity cyber range is vital as it is often infeasible to conduct such experiments and training using production environment. However, the design and implementation of cyber range requires extensive domain knowledge of physical and cyber aspect of the infrastructure. Furthermore, costs incurred for setup and maintenance of cyber range are significant. Moreover, most existing smart grid cyber ranges are designed as a one-off, proprietary system, and are limited in terms of configurability, accessibility, portability, and reproducibility. To address these challenges, an automated Smart grid Cyber Range generation framework is presented in this paper. Initially a human-/machine-friendly, XML-based modeling language called Smart Grid Modeling Language was defined, which incorporates IEC 61850 System Configuration Language files. Subsequently, a toolchain to parse SG-ML model files and automatically instantiate a functional smart grid cyber range was developed. The developed SG-ML models can be easily shared and/or modified to reproduce or customize for any cyber range. The application of Auto-SGCR is demonstrated through case studies with large-scale substation models. The toolchain along with example SG-ML models have been open-sourced.
