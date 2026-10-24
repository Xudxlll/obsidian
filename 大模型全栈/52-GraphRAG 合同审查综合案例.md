---
type: 学习笔记
course: 大模型全栈
order: 52
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/51-人工介入、Checkpoint 与时间旅行|51-人工介入、Checkpoint 与时间旅行]] · 下一篇：[[大模型全栈/53-AutoML 多 Agent：模块与数据流程|53-AutoML 多 Agent：模块与数据流程]]

> [!abstract] 学习目标
> 把复杂度判断、补充检索与人工审查放进同一状态图。

## 核心理解

本例先判断条款复杂度：简单条款直接分析，复杂条款查询图谱；模型发现缺少关键资料时，再提取关键词继续检索。最终风险结果决定是否进入人工审查。

这样可以将固定业务规则与动态取证组合：图控制可走的路径，模型负责在具体节点中理解文本。需要同时关注业务状态、检索证据与流程状态，不要把它们全塞进一个字符串。

工具文件提供 assess 与 query_kw，主文件负责节点和路由。模块边界意味着两份代码应分别保存并匹配导入路径，而不是直接当作一个文件串联。

这个项目最值得学习的是闭环：有证据则回答，缺资料则继续查，达到上限则说明不足，高风险则停下来审查。它不是靠一次很长提示词完成所有步骤。

## 课堂代码怎么读

按 ReviewState、judge_complexity、retrieve、generate、should_continue、human_approval、finalize 阅读，再回头看 graphrag_tools。核对新上下文如何累积，hops 如何限制扩展。

> [!warning] 易错点与资料边界
> 原 finalize 文本的“风险”位置又插入了 analysis，而没有使用 risk_level；风险字符串判断也较脆弱。静态暂停只表示走到审查节点，实际批准仍由后续交互决定。

## 复盘练习

为什么缺少资料和高风险不应该是同一个状态？

> [!question]- 参考思路
> 前者是证据完整性，后者是对条款的判断。资料不足时可能根本无法可靠评估风险，需要单独保留不确定性。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下034 %%

> [!quote]- 大模型全栈（下）.md · 智能合同项目
> 来源：原笔记第 2516–2755 行。
>
> **智能合同项目**
>
> **项目代码**
>
> **agent代码**
>
> ```python
> """
> Agent Graph Rag 合同只能审查系统
> 判断复杂度 -> 简单直接分析 复杂走 图RAG 多跳检索 高风险走人工
> 对接Neo4j 知识图谱做增强
> """
> import os
> from typing import TypedDict
> from dotenv import load_dotenv
> from langgraph.graph import StateGraph, END
> from langgraph.checkpoint.memory import MemorySaver
> from langchain_openai import ChatOpenAI
> from langchain_core.messages import HumanMessage, SystemMessage
> from graphrag_tools import assess, query_kw
>
> load_dotenv()
>
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     temperature=0,
> )
>
> # 状态
> class ReviewState(TypedDict):
>     clause: str
>     complexity: str  # 简单/复杂
>     risk_level: str  # 等级
>     graph_context: str  # 图检索结果
>     missing_keywords: list  # 还需要检索的关键词
>     hops: int
>     analysis: str  # 分析结论
>     approved: str
>     final_result: str
>
> # 1.判断条款复杂度
> def judge_complexity(state):
>     result = assess.invoke({"clause": state["clause"]})
>     print(f"[条款复杂度]: {result}")
>     return {"complexity": result}
>
> # 2.简单 直接分析
> def direct_analyze(state):
>     res = llm.invoke([
>         SystemMessage(content="你是一个专业的法律顾问,简要分析一下条款的风险,100字以内:"),
>         HumanMessage(content=state["clause"])
>     ])
>
>     return {"analysis": res.content, "risk_level": "低"}
>
> # 3.复杂 多跳检索
> def retrieve(state):
>     # 第一轮提取关键词,后续轮检索上轮确实关键词
>     if state["hops"] == 0:
>         res = llm.invoke([
>             SystemMessage(content="从条款中提取1~3个风险关键词,用逗号分隔:"),
>             HumanMessage(content=state["clause"])
>         ])
>         keywords = [k for k in res.content.split("，") if k.strip()]
>     else:
>         keywords = state["missing_keywords"]
>
>     context_parts = [state["graph_context"]]
>     for kw in keywords:
>         result = query_kw.invoke({"keyword": kw})
>         context_parts.append(f"[{kw}] {result}")
>
>     new_context = "\n".join(p for p in context_parts if p)
>     print(f"第 {state['hops'] + 1} 跳检索完成,关键词:{keywords} ")
>     return {"graph_context": new_context, "hops": state["hops"] + 1}
>
> # 4.基于图谱上下文分析
> def generate(state):
>     # 基于图谱上下文生成分析,信息不足则补充检索
>     resp = llm.invoke([
>         SystemMessage(content=(
>             "你是资深法律顾问。基于知识图谱检索结果分析条款风险。"
>             "如果信息充分，直接输出分析（含风险等级'高/低'和修改建议）。"
>             "如果信息不足，以'[需补充]'开头，说明还需检索什么关键词。\n"
>             f"知识图谱信息：\n{state['graph_context']}"
>         )),
>         HumanMessage(content=state["clause"]),
>     ])
>     content = resp.content
>
>     if content.startswith("[需补充]"):
>         if state["hops"] >= 3:
>             # 检索上限
>             final = llm.invoke([
>                 SystemMessage(content=(
>                     "基于以下有限信息做最终分析，明确标注信息不足之处：\n"
>                     f"{state['graph_context']}"
>                 )),
>                 HumanMessage(content=state["clause"]),
>             ])
>             risk = "高" if "高风险" in final.content else "低"
>             return {"analysis": final.content + "\n 部分信息未能从图谱中获取", "risk_level": risk}
>
>         missing = [content.replace("[需补充]", "")]
>         return {"analysis": "", "risk_level": "", "missing_keywords": missing}
>
>     risk = "高" if "高风险" in content else "低"
>     return {"analysis": content, "risk_level": risk, "missing_keywords": []}
>
> # 5.判断风险等级
> def router_by_risk(state):
>     return "human_approval" if state['risk_level'] == "高" else "finalize"
>
> def should_continue(state):
>     if state["analysis"]:
>         return router_by_risk(state)
>     return ("retrieve")
>
> # 6.高风险 走人审
> def human_approval(state):
>     print(f"高风险待审批:\n  {state['clause']}\n")
>     decision = input("是否确认通过审查结论?(y/n):")
>     return {"approved": decision == "y"}
>
> # 7.低风险 直接走
> def finalize(state):
>     return {"final_result": f"审查完成 | {state['analysis']} 风险: {state['analysis']}"}
>
> # 8.人审 通过/拒绝
> def reject(state):
>     return {"final_result": "人工审查未通过"}
>
> # 构建流程图
> graph = StateGraph(ReviewState)
> graph.add_node("judge_complexity", judge_complexity)
> graph.add_node("direct_analyze", direct_analyze)
> graph.add_node("retrieve", retrieve)
> graph.add_node("generate", generate)
> graph.add_node("human_approval", human_approval)
> graph.add_node("finalize", finalize)
> graph.add_node("reject", reject)
>
> graph.set_entry_point("judge_complexity")
> graph.add_conditional_edges(
>     "judge_complexity",
>     lambda s: "retrieve" if s['complexity'] == "复杂" else "direct_analyze",
>     {"retrieve": "retrieve", "direct_analyze": "direct_analyze"}
> )
> graph.add_conditional_edges(
>     "direct_analyze", router_by_risk,
>     {"human_approval": "human_approval", "finalize": "finalize"}
> )
> graph.add_edge("retrieve", "generate")
> graph.add_conditional_edges(
>     "generate", should_continue,
>     {
>         "retrieve": "retrieve",
>         "human_approval": "human_approval",
>         "finalize": "finalize"
>     }
> )
>
> graph.add_conditional_edges(
>     "human_approval",
>     lambda s: "finalize" if s['approved'] else "reject",
>     {"finalize": "finalize", "reject": "reject"}
> )
> graph.add_edge("finalize", END)
> graph.add_edge("reject", END)
>
> # 运行
> app = graph.compile(
>     checkpointer=MemorySaver(),
>     interrupt_before=["human_approval"]
> )
>
> test_clauses = [
>     "任何一方违约，应承担全部无限责任，并支付合同金额200%的违约金。",
>     "本合同自双方签字盖章之日起生效，有效期一年。"
> ]
>
> for i, clause in enumerate(test_clauses, 1):
>     print(f"审查条款:{i}:{clause}")
>     config = {"configurable": {"thread_id": f"review-{i}"}, "recursion_limit": 15}
>     init_state = {
>         "clause": clause,
>         "complexity": "", "risk_level": "", "graph_context": "", "missing_keywords": [],
>         "hops": 0, "analysis": "", "approved": False, "final_result": ""
>     }
>
>     app.invoke(init_state, config)
>     snapshot = app.get_state(config)
>     if snapshot.next and "human_approval" in snapshot.next:
>         result = app.invoke(None, config)
>     else:
>         result = snapshot.values
>
>     print(f"\n 最终结果: \n{result['final_result']}")
> ```
>
> **工具代码**
>
> ```python
> """
> Agent Graph Rag 合同只能审查系统
> 判断复杂度 -> 简单直接分析 复杂走 图RAG 多跳检索 高风险走人工
> 对接Neo4j 知识图谱做增强
> """
> import os
> from langchain_core.tools import tool
> from neo4j import GraphDatabase
>
> @tool
> def assess(clause):
>     """判断合同复杂度"""
>     complex_kw = ["无限责任", "200%", "连带责任", "知识产权归属", "竞业限制", "跨境", "违约", "及时交付", "赔偿",
>                   "追责", "法律"]
>     score = sum(1 for kw in complex_kw if kw in clause)
>     return "复杂" if score >= 3 else "简单"
>
> # 知识图谱的查询
> driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))
>
> @tool
> def query_kw(keyword):
>     """从法律知识图谱中检索与关键词相关的实体,关系,风险信息"""
>     with driver.session() as session:
>         result = session.run("""
>         MATCH (e1:Entity)-[r]->(e2:Entity)
>         WHERE e1.name CONTAINS $kw 
>         RETURN e1.name, type(r), e2.name
>         """, kw=keyword)
>
>         records = [f"{r['e1.name']}-{r['type(r)']}->{r['e2.name']}" for r in result]
>
>     return "\n".join(records) if records else f"知识图谱没找到{keyword}相关信息"
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/12.高阶Agent.pdf#page=38|12.高阶Agent.pdf · 第 38–59 页]]
- [[大模型全栈/资料/PDF/知识图谱.pdf#page=1|知识图谱.pdf · 第 1–9 页]]
- 关联知识：[[大模型全栈/40-Text2Cypher 与图谱问答|40-Text2Cypher 与图谱问答]]、[[大模型全栈/41-GraphRAG：向量召回与关系扩展|41-GraphRAG：向量召回与关系扩展]]、[[大模型全栈/49-LCEL 合同审查任务流|49-LCEL 合同审查任务流]]、[[大模型全栈/50-LangGraph：状态、条件分支与循环|50-LangGraph：状态、条件分支与循环]]、[[大模型全栈/51-人工介入、Checkpoint 与时间旅行|51-人工介入、Checkpoint 与时间旅行]]。
