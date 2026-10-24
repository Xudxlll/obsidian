---
type: 学习笔记
course: 大模型全栈
order: 45
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/44-Plan-and-Execute：规划与任务分解|44-Plan-and-Execute：规划与任务分解]] · 下一篇：[[大模型全栈/46-对话记忆：缓冲、摘要与向量检索|46-对话记忆：缓冲、摘要与向量检索]]

> [!abstract] 学习目标
> 用共享状态把计划、工具和总结连起来。

## 核心理解

本例把股票价格、财务与走势工具接进 LangGraph，用 plan、execute、summarize 三类节点形成报告流程。State 保存消息、计划、当前步骤和工具结果，边决定下一步去哪。

`Annotated[..., add_messages]` 一类 reducer 用于定义消息更新方式；普通字段若没有累加约定，新的返回值可能覆盖旧值。读图时既要看节点函数，也要看状态字段如何合并。

execute 让绑定工具的模型选择调用，再把工具返回结果写入后续可使用的状态。最终总结应基于实际结果，明确数据时间与缺失项。

作为课程项目，它展示“规划—行动—汇总”的工程连接；报告内容是否可靠，还依赖数据质量、指标单位与时间范围，不能因流程完成就认定结论有效。

## 课堂代码怎么读

先核对三种工具的参数与返回文本，再读 AgentState、plan_node、execute_node 和路由函数。跟踪 step_index 是否递增，以及 ToolMessage 与调用 ID 是否对应。

> [!warning] 易错点与资料边界
> 工具消息写入状态，不代表总结一定使用了全部证据。源站、字段与时间范围可能变化；课堂示例结果不是本轮已验证的市场事实。

## 复盘练习

为什么一个 execute 节点可能被调用多次？

> [!question]- 参考思路
> 每次处理当前计划步骤，路由根据剩余任务决定继续 execute 或进入 summarize。循环是图的执行逻辑，不等于代码意外重复。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下047 %%

> [!quote]- 大模型全栈（下）.md · 金融研报Plan
> 来源：原笔记第 3778–4034 行。
>
> **金融研报Plan**
>
> 国内通达信、东财、广发等开放mcp，老股民这些都知道，主业幻方，副业deepseek
>
> ```python
> """
> 金融研报
> """
> import os
> import requests
> import akshare as ak
> import pandas as pd
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
> from langchain_core.tools import tool
> from langchain_core.messages import HumanMessage, ToolMessage
> from langgraph.graph import StateGraph, START, END
> from langgraph.graph.message import add_messages
> from typing import Annotated, TypedDict
>
> load_dotenv()
>
> # 1.初始LLM
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     temperature=0,
>     max_retries=2,
> )
>
> # 2.金融工具集
> @tool
> def get_stock_price(stock_code="sh600519"):
>     """获取股票最新实时行情数据"""
>     try:
>         r = requests.get(f"http://qt.gtimg.cn/q={stock_code}", timeout=10)
>         parts = r.text.split("~")
>         price = float(parts[3])
>         pct = float(parts[32])
>         high = float(parts[33])
>         low = float(parts[34])
>         vol = int(float(parts[6]))
>         return f"""股票 {stock_code}最新行情:
>         - 最新价格: {price} 元
>         - 当日涨跌幅: {pct} %
>         - 当日最高价: {high} 元
>         - 当日最低价: {low} 元
>         - 成交量: {vol} 手
>         """
>     except Exception as e:
>         print(f"获取股票行情失败{e}")
>
> @tool
> def get_stock_financials(stock_code="sh600519"):
>     """获取股票核心财务基本面指标"""
>     # 盈利能力: ROE净资产收益率  毛利率&净利率
>     # 成长能力:营收增长率&净利润增长率
>     # 运营效率:应收账款/周转率
>     # 债偿能力:资产负债率 流动比/速动比
>     try:
>         # 1) 估值指标：腾讯行情
>         r = requests.get(f"http://qt.gtimg.cn/q={stock_code}", timeout=10)
>         parts = r.text.split("~")
>         mcap_yi = float(parts[45]) if len(parts) > 45 else None  # 总市值(亿元)
>         pe = float(parts[39]) if len(parts) > 39 else None  # 市盈率TTM
>         pb = float(parts[46]) if len(parts) > 46 else None  # 市净率
>
>         # 2) 基本面：东财财务摘要（最新报告期）
>         npm = roe = rev_growth = None
>         try:
>             symbol_num = stock_code.replace("sh", "").replace("sz", "")
>             fa = ak.stock_financial_abstract(symbol=symbol_num)
>             date_cols = [c for c in fa.columns if c not in ("选项", "指标")]
>             rev = pd.to_numeric(fa.loc[fa["指标"] == "营业总收入"].iloc[0][date_cols], errors="coerce").dropna()
>             npf = pd.to_numeric(fa.loc[fa["指标"] == "净利润"].iloc[0][date_cols], errors="coerce").dropna()
>             ne = pd.to_numeric(fa.loc[fa["指标"] == "股东权益合计(净资产)"].iloc[0][date_cols],
>                                errors="coerce").dropna()
>             if len(rev) >= 1 and rev.iloc[0] != 0:
>                 npm = npf.iloc[0] / rev.iloc[0] * 100
>             if len(npf) >= 1 and len(ne) >= 1 and ne.iloc[0] != 0:
>                 roe = npf.iloc[0] / ne.iloc[0] * 100
>             if len(rev) >= 5 and rev.iloc[4] != 0:  # 与一年前同期对比
>                 rev_growth = (rev.iloc[0] - rev.iloc[4]) / rev.iloc[4] * 100
>         except Exception:
>             pass
>
>         lines = [f"股票 {stock_code} 核心财务指标："]
>         if mcap_yi:
>             lines.append(f"- 总市值：{mcap_yi:.2f} 亿元（约 {mcap_yi / 10000:.2f} 万亿元）")
>         else:
>             lines.append("- 总市值：暂无数据")
>         lines.append(f"- 市盈率(TTM)：{pe:.2f}" if pe else "- 市盈率(TTM)：暂无数据")
>         lines.append(f"- 市净率：{pb:.2f}" if pb else "- 市净率：暂无数据")
>         lines.append(f"- 净利润率：{npm:.2f}%" if npm is not None else "- 净利润率：暂无数据")
>         lines.append(
>             f"- 净资产收益率(ROE，最新报告期)：{roe:.2f}%" if roe is not None else "- 净资产收益率(ROE)：暂无数据")
>         lines.append(f"- 营收增速(同比)：{rev_growth:.2f}%" if rev_growth is not None else "- 营收增速：暂无数据")
>         return "\n".join(lines)
>     except Exception as e:
>         return f"获取财务数据失败：{str(e)}"
>
> @tool
> def get_stock_trend(stock_code="sh600519"):
>     """获取 股票近30天走势统计"""
>     try:
>         hist = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")
>         if hist.empty:
>             return "未获取到历史行情数据"
>         hist_30 = hist.tail(30)
>         start_price = float(hist_30["close"].iloc[0])
>         end_price = float(hist_30["close"].iloc[-1])
>         change_pct = (end_price - start_price) / start_price * 100
>         return f"""股票 {stock_code} 近30天走势统计：
> - 区间涨跌幅：{change_pct:.2f}%
> - 区间最高价：{hist_30['high'].max():.2f} 元
> - 区间最低价：{hist_30['low'].min():.2f} 元
> - 区间均价：{hist_30['close'].mean():.2f} 元
> - 走势判断：{'上涨趋势' if change_pct > 0 else '下跌趋势'}
> """
>     except Exception as e:
>         return f"获取走势数据失败：{str(e)}"
>
> FINANCE_TOOLS = [get_stock_price, get_stock_financials, get_stock_trend]
> tool_map = {t.name: t for t in FINANCE_TOOLS}
> llm_with_tools = llm.bind_tools(FINANCE_TOOLS)
>
> # 3. 定义装与PAE节点
> class AgentState(TypedDict):
>     messages: Annotated[list, add_messages]
>     plan: list[str]
>     step_index: int
>     tool_result: list[str]
>
> # 节点1:规划阶段
> def plan_node(state: AgentState):
>     user_query = state["messages"][-1].content
>     plan_prompt = f"""你是资深金融分析师，请针对用户问题制定精准的执行步骤。
>     【用户问题】{user_query}
>     【可用工具】{', '.join([t.name for t in FINANCE_TOOLS])}
>     【工具说明】
>     - get_stock_price(stock_code)：获取股票实时行情
>     - get_stock_financials(stock_code)：获取股票财务基本面
>     - get_stock_trend(stock_code)：获取股票近30天走势
>     【要求】
>     1.从用户问题中识别股票代码，若用户只给股票名称，映射为sh/sz开头的标准代码。
>     2.请输出编号的执行步骤，每行一步，**只输出步骤，不要调用工具、不要输出结论**。
>     3.最后一步必须是「综合所有数据输出投资价值分析结论」，且该步骤不调用任何工具。
>     4.只调用用户真正需要的工具, 不要多余的调用
>     5.直接在工具调用步骤里用映射后的代码
>     """
>     response = llm.invoke([HumanMessage(content=plan_prompt)])
>     steps = [
>         s
>         for s in response.content.strip().split("\n")
>         if s.strip() and s.strip()[0].isdigit()
>     ]
>     print(f"\n 规划完成, 共{len(steps)} 步执行计划:")
>     for step in steps:
>         print(f"  {step}")
>
>     return {"plan": steps, "step_index": 0, "tool_result": []}
>
> # 节点2:执行阶段
> # 如果返回包含 tool_calls 遍历每个工具调用->找工具->执行->得到结果->保存->组装ToolMessages->更新状态->next
> def execute_node(state: AgentState):
>     current_index = state["step_index"]
>     plan = state["plan"]
>     current_step = plan[current_index]
>
>     print(f"\n 正在执行 {current_index + 1}/{len(plan)} 步 : {current_step}")
>
>     if "结论" in current_step or "综合" in current_step:
>         print("总结步骤, 不需要调用工具!")
>
>         return {
>             "messages": state["messages"],
>             "tool_result": state["tool_result"],
>             "step_index": current_index + 1,
>         }
>
>     step_prompt = f"""请完成当前执行步骤：{current_step}
>     根据步骤内容调用对应的工具，参数从步骤描述中提取股票代码相关信息。
>     **只调用工具，不要输出其他分析内容**。
>     **严格只调用这一步写明的那一个工具，禁止调用其他工具**。
>     """
>     messages = state["messages"] + [HumanMessage(content=step_prompt)]
>     response = llm_with_tools.invoke(messages)
>
>     new_messages = [response]
>     step_results = []
>     if response.tool_calls:
>         for tc in response.tool_calls:
>             res = tool_map[tc["name"]].invoke(tc["args"])
>             step_results.append(str(res))
>             new_messages.append(ToolMessage(content=str(res), tool_call_id=tc.get("id")))
>             print(f"    工具 {tc['name']} 执行完成")
>     else:
>         print("不需要调用工具!")
>
>     return {
>         "messages": new_messages,
>         "tool_result": state["tool_result"] + step_results,
>         "step_index": current_index + 1,
>     }
>
> # 路由:判断继续执行还是进入总结
> def route_after_execute(state: AgentState):
>     if state["step_index"] >= len(state["plan"]):
>         return "summarize"
>
>     return "execute"
>
> # 节点3:总结阶段
> def summarize_node(state: AgentState):
>     user_query = state["messages"][0].content
>     all_results = "\n".join(state["tool_result"])
>
>     summary_prompt = f"""你是资深金融分析师，请基于以下真实数据，对用户问题给出结构化综合分析。
>     【用户问题】{user_query}
>     【已获取的全部真实数据】
>     {all_results}
>
>     【要求】
>     1. 先分模块呈现核心数据
>     2. 给出综合投资价值判断
>     3. 附上风险提示，明确说明不构成投资建议
>     所有结论必须基于上述真实数据，严禁虚构。"""
>
>     response = llm.invoke([HumanMessage(content=summary_prompt)])
>     return {"messages": [response]}
>
> # 4.构建状态图
> builder = StateGraph(AgentState)
> builder.add_node("plan", plan_node)
> builder.add_node("execute", execute_node)
> builder.add_node("summarize", summarize_node)
>
> builder.add_edge(START, "plan")
> builder.add_edge("plan", "execute")
> builder.add_conditional_edges(
>     "execute", route_after_execute,
>     {
>         "execute": "execute",
>         "summarize": "summarize"
>     }
> )
> builder.add_edge("summarize", END)
> agent_graph = builder.compile()
>
> # 运行测试
> user_query = "贵州茅台(股票代码 sh600519)的实时股价"
>
> res = agent_graph.invoke({"messages": [HumanMessage(content=user_query)]})
> print(res["messages"][-1].content)
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/8.Create_Agent.pdf#page=31|8.Create_Agent.pdf · 第 31–37 页]]
- [[大模型全栈/资料/PDF/12.高阶Agent.pdf#page=31|12.高阶Agent.pdf · 第 31–46 页]]
- 关联知识：[[大模型全栈/44-Plan-and-Execute：规划与任务分解|44-Plan-and-Execute：规划与任务分解]]、[[大模型全栈/50-LangGraph：状态、条件分支与循环|50-LangGraph：状态、条件分支与循环]]。
