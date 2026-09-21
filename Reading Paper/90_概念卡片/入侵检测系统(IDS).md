---
type: "concept"
title: "入侵检测系统（IDS）"
aliases: ["IDS", "Intrusion Detection System", "入侵检测", "异常检测"]
tags: ["概念卡片", "L3-工控与电网安全", "网安迁移点"]
created: "2026-09-16"
updated: "2026-09-17"
---

# 入侵检测系统（IDS）

## 一句话

这是你**最熟悉的领域**，但要换个战场：从"IT 网络流量"搬到"工业控制网络的 OT 流量 + 电网物理量测"。

## 在电网/工控场景里，它长什么样

| 维度 | IT 的 IDS | 电网/ICS 的 IDS |
|---|---|---|
| 数据源 | 网络包、日志、系统调用 | **工业协议报文**（Modbus/DNP3/IEC 61850）+ **物理量测**（电压/电流/功率） |
| 正常基线 | 流量统计特征 | **物理规律**（功率平衡、基尔霍夫定律） |
| 攻击目标 | 数据窃取、提权 | **让物理过程失控** |
| 误报代价 | 打扰分析师 | **可能误切线路、误停机** → 代价极高 |
| 部署位置 | 网络边界 + 主机 | 现场层、控制层、监控层（多层级） |

## 三条技术路线（对应你熟悉的三代 IDS）

1. **基于规则/特征（Signature-based）**
   - 例：DNP3 报文里的异常功能码、非法地址范围
   - 优点：可解释、误报低；缺点：只能挡已知攻击

2. **基于异常/行为（Anomaly-based）**
   - 机器学习/深度学习：自编码器、LSTM、One-Class SVM
   - 例：[[虚假数据注入攻击(FDIA)]] 检测、[[状态估计]]残差异常
   - 优点：能发现未知攻击；缺点：误报高，且**自身可被[[对抗样本攻击]]**

3. **基于物理模型（Physics-based）**
   - 用物理约束做"不可能性检验"：比如功率不守恒 → 一定有异常
   - 这是电网 IDS 独有的优势：**有强物理先验可依赖**

**最新趋势**：把 2 和 3 融合 → 物理信息神经网络（PINN）、[[图神经网络]]（利用电网拓扑结构）。

## 关键公式

混淆矩阵（二分类）：

| | 预测为攻击 | 预测为正常 |
|---|---|---|
| **实际是攻击** | TP（真正例） | FN（漏报） |
| **实际是正常** | FP（误报） | TN（真负例） |

由这四个量导出的核心指标：

$$\mathrm{TPR} = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}, \qquad \mathrm{FPR} = \frac{\mathrm{FP}}{\mathrm{FP}+\mathrm{TN}}$$

$$\mathrm{Precision} = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}}, \qquad \mathrm{Recall} = \mathrm{TPR}$$

$$F_1 = \frac{2\cdot \mathrm{Precision}\cdot \mathrm{Recall}}{\mathrm{Precision}+\mathrm{Recall}}$$

- $\mathrm{TPR}$（召回率）：真实攻击中被检出的比例，越低说明**漏报**越多
- $\mathrm{FPR}$：正常样本被误判为攻击的比例，越低说明**误报**越少
- $\mathrm{Precision}$（精确率）：报出的告警里有多少是真的攻击
- $F_1$：精确率与召回率的调和平均，在类别极度不平衡时给出单一评价

白话：**检测器的好坏不能只看"检出了多少"，必须同时看"误报了多少"**。在电网里这一点尤其关键——误报的代价可能是误切线路、误停机，所以 FPR 常常比 TPR 更受关注。

## 用网安的话说（小电解读）

IDS 是你的主场。**你要学的不是检测算法，而是换了战场后哪些前提不成立了。**

- 工业 IDS ≈ **你的 IDS，但证据从"流量特征"扩到"流量特征 + 物理量测"**。传统 IDS 只有报文；电网 IDS 还能质问："这条报文和物理世界一致吗？"
- 电网 IDS ≈ **一个 FPR 比 TPR 更重要的检测系统**。IT 里误报顶多烦人，电网里一次误报可能误切线路。

### 相同点

1. **三代路线骨架一致**：特征匹配 → 异常检测 → 白盒模型，你熟的 Snort/Suricata、自编码器、One-Class SVM 都能搬（见[[电力系统异常检测]]、[[深度学习检测方法]]）。
2. **评估指标通用**：混淆矩阵、TPR/FPR、$F_1$ 两侧同一套语言。
3. **对抗性共通**：IDS 可被[[对抗样本攻击]]，训练集可被[[数据投毒攻击]]污染。

### 不同点 / 难点

1. **"正常"的定义变了：从统计基线变成物理定律**。IT 里正常是"上周的样子"，电网里判据是**功率守恒、基尔霍夫定律**。好处是**强先验可依赖、样本需求大降**；坏处是你得懂电网物理，否则连基线都写不出来。
2. **攻击目标变了：不是数据，是物理过程**。IT 攻击要窃密提权；电网攻击要让**物理过程失控**（见[[虚假数据注入攻击(FDIA)]]）。检测窗必须匹配物理时间尺度 —— 保护动作是毫秒级，攒 batch 就晚了。
3. **协议层没给抓手**。Modbus、GOOSE/SV 明文无认证，"纯流量异常检测"召回上限很低，须靠物理侧补。
4. **数据集是真正的瓶颈**：攻击样本稀缺、类不平衡、标注昂贵、跨系统不可迁移。

### 电网场景的特殊之处

1. **物理模型路线是独有优势**。用"不可能性检验"（功率不守恒即异常）不需要攻击样本，对未知攻击天然有效。
2. **多层部署看到的东西不同**：现场层报文、控制层、监控层（[[SCADA系统]]）视角各异，跨层联动检测仍有空间。
3. **趋势是物理与 AI 融合**：物理信息神经网络、[[图神经网络]]（吃拓扑）是当下热点。

切入建议：**从批判性题目入手最划算** —— [[20_Research/Papers/L3-工控与电网安全/A_False_Sense_of_Security_Revisiting_the_State_of_Machine_Learning-Based_Industrial_Intrusion_Detection|027 机器学习工控入侵检测的虚假安全感]]指出大量论文实验设置不严谨、检测率被高估。你可以做"在严格时序划分、跨系统泛化下重新评测工业 IDS 方法"，或做"物理约束 + 时序模型的混合检测器并测量 FPR 代价"。测试床稀缺是真障碍，可先靠公开数据起步，但须诚实说明泛化性问题。

## 相关论文

- [[20_Research/Papers/L3-工控与电网安全/A_False_Sense_of_Security_Revisiting_the_State_of_Machine_Learning-Based_Industrial_Intrusion_Detection|026 机器学习工控入侵检测的"虚假安全感"（必读）]]
- [[20_Research/Papers/L3-工控与电网安全/A_Survey_of_Machine_Learning_Methods_for_Detecting_False_Data_Injection_Attacks|022 FDIA 检测的机器学习方法综述]]
- [[20_Research/Papers/L3-工控与电网安全/A_Survey_on_Industrial_Control_System_Testbeds_and_Datasets_for_Security_Research|020 ICS 测试床与数据集综述]]
- [[20_Research/Papers/L4-AI与电网安全/Adversarial_Attacks_on_Time-Series_Intrusion_Detection_for_Industrial_Control_Systems|031 针对时序入侵检测的对抗攻击]]
- [[20_Research/Papers/L4-AI与电网安全/Safe_Reinforcement_Learning_for_Power_System_Control_A_Review|032 安全强化学习用于电力系统控制综述]]

## 相关概念

[[SCADA系统]] · [[虚假数据注入攻击(FDIA)]] · [[工控安全测试床与数据集]] · [[对抗样本攻击]] · [[图神经网络]]
