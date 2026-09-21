---
document_id: "arxiv-2308.03478"
arxiv_id: "2308.03478"
source_type: "arxiv"
source_url: "https://arxiv.org/abs/2308.03478"
title: "Network Security in the Industrial Control System: A Survey"
zh_title: "工业控制系统的网络安全：综述"
authors: ["Yang Li", "Shihao Wu", "Quan Pan"]
published: "2023-08-07"
venue: "arXiv (cs.CR)"
domain: "L3-工控与电网安全"
level: "L3"
reading_order: 19
difficulty: "入门"
tags: ["论文笔记", "L3-工控与电网安全", "ICS", "协议安全", "纵深防御"]
quality_score: 8
created: "2026-09-16"
updated: "2026-09-17"
status: "analyzed"
lang: "en"
---
# 019 | 工业控制系统的网络安全：综述

> [!abstract] 一句话
> 以**工业协议**为起点，用**纵深防御（Defence in Depth）**为框架，系统梳理 ICS 网络安全：数据加密、访问控制、入侵检测、软件定义网络。

## 为什么读它

这篇的独特价值在于**两条主线**：

1. **协议线**：把 ICS 常用协议（Modbus、DNP3、IEC 61850、OPC 等）的安全缺陷讲清楚
2. **防御线**：用"纵深防御"框架组织，让你知道**每一层该放什么**

而且它给了你一个很好的**"协议-漏洞"对应表**，这是做协议层检测的基础。

## 核心信息

| 项目 | 内容 |
|---|---|
| **标题** | Network Security in the Industrial Control System: A Survey |
| **作者** | Yang Li, Shihao Wu, Quan Pan（西北工业大学） |
| **发布** | 2023-08-07（作者注：该工作三年前完成） |
| **分类** | cs.CR |
| **链接** | [arXiv](https://arxiv.org/abs/2308.03478) \| [PDF](https://arxiv.org/pdf/2308.03478) |

> [!warning] 注意
> 作者明确说明"该工作三年前完成"（约 2020 年），所以内容**不包含 2020 年后的进展**。但基础性的协议分析和纵深防御框架仍然有效。

## 论文原图

> 下面是从论文原文提取的关键图表。**先看图、再看字**——图是论文作者花了最多心思表达的地方。

![[2308.03478_fig1.png]]

![[2308.03478_fig2.png]]

![[2308.03478_fig3.jpeg]]

![[2308.03478_fig4.jpg]]

![[2308.03478_fig5.png]]

![[2308.03478_fig6.png]]

---


## 这篇论文在讲什么（白话版）

### 出发点：协议种类多 = 漏洞多

> 原文：*"in practical usage, there are many types of protocols, which means a high vulnerability in protocols."*

**工业现场用的协议五花八门**（因为设备来自不同厂商、不同年代），而**每种协议都有自己的安全缺陷**。

**常见工业协议及其安全缺陷**：

| 协议 | 用途 | 安全缺陷 |
|---|---|---|
| **Modbus**（RTU/TCP） | 最通用的工业协议 | **无认证、无加密、无完整性校验**；功能码可被滥用 |
| **DNP3** | 电力/水务 SCADA | 早期版本无认证；支持"未经请求的响应"（可被滥用） |
| **IEC 61850**（MMS/GOOSE/SV） | 变电站自动化 | GOOSE/SV 二层广播，**无认证无加密**，可伪造跳闸 |
| **OPC / OPC UA** | 工业数据交换 | 老版 OPC（DA）依赖 DCOM，难穿越防火墙；OPC UA 较安全但部署少 |
| **Profinet / EtherNet-IP** | 工厂自动化 | 实时性优先，安全机制弱 |
| **IEC 60870-5-101/104** | 电力远动 | 无认证，可被伪造 |

**共同特征**：**为可靠性、实时性设计，安全是事后补的（甚至没补）**。

### 防御框架：纵深防御（Defence in Depth, DiD）

论文用 DiD 组织防御技术：

| 层次 | 技术 | 说明 |
|---|---|---|
| **数据加密** | TLS、IPsec、专有加密 | 挑战：会引入延迟，实时控制可能不接受 |
| **访问控制** | 白名单、RBAC、网络分段 | 挑战：工控设备往往不支持细粒度权限 |
| **入侵检测系统（IDS）** | 协议异常、流量异常、物理异常 | 挑战：无标注数据、误报代价高 |
| **软件定义网络（SDN）** | 集中控制、动态策略 | 挑战：单点失效、性能开销 |
| 其他 | 安全网关、单向隔离装置 | 中国的"横向隔离装置"就属此类 |

## 用网安的话说（小电解读）

> 这篇论文最实用的部分，是**"协议-漏洞-检测方法"的对应关系**。

**给你的实战表格**（综合论文内容 + 公开知识）：

| 协议 | 典型攻击 | 可检测的特征 |
|---|---|---|
| Modbus | 非法功能码、越界地址、异常写入频率 | 功能码白名单、地址范围、时序规律 |
| DNP3 | 伪造未经请求响应、重放 | 时序分析、序列号校验 |
| GOOSE | 伪造跳闸报文 | 报文频率、内容一致性、发布者身份 |
| SV | 伪造采样值 | 采样值物理一致性（基尔霍夫定律） |

**"纵深防御"和你的关系**：
- 你熟悉的企业安全也是 DiD（边界防火墙 → 内网分段 → 主机 EDR → 数据加密）
- **OT 的 DiD 不同之处**：**最内层不是"数据"，而是"物理过程"**
- 所以 OT 的最后一层防线是**物理约束校验**（如：功率守恒、电压范围）

**这个洞察很重要**：
> **在 OT 安全里，物理规律是你最后的、也是最可靠的防线。**
> 因为攻击者可以伪造数据、可以绕过协议校验，但**很难伪造物理一致性**。
> → 这就是"物理信息融合检测"（PINN、物理约束 ML）的理论基础。

**注意 SDN 部分**：
- SDN 被当作"解决 ICS 安全的方案"，但它本身也有安全问题（控制器是单点）
- **"SDN 控制器的安全"** 是一个相对新颖的方向

## 读完后你应该能回答

- [ ] 列举 4 种常见工业协议，并说出各自的安全缺陷
- [ ] 为什么工业协议普遍"不安全"？
- [ ] 纵深防御（DiD）在 ICS 中的层次划分是什么？
- [ ] 为什么说"物理规律是 OT 安全的最后防线"？
- [ ] 在 ICS 里加加密会带来什么问题？

## 局限性

- **内容约截止 2020 年**（作者自述），不包含最新进展。
- 偏**技术罗列**，缺乏定量对比（哪种检测方法在什么场景下更优）。
- 对"物理层安全"的讨论较浅。
- 未涉及 [[大语言模型(LLM)]]、联邦学习等新方法。

## 和你的方向有什么关系

- **协议层是你的"基本功"**：做 OT 入侵检测，必须先懂协议。
- **直接选题**：
  1. **某个具体协议的异常检测**（如 GOOSE 异常检测 —— 已有工作但仍有空间）
  2. **跨协议的统一检测框架**（多协议环境下的统一异常建模）
  3. **SDN 在 ICS 中的安全性与性能权衡**
- **动手建议**：用 Wireshark 抓一次 Modbus/DNP3 流量（可用开源测试床生成），亲手看看报文结构。**看一遍胜过读十篇**。

## 概念关联

- 核心概念：[[SCADA系统]] · [[IEC 61850]] · [[入侵检测系统(IDS)]] · [[工控安全测试床与数据集]] · [[电力监控系统安全防护体系]]
- 前置阅读：[[20_Research/Papers/L3-工控与电网安全/Architecture_and_Security_of_SCADA_Systems_A_Review|018 SCADA 系统架构与安全综述]]
- 后续阅读：[[20_Research/Papers/L3-工控与电网安全/SoK_Security_of_Programmable_Logic_Controllers|027 SoK：PLC 安全]] · [[20_Research/Papers/L3-工控与电网安全/A_False_Sense_of_Security_Revisiting_the_State_of_Machine_Learning-Based_Industrial_Intrusion_Detection|026 机器学习工控入侵检测的"虚假安全感"]]
- 物理防线：[[20_Research/Papers/L3-工控与电网安全/A_Taxonomy_of_Data_Attacks_in_Power_Systems|023 电力系统数据攻击分类学]]

## 原文摘要

> Along with the development of intelligent manufacturing, especially with the high connectivity of the industrial control system (ICS), the network security of ICS becomes more important. And in recent years, there has been much research on the security of the ICS network. However, in practical usage, there are many types of protocols, which means a high vulnerability in protocols. Therefore, in this paper, we give a complete review of the protocols that are usually used in ICS. Then, we give a comprehensive review on network security in terms of Defence in Depth (DiD), including data encryption, access control policy, intrusion detection system, software-defined network, etc. Through these works, we try to provide a new perspective on the exciting new developments in this field.
