---
type: 学习笔记
course: 大模型全栈
order: 43
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/42-工具调用：Schema、执行与结果回传|42-工具调用：Schema、执行与结果回传]] · 下一篇：[[大模型全栈/44-Plan-and-Execute：规划与任务分解|44-Plan-and-Execute：规划与任务分解]]

> [!abstract] 学习目标
> 理解 Agent 的核心是带反馈的行动循环。

## 核心理解

Agent 以目标为起点，在环境中选择动作、读取工具结果，再决定继续、调整或结束。Chain 通常预先固定流程，Agent 则允许模型在受控范围内选择下一步；RAG 可以作为 Agent 的一个取证工具。

ReAct 交替组织推断与工具行动，用观察结果修正后续动作。Self-Ask 先提出子问题，必要时调用外部工具，逐步解决原问题。它们是流程思路，不是每个框架都以相同类名实现。

课堂 Self-Ask 金融示例使用固定文本约定解析子问题与工具调用，并设置轮次上限。这样的教学实现直观，但对标点、模型措辞和参数解析较敏感。

判断系统是否为可靠 Agent，应该看它能否正确选择工具、利用返回结果、处理失败并及时停止，而不是只看输出里有没有“思考”字样。

## 课堂代码怎么读

读 `get_stock_info` 的实际数据来源，再读 `self_ask_analyze` 的问题、响应解析、工具映射和循环上限。把每轮输入、动作与观察记成三列，最容易看出闭环是否成立。

> [!warning] 易错点与资料边界
> 课堂金融工具只是流程案例，联网数据的时点与异常会影响输出。本轮不运行它，也不把生成分析转成投资建议。文本约定解析应与结构化工具协议区别理解。

## 复盘练习

Agent 为什么需要明确结束条件？

> [!question]- 参考思路
> 否则模型可能反复查询、重复行动或无限消耗预算。完成条件、最大轮数、成本限制和不可恢复错误都应有明确出口。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下046 %%

> [!quote]- 大模型全栈（下）.md · Self-ASK架构
> 来源：原笔记第 3671–3777 行。
>
> **Self-ASK架构**
>
> ```python
> import os
> from dotenv import load_dotenv
> import requests
> import akshare as ak
> import pandas as pd
> from langchain_openai import ChatOpenAI
> from langchain_core.tools import tool
>
> load_dotenv()
>
> # 1. 初始化 LLM
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     temperature=0,
> )
>
> # 2. 基础工具：股票行情财务查询
> @tool
> def get_stock_info(stock_code: str) -> str:
>     """获取 A 股股票的行情和核心财务数据，参数如 sh600519、sz300750"""
>     try:
>         num = stock_code[2:]
>         r = requests.get(f"http://qt.gtimg.cn/q={stock_code}", timeout=10)
>         p = r.text.split("~")
>         price = float(p[3])
>         pe = float(p[39])
>         mcap_yi = float(p[45])
>         # 近30日涨跌幅：新浪日线
>         hist = ak.stock_zh_a_daily(symbol=stock_code, adjust="qfq")
>         h30 = hist.tail(30)
>         chg30 = (float(h30["close"].iloc[-1]) - float(h30["close"].iloc[0])) / float(h30["close"].iloc[0]) * 100
>         # 净利润率：东财财务摘要
>         fa = ak.stock_financial_abstract(symbol=num)
>         dc = [c for c in fa.columns if c not in ("选项", "指标")]
>         rev = pd.to_numeric(fa.loc[fa["指标"] == "营业总收入"].iloc[0][dc], errors="coerce").dropna()
>         npf = pd.to_numeric(fa.loc[fa["指标"] == "净利润"].iloc[0][dc], errors="coerce").dropna()
>         npm = npf.iloc[0] / rev.iloc[0] * 100
>         return f"""
> 股票代码: {stock_code}
> 最新股价: {price:.2f} 元
> 市盈率(TTM): {pe:.2f}
> 净利润率: {npm:.2f}%
> 近30日涨跌幅: {chg30:.2f}%
> 总市值: {mcap_yi:.2f} 亿元
>         """.strip()
>     except Exception as e:
>         return f"获取数据失败: {str(e)}"
>
> tool_map = {get_stock_info.name: get_stock_info}
>
> # 3. Self-Ask 核心提示词
> SELF_ASK_PROMPT = """你是投资分析师，严格用Self-Ask方式回答用户问题。
> 规则：
> 1. 如果当前信息足够回答用户问题，直接输出 最终答案：xxx
> 2. 如果信息不足，只输出 追问：工具名|参数 ，一次只提一个子问题
> 3. 只能通过工具查询真实数据，禁止编造
> 4. 可用工具：get_stock_info，参数为 A 股股票代码（如 sh600519、sz300750）。请直接使用问题中给出的代码作为参数，不要使用中文名称。
>
> 当前已获取的信息：
> {context}
>
> 用户问题：{question}
> """
>
> # 4. Self-Ask 核心循环
> def self_ask_analyze(question: str):
>     context = ""
>     max_rounds = 8  # 最多追问8轮，防止死循环
>
>     for i in range(max_rounds):
>         # LLM 判断：继续追问 还是 输出最终答案
>         response = llm.invoke(
>             SELF_ASK_PROMPT.format(context=context, question=question)
>         ).content.strip()
>
>         print(f"\n[第 {i + 1} 轮推理]\nLLM输出: {response}")
>
>         # 情况1：信息足够，返回最终结论
>         if "最终答案" in response:
>             return response.replace("最终答案：", "")
>
>         # 情况2：信息不足，解析子问题，调用工具补全信息
>         if "追问" in response:
>             sub_query = response.replace("追问：", "").strip()
>             tool_name, arg = sub_query.split("|", 1)
>             print(f"执行工具查询: {tool_name}({arg})")
>
>             result = tool_map[tool_name].invoke({"stock_code": arg.strip()})
>             print(f"工具返回:\n{result}")
>
>             # 把答案补充到上下文，进入下一轮自问
>             context += f"\n[子问题结果] {sub_query}\n{result}\n"
>             continue
>
>     return "查询轮次超限，无法完成分析"
>
> # 5. 运行测试
> user_question = "对比贵州茅台(sh600519)和宁德时代(sz300750)，哪个短期投资性价比更高？"
> final_result = self_ask_analyze(user_question)
> print("最终结果\n", final_result)
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/8.Create_Agent.pdf#page=1|8.Create_Agent.pdf · 第 1–15 页]]
- [[大模型全栈/资料/PDF/8.Create_Agent.pdf#page=24|8.Create_Agent.pdf · 第 24–31 页]]
- 关联知识：[[大模型全栈/42-工具调用：Schema、执行与结果回传|42-工具调用：Schema、执行与结果回传]]、[[大模型全栈/44-Plan-and-Execute：规划与任务分解|44-Plan-and-Execute：规划与任务分解]]、[[大模型全栈/46-对话记忆：缓冲、摘要与向量检索|46-对话记忆：缓冲、摘要与向量检索]]、[[大模型全栈/47-Multi-Agent 与 CrewAI 基础|47-Multi-Agent 与 CrewAI 基础]]。
