---
document_id: "arxiv-2001.02925"
arxiv_id: "2001.02925"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2001.02925"
title: "Architecture and Security of SCADA Systems: A Review"
zh_title: "SCADA 系统的架构与安全：综述"
authors: ["Geeta Yadav", "Kolin Paul"]
published: "2020-01-09"
venue: "arXiv (cs.CR)"
domain: "L3-工控与电网安全"
level: "L3"
reading_order: 18
difficulty: "入门"
tags: ["论文笔记", "L3-工控与电网安全", "SCADA", "工控安全", "综述"]
quality_score: 9
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 018 | SCADA 系统的架构与安全：综述

> [!abstract] 一句话
> 从"SCADA 架构怎么演进"讲到"每一代架构带来了什么新攻击面"，再讲到"入侵检测怎么用""测试床怎么搭"，最后点出待解决的关键研究问题。

## 为什么读它

这是**理解 SCADA 的最佳英文综述**：

- **架构演进讲得很清楚**：从孤立的单体系统 → 分布式 → 网络化 → **物联网/云化**
- **每一代架构 = 一组新漏洞** → 这条线索非常有助于你建立"攻击面扩张史"的直觉
- 论文开头那个"事故清单"很有冲击力（管道爆裂、产线停机、核反应堆停机、ICU 断氧……）

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Architecture and Security of SCADA Systems: A Review |
| **作者** | Geeta Yadav, Kolin Paul（印度理工学院德里分校） |
| **发布** | 2020-01-09 |
| **分类** | cs.CR |
| **链接** | [arXiv](https://arxiv.org/abs/2001.02925) \| [PDF](https://arxiv.org/pdf/2001.02925) |

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2001.02925_fig1.png]]

![[2001.02925_fig2.png]]

![[2001.02925_fig3.png]]

![[2001.02925_fig4.png]]

![[2001.02925_fig5.png]]

![[2001.02925_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 开篇：SCADA 出错的后果

> 原文列举：*"Pipeline bursting, production lines shut down, frenzy traffic, trains confrontation, nuclear reactor shut down, disrupted electric supply, interrupted oxygen supply in ICU"*

**管道爆裂、产线停机、交通瘫痪、列车对撞、核反应堆停机、供电中断、ICU 断氧**

> **小电点评**：这七个后果里，有四个直接关系人命。这就是 OT 安全和 IT 安全的根本区别 —— **不是"数据丢了"，是"人会死"**。

### SCADA 的架构演进（核心线索）

> 原文：*"Modern SCADA systems have evolved from standalone systems into sophisticated complex, open systems, connected to the Internet."*

| 代际 | 架构 | 特点 | 新增攻击面 |
|---|---|---|---|
| **第一代（1970s）** | **单体式（Monolithic）** | 一台大型机 + 专有硬件，完全孤立 | 几乎无网络攻击面（但物理接触即可攻击） |
| **第二代（1980s-90s）** | **分布式（Distributed）** | 局域网内多台设备，信息共享 | 局域网嗅探、ARP 欺骗 |
| **第三代（2000s）** | **网络化（Networked）** | 使用开放协议（TCP/IP）、标准硬件、可连接企业网 | **互联网攻击、协议漏洞、IT→OT 横向移动** |
| **第四代（现在）** | **IoT/云化（IoT & Cloud）** | 云平台、无线、海量传感器 | **云侧攻击、无线劫持、供应链、API 漏洞** |

**关键洞察**：
> **每一代 SCADA 都"更开放、更高效"，但也"更脆弱"。**
> 这个 trade-off 是 OT 安全的核心矛盾。

### 论文的四个内容板块

1. **SCADA 架构综述** —— 已提出/已实现的架构
2. **针对 SCADA 的攻击** —— 理解并突出"演进中的安全需求"
3. **入侵检测技术现状** —— SCADA 场景下的 IDS 简析
4. **测试床研究** —— SCADA 测试床的简要调研

另外还专门分析了 **基于云和 IoT 的 SCADA 架构**（现代架构分析）。

### 结尾：关键研究问题

论文最后点出"需要解决的关键研究问题"，以"弥合 SCADA 安全缺口"。

## 用网安的话说（小电解读）

> 这篇论文和你的知识背景**契合度最高**，因为它讲的就是"OT 版的网络安全"。

**对照表：IT 安全 vs SCADA 安全**

| 维度 | IT 安全 | SCADA 安全 |
|---|---|---|
| **首要目标** | 机密性 | **可用性** |
| **协议** | HTTPS、TLS、认证完善 | **Modbus/DNP3/IEC 61850：明文、无认证** |
| **设备寿命** | 3-5 年 | **15-25 年** |
| **打补丁** | 常规操作 | **停机成本极高，常常不能打** |
| **实时性** | 尽力而为 | **硬实时（毫秒级）** |
| **检测手段** | EDR、NDR、SIEM | **受限（不能装 agent）** |
| **测试环境** | 虚拟机随便搞 | **需要测试床（贵、难搭）** |

**四个关键约束（记住这个，能解释 SCADA 安全的所有难点）**：

1. **不能停机** → 补丁难打、扫描难做
2. **不能加延迟** → 加密/认证难加（会拖慢实时控制）
3. **不能装 agent** → 主机级检测难做（只能网络侧）
4. **不能随便试** → 测试必须在仿真环境

**→ 这四条约束，定义了 SCADA 安全研究的"可行解空间"。你的方案如果不满足这四条，就是纸上谈兵。**

**关于"入侵检测"的部分**（对你最重要）：
- SCADA IDS 的困难：**没有攻击样本**、**类别不平衡**、**误报代价高**
- 主要路线：基于协议（白名单/规则）、基于流量统计、基于物理模型
- 详见 [[入侵检测系统(IDS)]]

## 读完后你应该能回答

- [ ] SCADA 的四代架构分别是什么？每代新增了什么攻击面？
- [ ] 为什么 SCADA 系统"不能随便打补丁"？
- [ ] SCADA 场景下做入侵检测有哪些特殊困难？
- [ ] 为什么 SCADA 测试床是必需的？

## 局限性

- **2020 年的综述**，未覆盖此后 AI/LLM 在 SCADA 安全中的应用。
- 偏**架构与威胁**层面，具体检测算法细节较少。
- 印度作者视角，案例多来自国际公开事件。
- 对"云化 SCADA"的分析仍偏概念，工程细节有限。

## 和你的方向有什么关系

- **这是你做 OT 安全研究的"基础设施知识"**：不理解 SCADA 架构，你写的检测算法就不知道部署在哪一层。
- **直接选题**：
  1. **SCADA 协议异常检测**（Modbus/DNP3/IEC 61850）
  2. **无 agent 场景下的网络侧检测**（约束下的创新）
  3. **云化 SCADA 的新攻击面**（相对新颖）
- **必做动作**：读完后去了解 [[工控安全测试床与数据集]] 里的开源测试床（如 `ICSSIM`、`EPICTWIN`），选一个跑起来。

## 概念关联

- 核心概念：[[SCADA系统]] · [[入侵检测系统(IDS)]] · [[工控安全测试床与数据集]] · [[IEC 61850]] · [[电力监控系统安全防护体系]]
- 前置阅读：[[20_Research/Papers/L1-零基础起步/乌克兰电网攻击事件复盘|007 乌克兰电网攻击事件复盘]]（看攻击怎么落到 SCADA 上）
- 后续阅读：[[20_Research/Papers/L3-工控与电网安全/Network_Security_in_the_Industrial_Control_System_A_Survey|019 ICS 网络安全综述]] · [[20_Research/Papers/L3-工控与电网安全/SoK_Security_of_Programmable_Logic_Controllers|027 SoK：PLC 安全]]
- 数据集：[[20_Research/Papers/L3-工控与电网安全/A_Survey_on_Industrial_Control_System_Testbeds_and_Datasets_for_Security_Research|020 ICS 测试床与数据集综述]]

## 原文摘要

> Pipeline bursting, production lines shut down, frenzy traffic, trains confrontation, nuclear reactor shut down, disrupted electric supply, interrupted oxygen supply in ICU - these catastrophic events could result because of an erroneous SCADA system/ Industrial Control System(ICS). SCADA systems have become an essential part of automated control and monitoring of many of the Critical Infrastructures (CI). Modern SCADA systems have evolved from standalone systems into sophisticated complex, open systems, connected to the Internet. This geographically distributed modern SCADA system is vulnerable to threats and cyber attacks. In this paper, we first review the SCADA system architectures that have been proposed/implemented followed by attacks on such systems to understand and highlight the evolving security needs for SCADA systems. A short investigation of the current state of intrusion detection techniques in SCADA systems is done, followed by a brief study of testbeds for SCADA systems. The cloud and Internet of things (IoT) based SCADA systems are studied by analysing the architecture of modern SCADA systems. This review paper ends by highlighting the critical research problems that need to be resolved to close the gaps in the security of SCADA systems.
