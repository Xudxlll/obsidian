---
type: 学习笔记
course: 大模型全栈
order: 50
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/49-LCEL 合同审查任务流|49-LCEL 合同审查任务流]] · 下一篇：[[大模型全栈/51-人工介入、Checkpoint 与时间旅行|51-人工介入、Checkpoint 与时间旅行]]

> [!abstract] 学习目标
> 用显式状态图表达可分支、可回环的业务。

## 核心理解

LangGraph 用 State 保存共享数据，Node 接收状态并返回更新，Edge 决定后续节点，条件边根据状态选择路径。普通链顺次执行，图则可以表达回环与多条出口。

课堂分支例子先识别风险，再选择深度或快速审查；循环例子根据回答是否缺资料再次检索，直到信息足够或达到上限。

循环设计需要明确进度：每轮增加了什么证据、改变了哪个查询、是否只是在重复同样调用。仅有最大轮数可以防止无限运行，却不能保证每一轮都有价值。

状态字段也需要清晰含义。missing_info 表示还缺什么，answer 表示当前产物，两者的更新与清空要一致，否则旧状态可能触发错误分支。

## 课堂代码怎么读

先画节点与边，再检查每个函数返回哪些字段。分支例子观察风险解析，循环例子观察轮数递增、缺失信息提取与终止条件；最后对照 compile 与 invoke 的职责。

> [!warning] 易错点与资料边界
> 从模型文本中直接搜索“高风险”等词可能受否定或解释文字影响；结构化路由结果更容易校验。课堂合同判断仅说明分支机制。

## 复盘练习

循环多次仍查不到证据时应怎样结束？

> [!question]- 参考思路
> 保留已查范围与缺失项，返回明确的不确定状态，而不是达到轮数上限后自动把模型猜测当作完整答案。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下037 %%

> [!quote]- 大模型全栈（下）.md · 分支模式
> 来源：原笔记第 2956–3036 行。
>
> **分支模式**
>
> ```python
> """
> 分支模式
> 评估风险->高(深度审查)  --> 结束
>       ->低(快速审查)   -↑
> """
> import os
> from dotenv import load_dotenv
> from typing import TypedDict
> from langgraph.graph import StateGraph, END
> from langchain_openai import ChatOpenAI
> from langchain_core.messages import SystemMessage, HumanMessage
>
> load_dotenv()
>
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     temperature=0.1
> )
>
> # 定义状态
> class S(TypedDict):
>     clause: str
>     risk_level: str
>     review_result: str
>
> # 1.风险评估函数
> def assess(state):
>     res = llm.invoke(
>         [
>             SystemMessage(content="判断一下合同条款的风险等级,只回复 '高','低'或者''"),
>             HumanMessage(content=state['clause'])
>         ]
>     )
>     level = "高" if "高" in res.content else "低"
>     print(f"[风险评估] {level} 风险")
>     return {"risk_level": level}
>
> # 分支
> route = lambda s: "deep" if s["risk_level"] == "高" else "quick"
>
> # 2a.深度审查
> def deep_review(state):
>     res = llm.invoke([
>         SystemMessage(content="你是一个法律专家,对高风险条款给出详细凤险分析和修改建议:"),
>         HumanMessage(content=state["clause"])
>     ])
>     return {"review_result": f"[深度审查] {res.content}"}
>
> # 2b.快速审查
> def quick_review(state):
>     return {"review_result": "[快速审查] 条款风险较低,常规审阅后可签署"}
>
> # 组装图
> g = StateGraph(S)
> g.set_entry_point("assess")  # 入口
> g.add_node("assess", assess)
> g.add_conditional_edges(
>     "assess", route,
>     {"deep": "deep_review", "quick": "quick_review"}
> )
> g.add_node("deep_review", deep_review)
> g.add_edge("deep_review", END)
> g.add_node("quick_review", quick_review)
> g.add_edge("quick_review", END)
>
> # 执行
> app = g.compile()
>
> for clause in [
>     "任何一方违约应承担全部责任,并支付200% 违约金",
>     "本合同双方签字盖章后生效" 
> ]:
>     res = app.invoke({"clause": clause, "risk_level": "", "review_result": ""})
>     print(f"条款: {clause}\n 结果: {res['review_result']}...\n")
> ```
>

%% source-id: 下036 %%

> [!quote]- 大模型全栈（下）.md · 循环模式
> 来源：原笔记第 2856–2955 行。
>
> **循环模式**
>
> ```python
> """
> 循环模式
> 不是while 是指回自己的边
> """
> import os
> from dotenv import load_dotenv
> from typing import TypedDict
> from langgraph.graph import StateGraph, END
> from langchain_openai import ChatOpenAI
> from langchain_core.messages import SystemMessage, HumanMessage
>
> load_dotenv()
>
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     temperature=0.1
> )
>
> # 模式知识
> KG = {
>     "营收": "苹果2024财年服务营收962亿美元，同比增长13%。",
>     "利润": "苹果2024财年净利润970亿美元，净利率25.3%。",
>     "AI": "苹果发布Apple Intelligence，2024年秋季随iOS 18推送。",
> }
>
> class S(TypedDict):
>     missing_info: str
>     question: str
>     context: str
>     answer: str
>     hops: int
>
> # 1.检索
> def retrieve(state):
>     target = state["missing_info"] or state["question"]
>     found = ""
>     for k, v in KG.items():
>         if k in target and v not in state["context"]:
>             found = v
>             break
>
>     print(f"[第{state['hops'] + 1}跳检索] 关键词='target' 命中={found[:20]}")
>
>     context = (state['context'] + '\n' + found) if found else state['context']
>     return {
>         "context": context,
>         "hops": state['hops'] + 1
>     }
>
> # 2.生成答案
> def generate(state):
>     resp = llm.invoke([
>         SystemMessage(content=(
>             "基于以下参考资料回答问题。如果资料不足以回答，"
>             "以'[信息不足]'开头，冒号后只写一个最缺的关键词。\n"
>             f"参考资料：{state['context']}"
>         )),
>         HumanMessage(content=state["question"]),
>     ])
>     text = resp.content
>     if text.startswith("[信息不足]"):
>         tail = text.split("]", 1)[-1].lstrip("：:").strip()
>         # 从大模型给的词里 匹配知识库的 没有命中的键
>         kw = next((k for k in KG if k in tail and KG[k] not in state['context']), tail[:10])
>         return {"missing_info": kw, "answer": ""}
>     return {"missing_info": "", "answer": text}
>
> # 3.循环判断
> def loop(state):
>     if state["answer"] or state["hops"] >= 3:
>         return "end"
>     return "retrieve"
>
> # 组装图
> g = StateGraph(S)
> g.set_entry_point("retrieve")
> g.add_node("retrieve", retrieve)
> g.add_edge("retrieve", "generate")
> g.add_node("generate", generate)
> g.add_conditional_edges(
>     "generate", loop,
>     {"retrieve": "retrieve", "end": END}
> )
>
> # 执行
> app = g.compile()
>
> res = app.invoke({
>     "question": "苹果2024财年的营收利润情况如何?",
>     "missing_info": "", "context": "", "answer": "", "hops": 0},
>     {"recursion_limit": 10}
> )
> print(f"共{res['hops']}跳检索: \n {res['answer']}")
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/12.高阶Agent.pdf#page=31|12.高阶Agent.pdf · 第 31–46 页]]
