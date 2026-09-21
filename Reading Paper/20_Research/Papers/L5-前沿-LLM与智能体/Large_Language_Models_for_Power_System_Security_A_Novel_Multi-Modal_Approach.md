---
document_id: "arxiv-2508.10044"
arxiv_id: "2508.10044"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2508.10044"
title: "Large Language Models for Power System Security: A Novel Multi-Modal Approach for Anomaly Detection in Energy Management Systems"
zh_title: "大语言模型用于电力系统安全：面向能量管理系统异常检测的新型多模态方法"
authors: ["Aydin Zaboli", "Junho Hong", "Alexandru Stefanov", "Chen-Ching Liu", "Chul-Sang Hwang"]
published: "2025-08-12"
venue: "IEEE Access 2025（已接收）；arXiv:2508.10044"
domain: "L5-前沿-LLM与智能体"
level: "L5"
reading_order: 36
difficulty: "入门+"
tags: ["论文笔记", "L5-前沿-LLM与智能体", "大语言模型", "多模态", "异常检测", "EMS"]
quality_score: 9
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 036 | 大语言模型用于电力系统安全：面向 EMS 异常检测的多模态方法

> [!abstract] 一句话
> **首次把生成式 AI 异常检测系统用于 EMS**：提出覆盖整条 SCADA 数据流的"多点攻击/错误模型"，并用**多模态（数值 + 视觉 + 规则）**方法检测 —— 包括传统数值方法**根本发现不了**的 HMI 界面篡改。

## 为什么这是 L5 里"最贴你方向"的一篇

理由：
1. **它做的是"安全检测"**，不是"应用" —— 与你的网安背景直接对口
2. **多模态** —— 对接你实验室的"多模态大模型"方向
3. **攻击模型很系统**：覆盖 SCADA 数据流全链路
4. **最新**（2025-08），代表当前前沿

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Large Language Models for Power System Security: A Novel Multi-Modal Approach for Anomaly Detection in Energy Management Systems |
| **作者** | Aydin Zaboli, Junho Hong, Alexandru Stefanov, Chen-Ching Liu, Chul-Sang Hwang（密歇根大学迪尔伯恩分校、弗吉尼亚理工、都柏林大学等） |
| **发表** | IEEE Access 2025（已接收） |
| **发布** | 2025-08-12（10 图，6 表） |
| **链接** | [arXiv](https://arxiv.org/abs/2508.10044) \| [PDF](https://arxiv.org/pdf/2508.10044) |

> **小电注**：**Chen-Ching Liu** 是电力系统保护与控制领域的国际知名学者（IEEE Fellow），这篇论文的学术分量值得重视。

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2508.10044_fig1.jpeg]]

![[2508.10044_fig2.jpeg]]

![[2508.10044_fig3.jpeg]]

![[2508.10044_fig4.jpeg]]

![[2508.10044_fig5.jpeg]]

![[2508.10044_fig6.jpeg]]

---


## 这篇论文在讲什么（白话版）

### 贡献一：覆盖整条数据流的"多点攻击/错误模型"

> 原文：*"A comprehensive multi-point attack/error model is initially proposed to systematically identify vulnerabilities throughout the entire EMS data processing pipeline, including post state estimation (SE) stealth attacks, EMS database manipulation, and human-machine interface (HMI) display corruption according to the real-time database (RTDB) storage."*

**这是本文最有价值的部分** —— 它把 EMS 的攻击面**按数据处理流程拆开了**：

```
传感器量测
  ↓
状态估计（SE）
  ↓  ← 攻击点①：SE 之后的隐蔽攻击（post-SE stealth attacks）
实时数据库（RTDB）
  ↓  ← 攻击点②：数据库篡改（EMS database manipulation）
人机界面（HMI）
  ↓  ← 攻击点③：界面显示篡改（HMI display corruption）
调度员看到的信息
```

**关键洞察**：
> **攻击者不一定非要攻击状态估计（那是研究最多的）**。
> **他可以攻击"状态估计之后"的环节** —— 数据库、HMI 显示。
> **这些环节的研究少得多，但同样能欺骗调度员！**

**"post-SE stealth attack"** 这个概念很重要：
- 状态估计本身没问题（残差正常）
- 但**估计结果被篡改**（在写入数据库时）
- 或**显示被篡改**（HMI 显示假数据，而数据库是真的）
- → **传统基于残差的检测完全失效**（因为攻击发生在 SE 之后！）

> **这是对 [[虚假数据注入攻击(FDIA)]] 研究的一个重要拓展**：
> 大家都在研究"怎么骗过状态估计"，但**"骗过调度员的眼睛"有更简单的路径**。

### 贡献二：生成式 AI 异常检测系统（ADS）

> 原文：*"generative AI (GenAI)-based anomaly detection systems (ADSs) for EMSs are proposed for the first time in the power system domain to handle the scenarios."*

**首次**把生成式 AI 异常检测系统用于 EMS。

### 贡献三：SoM-GI 多模态框架（核心创新）

> 原文：*"a set-of-mark generative intelligence (SoM-GI) framework, which leverages multimodal analysis by integrating visual markers with rules considering the GenAI capabilities, is suggested to overcome inherent spatial reasoning limitations."*

**Set-of-Mark（SoM）** 是一种让多模态模型"看懂图像"的技术：
- 在图像上**标注编号标记**（如把 HMI 界面的每个区域标上 1、2、3…）
- 让模型**引用这些编号**来定位和描述
- **解决了大模型"空间推理能力弱"的问题**

> **原文强调**：*"The SoM-GI methodology employs systematic visual indicators to enable accurate interpretation of segmented HMI displays and detect visual anomalies that numerical methods fail to identify."*

**"检测数值方法无法发现的视觉异常"** —— 这是本文的核心卖点。

**举个直观的例子**：
- 数据库里电压值 = 1.02 pu（正常）
- HMI 界面显示 = 0.98 pu（被篡改）
- **纯数值检测**：检查数据库 → 一切正常 → **检测不到**
- **多模态检测**：截图 HMI → 视觉分析 → 发现显示与数据库不一致 → **检测到**

### 验证

> 原文：*"Validation on the IEEE 14-Bus system shows the framework's effectiveness across scenarios, while visual analysis identifies inconsistencies."*

**在 IEEE 14 节点系统上验证**，视觉分析能识别不一致。

## 用网安的话说（小电解读）

> 这篇论文给你**两个非常重要的启发**。

**启发一：攻击面的"向下游扩展"**

> 传统 FDIA 研究盯着"状态估计"这一个点。
> 但真实的攻击链是**整条数据流**：
> ```
> 传感器 → 通信 → SE → 数据库 → 可视化 → 人
>         ↑         ↑      ↑        ↑
>       都可以攻击！
> ```

**这和你熟悉的"攻击链"思维完全一致**：
- 不一定要攻破最难的环节
- **找链条上最薄弱的一环**（HMI 显示？数据库？）
- **效果可能更好**（调度员直接看到假信息）

> **"post-SE attack"这个概念的启发**：
> 安全研究常常"盯着一个环节"，但**攻击者会选最省力的路径**。
> → **"全链路威胁建模"** 是更现实的做法。

**启发二：多模态是电网安全的"新武器"**

> 为什么多模态在电网安全里特别有用？

因为**电网信息本身就是多模态的**：
| 模态 | 内容 | 传统方法 |
|---|---|---|
| **数值** | 电压、电流、功率 | 状态估计、残差检测 |
| **文本** | 告警日志、调度规程 | 关键字匹配 |
| **视觉** | HMI 界面、曲线图、拓扑图 | **几乎没有自动检测！** |
| **时序** | 连续量测序列 | 时序异常检测 |
| **拓扑** | 电网结构图 | 图分析 |

> **"视觉模态"在电网安全里几乎是空白** —— 而调度员恰恰主要**靠看图**做决策！
> → **"面向 HMI 视觉篡改的检测"** 是一个极其新颖的方向。

**对你的直接价值**：
- 你实验室有**"多模态大模型"**方向 → 这篇论文给你一个**电力场景的多模态安全应用**
- 你实验室有**"图像识别与安全"**方向 → HMI 界面篡改检测 = **图像异常检测**！

> **小电的判断**：**"HMI/可视化界面的篡改检测"** 可能是这篇文章留给你最大的机会。
> 理由：
> 1. 攻击可行（改显示比改数据容易）
> 2. 后果严重（调度员被直接欺骗）
> 3. 传统方法完全无效（数值都是对的）
> 4. 你实验室有图像方向的技术储备
> 5. 文献极少

## 读完后你应该能回答

- [ ] EMS 数据流有哪些环节可以被攻击？
- [ ] 什么是"post-SE stealth attack"？为什么它难以检测？
- [ ] Set-of-Mark（SoM）技术解决什么问题？
- [ ] 为什么 HMI 界面篡改用数值方法检测不到？
- [ ] 多模态方法在电网安全中还有哪些应用可能？

## 局限性

- **验证规模有限**（IEEE 14 节点），未验证大规模 EMS。
- 依赖**多模态大模型**（推理慢、成本高）→ 与 EMS 实时性要求存在张力。
- SoM-GI 的**鲁棒性未充分评估**（如果攻击者也对图像做对抗扰动呢？）。
- **未讨论 LLM 自身的攻击面**（提示注入、幻觉）。
- 数据集可能是合成的（HMI 截图如何生成？真实性存疑）。
- 论文较新，**同行评价还不充分**。

## 和你的方向有什么关系

- **这是 L5 里与你实验室方向重合度最高的一篇**：多模态 + 安全 + 电力。
- **直接选题（按推荐度）**：
  1. **HMI/可视化界面的篡改检测**（新颖，对接"图像识别与安全"）
  2. **全链路威胁建模**（扩展 post-SE 攻击的概念）
  3. **多模态 EMS 检测的对抗鲁棒性**（对图像做对抗扰动）
  4. **轻量化多模态检测**（解决实时性问题）
- **技术储备**：多模态大模型、视觉异常检测、Set-of-Mark 技术。
- 与实验室方向对接：**"多模态大模型"**（核心）、**"图像识别与安全"**（HMI 视觉检测）、**"工业AI与智能体"**、**"入侵检测"**。

> [!tip] 小电的选题建议
> **"面向电力调度 HMI 的界面篡改检测"**
> - **问题新颖**：几乎没人做
> - **方法可迁移**：图像异常检测 + 多模态模型
> - **有数据可造**：可以自己搭一个 HMI 模拟界面，生成篡改样本
> - **对接实验室方向**：图像识别与安全 + 工业AI
> - **实用价值**：真实电网的 HMI 确实是攻击目标（乌克兰事件中就涉及 HMI 操作）
>
> 这个选题的**最大优点**是：**不需要昂贵的电网测试床**，一台机器 + 开源 HMI 软件（如 ScadaBR、OpenPLC 的 HMI）就能做实验。

## 概念关联

- 核心概念：[[大语言模型(LLM)]] · [[入侵检测系统(IDS)]] · [[虚假数据注入攻击(FDIA)]] · [[状态估计]] · [[SCADA系统]] · [[对抗样本攻击]]
- 前置阅读：[[20_Research/Papers/L5-前沿-LLM与智能体/Fault_Diagnosis_in_Power_Grids_with_Large_Language_Model|034 LLM 故障诊断]] · [[20_Research/Papers/L5-前沿-LLM与智能体/GAIA_A_Large_Language_Model_for_Advanced_Power_Dispatch|035 GAIA]]
- 攻击分类：[[20_Research/Papers/L3-工控与电网安全/A_Taxonomy_of_Data_Attacks_in_Power_Systems|023 电力系统数据攻击分类学]]
- 安全总纲：[[20_Research/Papers/L3-工控与电网安全/A_Comprehensive_Survey_on_the_Security_of_Smart_Grid|016 智能电网安全综合综述]]（点名 LLM 为未来方向）
- 能力评测：[[20_Research/Papers/L5-前沿-LLM与智能体/CritBench_A_Framework_for_Evaluating_Cybersecurity_Capabilities_of_Large_Language_Models|037 CritBench：LLM 网络安全能力评测]]

## 原文摘要

> This paper elaborates on an extensive security framework specifically designed for energy management systems (EMSs), which effectively tackles the dynamic environment of cybersecurity vulnerabilities and/or system problems (SPs), accomplished through the incorporation of novel methodologies. A comprehensive multi-point attack/error model is initially proposed to systematically identify vulnerabilities throughout the entire EMS data processing pipeline, including post state estimation (SE) stealth attacks, EMS database manipulation, and human-machine interface (HMI) display corruption according to the real-time database (RTDB) storage. This framework acknowledges the interconnected nature of modern attack vectors, which utilize various phases of supervisory control and data acquisition (SCADA) data flow. Then, generative AI (GenAI)-based anomaly detection systems (ADSs) for EMSs are proposed for the first time in the power system domain to handle the scenarios. Further, a set-of-mark generative intelligence (SoM-GI) framework, which leverages multimodal analysis by integrating visual markers with rules considering the GenAI capabilities, is suggested to overcome inherent spatial reasoning limitations. The SoM-GI methodology employs systematic visual indicators to enable accurate interpretation of segmented HMI displays and detect visual anomalies that numerical methods fail to identify. Validation on the IEEE 14-Bus system shows the framework's effectiveness across scenarios, while visual analysis identifies inconsistencies. This integrated approach combines numerical analysis with visual pattern recognition and linguistic rules to protect against cyber threats and system errors.
