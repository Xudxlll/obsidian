---
type: 学习笔记
course: 大模型全栈
order: 32
stage: 检索增强
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/31-论文 RAG：从朴素检索到 Advanced RAG|31-论文 RAG：从朴素检索到 Advanced RAG]] · 下一篇：[[大模型全栈/33-测试集构建与 RAGAS 评估流水线|33-测试集构建与 RAGAS 评估流水线]]

> [!abstract] 学习目标
> 把有没有找到证据，与有没有正确使用证据分开评估。

## 核心理解

检索指标需要固定相关性标注。Precision@K 是前 K 条中相关文档的比例；Recall@K 是全部相关文档中被前 K 条找回的比例。MRR 关注第一条相关结果的位置，NDCG 还考虑分级相关性与位置折扣。

$$
P@K=\frac{|R\cap S_K|}{K},\qquad
R@K=\frac{|R\cap S_K|}{|R|}
$$

生成端则检查回答是否基于上下文、是否回应问题。Faithfulness 关注陈述是否得到给定上下文支持；Answer Relevancy 关注是否切题。RAGAS 的 Context Recall 与 Context Precision 使用评价流程衡量上下文，不能直接当作人工 qrels 上同名检索指标。

忠实不等于事实一定正确：若知识库本身有错，模型忠实复述仍可能错误。多 Agent 还需增加任务完成、协作成本、工具成功与异常恢复等系统指标。

所有分数都应同时记录样本数、数据来源、评判模型和配置。

## 课堂代码怎么读

课堂分别给出 faithfulness、answer_relevancy 与 context_recall 的最小数据集，并用 LangchainLLMWrapper 等适配评判模型；另附 VertexAI 导入报错的历史补丁。先对齐 question、answer、contexts、ground_truth 各字段，再读评价调用。

> [!warning] 易错点与资料边界
> 原 VertexAI 补丁直接改包内部文件，且原片段有缩进与上下文缺失，不能直接当成通用修复。检索指标 ZIP 未附源码；本篇公式是概念补充，不是对该 ZIP 的复原。

## 复盘练习

若三条相关文档中找回两条，返回五条，P@5 与 R@5 是多少？

> [!question]- 参考思路
> P@5=2/5，R@5=2/3。前者惩罚返回的噪声，后者衡量遗漏了多少已知相关证据。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

上篇保留了网页公共缩进与不间断空格，执行前需在练习副本中核对输入类型、缩进与依赖。

%% source-id: 上011 %%

> [!quote]- 大模型全栈（上）.md · 评估指标分类
> 来源：原笔记第 755–769 行。
>
>
>    
>
>    RAG 里面 ：两套指标
>
>    Agent里面：两套指标
>
>    第一套： 检索相关指标：Recall@K，Precision@K，MRR，NDCG  只在RAG里体现
>
>    第二套： 生成相关指标：忠诚度（faithfulness），相关度（relevance），结构清晰度，专业性，可读性。  RAG和AGENT都使用，只要涉及到生成内容，都可以使用
>
>    第三套： MultiAgent系统指标 ： 任务完成率，协调效率，鲁棒性，可拓展性，整体质量
>
>    
>

%% source-id: 中030 %%

> [!quote]- 大模型全栈（中）.md · 检索端指标
> 来源：原笔记第 2345–2348 行。
>
> **检索端指标**
>
> 检索端指标.zip
>

%% source-id: 中029 %%

> [!quote]- 大模型全栈（中）.md · 忠诚度
> 来源：原笔记第 2296–2344 行。
>
> **忠诚度**
>
> ```python
> """
> 忠诚度
> """
> from datasets import Dataset
> from ragas import evaluate
> from ragas.metrics import faithfulness
> from ragas.llms import LangchainLLMWrapper
> from langchain_openai import ChatOpenAI
> import os
> from dotenv import load_dotenv
>
> load_dotenv()
>
> eval_data = Dataset.from_dict({
>     "question": [
>         "RAG系统的核心步骤是什么？",
>         "向量数据库的作用是什么？",
>     ],
>     "answer": [
>         "RAG系统的核心步骤是检索、增强和生成。首先检索相关文档，然后增强Prompt，最后生成回答。",
>         "向量数据库用于存储高维向量，并支持快速的相似度检索。",
>     ],
>     "contexts": [
>         [
>             "检索增强生成（RAG）包括两个核心阶段：检索阶段从知识库中检索相关文档，生成阶段将检索结果融入Prompt后由LLM生成回答。"],
>         ["向量数据库是专门用于存储和检索高维向量的数据库，支持近似最近邻（ANN）搜索。"],
>     ],
> })
>
> eval_llm = LangchainLLMWrapper(
>     ChatOpenAI(
>         api_key=os.getenv("DEEPSEEK_API_KEY"),
>         base_url=os.getenv("DEEPSEEK_BASE_URL"),
>         model="deepseek-chat",
>         temperature=0
>     ),
>     bypass_n=True
> )
>
> res = evaluate(eval_data, metrics=[faithfulness], llm=eval_llm)
> print(res)
>
> df = res.to_pandas()
> print(df)
> ```
>

%% source-id: 中028 %%

> [!quote]- 大模型全栈（中）.md · 答案相关性
> 来源：原笔记第 2242–2295 行。
>
> **答案相关性**
>
> ```python
> """
> 答案相关性
> """
> from datasets import Dataset
> from ragas import evaluate
> from ragas.metrics import answer_relevancy
> from ragas.llms import LangchainLLMWrapper
> from langchain_openai import ChatOpenAI
> from langchain_huggingface import HuggingFaceEmbeddings
> import os
> from dotenv import load_dotenv
>
> load_dotenv()
>
> eval_data = Dataset.from_dict({
>     "question": [
>         "如何提高RAG系统的检索准确率？",
>         "什么是向量数据库？",
>     ],
>     "answer": [
>         "可以通过使用混合检索（BM25+向量）、增加重排序模块、优化chunk_size等方法提高检索准确率。",
>         "今天天气很好，适合出去散步。",
>     ],
>     "contexts": [
>         ["混合检索结合了BM25和向量检索的优势，重排序可以进一步提升Top-K精度。"],
>         ["向量数据库用于存储高维向量。"],
>     ],
> })
>
> judge_llm = LangchainLLMWrapper(
>     ChatOpenAI(
>         model="deepseek-chat",
>         api_key=os.getenv("DEEPSEEK_API_KEY"),
>         base_url=os.getenv("DEEPSEEK_BASE_URL"),
>         temperature=0,
>     ),
>     bypass_n=True,
> )
>
> eval_emb = HuggingFaceEmbeddings(
>     model_name="./bge-base-zh-v1.5",
>     model_kwargs={"device": "cpu"},
> )
>
> res = evaluate(eval_data, metrics=[answer_relevancy], llm=judge_llm,embeddings=eval_emb)
> print(res)
>
> df = res.to_pandas()
> print(df)
> ```
>

%% source-id: 中026 %%

> [!quote]- 大模型全栈（中）.md · 上下文召回率
> 来源：原笔记第 2167–2214 行。
>
> **上下文召回率**
>
> ```python
> """
> 上下文召回率
> """
> from datasets import Dataset
> from ragas import evaluate
> from ragas.metrics import context_recall
> from ragas.llms import LangchainLLMWrapper
> from langchain_openai import ChatOpenAI
> import os
> from dotenv import load_dotenv
>
> load_dotenv()
>
> eval_data = Dataset.from_dict({
>     "question": ["RAG的优势是什么？"],
>     "answer": ["RAG可以减少幻觉，提供可追溯的来源。"],
>     "contexts": [
>         ["RAG通过检索外部知识来增强LLM回答，有效减少幻觉问题。"]
>     ],
>     "reference": [
>         "RAG可以减少LLM幻觉。RAG可以提供可追溯的信息来源。RAG可以实时更新知识库。"
>     ],
> })
>
> eval_llm = LangchainLLMWrapper(
>     ChatOpenAI(
>         model="deepseek-chat",
>         api_key=os.getenv("DEEPSEEK_API_KEY"),
>         base_url=os.getenv("DEEPSEEK_BASE_URL"),
>         temperature=0,
>     ),
>     bypass_n=True,
> )
>
> result = evaluate(eval_data, metrics=[context_recall], llm=eval_llm, raise_exceptions=True)
> print(result)
> print(result.to_pandas())
>
> score = result["context_recall"]
> if isinstance(score, list):
>     valid = [s for s in score if s == s]
>     score = sum(valid) / len(valid) if valid else float("nan")
> print(f"Context Recall = {score:.4f}")
> ```
>

%% source-id: 中027 %%

> [!quote]- 大模型全栈（中）.md · 如果VertexAI相关错误了
> 来源：原笔记第 2215–2241 行。
>
> **如果VertexAI相关错误了**
>
> ```python
> # ragas包的llms文件夹下的base.py 大概在12行左右
> try:
>     from langchain_community.chat_models.vertexai import ChatVertexAI
>     from langchain_community.llms.vertexai import VertexAI
> except ImportError:
>     # LangChain 1.x 已移除 vertexai 集成，用空类兜底避免 isinstance 报错
>     class _DummyVertex: pass
>     ChatVertexAI = _DummyVertex
>     VertexAI = _DummyVertex
>     
>     
>    # 大概在52行左右  is_multiple_completion_supported 函数
>    def is_multiple_completion_supported(llm: BaseLanguageModel) -> bool:
>     """Return whether the given LLM supports n-completion."""
>     # DeepSeek 等 OpenAI 兼容端点不支持 n>1 多 completion
>     model_name = getattr(llm, "model_name", None) or getattr(llm, "model", None)
>     if model_name and "deepseek" in str(model_name).lower():
>         return False
>     for llm_type in MULTIPLE_COMPLETION_SUPPORTED:
>         if isinstance(llm, llm_type):
>             return True
>     return False
> ```
>

## 资料与关联

- 本篇主要依据上述课堂代码补充讲解；相关讲义统一见 [[大模型全栈/资料/00-资料索引|资料索引]]。
- 关联知识：[[大模型全栈/33-测试集构建与 RAGAS 评估流水线|33-测试集构建与 RAGAS 评估流水线]]、[[大模型全栈/34-RAG 超参数搜索与评估偏差|34-RAG 超参数搜索与评估偏差]]、[[大模型全栈/35-论文系统：检索与生成的联合评测|35-论文系统：检索与生成的联合评测]]、[[大模型全栈/61-训练监控、LoRA 对照与困惑度|61-训练监控、LoRA 对照与困惑度]]。
