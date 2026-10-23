---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/cli.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **给部署与离线实验提供明确命令入口**。同一个option-risk命令通过子命令进入不同的执行链。

源文件：[src/option_risk/cli.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/cli.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

用户/部署传入命令行参数，CLI把它们转为Config并调用Agent、Pipeline或验收器；它不是风控计算模块。输出一般为JSON，validate还写报告，serve启动Streamlit子进程。入口来自pyproject.toml的option-risk映射。

## 逐个理解核心对象与函数

### `build_parser`（18—50 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/cli.py:18>)

创建required子命令：catalog列目录，analyze需product/timestamp，run需data-dir/output-dir并可选product/日期，serve可选port默认8501，validate可选catalog-only/products/report。run与Agent类命令用不同参数约束。

### `_add_agent_source_arguments`（53—57 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/cli.py:53>)

给catalog/analyze/serve/validate添加可选data-dir、archive-path、cache-dir、output-dir，其中默认cache为data/agent_cache、output为outputs。网页用户不应通过任意路径输入替代部署配置。

### `_agent_config`（60—69 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/cli.py:60>)

要求data-dir和archive-path至少有一个，否则parser.error退出；没有data-dir时使用cache/archive_source，把路径交AgentConfig。这里只建立配置，不负责解压或校验归档内容。

### `_product_payload`（72—79 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/cli.py:72>)

对agent.list_products的dataclass做asdict，再把start/end转换ISO字符串，返回product_count及products，方便机器与网页消费。

### `main`（82—142 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/cli.py:82>)

parse_args后，run直接调run_pipeline打印summary；其他分支先建AgentConfig。catalog建Agent列目录，analyze精确分析请求时点，validate调validate_deployment并将进度打stderr、报告存独立JSON，summary.status==passed时退出0，否则1；serve复制环境注入四个OPTION_RISK路径，通过当前Python执行streamlit dashboard.py并返回子进程退出码。未知命令由parser.error处理。

## 关键推导、具体例子与真实边界

想理解使用关系，可按三组阅读：`catalog→analyze`验证数据可选性与单点分析；`run`产生完整离线报告；`serve`把同一个Agent包装进网页；`validate`负责部署验收。`validate --catalog-only`明确不执行完整曲面分析，目录验收通过不能改口为所有品种全功能验收通过。

`subprocess.run(check=False)`不会因为网页进程非零自动抛CalledProcessError，而是把returncode返回；因此终端退出码仍应被部署方记录。CLI没有实现网络交易所行情订阅和自动定时调度，analyze是请求驱动的历史时点/当前数据截点分析。

## 面试怎么讲，追问怎么答

**问：命令能启动就代表系统全部可用吗？** 只能说明入口可解析或进程启动；还要确认实际品种、历史准备、曲面、证据、图谱与数据身份等条件。

**问：目录模式和完整验收差别？** 目录只证明有可选时点范围，完整模式还会让Agent真实生成响应。

## 下一步学习

[[02-循序学习/核心08-离线Pipeline与单时点Agent的完整关系]]
