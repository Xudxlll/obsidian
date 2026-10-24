---
类型: 源码教学
源文件: "/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py"
阅读方式: 实际完整源码与函数核对
---

> [!info] 在项目里的职责
> 它回答“源里有哪些品种、各自有哪些可分析时点、要读哪些分区”，不计算最终预警。界面下拉来自扫描结果，中文名称表只负责标签。对压缩包按品种提取，先暂存验证再原子发布。

源码入口：[src/option_risk/catalog.py 第1行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:1>)。本篇依据最终提交目录，源码保持只读；完整逐字源码由知识库档案区保存，本篇聚焦如何理解和讲解。

## 输入、输出和上下游

AgentConfig → ProductOption 列表 / DatetimeIndex / Parquet路径列表；上游Agent与界面，下游io实际读取、清洗与特征计算。

直接导入模块：`__future__`, `hashlib`, `json`, `os`, `re`, `shutil`, `subprocess`, `tempfile`, `pathlib`, `numpy`, `pandas`, `pyarrow.parquet`, `.config`, `.contracts`, `.errors`, `.io`。


## 一个时点为什么能出现在下拉框

`_build_timestamp_index`（554—696行）逐分区只读必要列；其筛选接近实际生产清洗口径：必需列齐备、同品种、call/put、无停牌、OHLC合法、IV/Delta/Greeks/期限/moneyness范围合法，并排除IV求解下限。随后只用ATM及虚值翼，按 `datetime/underlying/dte/strike` 去重。

每个期限至少3节点，整体满足最小节点数、最少期限数和至少1个ATM节点。最后计算过去日历窗口内严格早于当前的合格快照数：

$$
N_t=\#\{s:t-L\le s<t,\ s\text{通过节点质量门槛}\}.
$$

只有 $N_t\ge\text{min_history_bars}$ 才进入目录。`searchsorted`定位窗口左端，再用当前下标相减，因此当前bar不冒充自己的历史。目录是供分析的资格筛选；最终 `assess_features` 仍检查特征的 `history_ready` 与 `data_ready`。

## 按品种提取为什么分四步

成员清单验证 → 独立暂存提取 → 精确文件集合及Parquet页脚验证 → 原子发布并写完成标记。只看到目录存在不代表提取完成；程序用完成标记记录每个成员大小，损坏或不完整就重建。`source_fingerprint`纳入修改时间和大小以使缓存变更；它并非对每个源字节作密码学承诺。

## 例子与面试追问

若ag某个时点只有一个到期月，就算有几百份期权也不能形成要求的二维期限曲面，目录不应展示。若历史只有80个合格bar而门槛是96，也不能把当前bar加成第81条历史。目录选月只做粗过滤，精确 `<=t` 必须在Agent读入后执行。

问：为什么没有把2亿多行全部读进Pandas？答：目录扫描和按品种/月份选文件先缩小范围，列投影减少读量，分析只读所需窗口。这仍可能有成本，不应宣称任意规模都能即时响应。

## 逐个类与函数查阅

每个锚点都指向当前源文件的实际定义。嵌套函数属于所在外层算法；`self`表示实例状态，不是额外业务输入。

### `_decode_process_output` · 69—75行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:69>)。依次用UTF-8/GB18030解码系统tar输出，最后替换未知字符。

输入/输出接口：`(value: bytes)` → `str`。

### `_atomic_write_text` · 78—93行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:78>)。先写同目录临时文本再原子替换。

输入/输出接口：`(path: Path, value: str, *, encoding: str='utf-8')` → `None`。

### `_atomic_write_parquet` · 96—111行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:96>)。先完整写Parquet再原子替换，避免半文件缓存。

输入/输出接口：`(frame: pd.DataFrame, path: Path)` → `None`。

### `OptionDataCatalog` · 114—723行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:114>)。目录服务类，集中管理源清单、提取缓存和有效时点。

输入/输出接口：类；共享配置/方法边界。

### `OptionDataCatalog.__init__` · 121—126行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:121>)。保存配置、创建目录并初始化内存指纹/清单/品种缓存。

输入/输出接口：`(self, config: AgentConfig)`。

### `OptionDataCatalog.source_fingerprint` · 129—152行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:129>)。按源路径/文件大小/修改时间/配置版本做16位源指纹；它不是逐字内容哈希。

输入/输出接口：`(self)` → `str`。

### `OptionDataCatalog._directory_files` · 154—160行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:154>)。发现目录下Parquet或接受一个Parquet文件路径。

输入/输出接口：`(self)` → `list[Path]`。

### `OptionDataCatalog._validate_archive_path` · 163—174行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:163>)。拒绝绝对路径、..、反斜杠、盘符、空字节等不安全成员。

输入/输出接口：`(member: str)` → `PurePosixPath`。

### `OptionDataCatalog._validated_archive_member` · 177—182行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:177>)。安全路径还须匹配赛题archive/交易所/合约/options/年/月结构。

输入/输出接口：`(cls, member: str)` → `tuple[PurePosixPath, re.Match[str]]`。

### `OptionDataCatalog._archive_members` · 184—230行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:184>)。读取或建立已校验tar成员清单，剔除非目标文件。

输入/输出接口：`(self)` → `list[str]`。

### `OptionDataCatalog._member_product` · 233—238行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:233>)。从清单中期货合约前缀取得品种代码。

输入/输出接口：`(member: str)` → `str | None`。

### `OptionDataCatalog.list_products` · 240—271行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:240>)。由目录分区和压缩包成员收集coverage，生成带中文标签的ProductOption。

输入/输出接口：`(self)` → `list[ProductOption]`。

### `OptionDataCatalog._validate_product` · 273—280行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:273>)。规范小写并检查真实可用集合，未知品种抛错。

输入/输出接口：`(self, product: str)` → `str`。

### `OptionDataCatalog._completion_marker` · 283—284行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:283>)。计算某品种提取完成标记的路径。

输入/输出接口：`(root: Path, product: str)` → `Path`。

### `OptionDataCatalog._expected_archive_paths` · 287—292行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:287>)。把经过校验的成员路径映射到提取根目录内。

输入/输出接口：`(cls, members: list[str], base: Path)` → `list[Path]`。

### `OptionDataCatalog._completed_product_files` · 295—333行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:295>)。查完成标记版本、精确文件数/大小、非符号链接、根内路径与Parquet页脚可读性。

输入/输出接口：`(cls, root: Path, product: str, members: list[str])` → `list[Path]`。

### `OptionDataCatalog._write_completion_marker` · 336—356行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:336>)。只在文件发布后写成员路径/大小清单。

输入/输出接口：`(cls, root: Path, product: str, members: list[str])` → `None`。

### `OptionDataCatalog._migrate_legacy_product_cache` · 359—388行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:359>)。旧缓存只有精确成员集合且页脚均可读才升级完成标记。

输入/输出接口：`(cls, root: Path, product: str, members: list[str])` → `list[Path]`。

### `OptionDataCatalog._selection_patterns` · 391—400行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:391>)。产生ASCII提取选择路径，兼容顶层中文目录。

输入/输出接口：`(members: list[str])` → `list[str]`。

### `OptionDataCatalog._validate_staged_files` · 403—426行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:403>)。暂存Parquet集合必须与选定成员精确一致，再查越界/链接/页脚。

输入/输出接口：`(cls, staging: Path, members: list[str])` → `list[Path]`。

### `OptionDataCatalog._publish_staged_product` · 429—451行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:429>)。逐文件原子移动后写完成标记，最后复验。

输入/输出接口：`(cls, staging: Path, root: Path, product: str, members: list[str])` → `list[Path]`。

### `OptionDataCatalog._ensure_product_extracted` · 453—511行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:453>)。按品种查可信缓存，必要时tar到独立暂存目录，校验后发布且清理暂存。

输入/输出接口：`(self, product: str)` → `list[Path]`。

### `OptionDataCatalog.product_files` · 513—538行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:513>)。先确定品种文件，再按月份与start/end窗口有交集选择；精确时点裁剪由Agent执行。

输入/输出接口：`(self, product: str, start: pd.Timestamp | None=None, end: pd.Timestamp | None=None)` → `list[Path]`。

### `OptionDataCatalog._timestamp_cache_path` · 540—552行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:540>)。将lookback与产品管线配置哈希成时间目录缓存名。

输入/输出接口：`(self, product: str)` → `Path`。

### `OptionDataCatalog._build_timestamp_index` · 554—696行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:554>)。逐分区读必要列、按生产清洗门槛筛节点、检查多期限/ATM，再计窗口内严格早于当前的历史数。

输入/输出接口：`(self, product: str)` → `pd.DataFrame`。

### `OptionDataCatalog.list_timestamps` · 698—723行

[查看定义](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py:698>)。读取/重建时间目录缓存，清理重复/无效时间并递增返回。

输入/输出接口：`(self, product: str)` → `pd.DatetimeIndex`。

## 面试先讲清楚这一问

**问：品种表是不是写死35种？**

答：不是。PRODUCT_LABELS只是显示名映射；list_products从实际目录与压缩包成员建立coverage。

继续学习：[[曲面观策项目学习与面试/02-循序学习/20 - Agent如何把一次请求变成可复核风险判断.md|20 - Agent如何把一次请求变成可复核风险判断]] → [[曲面观策项目学习与面试/02-循序学习/21 - 动态知识图谱的机制与推理边界.md|21 - 动态知识图谱的机制与推理边界]] → [[曲面观策项目学习与面试/02-循序学习/22 - 可追溯、防未来与运行身份.md|22 - 可追溯、防未来与运行身份]] → [[曲面观策项目学习与面试/02-循序学习/23 - 界面、真实案例与35品种验收.md|23 - 界面、真实案例与35品种验收]]。
