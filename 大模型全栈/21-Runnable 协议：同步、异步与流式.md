---
type: 学习笔记
course: 大模型全栈
order: 21
stage: 工作流
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/20-订单客服：信息抽取与业务查询|20-订单客服：信息抽取与业务查询]] · 下一篇：[[大模型全栈/22-LCEL：串行、并行与数据流|22-LCEL：串行、并行与数据流]]

> [!abstract] 学习目标
> 用统一接口调用不同 AI 组件。

## 核心理解

Runnable 是可执行组件的统一接口。Prompt、模型、解析器、检索器与包装后的函数可以使用相近的调用方式，从而组合成更大的链。

`invoke` 处理一个输入，`batch` 处理多个输入，`stream` 持续返回输出片段；对应异步形式为 `ainvoke`、`abatch`、`astream`。异步表达的是等待方式，并不保证模型本身更快。

流式通常改善首个内容到达的体验，完整答案仍需等待后续片段。若下游需要完整 JSON，应考虑何时累积、何时解析，不能把一个尚未结束的片段当成完整对象。

并发要控制数量：`max_concurrency` 限制同时进行的任务，但远程限流、重试与本地资源也会影响总耗时。比较性能时应明确测量首字延迟还是整段完成时间。

## 课堂代码怎么读

课堂同一大代码块中重复了若干导入和 demo 定义，建议按六种调用方法逐个读，而不是一次执行全部。异步主函数中再检查 `asyncio.gather` 如何组合多个流。

> [!warning] 易错点与资料边界
> 把重复代码一口气当作单一模块运行，后定义可能覆盖前定义。在已有事件循环的环境中，启动方式也与普通脚本不同；本轮保留原始教学片段。

## 复盘练习

batch 和 RunnableParallel 是同一件事吗？

> [!question]- 参考思路
> batch 通常让同一组件处理多个输入；RunnableParallel 则把同一个输入分发给多个命名分支，并把各分支输出组合起来。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 中061 %%

> [!quote]- 大模型全栈（中）.md · RUNNABLE
> 来源：原笔记第 4112–4291 行。
>
> **RUNNABLE**
>
> ```python
> """
> runnable--
> """
> import os
> import time
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
> import asyncio
>
> load_dotenv()
>
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
> )
> """
> runnable
> """
> import os
> import time
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
> import asyncio
>
> load_dotenv()
>
> llm = ChatOpenAI(
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     model="deepseek-chat",
> )
>
> questions = [
>     "用50个字介绍RAG",
>     "用50个字介绍深度学习",
>     "用50个字介绍机器学习",
>     "用50个字介绍NLP",
> ]
>
> # 同步,单次执行
> def demo_invoke():
>     result = llm.invoke("请用一句话介绍RAG")
>     print(result.content, "\n")
>
> # 同步,流式执行
> def demo_stream():
>     for chunk in llm.stream("请介绍RAG原理"):
>         print(chunk.content, end="")
>
>     print()
>
> # 同步,批量执行
> def demo_batch():
>     t0 = time.time()
>     results = llm.batch(questions, config={"max_concurrency": 5})
>     print(f"总耗时:{time.time() - t0:.2f}秒")
>     for i, r in enumerate(results):
>         print(f"  [{i + 1} {r.content}]")
>
> # 异步,单次执行
> async def demo_ainvoke():
>     result = await llm.ainvoke("请用一句话介绍RAG")
>     print(result.content, "\n")
>
> # 异步,流式执行
> async def demo_astream():
>     async for chunk in llm.astream("请介绍RAG原理"):
>         print(chunk.content, end="")
>
>     print()
>
> # 异步,批量执行(内部已并发)
> async def demo_abatch():
>     t0 = time.time()
>     results = await llm.abatch(questions, config={"max_concurrency": 5})
>     print(f"总耗时:{time.time() - t0:.2f}秒")
>     for i, r in enumerate(results):
>         print(f"  [{i + 1} {r.content}]")
>
> async def demo_concurrent_stream():
>     start = time.time()
>
>     async def stream_one(idx, q):
>         async for chunk in llm.astream(q):
>             print(f"[流{idx + 1}:]{chunk.content}", end='')
>
>         print(f"\n[流{idx + 1}] 完成 @ {time.time() - start:.2f}秒")
>
>     tasks = [stream_one(i, q) for i, q in enumerate(questions)]
>     await asyncio.gather(*tasks)
>
> async def main():
>     # demo_invoke()
>     # demo_stream()
>     # demo_batch()
>
>     # await demo_ainvoke()
>     # await demo_astream()
>     # await demo_abatch()
>
>     await demo_concurrent_stream()
>
> asyncio.run(main())
> questions = [
>     "用50个字介绍RAG",
>     "用50个字介绍深度学习",
>     "用50个字介绍机器学习",
>     "用50个字介绍NLP",
> ]
>
> # 同步,单次执行
> def demo_invoke():
>     result = llm.invoke("请用一句话介绍RAG")
>     print(result.content, "\n")
>
> # 同步,流式执行
> def demo_stream():
>     for chunk in llm.stream("请介绍RAG原理"):
>         print(chunk.content, end="")
>
>     print()
>
> # 同步,批量执行
> def demo_batch():
>     t0 = time.time()
>     results = llm.batch(questions, config={"max_concurrency": 5})
>     print(f"总耗时:{time.time() - t0:.2f}秒")
>     for i, r in enumerate(results):
>         print(f"  [{i + 1} {r.content}]")
>
> # 异步,单次执行
> async def demo_ainvoke():
>     result = await llm.ainvoke("请用一句话介绍RAG")
>     print(result.content, "\n")
>
> # 异步,流式执行
> async def demo_astream():
>     async for chunk in llm.astream("请介绍RAG原理"):
>         print(chunk.content, end="")
>
>     print()
>
> # 异步,批量执行(内部已并发)
> async def demo_abatch():
>     t0 = time.time()
>     results = await llm.abatch(questions, config={"max_concurrency": 5})
>     print(f"总耗时:{time.time() - t0:.2f}秒")
>     for i, r in enumerate(results):
>         print(f"  [{i + 1} {r.content}]")
>
> async def demo_concurrent_stream():
>     start = time.time()
>
>     async def stream_one(idx, q):
>         async for chunk in llm.astream(q):
>             print(f"[流{idx + 1}:]{chunk.content}", end='')
>
>         print(f"\n[流{idx + 1}] 完成 @ {time.time() - start:.2f}秒")
>
>     tasks = [stream_one(i, q) for i, q in enumerate(questions)]
>     await asyncio.gather(*tasks)
>
> async def main():
>     # demo_invoke()
>     # demo_stream()
>     # demo_batch()
>
>     # await demo_ainvoke()
>     # await demo_astream()
>     # await demo_abatch()
>
>     await demo_concurrent_stream()
>
> asyncio.run(main())
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/4.Runnable协议.pdf#page=1|4.Runnable协议.pdf · 第 1–25 页]]
- [[大模型全栈/资料/PDF/9.LCEL高阶.pdf#page=1|9.LCEL高阶.pdf · 第 1–6 页]]
