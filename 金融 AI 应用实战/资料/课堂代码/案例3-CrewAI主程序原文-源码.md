---
type: 课堂原始代码
---

```python
"""
金融投研 Multi Agent
数据收集员 -> 行业分析师 -> 报告撰写员 -> 风控审核员
"""
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os
from CREW_tools import FINANCE_TOOLS

load_dotenv()
llm = LLM(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),  # 17:25继续
)

# 4个agent
data_collector = Agent(
    role="金融数据收集员",
    goal="收集目标股票的行情,财务指标与相关新闻,产出完整,可以直接用于分析的结构化素材",
    backstory="你是专业金融数据专员,擅长调用工具拉去市场数据,不做主观推演,严格记录原始结果",
    tools=FINANCE_TOOLS,
    llm=llm,
    verbose=True,
)

industry_analyst = Agent(
    role="资深行业分析师",
    goal="基于已收集的原始数据，完成行业、基本面、估值三维分析，输出带数据支撑的分析结论，同时列出风险点。",
    backstory="拥有多年二级市场研究经验，只基于工具返回的数据开展分析，会调用估值工具计算PEG，客观看待利好与利空，不做情绪化预判。",
    tools=FINANCE_TOOLS,
    llm=llm,
    verbose=True,
)

report_writer = Agent(
    role="投研报告撰写员",
    goal="把分析师输出的分析材料整理成格式规范的Markdown投研报告，控制篇幅，结构清晰，只复用上游产出，不新增外部事实。",
    backstory="投行研究报告撰稿人，擅长把分析结果整理成可读性强的正式文档，严格遵循已有素材，不凭空捏造信息。",
    llm=llm,
    verbose=True,
)

risk_reviewer = Agent(
    role="风控审核专家",
    goal="审核报告事实一致性、逻辑漏洞、风险提示完备度，输出终稿，并输出修改对比表，做到每一处修改留痕可追溯。",
    backstory="金融机构风控审核负责人，对事实错误、夸大表述零容忍，所有修改必须写明修改前、修改后、修改理由，无改动也要明确声明。",
    llm=llm,
    verbose=True,
)

# 4个Task
symbol = "sh600519"
task_collect = Task(
    description=f"""
【任务背景】
需要完成股票{symbol}投研报告，你负责原始数据采集环节，输出给分析师使用。

【执行步骤】
1.调用get_stock_basic获取股票行情、财务、行业基础信息；
2.调用get_stock_news获取最新相关新闻；
3.整理全部工具返回结果，结构化输出，缺失的数据直接标注，禁止脑补。

【输出格式】
Markdown，包含：股票基础信息块、新闻列表、备注（标注哪些字段获取失败）。
""",
    expected_output="结构化Markdown原始数据汇总，包含行情财务、新闻、数据缺失备注。",
    agent=data_collector,
)
task_analyze = Task(
    description=f"""
【任务背景】
已有{symbol}原始数据，需要完成专业分析。

【执行步骤】
1.研读数据收集员返回全部素材；
2.读取PE、利润增速，调用calculate_valuation完成PEG估值测算，假设行业平均PE取20；
3.从行业格局、公司基本面、估值水平三个维度展开；
4.至少列出2项潜在风险。

【输出格式】
Markdown，包含：核心指标概览、行业与基本面分析、估值测算结果、风险提示。
""",
    expected_output="完整分析文档，包含指标概览、基本面、估值、风险提示。",
    agent=industry_analyst,
    context=[task_collect],
)

task_write_report = Task(
    description="""
【任务背景】
分析师已经完成分析，现在生成正式投研报告初稿。

【执行步骤】
1.完全基于上游task_collect、task_analyze内容，禁止引入外部信息；
2.结构：标题、公司概况、基本面分析、估值解读、投资观点、风险提示；
3.输出Markdown格式。
""",
    expected_output="Markdown格式投研报告初稿。",
    agent=report_writer,
    context=[task_collect, task_analyze],
    output_file="report_draft.md",
)

task_review = Task(
    description="""
【任务背景】
对初稿做最终风控审核，修改记录必须完整留痕。

【执行步骤】
1.事实校验：逐段比对原始素材，检查是否出现编造信息；
2.逻辑校验：检查论证链条，删除夸大、过度乐观表述；
3.语言润色；
4.输出三部分：终稿文章、修改对比表、审校总结。

【输出格式】
Markdown，依次输出：
## 一、最终定稿报告
## 二、修改前后条文对比表
|序号|段落位置|修改前原文|修改后文本|修改类型(事实/逻辑/语言)|修改理由|
## 三、审校结论
如果没有任何修改，表格填写一行：全文通过，无修改。
""",
    expected_output="审校报告，含终稿、修改对比表、审校结论。",
    agent=risk_reviewer,
    context=[task_collect, task_analyze, task_write_report],
    output_file="final_report.md",
)

# 1个团队
crew = Crew(
    agents=[data_collector, industry_analyst, report_writer, risk_reviewer],
    tasks=[task_collect, task_analyze, task_write_report, task_review],
    process=Process.sequential,
    verbose=True,
)
res = crew.kickoff()
print(res.raw)

```
