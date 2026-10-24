---
type: 学习笔记
course: 大模型全栈
order: 22
stage: 工作流
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/21-Runnable 协议：同步、异步与流式|21-Runnable 协议：同步、异步与流式]] · 下一篇：[[大模型全栈/23-Document 与多格式文档加载|23-Document 与多格式文档加载]]

> [!abstract] 学习目标
> 沿着每条边追踪数据，而不是只记住管道符。

## 核心理解

LCEL 用 `|` 表达组件的串联。最常见的链是 Prompt → Model → Parser：前一步的输出成为后一步输入，因此每个接口的类型与字段必须衔接。

RunnableParallel 将同一份输入交给多个分支，再返回以分支名为键的字典。课堂对一篇文章同时生成摘要、关键词和情感结果；另一份用两个等待任务直观展示并行耗时。

`RunnableLambda` 把普通函数包装成组件，`RunnablePassthrough` 保留原输入，适合把问题与检索上下文一起送到模板。分支与串行只是编排形式，结果正确仍取决于函数与输入契约。

阅读复杂链时，建议从右往左列出下游所需字段，再从左往右验证哪些组件提供这些字段。这样很容易发现 question 被误当成 context、列表未格式化等问题。

## 课堂代码怎么读

先画出摘要、关键词、情感三个分支的输入输出，再对照 `RunnableParallel` 的返回字典。等待示例中的总时间只说明独立任务能重叠等待，不能直接推断真实模型调用一定获得同样加速。

> [!warning] 易错点与资料边界
> 原标题把 LCEL 写成 LECL，属于文字误写。并行分支默认收到相同输入；若各分支需要不同字段，应显式选择或转换。

## 复盘练习

为什么检索器返回的 Document 列表通常还要格式化？

> [!question]- 参考思路
> 模板需要的是可读上下文。格式化可以保留文本、来源和编号，并明确每条证据的边界，避免直接依赖对象的默认字符串表示。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中060 %%

> [!quote]- 大模型全栈（中）.md · LECL
> 来源：原笔记第 4045–4111 行。
>
> **LECL**
>
> ```python
> """
> 声明式链式组合语言
> 并发
> """
> import os
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
> from langchain_core.prompts import ChatPromptTemplate
> from langchain_core.output_parsers import StrOutputParser
> from langchain_core.runnables import RunnableParallel
>
> load_dotenv()
>
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
> )
>
> parser = StrOutputParser()
>
> # 子链1:摘要
> summary_prompt = ChatPromptTemplate.from_messages([
>     ("system", "你是一个摘要专家,用一句话总结文章内容"),
>     ("user", "文章:{text}\n一句话摘要:")
> ])
>
> # 管道操作符
> summary_chain = summary_prompt | llm | parser
>
> # 子链2:关键词提取
> kw_prompt = ChatPromptTemplate.from_messages([
>     ("system", "你是一个关键词提取专家,从文章中提取3个关键词,用逗号分隔"),
>     ("user", "文章:{text}\n关键词:")
> ])
>
> # 管道操作符
> kw_chain = kw_prompt | llm | parser
>
> # 子链3:情感分析
> sentiment_prompt = ChatPromptTemplate.from_messages([
>     ("system", "你是一个情感专家,判断内容的情感倾向,正面/负面/中性"),
>     ("user", "文章:{text}\n情感分析:")
> ])
>
> # 管道操作符
> sentiment_chain = sentiment_prompt | llm | parser
>
> # 并发
> parallen_chain = RunnableParallel({
>     "summary":summary_chain,
>     "kw":kw_chain,
>     "sentiment":sentiment_chain
> })
>
> article = """
> 今天发布了新款AI芯片，性能提升3倍，功耗降低50%。
> 业界普遍认为这将推动人工智能产业的快速发展，
> 多家科技公司已经表示将采用这款新芯片。
> """
> res = parallen_chain.invoke({"text":article})
> print(res)
> ```
>

%% source-id: 中001 %%

> [!quote]- 大模型全栈（中）.md · Runnable并行
> 来源：原笔记第 2–24 行。
>
> **Runnable并行**
>
> ```python
> from langchain_core.runnables import RunnableParallel, RunnableLambda
> import time
>
> def taska(x):
>     time.sleep(2)
>     return f"a处理了{x}"
>
> def taskb(x):
>     time.sleep(2)
>     return f"b处理了{x}"
>
> parallel = RunnableParallel(a=RunnableLambda(taska), b=RunnableLambda(taskb))
>
> start = time.time()
> res = parallel.invoke("数据")
> end = time.time() - start
>
> print(res, f"耗时:{end}")
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/4.Runnable协议.pdf#page=1|4.Runnable协议.pdf · 第 1–25 页]]
- [[大模型全栈/资料/PDF/9.LCEL高阶.pdf#page=6|9.LCEL高阶.pdf · 第 6–18 页]]
- 关联知识：[[大模型全栈/21-Runnable 协议：同步、异步与流式|21-Runnable 协议：同步、异步与流式]]、[[大模型全栈/26-最小 RAG：检索、上下文与生成|26-最小 RAG：检索、上下文与生成]]、[[大模型全栈/49-LCEL 合同审查任务流|49-LCEL 合同审查任务流]]。
