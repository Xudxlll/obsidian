---
type: 学习笔记
course: 大模型全栈
order: 26
stage: 检索增强
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/25-文本切片：固定、递归、结构与语义|25-文本切片：固定、递归、结构与语义]] · 下一篇：[[大模型全栈/27-FAISS：Flat、HNSW、IVF 与 PQ|27-FAISS：Flat、HNSW、IVF 与 PQ]]

> [!abstract] 学习目标
> 跑通一条最小链，并能分别检查检索与回答。

## 核心理解

RAG 先检索外部资料，再把资料与问题一起交给模型。离线阶段准备文档、切片与索引；在线阶段编码查询、召回片段、组织上下文并生成答案。

课堂最小例子用 Chroma 存文本，Embedding 生成向量，retriever 找相关内容，再通过 Prompt → LLM → Parser 形成回答。BM25 与向量检索对照展示的是两种召回方式，而不是两种不同语言模型。

检索返回正确证据，是回答可靠的重要前提，但还不是充分条件。模型可能忽略限制条件、混淆来源，或在证据不足时补写。提示词应说明引用边界与信息不足时的行为，调试时应同时查看命中的片段。

一个实用排错顺序是：库里有没有资料 → 是否召回 → 上下文是否被正确拼接 → 模型是否按证据回答。

## 课堂代码怎么读

先对照 BM25Retriever 与 Chroma retriever 的返回列表，再读最小 RAG 中 `debug_retrieve` 打印的真实片段。Passthrough 保留原问题，Lambda 把 Document 列表变成上下文。

> [!warning] 易错点与资料边界
> RAG 不会把知识永久写入模型权重。示例内存库与持久化库的生命周期不同；重复创建集合或更换 Embedding 后复用旧库，可能造成数据与空间不一致。

## 复盘练习

答案错了，应该立即换模型吗？

> [!question]- 参考思路
> 先分离检索错误与生成错误。没有召回正确资料时，应优先检查数据、切片、检索与查询；证据正确而回答错误时，再分析上下文和生成。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中057 %%

> [!quote]- 大模型全栈（中）.md · RAG检索
> 来源：原笔记第 3941–3977 行。
>
> **RAG检索**
>
> ```python
> """
> 检索方式
> """
> from langchain_chroma import Chroma
> from langchain_community.retrievers import BM25Retriever
> from langchain_huggingface import HuggingFaceEmbeddings
>
> # 准备文档
> documents = [
>     "订单退货流程：用户需在收到商品后7天内提交退货申请，客服审核后安排上门取件",
>     "退款政策：退货商品入库检验无误后，款项将在3-5个工作日内原路退回",
>     "电脑产品支持15天无理由退换货，需保留原包装和配件",
>     "计算机外设（鼠标、键盘）不支持无理由退货，质量问题除外",
>     "订单物流查询：可在订单详情页查看实时物流状态，或联系客服获取快递单号",
> ]
>
> # 1.精确匹配
> query = "如何退货?"
> res = [d for d in documents if query in d]
> print(f"命中:{len(res)}篇")
>
> # 2.BM25
> bm25_ret = BM25Retriever.from_texts(documents, k=2)
> bm25_res = bm25_ret.invoke(query)
> print(f"BM25命中: {len(bm25_res)}篇, {bm25_res}")
>
> # 3.向量
> embeddings = HuggingFaceEmbeddings(model_name="./bge-base-zh-v1.5")
> vec = Chroma.from_texts(documents, embeddings)
> vec_ret = vec.as_retriever(search_kwargs={"k": 3})
> vec_res = vec_ret.invoke(query)
> print(f"向量命中: {len(vec_res)}篇, {vec_res}")
> ```
>

%% source-id: 中056 %%

> [!quote]- 大模型全栈（中）.md · 简易RAG
> 来源：原笔记第 3867–3940 行。
>
> **简易RAG**
>
> ```python
> """
> 简易RAG实现
> """
> import os
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
> from langchain_core.prompts import ChatPromptTemplate
> from langchain_core.output_parsers import StrOutputParser
> from langchain_chroma import Chroma
> from langchain_huggingface import HuggingFaceEmbeddings
> from langchain_core.runnables import RunnablePassthrough, RunnableLambda
>
> load_dotenv()
>
> # 知识库文档
> documents = [
>     "RAG（检索增强生成）通过检索外部知识库来增强大语言模型的回答能力，减少幻觉。",
>     "RAG系统包括离线索引阶段（文档切片、向量化、存储）和在线查询阶段（检索、增强、生成）。",
>     "向量数据库用于存储高维嵌入向量，支持近似最近邻搜索，常见产品有Chroma、Pinecone、Weaviate。",
>     "LangChain是一个大语言模型应用开发框架，提供链式调用、工具集成和记忆管理等能力。",
> ]
>
> # 构建向量库
> embeddings = HuggingFaceEmbeddings(
>     model_name="./bge-base-zh-v1.5",
>     model_kwargs={"device": "cpu"},
>     encode_kwargs={"normalize_embeddings": True}
> )
> vec = Chroma.from_texts(documents, embeddings)
> retriever = vec.as_retriever(search_kwargs={"k": 2})
>
> # 构建Prompt模板
> prompt = ChatPromptTemplate.from_template("""
> 你是一个RAG专家,请根据以下参考资料回答问题,仅基于参考资料回答,资料中没有的信息,请说名无法回答
> 参考资料:
> {context}
> 用户问题:{question}
> """)
>
> # LLM
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
> )
>
> # 调试函数
> def debug_retrieve(docs):
>     for i, doc in enumerate(docs):
>         print(f" [{i + 1}] {doc.page_content}")
>
>     return docs
>
> debug_runnable = RunnableLambda(debug_retrieve)
> join_doc_runnable = RunnableLambda((lambda docs: "\n\n".join(d.page_content for d in docs)))
>
> # 构建RAG链
> rag_chain = (
>         {
>             "context": retriever | debug_runnable | join_doc_runnable,
>             "question": RunnablePassthrough(),
>         }
>         | prompt  # type: ignore
>         | llm | StrOutputParser()
> )
>
> # 输出
> answer = rag_chain.invoke("RAG包含哪两个阶段?")
> print(answer)
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/3.RAG简易实现.pdf#page=11|3.RAG简易实现.pdf · 第 11–27 页]]
