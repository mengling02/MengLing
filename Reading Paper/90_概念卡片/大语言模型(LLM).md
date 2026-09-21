---
type: "concept"
title: "大语言模型（LLM）"
aliases: ["LLM", "Large Language Model", "大模型", "智能体", "Agent"]
tags: ["概念卡片", "L5-前沿-LLM与智能体", "前沿"]
created: "2026-09-16"
updated: "2026-09-17"
---

# 大语言模型（LLM）在电网中

## 一句话

把 LLM 当作**电网的"自然语言接口 + 推理引擎"**：让它读调度规程、看告警日志、解释故障、辅助决策 —— 甚至让它扮演攻击者去测试电网安全。

## 四类应用（按成熟度排序）

| 方向 | 做什么 | 代表工作 |
|---|---|---|
| **故障诊断与解释** | 输入告警/量测，输出故障原因（可解释） | [[20_Research/Papers/L5-前沿-LLM与智能体/Fault_Diagnosis_in_Power_Grids_with_Large_Language_Model\|035]] |
| **调度辅助** | 理解调度员自然语言指令，生成调度方案 | [[20_Research/Papers/L5-前沿-LLM与智能体/GAIA_A_Large_Language_Model_for_Advanced_Power_Dispatch\|036]] |
| **安全异常检测** | 多模态（时序+文本）分析 EMS 告警 | [[20_Research/Papers/L5-前沿-LLM与智能体/Large_Language_Models_for_Power_System_Security_A_Novel_Multi-Modal_Approach\|038]] |
| **攻防能力评测** | 评测 LLM 能否发现/利用电网漏洞 | [[20_Research/Papers/L5-前沿-LLM与智能体/CritBench_A_Framework_for_Evaluating_Cybersecurity_Capabilities_of_Large_Language_Models\|037]] |

## 关键挑战（也是选题机会）

1. **幻觉（Hallucination）**：电网里编造一个数字 = 事故。所以必须**物理约束校验 + RAG（检索增强）**。
2. **数值能力弱**：LLM 算不好[[潮流计算]]。主流方案是 **LLM 做编排，专业求解器做计算**（Tool-use / Agent 架构）。
3. **时序数据**：电网数据是连续时序，LLM 不擅长 → 需要与时序模型（LSTM/Transformer）结合。
4. **安全对齐**：**LLM 本身会被攻击**（提示注入、越狱），且它可能成为攻击者的助力（自动生成攻击策略）。
5. **实时性**：调度要求毫秒级，LLM 推理太慢 → 只能用于"人类在环"的辅助场景。

## 关键公式

Transformer 的核心——缩放点积注意力：

$$\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^{\mathsf T}}{\sqrt{d_k}}\right)V$$

- $Q, K, V$：查询（Query）、键（Key）、值（Value）矩阵，由输入表示经线性变换得到
- $d_k$：键向量的维度；除以 $\sqrt{d_k}$ 是为了防止内积过大导致 softmax 进入饱和区、梯度消失
- $\mathrm{softmax}(\cdot)$：按行归一化成注意力权重，即"每个位置该关注其他哪些位置"

白话：**每个 token 用 $Q$ 去和所有 token 的 $K$ 做相似度匹配，得到一组权重，再按权重把它们的 $V$ 加权求和**——这就是上下文建模的全部机制，也解释了它为什么擅长处理长文本、却不擅长精确数值计算。

自回归生成的目标（最大似然）：

$$\mathcal{L}(\theta) = -\sum_{t=1}^{T} \log p_{\theta}\!\left(w_t \mid w_1, \dots, w_{t-1}\right)$$

- $w_t$：第 $t$ 个 token；$T$：序列长度
- $p_{\theta}(\cdot)$：模型在给定前文时对下一个 token 的预测概率
- 训练目标即最小化该负对数似然，等价于最大化"预测下一个词"的准确度

白话：**LLM 本质上就是一个"猜下一个词"的概率模型**，所以它的输出是"最像话的续写"而不是"算得最准的结果"——这既解释了幻觉的根源，也解释了为什么电网里必须给它配物理约束校验与专业求解器调用。

## 用网安的话说（小电解读）

LLM 在电网里最要紧的不是"它多强"，而是**它同时改变了攻防两边**：

- **≈ 一个会说话的 SOC 分析师**。它读日志、串联告警、给人话解释 —— 相当于把 SIEM 里的关联分析和报告撰写交给它。
- **≈ 一个会读规程的渗透测试员**。攻击者侧的同构映射：读文档、查配置、生成利用链。

### 相同点

1. **提示注入、越狱、数据泄露这套攻击面完全一致**。你在 Web/Agent 里玩的注入技巧，原封不动就能用在电网运维助手上，只是后果更重。
2. **评测方法论可以复刻**。CritBench 这类"给模型一套安全任务看能否完成"的框架，本质就是能力基准测试。
3. **幻觉 ≈ 格式正确但没有依据的一句话**。你对"误报"的要求，在这里要再严格一个数量级。

### 不同点 / 难点

1. **编一个数字就是事故**。电网里它可能报出不存在的线路编号。必须叠加物理一致性校验，或者让它只做编排、计算交给专业求解器。
2. **知识有版本**。规程会改、拓扑会变，权重里没有时效信息，RAG 检索到的也可能过期 —— **跟老漏洞库的问题同源**。这也让 [[后门攻击]] 在电网 LLM 上更隐蔽：投毒进的是知识库，而不是权重。

### 电网场景的特殊之处

1. **规程文本是天然的知识库**，运维有大量成文文档，恰好适合 RAG。
2. **多模态是真需求**。告警是文本、量测是时序、接线图是图像，单模态吃不下，见 [[20_Research/Papers/L5-前沿-LLM与智能体/Large_Language_Models_for_Power_System_Security_A_Novel_Multi-Modal_Approach|036 LLM 用于电力系统安全：多模态异常检测]]。
3. **可以拿它当攻击者用**，自动化侦察与攻击构造 —— 跟你想做的 [[提示注入]] 是同一枚硬币的两面。

### 切入建议

这个方向**综述多、扎实工作少、评测基准刚起步**，对研一是难得的时间窗口。最可行的切入点是**做电网领域的 LLM 安全评测基准**：构造运维助手场景，测它对 [[提示注入]]、越狱、信息泄漏的抵抗力，并对比与通用模型的差异。好处是**不需要你懂电力系统深层原理**，却能吃到你实验室"工业 AI 与安全"的方向红利。风险自陈：基准类工作容易被认为贡献偏浅，最好再叠一个防御机制。

## 相关论文

- [[20_Research/Papers/L5-前沿-LLM与智能体/Fault_Diagnosis_in_Power_Grids_with_Large_Language_Model|034 LLM 用于电网故障诊断]]
- [[20_Research/Papers/L5-前沿-LLM与智能体/GAIA_A_Large_Language_Model_for_Advanced_Power_Dispatch|035 GAIA：面向高级调度的 LLM]]
- [[20_Research/Papers/L5-前沿-LLM与智能体/Large_Language_Models_for_Power_System_Security_A_Novel_Multi-Modal_Approach|036 LLM 用于电力系统安全：多模态异常检测]]
- [[20_Research/Papers/L5-前沿-LLM与智能体/CritBench_A_Framework_for_Evaluating_Cybersecurity_Capabilities_of_Large_Language_Models|037 CritBench：LLM 网络安全能力评测]]

## 相关概念

[[强化学习]] · [[入侵检测系统(IDS)]] · [[虚假数据注入攻击(FDIA)]] · [[IEC 61850]]
