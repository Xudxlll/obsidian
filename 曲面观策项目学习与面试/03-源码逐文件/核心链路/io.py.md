---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/io.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **在分区可能污染时仍按合约重新识别品种**。目录只是第一道过滤，合约代码才是第二道数据证据。

源文件：[src/option_risk/io.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/io.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入：一个 Parquet 文件或递归目录、品种、可选起止日期。输出：拼接后的 pandas DataFrame 与 ingest_profile。主键尚未去重，质量尚未过滤。`read_option_files → clean_and_profile` 是明确的责任边界。

## 逐个理解核心对象与函数

### `discover_parquet_files`（39—46 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/io.py:39>)

若参数本身是后缀 .parquet 的文件则直接返回；否则递归找 *.parquet 并排序，无文件则抛异常。后缀为 .parquet.bak 的文件本来就不匹配该 glob，额外 endswith(.bak) 是一道保护。不会识别合并文件和 archive 分区是否包含相同数据，两个副本一起输入会增加扫描与去重负担。

### `contract_product`（49—50 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/io.py:49>)

先转 pandas 字符串，再提取合约开头连续英文字母并转小写。例如 AG2406C6000 → ag；无字母前缀可能得到缺失值。这里不解析执行价和期权类型。

### `_available_columns`（53—54 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/io.py:53>)

只读 Parquet 元数据 schema，不先把全表载入；返回列名集合，用于每文件读取前的结构检查。

### `partition_product`（57—62 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/io.py:57>)

从路径末尾向前查完全匹配“字母+3或4位数字”的目录部分，例如 ag2406 → ag。若任意路径部分无法匹配则返回 None，不能仅凭路径过滤。

### `read_option_files`（65—136 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/io.py:65>)

逐文件先按路径品种跳过明显无关分区；再检查 `READ_COLUMNS` 全部24列是否存在，缺一列就跳过整文件并记录原因。随后 PyArrow 选择这24列读取、转 pandas，统计扫描行数与 schema 变体，再从 contract 提取 product，过滤掉污染行。时间戳按 `%Y%m%d%H%M%S` 解析，无法解析变 NaT；日期筛选是开始日闭区间、结束日加一天后的开区间。非空数据添加 source_file 后累计，最终拼接。无任何目标行则抛 ValueError。profile 中 rows_after_product_filter 实际也已经过日期过滤，不能仅从字段名字理解统计口径。

## 关键推导、具体例子与真实边界

若路径 ag2406/part.parquet 内有 100 行 ag 与 5 行 cu，目录初筛会允许读取，合约筛选留下100行。若文件在 cu2406 目录内却有 ag 污染行，这个函数会整文件按路径跳过；它不是全库污染修复器。

24列选择读取节省列宽，但 `pq.read_table` 在此没有日期 filters 下推，日期是转 pandas 后才筛；所有所选文件的目标行最终仍累计在内存中。不能把此实现说成“全流程流式/零拷贝/全量数据无需内存”。原始数据有两亿行时应按品种与时间分区取数，勿把整库无差别传入。

时间戳为本地无时区的 pandas 时间；`timezone` 没有在本模块应用。schema_variants 只记录类型组合，不会把变体自动迁移为统一标准。

## 面试怎么讲，追问怎么答

**问：为什么目录过滤后再查 contract？** 因为分区可能混入其他品种，必须防止把其他资产的报价组成同一截面。

**问：为什么缺 open 也跳文件，清洗核心字段却不含 open？** 入口要求24列“存在”，清洗要求核心字段“每行非空”，结构完整与行级完整是两道不同检查。

**问：文件乱序会影响曲面吗？** 后续显式 groupby 与排序；不依赖文件物理相邻行代表同一个曲面。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心01-从一条期权报价到可分析的干净样本.md|核心01-从一条期权报价到可分析的干净样本]]
