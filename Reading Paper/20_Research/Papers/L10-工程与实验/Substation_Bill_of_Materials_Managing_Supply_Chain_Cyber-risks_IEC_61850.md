---
document_id: "arxiv-2503.19638"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2503.19638"
arxiv_id: "2503.19638"
title: "Substation Bill of Materials: A Novel Approach to Managing Supply Chain Cyber-risks on IEC 61850 Digital Substations"
authors: ["Xabier Yurrebaso", "Fernando Ibañez", "Ángel Longueira-Romero"]
published: "2025-03-25"
venue: "arXiv preprint"
domain: "L10-工程与实验"
level: "L10"
reading_order: 95
difficulty: "入门+"
lang: "en"
tags: ["电网安全", "L10-工程与实验", "供应链安全", "SBOM", "IEC 61850"]
quality_score: 9
created: "2026-09-17"
updated: "2026-09-17"
status: "analyzed"
---
# 095 | 变电站物料清单：管理 IEC 61850 数字变电站供应链网络风险的新方法

> [!abstract] 一句话
> 把 IT 界的 **SBOM（软件物料清单）** 思路搬进数字变电站：用 IEC 61850 的 SCD 配置文件自动生成一份"变电站物料清单（Subs-BOM）"，把站内所有 IED、固件版本、开放服务都列清楚，再用 OWASP Dependency-Track 自动查漏洞。

## 为什么读它

这是整个 L10 专题里**视角最不一样**的一篇。前面几篇都在讲"怎么搭环境打攻击"，这篇讲的是**"你连自己变电站里有什么设备都说不清楚，还谈什么安全"**。

它把网安界的**供应链安全（supply chain security）** 和 **SBOM（Software Bill of Materials，软件物料清单）** 这套方法论，第一次系统性地搬到了电力数字变电站场景。对你来说这是**极其值得关注的方向**——原因有三：

1. **这是网安热点，你的知识可以直接迁移**。Log4Shell 之后，SBOM 在 IT 领域已经是标配，但在电力行业才刚刚起步；
2. **它用的技术栈你全懂**：CycloneDX 是 IT 界的 SBOM 标准格式，Dependency-Track 是 OWASP 的开源工具，**门槛极低**；
3. **它有明确的落地缺口**：论文只做了"生成 + 查漏洞"，**没做"漏洞被利用的可行性分析"，也没做"攻击图"**——这些都是你可以接着做的。

## 核心信息

| 项目 | 内容 |
|---|---|
| 标题 | Substation Bill of Materials: A Novel Approach to Managing Supply Chain Cyber-risks on IEC 61850 Digital Substations |
| 作者 | Xabier Yurrebaso, Fernando Ibañez, Ángel Longueira-Romero |
| 发表 | arXiv preprint, 2025-03-25 |
| 链接 | [arXiv](https://arxiv.org/abs/2503.19638) |
| 类型 | arXiv 预印本 |
| 难度 | 入门+ |
| 关键词 | 供应链安全、SBOM、CycloneDX、IEC 61850、SCD、IED、数字变电站 |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2503.19638_fig1.png]]

![[2503.19638_fig2.png]]

![[2503.19638_fig3.png]]

![[2503.19638_fig4.png]]

![[2503.19638_fig5.png]]

![[2503.19638_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 背景：数字变电站是"多厂商拼盘"，供应链成了软肋

先说 **数字变电站（DS，Digital Substation）**。智能电网经历了一场深刻的数字化进程，把新的**数据驱动的控制与监视技术**整合进来，结果就是现代数字变电站。它和传统变电站的最大区别是：**一次设备（变压器、断路器）和二次设备（保护、测控）之间的连接，从铜缆变成了光纤以太网上的 IEC 61850 报文。**

论文指出一个关键事实：**数字变电站是一个多厂商环境（multivendor environment）**。一个站里可能有 A 厂的保护装置、B 厂的合并单元、C 厂的交换机、D 厂的网关——因为 IEC 61850 是开放标准，理论上不同厂商的设备能互通，实践中也确实需要互通。

**问题就出在这里。**论文明确指出：**攻击者越来越把重点放在攻击数字变电站的供应链上（Attackers are more focused on attacking the supply chain of the DS）**——正是因为多厂商环境给了攻击者更多入口。

> **用网安的话说**：这是典型的**供应链攻击（supply chain attack）**。你不需要攻破变电站的网络边界，只需要**在某一家厂商的固件里埋一个后门**，这个后门就会随着设备部署，自动进入所有采购了该设备的变电站。SolarWinds 事件就是这个思路的教科书案例——**攻击者打的是"信任链的上游"，而不是"防御的边界"。**

而供应链安全的前提是：**你得先知道你有什么。** 这正是 SBOM 要解决的问题。

### 问题：变电站里到底装了什么，没人说得清

在 IT 领域，这个问题的标准解法是 **SBOM（Software Bill of Materials，软件物料清单）**。它是一份机器可读的清单，列出一个软件产品用到的所有组件及其版本。有了 SBOM，当某个开源组件爆出漏洞（比如 Log4Shell），你可以**在几分钟内查出自己有多少系统受影响**，而不是靠人工翻台账。

**但数字变电站没有 SBOM。**原因很实际：

- 变电站的设备是**嵌入式 IED（Intelligent Electronic Device，智能电子设备）**，不是普通服务器，很难直接扫描；
- 电力行业的资产台账通常是**人工维护的 Excel 表格**，更新滞后、不完整、不可机读；
- 一个电力公司可能管着**几十上百个变电站**，每个站几十台 IED，人工盘点不现实。

### 方法：Subs-BOM —— 从 SCD 文件自动生成物料清单

论文的核心贡献是提出了 **Subs-BOM（Substation Bill of Materials，变电站物料清单）** 的 **schema（模式/数据结构定义）**。

它有几个关键设计：

**1）基于 CycloneDX 规范**

论文的 Subs-BOM schema **建立在 CycloneDX 规范之上**。CycloneDX 是 IT 界主流的 SBOM 标准（由 OWASP 社区维护），已经被大量工具支持。**选择复用 IT 标准而不是自己造一个，是这篇论文最聪明的地方**——因为这意味着电力行业可以直接借用 IT 界成熟的工具链。

**2）能够建模数字变电站里的所有 IED 及其关系**

论文说 Subs-BOM **"capable of modeling all the IEDs in a DS and their relationships from a cybersecurity perspective"**——不只是列设备清单，还从**网络安全视角**建模设备之间的关系。这一点很重要：**光知道"有 30 台 IED"没用，你还得知道"哪台能连哪台"**，才能分析攻击的横向移动路径。

**3）以 IEC 61850 的 SCD 文件为主要信息来源**

这是最巧妙的一步。数字变电站的设计阶段本来就必须产出一份 **SCD（Substation Configuration Description，变电站配置描述）文件**——它是 IEC 61850 标准规定的，用 **SCL（Substation Configuration Language，变电站配置语言）** 写成，**里面本来就记录了站里有哪些 IED、它们提供什么逻辑节点、怎么通信**。

论文的做法是：**用 SCD 文件作为 Subs-BOM 的主要信息来源，自动生成物料清单。** 也就是说，**不需要额外做资产测绘——设计文件里已经有了，只是以前没人拿它做安全分析。**

**4）能同时管理多个数字变电站**

论文明确说 Subs-BOM **"enables managing multiple DS at the same time"**。这对电力公司很关键：**供应链风险的真正价值在于"跨站聚合"**——如果某厂商固件爆漏洞，你要能一次性查出所有受影响站点。

**摘要中没有给出的关键信息**（不要臆造）：
- Subs-BOM 的具体字段结构（除了"能建模 IED 及其关系"之外，摘要未展开）
- 一个实际变电站的规模（多少台 IED、多少种厂商，摘要未给出）
- SCD 到 Subs-BOM 的转换是自动工具还是手工流程（摘要未明确说明）
- 生成的 Subs-BOM 文件大小、转换耗时等（摘要未给出）

### 验证：用 OWASP Dependency-Track 做实测

论文的验证方式很实在：**用 OWASP 的 Dependency-Track 软件对 Subs-BOM schema 做了验证**。

验证结论有两条：

1. **"proved that the schema is correctly recognized by CycloneDX-compatible tools"**——schema 能被 CycloneDX 兼容的工具正确识别。这一条的意义是：**证明这个电力行业的 SBOM 没有偏离 IT 标准，可以复用整个 IT 生态的工具链**。
2. **"Dependency-Track software could track existing vulnerabilities in the IEDs represented by the Subs-BOM"**——Dependency-Track 能够**追踪 Subs-BOM 中所表示的 IED 里存在的漏洞**。

第二条是整篇论文的"决定性证据"：**它证明了这条链路是通的**——SCD 文件 → Subs-BOM → 自动查漏洞。这正是 SBOM 的价值所在。

### 结论：给电力公司一份准确完整的资产清单

论文总结 Subs-BOM 能提供什么：**"an accurate and complete inventory of the devices, the firmware they are running, and the services that are deployed into the DS"**——一份关于**设备、其运行的固件、以及部署在数字变电站中的服务**的准确且完整的清单。

## 关键公式（小白版）

这篇以数据建模与工具验证为主，没有需要展开的核心公式。它的技术路线是一条"标准复用"的链路：

```
IEC 61850 SCD 文件（设计阶段已有）
        ↓ 提取设备/服务/关系信息
   Subs-BOM（基于 CycloneDX schema）
        ↓ 输入
   OWASP Dependency-Track（IT 界现成工具）
        ↓ 输出
   每个 IED 的已知漏洞列表 → 跨变电站的供应链风险视图
```

**一句话概括**：不新增任何采集设备，只是把变电站设计阶段就存在的 SCD 文件"翻译"成 IT 界通用的 SBOM 格式，然后白嫖 IT 界成熟的漏洞管理工具。

## 用网安的话说（小电解读）

**Subs-BOM ≈ 给变电站做一次"资产测绘 + 依赖分析"，只不过数据源不是扫描器，而是设计文档。**

这篇论文的方法论对你来说**几乎是零学习成本**，因为它就是 IT 供应链安全的平移：

| IT 领域 | 数字变电站 | 论文的贡献 |
|---|---|---|
| 源码依赖（如 log4j 2.14.1） | IED 固件（厂商 + 版本） | 定义怎么在 CycloneDX 里表示 IED |
| package.json / pom.xml | **SCD 文件（SCL 语言）** | **用 SCD 作为 SBOM 的数据源（核心创新）** |
| CycloneDX 格式 | Subs-BOM schema | 扩展 CycloneDX 适配电力场景 |
| OWASP Dependency-Track | 同一个工具 | 验证可用性 |
| CVE 数据库 | 同一个 CVE 数据库 | 自动匹配 IED 固件漏洞 |

**几个关键洞察**：

1. **"SCD 文件就是变电站的 package.json"**——这个类比是整个论文的精髓。变电站设计时必须产出 SCD，**这份文件天生就是资产清单，只是过去只被当作配置下发文件用，没人拿它做安全分析**。这种"把已有数据源用于新目的"的思路，是**低投入高产出的典型**。

2. **供应链攻击的可怕之处在于"信任链"**。
   传统安全假设"边界内是可信的"。供应链攻击打破了这个假设——**你采购的合规设备本身可能就是攻击载荷**。而且它的**传播是自动的**：一次攻击，所有采购方中招。呼应 [[高级持续性威胁(APT)]] 的典型手法。

3. **攻击面在这里不是"网络"而是"流程"**。SBOM 解决的是**可见性（visibility）** 问题，这是零信任"永不信任、始终验证"的前提——**你无法保护你不知道存在的东西**。这正是 [[零信任架构]] 的第一条原则。

4. **论文的明显空白 = 你的机会**：
   - 它只做到"**列出漏洞**"，没做到"**分析哪些漏洞组合起来能被利用**"（攻击图/攻击路径分析）；
   - 它没做"**漏洞到物理后果的映射**"——某个 IED 的漏洞被利用，会导致哪个间隔失去保护？
   - 它没做"**供应链攻击的检测**"——如果有人往 Subs-BOM 里注入假条目怎么办？SBOM 本身的完整性如何保证？

**可迁移的选题（这个方向非常值得投入）**：

1. **基于 Subs-BOM 的攻击图自动生成**——把 IED 关系图 + 漏洞列表 + 网络拓扑合成一张"从攻击者入口到物理后果"的路径图；
2. **Subs-BOM 的完整性保护**——用签名/区块链防止清单被篡改（对接 [[区块链与能源交易]]）；
3. **跨站供应链风险聚合与优先级排序**——当一家厂商爆漏洞时，如何在几百个变电站里自动排出"最该先修的"；
4. **把 SBOM 思路扩展到其他电力资产**（如光伏逆变器、充电桩），做"能源行业 SBOM 体系"。

## 读完后你应该能回答

- [ ] 什么是 SBOM？它解决什么问题？
- [ ] 为什么数字变电站特别容易受供应链攻击？
- [ ] SCD 文件是什么？为什么它能作为 Subs-BOM 的数据源？
- [ ] Subs-BOM 为什么选择基于 CycloneDX 而不是自定义格式？
- [ ] 论文的验证实验证明了什么？没证明什么？

## 局限性

- **只做到"漏洞可见"，没做到"风险可评估"**：论文的验证结论止于"Dependency-Track 能追踪 IED 里的已知漏洞"。**但"有漏洞"不等于"可被利用"**——IED 是嵌入式设备，很多 CVE 在变电站的实际部署环境下未必可触发。论文未做可利用性分析。
- **依赖 CVE 数据库对 IED 固件的覆盖**：论文假设 Dependency-Track 能匹配到 IED 固件的漏洞。**但工业设备的固件版本命名往往不规范化，很多厂商漏洞不上 CVE**，这个匹配的召回率可能很低。摘要未给出匹配成功率。
- **SCD 文件的完整性未知**：SCD 是设计文件，**实际运行的变电站可能已经偏离设计**（现场改接线、临时替换设备、固件升级没回写）。如果 SCD 与实际情况不符，生成的 Subs-BOM 就是错的。摘要未讨论这个问题。
- **未涉及 Subs-BOM 自身的供应链问题**：如果生成 Subs-BOM 的工具链本身被污染，或者清单在传输中被篡改，怎么办？摘要未讨论。
- **摘要未给出任何规模数据**（多少台 IED、多少种厂商、多少漏洞），因此无法判断方法的可扩展性。

## 和你的方向有什么关系

- **这是 L10 里和你的网安背景最"无缝对接"的一篇**——你懂 SBOM、懂 CycloneDX、懂依赖分析，**几乎不需要补电力知识就能上手**。
- **直接选题（按推荐度排序）**：
  1. **从 Subs-BOM 到攻击图**：把资产清单升级成"可被利用的攻击路径图"，这是论文明确没做的下一步；
  2. **IED 固件版本识别与 CVE 匹配的鲁棒性研究**：解决"匹配不上"的现实问题，这是纯工程问题，适合发应用型论文；
  3. **供应链风险的跨站聚合与优先级排序算法**；
  4. **SBOM 在新能源资产（逆变器、充电桩）上的扩展**——对接 L9 的新能源方向。
- **和你实验室方向的对接**：**"AI与数据安全"**（供应链与依赖安全）、**"程序逆向"**（IED 固件逆向 → 提取真实组件清单，直接补上 SBOM 数据源的可信性问题，**这是一个很好的交叉点**）、**"入侵检测"**（供应链攻击的检测）。

## 概念关联

[[IEC 61850]] · [[IEC 62443]] · [[高级持续性威胁(APT)]] · [[零信任架构]]

## 原文摘要

> Smart grids have undergone a profound digitization process, integrating new data-driven control and supervision techniques, resulting in modern digital substations (DS). Attackers are more focused on attacking the supply chain of the DS, as they a comprise a multivendor environment. In this research work, we present the Substation Bill of Materials (Subs-BOM) schema, based on the CycloneDX specification, that is capable of modeling all the IEDs in a DS and their relationships from a cybersecurity perspective. The proposed Subs-BOM allows one to make informed decisions about cyber risks related to the supply chain, and enables managing multiple DS at the same time. This provides energy utilities with an accurate and complete inventory of the devices, the firmware they are running, and the services that are deployed into the DS. The Subs-BOM is generated using the Substation Configuration Description (SCD) file specified in the IEC 61850 standard as its main source of information. We validated the Subs-BOM schema against the Dependency-Track software by OWASP. This validation proved that the schema is correctly recognized by CycloneDX-compatible tools. Moreover, the Dependency-Track software could track existing vulnerabilities in the IEDs represented by the Subs-BOM.
