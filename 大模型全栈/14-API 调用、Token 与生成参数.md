---
type: 学习笔记
course: 大模型全栈
order: 14
stage: 模型交互
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/13-推测解码：草稿、验证与接受率|13-推测解码：草稿、验证与接受率]] · 下一篇：[[大模型全栈/15-PromptTemplate 与消息角色|15-PromptTemplate 与消息角色]]

> [!abstract] 学习目标
> 把模型调用拆成服务地址、凭证、模型和消息四件事。

## 核心理解

一次模型请求包含服务地址、身份凭证、模型名和输入消息。SDK 把网络请求包装为对象接口，但模型是否存在、参数是否支持，仍由目标服务决定。兼容同一种接口风格，也不代表所有模型参数完全一致。

Token 是模型 tokenizer 的单位，不固定等于一个汉字或一个英文单词。课堂用 tiktoken 的指定编码器演示计数；其他模型必须按各自 tokenizer 或服务的计量规则处理。

最大生成长度是上限，不是必须写满的目标。上下文预算还要容纳系统消息、历史、检索内容与工具结果。若超限，应先明确截断或压缩策略，而不是只增大输出上限。

FM 指更宽泛的基础模型，LLM 是面向语言的一类；对话产品则还包含检索、工具、界面和权限等应用层。理解这层区别，才能解释为什么同一模型接入不同应用会有不同表现。

## 课堂代码怎么读

先看课堂的 FM/LLM 与应用关系，再跟踪 tiktoken 把字符串转成 token ID 的过程。后续封装类中的 temperature、top_p、max_tokens 都是本次请求配置，并不改变预训练权重。

> [!warning] 易错点与资料边界
> 课堂对大模型缺陷的某些表述较绝对，宜理解为可靠性问题的概括，而不是已经证明的能力定理。示例编码器不能用来精确计量全部 DeepSeek、Qwen 或 BERT 请求。

## 复盘练习

一次请求需要哪些内容才能重现输出？

> [!question]- 参考思路
> 至少记录模型与服务、完整消息、采样与长度配置、模型或接口版本；若含检索和工具，还需要保存当时的外部输入与返回结果。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

上篇保留了网页公共缩进与不间断空格，执行前需在练习副本中核对输入类型、缩进与依赖。

%% source-id: 上002 %%

> [!quote]- 大模型全栈（上）.md · Model 与 Input
> 来源：原笔记第 184–313 行。
>
>    Day 06 ： Model + Input
>
>    1. **FM、LLM 与 应用**
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/JATB2EZHACAAY?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkpBVEIyRVpIQUNBQVkiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NTI0LCJoZWlnaHQiOjI3Nn0)
>
>    1.FM 与 LLM的区别
>
>    **FM** 是“大家族”（所有基础大模型）
>
>    **LLM** 是“语言分支”（FM 里最强、最常用的那一支）
>
>    
>
>    2.FM/LLM 与 对话产品的区别
>
>    FM 和 LLM 解决的是“智能能力从哪里来”的问题，它们是底层的技术基座；
>
>    而对话产品解决的是“如何让普通人安全、方便地使用这些能力”的问题。
>
>    
>
>    3.大模型的缺点
>
>    **3.1 基础设施要求高，成本极高（训练与运行堪比“烧钱”）**
>
>    尽管大模型在各个领域取得了显著进展，但其训练和推理过程对计算资源和能源的需求极高。训练一个大模型需
>
>    要数百甚至上千台 GPU/TPU 服务器并消耗海量电力，导致大模型应用成本居高不下。虽然云计算服务提供了便利，
>
>    但如何在保证性能的同时降低计算和能源消耗，仍然是一个亟待解决的挑战。
>
>    
>
>    **3.2 数据饥渴：需要海量且高质量的数据，远远超出人类学习所需**
>
>    人类从有限、嘈杂的输入中提炼出语法、语义和世界知识；而大模型本质上是一个“数据黑洞”——它依赖
>
>    的语料规模比人类高出百万倍，但泛化能力和适应性却远不及人类。
>
>    
>
>    **3.3 语言理解的缺陷：从“字面接龙”到“表面懂、实质错”**
>
>    人类理解一个句子时，会调用**世界知识、逻辑推理、自我怀疑、对不确定性的感知**。而大模型本质上是一个**概率**
>
>    **生成器**——它只在训练数据的统计模式中工作。
>
>    缺陷1：不知道自己不知道（元认知缺失）
>
>    缺陷2：新知识“覆盖”旧知识：学习的“副作用”
>
>    缺陷3：“知识遮蔽”：主流知识掩盖小众细节
>
>    
>
>    大模型的“语言理解”本质是一种高级的模式匹配与概率生成。它在主流知识、标准化任务上表现出接近甚至超越
>
>    人类的水平，但在**不确定性判断、知识更新时的遗忘、长尾知识的可靠检索**三个维度上，仍存在系统性的、原理级的
>
>    缺陷。
>
>    这些缺陷不是“偶尔犯错”，而是由模型架构与训练范式决定的固有局限。认识这些局限，是正确使用大模型的前
>
>    提。
>
>    
>
>    4.大模型训练流程
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/46YCAEZHAAQEI?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IjQ2WUNBRVpIQUFRRUkiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTE5NSwiaGVpZ2h0Ijo0MzN9)
>
>    
>
>    5.Model
>
>    5.1 必填参数
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/ZDWCCEZHADQBG?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlpEV0NDRVpIQURRQkciLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTE0MCwiaGVpZ2h0IjoxOTB9)
>
>    5.2 核心参数
>
>    **核心参数1：最大生成长度**
>
>    5.2.1 理论知识
>
>    **能力界定：设定的是“天花板”，而非“保证值”**
>
>    该参数的作用是给出一个**硬性的上限**：无论模型多么“想”继续写下去，一旦生成的 token 数达到该阈值，生成过
>
>    程会立即截断并返回当前内容。
>
>    但需要注意：**实际返回的内容长度常常小于该上限**。max\_tokens 更像一个 **“安全阀”**：它防止模型无休止地生成导致资源耗尽，但不保证每次都能用完这个额度。
>
>    5.2.2 token数估算
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/TP4SKEZHADADW?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlRQNFNLRVpIQURBRFciLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6ODc3LCJoZWlnaHQiOjQxNX0)
>
>    5.2.3 代码
>
>    ```python
>    import tiktoken
>    # 选择编码器（GPT-4 / GPT-3.5-turbo 使用 cl100k_base）
>    enc = tiktoken.get_encoding("cl100k_base")
>    text = "大模型在日常对话中的表现已经相当成熟"
>    tokens = enc.encode(text)
>    print(len(tokens)) # 输出 token 数量
>    print(tokens) # 输出 token ID 列表（可选）
>    ```
>
>    
>
>    **核心参数2：温度**
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/NX4SOEZHADQFY?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6Ik5YNFNPRVpIQURRRlkiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6NzUzLCJoZWlnaHQiOjM4N30)
>
>    **核心参数3：核采样**
>
>    top\_p （又称核采样）用于动态决定模型每一步生成时考虑的候选词集合。它不固定候选词数量，而是根据概率
>
>    分布的集中程度自动调整。
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/PZTCQEZHACAFE?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IlBaVENRRVpIQUNBRkUiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTE1NCwiaGVpZ2h0IjoyOTV9)
>
>    与temperature 搭配使用
>
>    [原课堂图片外链（未能直接下载）](http://www.kdocs.cn/api/v3/office/copy/VUdXRHNRNjJyaUk5L0dJRUZ1OG5DNEpQaktEdjJUdlpaODVINlpmblIyYkVuNm13eW5UODNnMUxLTE51ZHBsQnV3djBuemcwOUxqNVJTellkZTRsUWJRTnNScG4waHo1d084MmlWNFRCd254bVNkWTYrNXQza2xnd2dKTzg5V3dYazFuVG9hTlZUVkxTQVdlN1FnMk1Ya0JaRmtkcmVWNUJoZlRXdXhTc0ZsUncyOVJQUktmenBDOCs4OWFUcG05WkFrb2Y4SkMxSTFxOWtIRkh1Z0VrVU94YWl0alluYmJGbm5jb25aeXRWbS9tTzF6THJBME9RTWVsbkg0U0EyMjhtU0xYbDhXL0tjPQ==/attach/object/FH7CQEZHADAEU?&kso_type=image&kso_extra=eyJ0eXBlIjoiaW1hZ2UiLCJpZCI6IkZIN0NRRVpIQURBRVUiLCJvd25lciI6IjUxNDg3NTkwNTM4MyIsInJvdGF0ZSI6MCwic3RvcmFnZSI6ImJhc2UiLCJ3aWR0aCI6MTE2MywiaGVpZ2h0Ijo1MTB9)
>
>    
>

## 资料与关联

- [[大模型全栈/资料/PDF/1.从调用API开始.pdf#page=1|1.从调用API开始.pdf · 第 1–10 页]]
- [[大模型全栈/资料/PDF/2.Model+I+O.pdf#page=1|2.Model+I+O.pdf · 第 1–9 页]]
- 关联知识：[[大模型全栈/10-GPT 自回归生成与采样策略|10-GPT 自回归生成与采样策略]]、[[大模型全栈/15-PromptTemplate 与消息角色|15-PromptTemplate 与消息角色]]、[[大模型全栈/17-多轮对话、历史消息与模型封装|17-多轮对话、历史消息与模型封装]]、[[大模型全栈/19-结构化输出与解析器|19-结构化输出与解析器]]。
