---
type: 学习笔记
course: 大模型全栈
order: 44
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/43-Agent、ReAct 与 Self-Ask|43-Agent、ReAct 与 Self-Ask]] · 下一篇：[[大模型全栈/45-金融研报：LangGraph 规划与工具执行|45-金融研报：LangGraph 规划与工具执行]]

> [!abstract] 学习目标
> 先把目标转成可执行步骤，再逐步验证产物。

## 核心理解

Plan-and-Execute 将规划器与执行器分开：规划器提出步骤，执行器按依赖调用工具并产生产物，最后汇总或重新规划。适合步骤较多、需要追踪进度的任务。

课堂示例为内容生产先列章节，再逐节生成并检查限制词。这个检查展示了独立验证步骤，但只覆盖字符串规则，不能据此认定内容全面合规或事实正确。

一个有用的步骤应说明输入、动作、输出与验收条件。例如“分析数据”太宽泛，“读取 CSV 并输出缺失率表”更容易执行与检查。

计划也不能僵化。工具失败、资料缺失或新证据改变目标时，应允许局部调整，同时保留原计划、修改原因和已完成产物，避免重做全部工作。

## 课堂代码怎么读

按 plan_prompt、解析步骤、工具映射、生成章节和检查结果顺序阅读。观察检查失败后代码是否真正修正或重试，而不是只把错误打印出来。

> [!warning] 易错点与资料边界
> 按行拆模型输出可能把序号与解释当任务。原代码采用教学级计划解析与规则检查，没有实现完整依赖调度、质量保证或生产重试体系。

## 复盘练习

什么时候固定工作流比 Agent 自主规划更合适？

> [!question]- 参考思路
> 步骤稳定、规则明确、结果可验证时，固定工作流通常更容易测试和控制；只有确实需要动态选择动作时，规划的额外成本才更有意义。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下045 %%

> [!quote]- 大模型全栈（下）.md · 规划分解
> 来源：原笔记第 3579–3670 行。
>
> **规划分解**
>
> ```python
> """
> 规划分解
> """
> import os
> from dotenv import load_dotenv
> from langchain_openai import ChatOpenAI
> from langchain_core.tools import tool
>
> load_dotenv()
> llm = ChatOpenAI(
>     model="deepseek-chat",
>     api_key=os.getenv("DEEPSEEK_API_KEY"),
>     base_url=os.getenv("DEEPSEEK_BASE_URL"),
>     temperature=0
> )
>
> @tool
> def generate_section(section_name, goal):
>     """生成指定模块的活动方案内容,参数为模块名称和总目标"""
>     propmt = f"请围绕总目标 {goal}, 撰写 {section_name} 模块的详细方案与内容,200字以内,可以用极限词"
>
>     return llm.invoke(propmt).content
>
> @tool
> def compliance_check(content):
>     """合规性检验工具,检查内容是否符合宣传规范"""
>     if "最" in content or "顶级" in content:
>         return "校验不通过,存在极限词"
>     return "校验通过"
>
> tool_map = {
>     generate_section.name: generate_section,
>     compliance_check.name: compliance_check
> }
>
> # 执行
> def plan_execute(goal):
>     print(f"[规划分解]🎯: {goal}\n")
>     plan_prompt = f"""请将任务{goal}拆分成若干个可独立执行的子任务。
>     要求：
>     - 根据任务复杂度决定数量，最少2个，最多6个
>     - 按执行先后顺序排列
>     - 每行一个，严格格式：序号.子任务名称
>     - 只输出任务列表，不要解释"""
>
>     plan_raw = llm.invoke(plan_prompt).content.splitlines()
>     plan = [
>         line.split(".", 1)[1]
>         for line in plan_raw
>         if "." in line
>     ]
>     print(f"📝 自动拆解规划出{len(plan)}个子任务")
>     for i, t in enumerate(plan, 1):
>         print(f" {i}.{t}")
>     print()
>
>     final_content = ""
>     max_retry = 2
>
>     for idx, task in enumerate(plan, 1):
>         retry = 0
>         while retry <= max_retry:
>             print(f" 🎬 执行子任务 {idx}/{len(plan)}: {task} (第{retry + 1}次)")
>             section = tool_map["generate_section"].invoke({
>                 "section_name": task,
>                 "goal": goal
>             })
>             print(f"   生成内容: {section}\n")
>
>             # 检查点
>             check_res = tool_map["compliance_check"].invoke({"content": section})
>             print(f"  检验结果:{check_res}")
>
>             if "不通过" not in check_res:
>                 final_content += f" {task}\n {section}\n"
>                 print(f"👍 子任务通过,进入下一个~")
>                 break
>             else:
>                 retry += 1
>                 if retry > max_retry:
>                     print(f"❌ 多次校验失败,触发回溯,重新生成")
>                 else:
>                     print("f⚠️ 校验不通过,请修正\n")
>
>     return final_content
>
> print(plan_execute("生成一份校园社团招新活动方案"))
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/8.Create_Agent.pdf#page=26|8.Create_Agent.pdf · 第 26–37 页]]
