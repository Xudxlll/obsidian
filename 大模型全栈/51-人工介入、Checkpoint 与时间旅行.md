---
type: 学习笔记
course: 大模型全栈
order: 51
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/50-LangGraph：状态、条件分支与循环|50-LangGraph：状态、条件分支与循环]] · 下一篇：[[大模型全栈/52-GraphRAG 合同审查综合案例|52-GraphRAG 合同审查综合案例]]

> [!abstract] 学习目标
> 把暂停、继续与历史状态分叉区别理解。

## 核心理解

人工介入在关键节点暂停流程，等待外部决定后继续。LangGraph 的动态 interrupt 与 Command(resume=...) 配合，checkpointer 保存状态，thread_id 标识待恢复的执行。

时间旅行是读取历史 checkpoint，再从指定状态继续或更新后分叉。它适合调试与修正，但恢复的是图状态，不会自动撤销先前发生的文件写入、网络请求或其他外部动作。

动态中断恢复时节点可能从头重新执行，因此中断前的副作用需要可重复处理，或被拆到独立步骤。静态 interrupt_before 与节点内动态 interrupt 的使用方式也应区分。

课堂转账只是文字模拟，时间旅行例子用 SQLite 保存执行历史并修正参数，不能据此理解为真实资金操作或数据库事务回滚。

## 课堂代码怎么读

先看人工模式中的 risk 路由、interrupt、checkpointer 与恢复配置；再看历史列表、checkpoint_id、update_state 和 fork_config。检查恢复时是否沿用正确的 thread_id。

> [!warning] 易错点与资料边界
> 人工示例默认 8000 元，按其规则会直接走低风险分支，并不演示暂停；观察人工路径需另选满足阈值的教学输入。检查点文件持久化与内存 Saver 生命周期不同。

## 复盘练习

从过去状态重新执行，为什么可能重复发送通知？

> [!question]- 参考思路
> 检查点保存的是图内状态，外部通知可能已发生。重新执行相关节点会再次调用外部系统，需要幂等键或独立动作记录。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下035 %%

> [!quote]- 大模型全栈（下）.md · 人审模式
> 来源：原笔记第 2756–2855 行。
>
> **人审模式**
>
> ```python
> """
> 人审模式
> 评估风险->高(人工审批)  --> 通过/拒绝
>       ->低(直接执行)
> """
> import os
> from dotenv import load_dotenv
> from typing import TypedDict
> from langgraph.graph import StateGraph, END
> from langchain_openai import ChatOpenAI
> from langgraph.checkpoint.memory import MemorySaver
> from langgraph.types import interrupt, Command
>
> load_dotenv()
>
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     temperature=0
> )
>
> # 定义状态
> class S(TypedDict):
>     amount: float
>     to_account: str
>     risk: str
>     approved: bool
>     result: str
>
> # 风险检查
> def check_risk(state):
>     risk = "高" if state["amount"] > 50000 else "低"
>     print(f"[风险检查] 转账 {state['amount']}元,风险:{risk}")
>     return {"risk": risk}
>
> # 分支 走人工 or 直接执行
> route = lambda s: "human_approval" if s['risk'] == "高" else "execute"
>
> # 人工审批
> def human_approval(state):
>     # interrupt() #图在这里暂停
>     decision = interrupt(f"待审批:向 {state['to_account']} 转账 {state['amount']} 元 (y/n)")
>     return {"approved": str(decision) == "y"}
>
> # 分支 执行 or 不执行
> route_after_approval = lambda s: "execute" if s['approved'] else "reject"
>
> # 执行/拒绝
> def execute(state):
>     return {"result": f"转账成功:向 {state['to_account']} 转账 {state['amount']} 元"}
>
> def reject(state):
>     return {"result": f"转账已经拒绝(人工审批不通过)"}
>
> # 组装图
> g = StateGraph(S)
> g.set_entry_point("check_risk")
> g.add_node("check_risk", check_risk)
> g.add_conditional_edges(
>     "check_risk", route,
>     {"human_approval": "human_approval", "execute": "execute"}
> )
> g.add_node("human_approval", human_approval)
> g.add_conditional_edges(
>     "human_approval", route_after_approval,
>     {"execute": "execute", "reject": "reject"}
> )
> g.add_node("execute", execute)
> g.add_edge("execute", END)
> g.add_node("reject", reject)
> g.add_edge("reject", END)
>
> # 执行
> # 必须配置 checkpointer
> app = g.compile(checkpointer=MemorySaver())
> config = {
>     "configurable": {"thread_id": "transfer-001"}
> }
>
> result = app.invoke({"amount": 8000, "to_account": "6222****1234", "risk": "", "approved": False, "result": ""},
>                  config=config)
>
> if not result.get('result'):
>     print("图暂停等待人工审核...")
>     while True:
>         raw = input(f"是否批准向{result['to_account']} 转账 {result['amount']} 元? (y/n)").strip()
>
>         if raw in ("y", "n"):
>             decision = "y" if raw == "y" else "n"
>             break
>
>     result = app.invoke(Command(resume=decision), config=config)
>
> print(f"最终结果:{result['result']}")
> ```
>

%% source-id: 下033 %%

> [!quote]- 大模型全栈（下）.md · 时间旅行
> 来源：原笔记第 2406–2515 行。
>
> **时间旅行**
>
> ```python
> """
> agent 自我纠错
> """
> import os
> import sqlite3
> from typing import List, TypedDict
> from langgraph.graph import StateGraph, START, END
> from langgraph.checkpoint.sqlite import SqliteSaver
> from langchain_openai import ChatOpenAI
> from dotenv import load_dotenv
>
> load_dotenv()
>
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     temperature=0
> )
>
> class AgentState(TypedDict):
>     messages: List
>     tool_calls: List
>     tool_result: str
>
> def agent_thinking(state):
>     resp = llm.invoke(state["messages"])
>     return {
>         "messages": [resp],
>         "tool_calls": [{"tool": "calc", "arg": "-100"}]
>     }
>
> def tool_exec(state):
>     call = state["tool_calls"][0]
>     arg = int(call["arg"])
>     if arg < 0:
>         return {"tool_result": "ERROR: 参数不能为负数！工具执行失败"}
>     return {"tool_result": f"计算结果={arg * 2}"}
>
> builder = StateGraph(AgentState)
> builder.add_node("agent_thinking", agent_thinking)
> builder.add_node("tool_exec", tool_exec)
> builder.add_edge(START, "agent_thinking")
> builder.add_edge("agent_thinking", "tool_exec")
> builder.add_edge("tool_exec", END)
>
> os.makedirs("checkpoint", exist_ok=True)
> db_path = "./checkpoint/agent_roll.db"
> if os.path.exists(db_path):
>     os.remove(db_path)
>
> conn = sqlite3.connect(db_path, check_same_thread=False)
> checkpointer = SqliteSaver(conn)
> app = builder.compile(checkpointer=checkpointer)
>
> thread_cfg = {"configurable": {"thread_id": "demo_001"}}
>
> print("第一轮完整执行，Agent产生错误参数，工具报错")
> res1 = app.invoke({
>     "messages": [("human", "请帮我做一个数值计算")],
>     "tool_calls": [],
>     "tool_result": ""
> }, config=thread_cfg)
> print("tool_result:", res1["tool_result"])
>
> history = list(app.get_state_history(thread_cfg))
> print("\n全部快照列表")
> for idx, snap in enumerate(history):
>     meta = snap.metadata
>     step = meta.get("step")
>     src = meta.get("source")
>     cid = snap.config["configurable"]["checkpoint_id"]
>     vals = snap.values
>     toolcall = vals.get("tool_calls", [])
>     print(f"idx:{idx} step:{step} source:{src:6s} cid:{cid[:8]} tool_calls:{toolcall}")
>
> # 找出出错的快照
> rollback_cid = None
> for snap in reversed(history):
>     vals = snap.values
>     tc = vals.get("tool_calls", [])
>     tr = vals.get("tool_result", "")
>     if len(tc) > 0 and tr == "":
>         rollback_cid = snap.config["configurable"]["checkpoint_id"]
>         break
>
> # 回滚
> roll_config = {
>     "configurable": {
>         "thread_id": "demo_001",
>         "checkpoint_id": rollback_cid,
>         "checkpoint_ns": ""
>     }
> }
>
> # 重新开启新分支执行
> new_cfg = app.update_state(
>     roll_config,
>     {"tool_calls": [{"tool": "calc", "arg": "500"}]},
>     as_node="agent_thinking"
> )
> fork_config = new_cfg if isinstance(new_cfg, dict) else new_cfg.config
>
> res_fixed = app.invoke(None, fork_config)
> print("tool_result:", res_fixed["tool_result"])
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/12.高阶Agent.pdf#page=45|12.高阶Agent.pdf · 第 45–59 页]]
- [LangGraph 官方 interrupt 参考](https://reference.langchain.com/python/langgraph/types/interrupt)：动态中断依赖 checkpointer，恢复值通过 Command 传入。（补充核对日期：2026-10-25）
- 关联知识：[[大模型全栈/50-LangGraph：状态、条件分支与循环|50-LangGraph：状态、条件分支与循环]]、[[大模型全栈/52-GraphRAG 合同审查综合案例|52-GraphRAG 合同审查综合案例]]、[[大模型全栈/54-工具权限、审计与代码执行边界|54-工具权限、审计与代码执行边界]]。
