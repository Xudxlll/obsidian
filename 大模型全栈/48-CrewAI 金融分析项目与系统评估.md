---
type: 学习笔记
course: 大模型全栈
order: 48
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/47-Multi-Agent 与 CrewAI 基础|47-Multi-Agent 与 CrewAI 基础]] · 下一篇：[[大模型全栈/49-LCEL 合同审查任务流|49-LCEL 合同审查任务流]]

> [!abstract] 学习目标
> 区分数据工具、分析任务与最终汇总的责任。

## 核心理解

课堂金融 Multi-Agent 将行情、新闻与计算工具交给不同任务，再由团队产生综合输出。读项目时先列“谁获取数据、谁做计算、谁审核、谁汇总”，比先背角色名称更有帮助。

工具中的 PE、行业均值、增速等字段必须统一单位。PEG 示例尤其要注意增速写成 20 还是 0.20，不同约定会带来百倍差异；非正增速时也不能机械使用比值。

多 Agent 系统评价要加入端到端完成率、工具失败、事实引用、调用成本与耗时。PDF 给出的对比实验是实验设计参考，不是本轮实际运行的结果。

原笔记末尾另有一个较大的金融项目包；本地课程目录中可见同名 ZIP 与解压目录。本轮登记其位置，未把该目录中的全部源码扩展导入到本篇。

## 课堂代码怎么读

先读 CREW_tools 中行情、新闻与 calc，再读 Agent/Task 的工具分配与 context。检查某个计算数字来自工具还是模型自己估计，并查看最终产物是否保留数据时间。

> [!warning] 易错点与资料边界
> 本例的文本抓取与接口可能变化。课堂演示不能证明可交易收益、自动投研准确率或已实现可靠金融决策。

## 复盘练习

为什么要把数值计算交给工具，而不是只让不同 Agent 互相讨论？

> [!question]- 参考思路
> 讨论不替代确定性计算。工具可保留输入、公式与结果，便于复核；Agent 负责选择适当计算和解释适用条件。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下039 %%

> [!quote]- 大模型全栈（下）.md · 金融Mutil Agent
> 来源：原笔记第 3041–3306 行。
>
> **金融Mutil Agent**
>
> **tools**
>
> ```python
> """
> 金融投研 Mutil-Agent
> 数据获取, 估值计算
> """
> from crewai.tools import tool
> import re
> import requests
> from datetime import datetime
>
> @tool
> def get_stock_basic(symbol="sh600519"):
>     """获取股票最新实时行情数据"""
>     try:
>         r = requests.get(f"http://qt.gtimg.cn/q={symbol}", timeout=10)
>         parts = r.text.split("~")
>         price = float(parts[3])
>         pct = float(parts[32])
>         high = float(parts[33])
>         low = float(parts[34])
>         vol = int(float(parts[6]))
>         return f"""股票 {symbol}最新行情:
>         - 最新价格: {price} 元
>         - 当日涨跌幅: {pct} %
>         - 当日最高价: {high} 元
>         - 当日最低价: {low} 元
>         - 成交量: {vol} 手
>         """
>     except Exception as e:
>         print(f"获取股票行情失败{e}")
>
> def clean(text):
>     text = re.sub(r"<!--.*?-->", "", text, re.S)
>     text = re.sub(r"<.*?>", "", text, re.S)
>     return text.strip()
>
> @tool
> def get_stock_news(symbol):
>     """
>     查询股票相关的最新市场新闻
>     输入股票代码,返回最多5条新闻,包含标题,时间,来源
>     """
>     keyword = f"{symbol.upper()} 美股"
>     url = f"http://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&wd={keyword}"
>     response = requests.get(
>         url,
>         headers={
>             "Cookie": """PSTM=1782311186; BIDUPSID=D98BFC1565E2033D470E5F2860618121; BD_UPN=12314753;""",
>             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
>         }
>     )
>     response.encoding = "utf-8"
>
>     html = response.text
>
>     # 把html切分得到结果块
>     blocks = re.split(r'(?=<h3 class="news-title_)', html)
>     results = []
>     for b in blocks[1:]:
>         title_m = re.search(r'aria-label="标题：([^"]+)"', b)
>         time_m = re.search(r'aria-label="发布于：([^"]+)"', b)
>         source_m = re.search(r'aria-label="新闻来源：([^"]+)"', b)
>
>         title = title_m.group(1).strip() if title_m else ""
>         time = time_m.group(1).strip()
>         source = source_m.group(1).strip()
>
>         cut = re.split(r'<div class="(news-source_|result-op)', b)[0]
>         b2 = re.sub(r'<h3 class="news-title_.*?</h3>', '', cut, flags=re.S)
>         content = clean(b2)
>         for drop in (time, source):
>             if drop and drop in content:
>                 content = content.replace(drop, "", 1)
>             content = content.strip()
>
>         if title:
>             results.append({
>                 "title": title,
>                 "time": time,
>                 "source": source,
>                 "content": content
>             })
>
>     # 组装信息
>     lines = []
>     for i, r in enumerate(results[:5], 1):
>         lines.append(
>             f"[{i}] {r['title']}\n"
>             f"来源: {r['source']}\n"
>             f"时间: {r['time']}\n"
>             f"内容: {r['content']}\n"
>         )
>
>     return "\n".join(lines)
>
> @tool
> def calc(pe, industry_avg_re, profit_growth):
>     """
>     简单估值分析,计算PEG, 当前动态的PE 行业平均PE 利润增速
>     """
>     pe = float(pe)
>     industry_avg_re = float(industry_avg_re)
>     profit_growth = float(profit_growth)
>
>     if profit_growth <= 0:
>         return f"利润增速为: {profit_growth}, PEG不适用"
>
>     peg = pe / (profit_growth * 100)
>     pe_vs_industry = (pe - industry_avg_re) / industry_avg_re
>     judgment = "可能低估" if peg < 1 else ("估值合理" if peg < 1.5 else "可能高估")
>
>     return (
>         f"PEG :{judgment}"
>         f"PE 相对行业 {'溢价' if pe_vs_industry > 0 else '折价'} {abs(pe_vs_industry):.1}%"
>     )
>
> FINANCE_TOOLS = [get_stock_basic, get_stock_news, calc]
> ```
>
> **主程序Agent**
>
> ```python
> """
> 金融投研 Multi Agent
> 数据收集员 -> 行业分析师 -> 报告撰写员 -> 风控审核员
> """
> from crewai import Agent, Task, Crew, Process, LLM
> from dotenv import load_dotenv
> import os
> from CREW_tools import FINANCE_TOOLS
>
> load_dotenv()
> llm = LLM(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),  # 17:25继续
> )
>
> # 4个agent
> data_collector = Agent(
>     role="金融数据收集员",
>     goal="收集目标股票的行情,财务指标与相关新闻,产出完整,可以直接用于分析的结构化素材",
>     backstory="你是专业金融数据专员,擅长调用工具拉去市场数据,不做主观推演,严格记录原始结果",
>     tools=FINANCE_TOOLS,
>     llm=llm,
>     verbose=True,
> )
>
> industry_analyst = Agent(
>     role="资深行业分析师",
>     goal="基于已收集的原始数据，完成行业、基本面、估值三维分析，输出带数据支撑的分析结论，同时列出风险点。",
>     backstory="拥有多年二级市场研究经验，只基于工具返回的数据开展分析，会调用估值工具计算PEG，客观看待利好与利空，不做情绪化预判。",
>     tools=FINANCE_TOOLS,
>     llm=llm,
>     verbose=True,
> )
>
> report_writer = Agent(
>     role="投研报告撰写员",
>     goal="把分析师输出的分析材料整理成格式规范的Markdown投研报告，控制篇幅，结构清晰，只复用上游产出，不新增外部事实。",
>     backstory="投行研究报告撰稿人，擅长把分析结果整理成可读性强的正式文档，严格遵循已有素材，不凭空捏造信息。",
>     llm=llm,
>     verbose=True,
> )
>
> risk_reviewer = Agent(
>     role="风控审核专家",
>     goal="审核报告事实一致性、逻辑漏洞、风险提示完备度，输出终稿，并输出修改对比表，做到每一处修改留痕可追溯。",
>     backstory="金融机构风控审核负责人，对事实错误、夸大表述零容忍，所有修改必须写明修改前、修改后、修改理由，无改动也要明确声明。",
>     llm=llm,
>     verbose=True,
> )
>
> # 4个Task
> symbol = "sh600519"
> task_collect = Task(
>     description=f"""
> 【任务背景】
> 需要完成股票{symbol}投研报告，你负责原始数据采集环节，输出给分析师使用。
>
> 【执行步骤】
> 1.调用get_stock_basic获取股票行情、财务、行业基础信息；
> 2.调用get_stock_news获取最新相关新闻；
> 3.整理全部工具返回结果，结构化输出，缺失的数据直接标注，禁止脑补。
>
> 【输出格式】
> Markdown，包含：股票基础信息块、新闻列表、备注（标注哪些字段获取失败）。
> """,
>     expected_output="结构化Markdown原始数据汇总，包含行情财务、新闻、数据缺失备注。",
>     agent=data_collector,
> )
> task_analyze = Task(
>     description=f"""
> 【任务背景】
> 已有{symbol}原始数据，需要完成专业分析。
>
> 【执行步骤】
> 1.研读数据收集员返回全部素材；
> 2.读取PE、利润增速，调用calculate_valuation完成PEG估值测算，假设行业平均PE取20；
> 3.从行业格局、公司基本面、估值水平三个维度展开；
> 4.至少列出2项潜在风险。
>
> 【输出格式】
> Markdown，包含：核心指标概览、行业与基本面分析、估值测算结果、风险提示。
> """,
>     expected_output="完整分析文档，包含指标概览、基本面、估值、风险提示。",
>     agent=industry_analyst,
>     context=[task_collect],
> )
>
> task_write_report = Task(
>     description="""
> 【任务背景】
> 分析师已经完成分析，现在生成正式投研报告初稿。
>
> 【执行步骤】
> 1.完全基于上游task_collect、task_analyze内容，禁止引入外部信息；
> 2.结构：标题、公司概况、基本面分析、估值解读、投资观点、风险提示；
> 3.输出Markdown格式。
> """,
>     expected_output="Markdown格式投研报告初稿。",
>     agent=report_writer,
>     context=[task_collect, task_analyze],
>     output_file="report_draft.md",
> )
>
> task_review = Task(
>     description="""
> 【任务背景】
> 对初稿做最终风控审核，修改记录必须完整留痕。
>
> 【执行步骤】
> 1.事实校验：逐段比对原始素材，检查是否出现编造信息；
> 2.逻辑校验：检查论证链条，删除夸大、过度乐观表述；
> 3.语言润色；
> 4.输出三部分：终稿文章、修改对比表、审校总结。
>
> 【输出格式】
> Markdown，依次输出：
> ## 一、最终定稿报告
> ## 二、修改前后条文对比表
> |序号|段落位置|修改前原文|修改后文本|修改类型(事实/逻辑/语言)|修改理由|
> ## 三、审校结论
> 如果没有任何修改，表格填写一行：全文通过，无修改。
> """,
>     expected_output="审校报告，含终稿、修改对比表、审校结论。",
>     agent=risk_reviewer,
>     context=[task_collect, task_analyze, task_write_report],
>     output_file="final_report.md",
> )
>
> # 1个团队
> crew = Crew(
>     agents=[data_collector, industry_analyst, report_writer, risk_reviewer],
>     tasks=[task_collect, task_analyze, task_write_report, task_review],
>     process=Process.sequential,
>     verbose=True,
> )
> res = crew.kickoff()
> print(res.raw)
> ```
>

%% source-id: 下001 %%

> [!quote]- 大模型全栈（下）.md · 多Agent金融分析项目
> 来源：原笔记第 3–10 行。
>
> **多Agent金融分析项目**
>
> 本打算用按照咱们在直播间约定2个周的时间给大家搞本地化再传项目的,但是咱们班级部分同学催得紧, 所以现在提前把项目放出来了,供大家研究,这回不用催了😄
>
> 祝大家前程似锦, 内容请及时下载
>
> 金融多Agent智能体项目(项目很大需要耐心研究).zip
>

## 资料与关联

- [[大模型全栈/资料/PDF/10.MultiAgent.pdf#page=21|10.MultiAgent.pdf · 第 21–32 页]]
