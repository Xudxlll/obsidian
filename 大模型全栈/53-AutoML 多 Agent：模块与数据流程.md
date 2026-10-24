---
type: 学习笔记
course: 大模型全栈
order: 53
stage: Agent 与协作
created: 2026-10-25
tags:
  - 课程/大模型全栈
---

[[大模型全栈/00-学习导航|返回总目录]] · 上一篇：[[大模型全栈/52-GraphRAG 合同审查综合案例|52-GraphRAG 合同审查综合案例]] · 下一篇：[[大模型全栈/54-工具权限、审计与代码执行边界|54-工具权限、审计与代码执行边界]]

> [!abstract] 学习目标
> 从多个源码文件理解一套自动建模项目。

## 核心理解

课堂 AutoML 由主管、数据、训练和评估角色协作。main 启动流程，crew 组装团队，tasks 定义任务依赖，agents 定义角色与工具，config 管理路径与模型，logger 记录运行。

工具分为数据画像与特征处理、代码执行、指标解析。读工程时应先画模块依赖，再定位每个工具的输入和产物，例如清洗后 CSV、训练日志、模型文件与报告。

建模流程还需要遵守数据隔离：先划分数据，再只在训练部分拟合预处理，最后在独立数据上评估。若为了自动化而把全体数据先编码、填充或选特征，可能引入泄漏或不一致。

模型生成并执行代码增加了灵活性，也增加了可控性要求。独立子进程加超时只能控制部分运行行为，不等于完整隔离环境。

## 课堂代码怎么读

按 main.py、crew.py、tasks.py、agents.py，再到三个 tools 文件和 logger/config 阅读。`context` 解释任务之间如何传递成果；callback 与日志用于观察中间过程。

> [!warning] 易错点与资料边界
> 原 eval_tools.py 写成 `import ref` 却调用 re，且直接索引可能不存在的 train_score、test_score、accuracy。原章节路径 tool 与导入 tools 也需统一；这些是实际源码问题，不应误归为 Agent 不智能。

## 复盘练习

为什么只解析 stdout 中的 accuracy 不足以验收模型？

> [!question]- 参考思路
> 文本可能缺字段、单位不明或由模型编造。应让训练程序输出结构化指标与数据划分信息，并核对模型文件和可复现计算。

## 课堂原始内容

以下为对应知识点的课堂原始片段，默认折叠，代码正文保留原样。

%% source-id: 下029 %%

> [!quote]- 大模型全栈（下）.md · AutoML综合项目
> 来源：原笔记第 1469–1661 行。
>
> **AutoML综合项目**
>
> **main.py**
>
> ```python
> """
> 主入口
> 加载本地数据集 -> 运行多Agent团队 -> 报告和模型
> """
> import os
> from config import IRIS_DIR, logger
> from crew import create_automl_crew
> import time
>
> crew = create_automl_crew(IRIS_DIR)
>
> start_time = time.perf_counter()
> result = crew.kickoff()
> end_time = time.perf_counter() - start_time
> logger.info(f"✅️ Crew 执行结束 | 耗时 {end_time} 秒")
> ```
>
> **crew.py**
>
> ```python
> """
> Agent任务编排
> """
> from crewai import Crew, Process
> from agents import *
> from tasks import create_tasks
> from config import logger
>
> # 回调函数
> def crew_step_callback(*args, **kwargs):
>     step = args[0] if args else None
>     try:
>         if step is not None:
>             role = getattr(step, "agent_role", None) or getattr(step, "agent", None)
>             role = getattr(role, "role", role) if role else "?"
>             action = getattr(step, "action", None) or getattr(step, "text", None) or str(step)
>
>             logger.info("▶ [%s] %s", role, str(action).replace('\n', ' '))
>     except Exception:
>         pass
>
> # 生成任务序列
> def create_automl_crew(csv_path):  
>     tasks = create_tasks(csv_path)
>     agents = [supervisor_agent, data_agent, code_agent, evaluator_agent]
>     logger.info("准备创建 crew~~")
>
>     crew = Crew(
>         agents=agents,
>         tasks=tasks,
>         process=Process.sequential,
>         verbose=True,
>         memory=False,
>         step_callback=crew_step_callback
>     )
>
>     logger.info("AutoML Crew 流水线创建完成~")
>     return crew
> ```
>
> **tasks.py**
>
> ```python
> """
> 任务定义
> """
> import os
> from crewai import Task
> from agents import *
> from config import REPORT_DIR, logger
>
> # 回调函数
> def task_callback(*args, **kwargs):
>     """
>     任务完成回调 从回调参数里去除任务描述,写入日志文件,方便回溯流水线进度
>     """
>     out = args[0] if args else None
>     desc = ""
>     try:
>         if out is not None:
>             task = getattr(out, "task", None)
>             if task is not None:
>                 desc = getattr(task, "description", None)
>             if not desc and hasattr(out, "description"):
>                 desc = out.deprecation or ""
>     except Exception as e:
>         desc = ""
>
>     desc = (desc or "未知任务").replace("\n", " ").strip()
>     logger.info(f"√ 任务完成: {desc[:30]}")
>
> def create_tasks(csv_path):
>     """根据输入 csv路径构建并返回5个串行 Task的列表"""
>     logger.info("开始构建 AutoML 任务流水线~")
>
>     # 制定方案
>     task_plan = Task(
>         description=(
>             f"分析数据集 {csv_path} 制定机器学习方案:\n"
>             f"1. 判断这是分类任务还是回归任务（根据目标列特征）\n"
>             f"2. 推荐2-3个候选模型及理由\n"
>             f"3. 建议评估指标\n"
>             f"注意:你只需要制定方案不要自己处理数据。"
>         ),
>         expected_output="一份简洁的机器学习方案:任务类型、目标列推断、候选模型列表、评估指标。",
>         agent=supervisor_agent,
>         callback=task_callback
>     )
>     logger.info(f"[任务1/5] 制定方案 -> Agent: {supervisor_agent.role}")
>
>     # 数据处理
>     task_data = Task(
>         description=(
>             f"对数据集 {csv_path} 进行完整数据处理:\n"
>             f"1. 用 load_and_profile_csv 加载并生成数据画像\n"
>             f"2. 根据画像判断目标列（通常是最后一列或名为 target/label/species 的列）\n"
>             f"3. 用 feature_engineer 执行清洗、编码、划分\n"
>             f"4. 报告处理结果和数据路径"
>         ),
>         expected_output=(
>             "数据处理报告:数据集形状、目标列、特征列、训练/测试集路径"
>             "以及处理过程中发现的数据质量问题。"
>         ),
>         agent=data_agent,
>         context=[task_plan],
>         callback=task_callback,
>     )
>     logger.info(f"[任务2/5] 数据处理 -> Agent: {data_agent.role}")
>
>     # 训练模型
>     task_train = Task(
>         description=(
>             "根据 ML 方案和处理后的数据编写并执行训练代码:\n"
>             "1. 读取 processed_train.csv 和 processed_test.csv\n"
>             "2. 根据方案选择模型（优先 RandomForest/GradientBoosting）\n"
>             "3. 训练模型print 训练集和测试集的 accuracy/f1 等指标\n"
>             "4. 用 joblib 保存模型到 models/ 目录\n"
>             "5. 如果代码报错阅读错误信息并修正后重试（最多重试2次）\n"
>             "6. 输出3个测试样本的预测示例"
>         ),
>         expected_output=(
>             "训练结果:模型名称、训练集/测试集指标、模型保存路径、3个预测示例。"
>         ),
>         agent=code_agent,
>         context=[task_plan, task_data],
>         callback=task_callback,
>     )
>     logger.info(f"[任务3/5] 模型训练 -> Agent: {code_agent.role}")
>
>     # 评估
>     task_eval = Task(
>         description=(
>             "对训练结果进行评估:\n"
>             "1. 用 evaluate_model_output 解析训练输出中的指标\n"
>             "2. 判断是否过拟合或欠拟合\n"
>             "3. 给出具体优化建议（调参/换模型/特征工程）\n"
>             "4. 给出最终评分（A/B/C/D）"
>         ),
>         expected_output="结构化评估报告:指标、泛化分析、优化建议、最终评级。",
>         agent=evaluator_agent,
>         context=[task_train],
>         callback=task_callback,
>     )
>     logger.info(f"[任务4/5] 模型评估 -> Agent: {evaluator_agent.role}")
>
>     # 验收并生成最终报告
>     report_path = os.path.join(REPORT_DIR, "training_report.md")
>     task_report = Task(
>         description=(  # 17:35 休息+练习 继续
>             "验收模型训练成果并生成最终报告:\n"
>             "1. 综合方案、数据处理、训练结果、评估结论\n"
>             "2. 判断模型是否达到可接受标准（准确率≥0.7或评级≥C）\n"
>             "3. 如果不达标指出需要改进的方向\n"
>             "4. 生成 Markdown 格式的完整训练报告包含:"
>             "数据集概况、处理方法、模型选择、训练指标、评估结论、模型路径、预测示例"
>         ),
>         expected_output="一份完整的 Markdown 训练报告保存到 training_report.md。",
>         agent=supervisor_agent,
>         context=[task_plan, task_data, task_train, task_eval],
>         output_file=report_path,
>         callback=task_callback,
>     )
>     logger.info(f"[任务5/5] 模型评估 -> Agent: {supervisor_agent.role}")
>     tasks = [task_plan, task_data, task_train, task_eval, task_report]
>     logger.info(f"任务流水线流水线构建完成,共{len(tasks)}子任务")
>     return tasks
> ```
>

%% source-id: 下030 %%

> [!quote]- 大模型全栈（下）.md · agents.py
> 来源：原笔记第 1662–2121 行。
>
> **agents.py**
>
> ```python
> """
> 主管+数据+训练+评估
> """
> from crewai import Agent
> from config import get_llm, logger
> from tools.data_tools import DATA_TOOLS
> from tools.code_tools import CODE_TOOLS
> from tools.eval_tools import EVAL_TOOLS
>
> # 主管Agent 负责全局调度和最终验收
> supervisor_agent = Agent(
>     role="Auto ML 项目主管",
>     goal=(
>         "分析数据集特征,制定合适的机器学习方案(判断分类/回归,选择候选模型。)"
>         "并在训练完成后验收最终成果,确保模型质量达标。"
>     ),
>     backstory=(
>         "你是一个资深的 机器学习ML 技术负责人,擅长根据数据特点快速定制建模方案。"
>         "你熟悉各种算法的适用场景, 对模型的质量有严格的评估标准。"
>         "你的职责是前期定方向,后期质量把关。"
>     ),
>     llm=get_llm(),
>     allow_delegation=True,
>     verbose=True,
>     max_iter=5
> )
>
> # Data Agent：数据处理
> data_agent = Agent(
>     role="数据工程师",
>     goal="完成数据加载、数据画像、清洗和特征工程，产出可直接用于建模的训练/测试集",
>     backstory=(
>         "你是一位严谨的数据工程师，精通 pandas 和 scikit-learn 预处理。"
>         "你知道垃圾进垃圾出，所以总是先仔细分析数据质量再做处理。"
>         "你会妥善处理缺失值、编码分类变量，并合理划分数据集。"
>     ),
>     tools=DATA_TOOLS,
>     llm=get_llm(),
>     allow_delegation=False,
>     verbose=True,
>     max_iter=5,
> )
>
> # Code Agent：模型训练
> code_agent = Agent(
>     role="机器学习工程师",
>     goal="根据方案选择合适模型，编写并执行训练代码，遇到报错自主调试修复，最终保存模型",
>     backstory=(
>         "你是一位实战经验丰富的 ML 工程师，精通 scikit-learn。"
>         "你擅长根据任务类型选择模型(分类用 RandomForest/GradientBoosting，"
>         "回归用 RandomForestRegressor 等)，代码规范，"
>         "遇到报错会阅读错误信息、定位问题、修正代码重新执行，从不放弃。"
>         "训练完成后会把模型保存为 joblib 文件，并 print 评估指标。"
>     ),
>     tools=CODE_TOOLS,  # 授予 execute_python_code(安全沙箱执行)
>     llm=get_llm(),
>     allow_delegation=False,
>     verbose=True,
>     max_iter=8,
> )
>
> # Evaluator Agent：模型评估
> evaluator_agent = Agent(
>     role="模型评估专家",
>     goal="客观评估模型表现，诊断过拟合/欠拟合，给出具体的优化建议",
>     backstory=(
>         "你是一位严格的模型评审专家，只看数据不看情面。"
>         "你会从准确率、泛化能力、效率多个维度评估模型，"
>         "并给出可操作的改进建议(调参方向、特征建议、模型替换建议)。"
>     ),
>     tools=EVAL_TOOLS,
>     llm=get_llm(),
>     allow_delegation=False,
>     verbose=True,
>     max_iter=4,
> )
>
> # 团队就绪日志
> logger.info(
>     "AutoML 团队已就绪 | Supervisor(委派=%s, max_iter=%d) / Data(max_iter=%d) / "
>     "Code(max_iter=%d) / Evaluator(max_iter=%d)",
>     supervisor_agent.allow_delegation, supervisor_agent.max_iter,
>     data_agent.max_iter, code_agent.max_iter, evaluator_agent.max_iter,
> )
> ```
>
> **tool/eval_tools.py**
>
> ```python
> """
> 评估工具:从代码的 stdout 出解释指标
> """
> import ref
> import logging
> from crewai.tools import tool
>
> logger = logging.getLogger(__name__)
>
> @tool("evaluate_model_output")
> def evaluate_model_output(training_output):
>     """解释训练输出中的评估指标,给出综合评价和改进建议"""
>     metrics = {}
>     patterns = {
>         # (?:) 非捕获组 只做匹配
>         "accuracy": r"(?:accuracy|准确率|Accuracy)[^\d]*([0-9.]+)",
>         "f1": r"(?:f1|F1)[^\d]*([0-9.]+)",
>         "precision": r"(?:precision|精确率)[^\d]*([0-9.]+)",
>         "recall": r"(?:recall|召回率)[^\d]*([0-9.]+)",
>         "train_score": r"(?:train(?:ing)?(?:_score)?|训练集)[^\d]*([0-9.]+)",
>         "test_score": r"(?:test(?:_score)?|测试集)[^\d]*([0-9.]+)",
>     }
>
>     for key, pattern in patterns.items():
>         match = re.search(pattern, training_output, re.IGNORECASE)
>         if match:
>             try:
>                 metrics[key] = float(match.group(1))
>             except ValueError:
>                 pass
>     if not metrics:
>         return "没有从输出内容中解析到评估指标"
>     # 组装报告文本
>     lines = ["模型评估报告:"]
>     for k, v in metrics.items():
>         lines.append(f"{k}: {v:.4f}")
>
>     # 过拟合/欠拟合诊断
>     gap = metrics["train_score"] - metrics["test_score"]
>     if gap > 0.15:
>         lines.append(f"\n ⚠️ 过拟合风险")
>     elif metrics["train_score"] < 0.6:
>         lines.append(f"\n ⚠️ 欠拟合风险")
>     else:
>         lines.append(f"\n ✅️ 泛化良好~")
>
>     acc = metrics["accuracy"]
>     if acc > 0.9:
>         lines.append("综合评级: 优秀A")
>     elif acc >= 0.7:
>         lines.append("综合评级: 良好B")
>     else:
>         lines.append("综合评级: 较差C")
>     return "\n".join(lines)
>
> EVAL_TOOLS = [evaluate_model_output]
> ```
>
> **tool/code_tools.py**
>
> ```python
> """
> 安全代码执行工具:在独立的子进程中跑 python
> """
> import os
> import sys
> import subprocess
> import tempfile
> from crewai.tools import tool
> from config import CODE_EXEC_TIMEOUT, logger
>
> @tool("execute_python_code")
> def execute_python_code(code, description=""):
>     """
>     在安全沙箱中执行Python代码并返回结果
>     """
>     with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
>         f.write(code)
>         temp_path = f.name
>
>     try:
>         result = subprocess.run(
>             [sys.executable, temp_path],
>             capture_output=True,
>             text=True,  # 返回字符串
>             encoding="utf-8",
>             errors="replace",
>             timeout=CODE_EXEC_TIMEOUT,
>             cwd=os.path.dirname(temp_path),
>             env={
>                 **os.environ,
>                 "MPLBACKEND": "Agg",
>                 "PYTHONIOENCODING": "utf-8",
>             }
>         )
>         output = result.stdout  # 脚本的所有print输出
>
>         if result.returncode != 0:
>             error_msg = result.stderr[-1500:]
>             logger.waring(f"代码执行失败: {result.returncode}: {error_msg}")
>             return f"代码执行失败: {result.returncode}: {error_msg}"
>         # 代码执行成功但没有输出
>         if not output.strip():
>             return "代码执行成功,但无输出"
>
>         return output[:3000]
>     except Exception as e:
>         return f"执行异常:{e}"
>     finally:
>         os.unlink(temp_path)
>
> CODE_TOOLS = [execute_python_code]
> ```
>
> **tool/data_tools.py**
>
> ```python
> """
> 数据工具集: 加载CSV 数据画像 特征工程 数据集划分
> """
> import os
> import logging
> import pandas as pd
> from crewai.tools import tool
>
> logger = logging.getLogger(__name__)
>
> @tool("load_and_profile_csv")
> def load_and_profile_csv(filepath):
>     """加载 CSV文件并生成数据画像"""
>     try:
>         df = pd.read_csv(filepath)
>         profile = []
>         profile.append(f"数据集形状: {df.shape[0]}行 x {df.shape[1]}列 ")
>         profile.append("列信息:")
>         for col in df.columns:
>             dtype = df[col].dtype
>             missing = df[col].isnull().sum()
>             unique = df[col].nunique()
>             profile.append(f" - {col}: 类型={dtype},缺失={missing}({missing / len(df):.1%}),唯一值={unique}")
>         profile.append("数值列统计:")
>         profile.append(df.describe().to_string())
>         profile.append("前5行样本:")
>         profile.append(df.head(5).to_string())
>         profile_path = os.path.join(os.path.dirname(filepath), "data_profile.txt")
>         with open(profile_path, "w", encoding="utf-8") as f:
>             f.write("\n".join(profile))
>         logger.info(f"数据画像完成~ 已保存")
>         return "\n".join(profile)
>     except Exception as e:
>         logger.error(f"CSV 加载失败:{e}")
>         return f"加载失败:{e}"
>
> @tool("feature_engineer")
> def feature_engineer(file_path, target_column):
>     """
>     执行数据清洗和特征工程:处理缺失值,编码分类变量,划分训练/测试集
>     """
>     try:
>         df = pd.read_csv(file_path)
>         # 分离特征和标签 x 特征矩阵 y 标签向量
>         x = df.drop(columns=target_column)
>         y = df[target_column]
>
>         # 缺失值
>         for col in x.select_dtypes(include=['number']).columns:
>             x[col] = x[col].fillna(x[col].median())
>         for col in x.select_dtypes(exclude=['number']).columns:
>             x[col] = x[col].fillna(x[col].mode()[0] if not x[col].mode().empty else "unknown")
>
>         # 分类变量用标签编码/独热编码 变数字
>         from sklearn.preprocessing import LabelEncoder, OneHotEncoder
>         for col in x.select_dtypes(exclude=['number']).columns:
>             x[col] = LabelEncoder().fit_transform(x[col].astype(str))
>
>         if y.dtype == "object":
>             y = LabelEncoder().fit_transform(y.astype(str))
>
>         # 分层抽样
>         counts = pd.Series(y).value_counts()
>         stratify = y if (len(counts) < 50 and counts.min() >= 2) else None
>         from sklearn.model_selection import train_test_split
>         x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=42, stratify=stratify)
>
>         # 把特征和标签拼接,分别保存数据集
>         out_dir = os.path.dirname(file_path)
>         train_df = pd.concat(
>             [x_train, pd.Series(y_train, name=target_column)], axis=1
>         )
>         test_df = pd.concat(
>             [x_test, pd.Series(y_test, name=target_column)], axis=1
>         )
>
>         train_path = os.path.join(out_dir, "processed_train.csv")
>         test_path = os.path.join(out_dir, "processed_test.csv")
>         train_df.to_csv(train_path, index=False)
>         test_df.to_csv(test_path, index=False)
>
>         result = (
>             f"特征工程完成:\n"
>             f"- 训练集: {x_train.shape}, 测试集: {x_test.shape}\n"
>             f"- 特征列: {list(x.columns)}\n"
>             f"- 目标列: {target_column}, 类别数: {len(set(y))}\n"
>             f"- 训练集路径: {train_path}\n"
>             f"- 测试集路径: {test_path}"
>         )
>         logger.info(result.replace("\n", " "))
>         return result
>     except Exception as e:
>         logger.error(f"特征工程失败: {e}")
>         return f"特征工程失败: {e}"
>
> DATA_TOOLS = [load_and_profile_csv, feature_engineer]
> ```
>
> **logger.py**
>
> ```python
> """
> 日志模块(源自于班级同学提供的很哇塞的日志)
>
> 做了一点改进:
> 1.BASE_DIR  LOG_DIR需要按照项目走
> 2.配置root logger 所有模块都能自动继承,不用一个一个调方法了
> """
> import sys
> import logging
> from logging.handlers import TimedRotatingFileHandler
> from pathlib import Path
>
> # 配置日志区域
> # 1.定义日志保存路径
> BASE_DIR = Path(__file__).resolve().parent
> LOG_DIR = BASE_DIR / "logs"
> LOG_DIR.mkdir(parents=True, exist_ok=True)
>
> # 2.定义日志格式
> # 文件格式：[时间][级别][文件名:行号] - 消息
> FILE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
> # 控制台格式（不带文件名:行号，保持清爽）
> CONSOLE_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
>
> # 彩色日志格式器（仅显示在控制台）
> class ColoredFormatter(logging.Formatter):
>     """继承后重写 format 方法，控制台日志带颜色方便调试，使用 ANSI 转义码。"""
>     grey = "\x1b[38;21m"
>     green = "\x1b[32;21m"
>     yellow = "\x1b[33;21m"
>     red = "\x1b[31;21m"
>     bold_red = "\x1b[31;1m"  # 加粗红色
>     reset = "\x1b[0m"  # 重置颜色，否则后面所有字都会变色
>
>     format_str = CONSOLE_FORMAT
>     FORMATS = {
>         logging.DEBUG: grey + format_str + reset,
>         logging.INFO: green + format_str + reset,
>         logging.WARNING: yellow + format_str + reset,
>         logging.ERROR: red + format_str + reset,
>         logging.CRITICAL: bold_red + format_str + reset,
>     }
>
>     def format(self, record):
>         # 根据当前日志的级别，去字典查对应的颜色格式
>         log_fmt = self.FORMATS.get(record.levelno)
>         # 创建一个临时的标准格式器
>         formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
>         return formatter.format(record)
>
> # 初始化 root logger（全局只配置一次）
> _ROOT_CONFIGURED = False
>
> def setup_logging():
>     """把控制台 / app.log / error.log 三个 handler 挂到 root logger 上。"""
>     global _ROOT_CONFIGURED
>     if _ROOT_CONFIGURED:
>         return
>
>     root = logging.getLogger()
>     root.setLevel(logging.DEBUG)  # 总开关设为最低，由每个 handler 决定具体过滤
>
>     # 控制台 handler（彩色，INFO 以上）
>     console_handler = logging.StreamHandler(sys.stdout)  # 输出到标准输出
>     console_handler.setLevel(logging.INFO)  # 只看 info 以上，格式彩色
>     console_handler.setFormatter(ColoredFormatter())
>     root.addHandler(console_handler)
>
>     # 通用日志（每天轮转，保留 30 天，INFO 以上）
>     app_handler = TimedRotatingFileHandler(
>         filename=str(LOG_DIR / "app.log"),
>         when="midnight",  # 半夜切割
>         interval=1,  # 一天切割一次
>         backupCount=30,  # 只保留 30 天
>         encoding="utf-8",  # 编码防止中文乱码
>     )
>     app_handler.setLevel(logging.INFO)  # info 以上写入文件
>     app_handler.setFormatter(logging.Formatter(FILE_FORMAT))
>     root.addHandler(app_handler)
>
>     # 错误日志（每天轮转，保留 60 天，ERROR 以上）
>     error_handler = TimedRotatingFileHandler(
>         filename=str(LOG_DIR / "error.log"),
>         when="midnight",
>         interval=1,
>         backupCount=60,
>         encoding="utf-8",
>     )
>     error_handler.setLevel(logging.ERROR)
>     error_handler.setFormatter(logging.Formatter(FILE_FORMAT))
>     root.addHandler(error_handler)
>
>     # 压低第三方库日志，避免刷屏
>     for lib in ("crewai", "openai", "httpx", "urllib3", "sentence_transformers"):
>         logging.getLogger(lib).setLevel(logging.WARNING)
>
>     _ROOT_CONFIGURED = True
>
> def get_logger(name="automl"):
>     """获取配置好的 logger 实例（会自动确保 root 已初始化）。"""
>     setup_logging()
>     return logging.getLogger(name)
>
> # 模块被 import 时立即初始化一次，保证任何地方 print 不出来也能落盘
> setup_logging()
> ```
>
> **config.py**
>
> ```python
> """
> 全局配置 LLM 路径 日志 Embedding
> """
> import os
> import logging
> from dotenv import load_dotenv
> from logger import get_logger
>
> load_dotenv()
> logger = get_logger("automl")
>
> # 路径配置
> BASE_DIR = os.path.dirname(os.path.abspath(__file__))
> DATA_DIR = os.path.join(BASE_DIR, 'data')
> WORKSPACE_DIR = os.path.join(BASE_DIR, 'workspace')
> MODEL_DIR = os.path.join(WORKSPACE_DIR, 'models')
> REPORT_DIR = os.path.join(WORKSPACE_DIR, 'reports')
> IRIS_DIR = os.path.join(DATA_DIR, '鸢尾花数据集.csv')
> os.makedirs(REPORT_DIR, exist_ok=True)
> os.makedirs(MODEL_DIR, exist_ok=True)
> os.makedirs(DATA_DIR, exist_ok=True)
>
> # 大模型与Embedding
> def get_llm():
>     from crewai import LLM
>     return LLM(
>         model="deepseek-chat",
>         api_key=os.getenv("DEEPSEEK_API_KEY"),
>         base_url=os.getenv("DEEPSEEK_BASE_URL"),
>         temperature=0.1,
>         timeout=60
>     )
>
> EMBEDDING_MODEL = "./bge-base-zh-v1.5"
>
> # 代码安全配置
> CODE_EXEC_TIMEOUT = 60
> MAX_CODE_RETRIES = 3
> ```
>

## 资料与关联

- [[大模型全栈/资料/PDF/10.MultiAgent.pdf#page=16|10.MultiAgent.pdf · 第 16–21 页]]
- 关联知识：[[大模型全栈/47-Multi-Agent 与 CrewAI 基础|47-Multi-Agent 与 CrewAI 基础]]、[[大模型全栈/54-工具权限、审计与代码执行边界|54-工具权限、审计与代码执行边界]]。
