---
tags: [曲面观策, 源码逆向, 状态机, 可复现, 产物验证]
source: src/option_risk/surface_fit_diagnostics.py
source_lines: 5347
read_scope: 全文件逐块阅读
---

> [!abstract] 文件定位
> 前半部分把单时点节点规范化并运行两阶段期限选择，正式IV曲面复用这一引擎；后半部分是AG专用批量诊断的装载、分层抽样、严格缓存、统计、画图与六件产物发布。不能因文件名带 diagnostics 或字段 `diagnostic_only=True` 就断言所有函数都不参与正式运行。

源文件：[surface_fit_diagnostics.py](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1)。上下游：[[曲面观策项目学习与面试/03-源码逐文件/曲面拟合/total_variance_fit.py-总方差公式、优化与本地检查.md|total_variance_fit.py-总方差公式、优化与本地检查]]，正式调用见 [surfaces.py](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surfaces.py:51)。

## 1. 真正的公共入口与死路径排查

`diagnose_timestamp` [1170](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1170)是单时点引擎；`run_ag_fit_diagnostics` [5205](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:5205)是AG专用批处理。后者通过缓存builder调用前者，前者不调用后者。

正式入口 `surface_grid(metric="iv")` 直接调用 `diagnose_timestamp`，不会通过 `_load_ag_input`、缓存或六件产物发布。该分离解释了文件首部说明。画图标题的“not used in formal warning”指独立比较图/批量诊断产物，不应扩展成“拟合算法没接正式管线”。

顶层AST核查没有同名函数/类重定义；`__all__` [5327](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:5327)列出正式导出名称。嵌套的 `reserve/process_candidate/build_fallback/builder` 是当前调用内部的闭包，不能误认为后段同名实验版本覆盖公共入口。

## 2. 三层输入错误：结构错误、行级排除、时点失败

`_REQUIRED_INPUT_COLUMNS` 要求9列：product、datetime、dte、time_to_expiry、strike、iv、log_moneyness、forward_price、forward_source。

`_validate_call_schema` [365](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:365)把这些视作调用约定：DataFrame类型、必需列、每行产品/时点、dte精确整数、来源枚举，以及代理/未知来源不允许带forward_price。违反结构约定直接抛ValueError，不悄悄丢行。

`prepare_timestamp_nodes` [463](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:463)再按固定次序对数值内容做排除，每行只计第一个失败：

| 阶段 | 排除码 | 细节 |
|---|---|---|
| 行权价 | invalid_strike | 有限且正，布尔不能冒充数字 |
| 真实远期 | invalid_forward | 仅真实远期分支要求有限且正 |
| IV | invalid_iv | IV正；最终 $\mathrm{IV}^2T$ 溢出或非正也记此码 |
| 期限 | invalid_time_to_expiry | 有限且正 |
| 横轴 | invalid_log_moneyness | 有限且指数有限；代理/未知必须提供 |
| 一致性 | inconsistent_log_moneyness | 真实远期重算值与输入 $k$ 偏差>$10^{-10}$ |

只在有效行中统计来源。有效来源超过一种，整个时点 `failed_input/mixed_forward_sources`，合并节点数置0并且不拟合；无效行上的来源不会单独使时点混用失败。有效数据的期限→$T$必须一一映射，违反也属于结构冲突而抛错。

## 3. 节点合并与三个指纹

每个 $k$ 舍入到10位小数，把负零规范为0；按期限、$T$和舍入 $k$ 分组，排序后取 $w$ 中位数。`duplicate_group_node_count`保留重复组大小，原始有效节点数等于组大小之和。合并后IV重新按 $\sqrt{w/T}$ 算，不能把它误称“直接取IV中位数”。

对应类型：`EffectiveInputNode` [120](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:120)服务指纹，`PreparedExpiryNodes` [132](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:132)包装只读数组与本地拟合输入，`PreparedTimestampNodes` [176](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:176)封装整个边界结果。

`_build_fingerprints` [418](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:418)分三层：

1. effective：产品、时点、规范合并节点（包括组大小和来源）。
2. quality：输入/排除计数、时点状态和来源事实。
3. input：上面两个指纹组成的规范对象再哈希。

这样改一条被排除的输入可能不改变有效拟合节点，但若质量计数变化仍会改变完整input指纹。指纹不把所有无效行内容原样纳入，而保存结果口径；不能说它等于原始行情文件逐字哈希。

规范JSON固定排序、无多余空格、UTF-8、结尾换行，禁止非有限数。输入行重新排序不应改变规范结果。

## 4. 单时点状态机：先预留身份，再最终物化

引擎维护身份列表、身份→状态/草稿字典、每期限历史、日历配对证据。嵌套 `reserve` 连续分配 `attempt_order`，用完整input指纹构造确定ID。最后 `_materialize_attempt` [1079](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1079)把内部草稿转成严格导出dataclass。

这样数值层不会私自决定accepted，也不会因为先试了多个起点就创造36条顶层attempt。一个方法对一个期限通常是一条候选记录，起点过程收在summary里。

### 阶段A：SSVI父级

合并节点至少4个的期限才参与。

- 0个合格期限：没有SSVI父级。
- 1个：生成skipped父级，不进入优化，原因not_enough_maturities。
- 至少2个：调用fit_ssvi_local；异常则生成规范optimizer_exception父级。
- 有完整可求值子payload时，每个参与期限都保留一个子草稿；父级本地失败也可以有这些失败诊断曲线。

父级本地成功后，对所有参与期限两两组合检查日历，共 $m(m-1)/2$ 对；不是仅比较邻近期限。父级本地失败时保留同样配对宇宙但标记not_run，便于验证“到底应有哪些比较”。

父级失败会阻断所有子级；原本本地成功的子级记 `parent_ssvi_rejected`，本地失败的子级保留自己的更早失败码。被阻断子级不进入最终候选选择。

### 阶段B：按期限惰性选择

`process_candidate` 位于 [1450附近](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1450)，对本地成功候选，与此前所有已接受期限检查共同支持区间。失败或不确定时尝试符合节点资格的下一个方法。

| 合并点数 | 回退方法 |
|---|---|
| 少于2 | 不拟合 |
| 2或3 | 只LINEAR |
| 4 | 只PCHIP |
| 至少5 | RAW_SVI，再PCHIP |

若父级已释放SSVI子级，先处理该子级；一旦接受，就不再执行后续回退。源码 [1583](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1583)没有“大于等于4点仍可最后线性兜底”的分支。

日历聚合 `_aggregate_calendar_checks` [770](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:770)优先级：失败→不确定→通过；全部无重叠则NOT_TESTABLE。没有先前接受期限时才是no_prior，不会虚构一条日历配对记录。

## 5. 选中、终止、最后有曲线：三个引用的意义

`ExpiryFitResult` 在 [1627起](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1627)构造：

| 引用 | 含义 | 失败后可能怎样 |
|---|---|---|
| selected_attempt_id | 最终接受方法 | 不可用时为空 |
| terminal_attempt_id | 最后执行的可选择候选 | 可能只有失败码、没有曲线 |
| last_candidate_attempt_id | 最后一个实际保存候选曲线数组的尝试 | 可以指向比terminal更早的尝试，包括被阻断SSVI子级 |

因此展示灰色“被拒参数候选”只是诊断证据。不可用期限的正式fit数组为空；不能把最后有曲线的失败候选直接填进正式矩阵。

少于2个合并节点时没有尝试历史，失败码insufficient_nodes，三个引用全空。至少2个节点却无可用拟合时，terminal必须指向真实执行的最后候选，最终失败码与检查从该候选复制。

## 6. 全局201点矩阵怎样生成

支持区间的并集外包区间来自所有至少2点期限，包括最后不可用的期限。因此，一个最终不可用但边界更宽的期限也可能扩展展示横轴。所有期限保留为矩阵行；不可用整行None；可用期限只在各自闭区间填值。不是只对可用期限求共同区间，也没有跨期限插值。

[1730附近](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1730)调用统一evaluate_curve保留缺口。`surface_grid_status=AVAILABLE`只说明有正宽节点支持可生成横轴，不代表有任何usable期限；代表时点可能有201列而可用期限为0。

实际IV展示values会在surfaces.py将None转NaN；导出JSON保持None。Greeks图独立线性网格，对已有Greek节点插值，既不复用这201点，也不从SSVI导数计算Delta/Gamma。

## 7. 验证器是“重放状态机”，并非再拟合一次

`validate_timestamp_diagnostic` [1839](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1839)补强dataclass自身检查：

- 重算输入合并数与逐期限原始节点事实，核对相同期限的raw_node_count。
- 核对SSVI参与集合、共享参数、每期限theta、逐期限指标与子草稿一致。
- 不完整阶段必须保留规范fail-closed标记，不能删掉标记假装“没运行所以可忽略”。
- 重建父级应有的所有两两配对和逐期限选择应有配对，拒绝缺项、重复和多余记录。
- 重放已接受期限的顺序，禁止某期限接受后还执行后续可选择回退。
- 核对配对共同区间、状态、顺序，重建201点横轴与None掩码。

它主要校验结构、身份和证据的内部一致性，不从原始行情独立重新跑优化，更不证明某个数值检查永不漏检。哈希正确与金融结论正确也不是一回事。

## 8. AG批处理装载和分层抽样

`_load_ag_input` [2604](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2604)只读数据目录：按Parquet模式筛选、按产品路由筛AG、从路径YYYY/MM或options_YYYYMM解析月份，再按月装载。文件内记录月份必须匹配路由。复用正式read→clean_and_profile→build_surface_nodes，不另造一套业务清洗。

`_deduplicate_raw_quotes` [2553](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2553)在quality的keep-first前检查同datetime、contract重复是否业务字段一致；一致则按稳定来源顺序保留一条，冲突直接报错。它与拟合前按舍入 $k$ 合并w，是两个不同粒度的去重。

`_adapt_surface_nodes` [2581](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2581)标注underlying_price_proxy；`TimestampProfile`统计至少2点期限数和合并节点总数。source指纹由所有时点profile输入指纹构成，并非只覆盖选中21个时点。

`select_stratified_timestamps` [2760](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2760)固定额外抽样数20，排除代表时点；有效候选≤20则全取。超过20时：时间顺序分5段×期限数高低×节点总数高低，最多20层；层内选距中位中心最近的代表；不足20再按目标时间秩补位，遇占用向左右扩展并优先较早索引。没有随机种子，因为根本不使用随机抽样。

样本能覆盖不同时间与数据密度，但不是随机独立同分布抽样，不能仅凭这20个时点给全市场统计置信保证。

## 9. 严格JSON与缓存：缓存命中也要验证

`_decode_typed` [2894](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2894)递归按注解重建封闭类型，拒绝未知键和错误精确类型；例如JSON中的int不能随便冒充期望float。`decode_timestamp_diagnostic` [3045](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3045)还核对参数模式并执行完整状态验证。

缓存key [3059](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3059)包含schema版本、完整policy、source指纹和input指纹。`_strict_json_bytes_load`拒绝重复键、NaN/Infinity和非UTF-8；要求规范JSON字节恰好相等。

`_cached_timestamp_diagnostic` [3145](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3145)：旧/坏记录视作miss，重新builder；命中记录必须身份、来源、版本、类型和状态全部匹配；新记录先写独占临时文件，再os.replace。它还有路径能力校验防止缓存写进数据/输出或符号链接逃逸；并非“看到同名JSON就信任”。

## 10. 统计口径与六件产物

`build_summary` [3713](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3713)独立重算：

- final_expiry_method_counts按最终期限结果，包含UNUSABLE。
- selection_attempt_outcomes按 `scope=expiry` 且 `selection_eligible` 的尝试；被父级阻断子级不进这个分母。
- SSVI父级outcomes单列；不能把一个父级成功加到单期限选择成功率分子。
- accepted_fit_error只统计最终选中的可用曲线；因此是有选择条件的误差分布，不能代表所有候选误差。
- 检查计数按选择尝试、日历计数按所有配对；失败码又区分所有attempt失败与最终不可用失败。
- p95采用numpy线性分位数插值，空样本返回count0和空统计值。

六件固定产物：diagnostics.json、attempts.csv、summary.json、sampled_timestamps.json、代表时点对比PNG、artifact_manifest.json。CSV用UTF-8 BOM、CRLF、精确列名，嵌套对象以紧凑JSON写入。

`plot_representative_comparison` [4756](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4756)每期限画原始IV节点、接受曲线，以及至多一条最新被拒的参数候选；不会把所有失败迭代混在一张图里。None转NaN形成断线。

## 11. 产物验证和发布的实际承诺

`validate_artifact_bundle` [4419](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4419)要求目录恰有6个普通文件；严格解析主诊断，重算抽样、summary与CSV字节；PNG检查文件头；manifest核对5个内容文件大小和SHA256、运行时版本与身份引用。

PNG头和哈希检查只能证明格式头/字节完整性，不能证明图像视觉布局正确或每像素对应正确数值。summary重算验证的是与diagnostics一致，不是与原始行情重新比对。

`publish_artifact_bundle` [4653](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4653)只能使用当前进程注册的staging能力，验证后逐文件replace，manifest最后替换，再验证输出。每个文件替换是单独动作；不是一次原子替换整个目录，也没有写出完整多文件事务回滚。不要把“manifest最后”讲成整个发布过程绝对不可中断。

路径边界 [3925–4279](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3925)同时比较词法绝对路径与实际解析路径、大小写折叠、父子重叠、符号链接/Windows junction；只精确放行两个默认诊断目录。staging与cache能力保存设备、inode、mode、ctime等身份，并在关键步骤重检。跨平台文件系统行为需要由实际环境测试确认，本篇不把未运行的发布流程标成成功。

## 12. Runner返回码与固定场景

`run_ag_fit_diagnostics`固定代表时点为2025-04-07 10:15:00、额外20样本；其他参数值返回1。其返回码：

| 返回值 | 真实含义 |
|---|---|
| 0 | 完成发布，代表时点至少一个usable期限 |
| 1 | 参数/输入/边界/输出/异常等失败；代表时点failed_input也为1 |
| 2 | 代表时点不存在，打印最近可用时点但不替代 |
| 3 | 完成诊断产物，但代表时点usable期限为0 |

它检查已有输出，未force时拒绝覆盖；最后清理自己持有能力的staging。这里的`force`也不等于允许任意删除陌生目录。

## 13. 数值例子与面试问答

例：短期2点支持 $[-0.1,0.1]$，$T=0.1,w=0.01$；长期4点支持 $[-0.2,0.2]$，$T=0.2,w=0.02$。仅长期有SSVI资格，因此父级skipped；短期走LINEAR并无先验日历比较；长期走PCHIP并与已接受短期比较 $[-0.1,0.1]$，差0.01加容差为正。全局矩阵横轴201点覆盖 $[-0.2,0.2]$；短期两翼空，长期填满；没有生成 $T=0.15$ 的新行。

**问：为什么父级通过后子级还要再查日历？** 答：父级配对只涉及SSVI参与集合，逐期限选择还可能包含短期限稀疏插值或其他已接受方法；要让最终混合方法集合一致，不能只查SSVI内部。

**问：为什么有3种“没有检查”状态？** 答：not_run可能因前门阻断，no_prior表示没有比较对象，no_overlap表示有对象却没有共同区间；另有方法结构性不适用。这些理由对审计和成功语义不同。

**问：如果有曲面横轴，是否一定有可用结果？** 答：不是。横轴存在取决于至少一个期限有2点支持，可用性取决于全部门与选择；所有拟合失败仍可能保留201列全空矩阵。

继续：[[曲面观策项目学习与面试/04-面试与验证/曲面拟合专项追问.md|曲面拟合专项追问]]，以及全函数定位索引。

## 附录：完整顶层定义定位索引

下表覆盖此文件每一个顶层函数/类定义；“所属功能簇”对应正文解释。类内方法随所属类阅读，嵌套闭包随外层函数阅读。

| 定义 | 原始行号 | 所属功能簇 |
|---|---|---|
| `EffectiveInputNode` | [第120–128行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:120) | 输入类型、规范格式与指纹 |
| `PreparedExpiryNodes` | [第132–172行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:132) | 输入类型、规范格式与指纹 |
| `PreparedTimestampNodes` | [第176–191行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:176) | 输入类型、规范格式与指纹 |
| `_ValidInputRow` | [第195–201行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:195) | 输入类型、规范格式与指纹 |
| `TimestampProfile` | [第205–232行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:205) | 输入类型、规范格式与指纹 |
| `AgDiagnosticInput` | [第236–242行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:236) | 输入类型、规范格式与指纹 |
| `_canonical_json_bytes` | [第245–256行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:245) | 输入类型、规范格式与指纹 |
| `_fingerprint` | [第259–260行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:259) | 输入类型、规范格式与指纹 |
| `_require_canonical_sha256` | [第263–266行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:263) | 输入类型、规范格式与指纹 |
| `_require_nonnegative_json_int` | [第269–277行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:269) | 输入类型、规范格式与指纹 |
| `_require_generated_at` | [第280–291行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:280) | 输入类型、规范格式与指纹 |
| `_canonical_product` | [第294–302行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:294) | 输入类型、规范格式与指纹 |
| `_canonical_timestamp` | [第305–318行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:305) | 输入类型、规范格式与指纹 |
| `_is_null` | [第321–326行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:321) | 输入类型、规范格式与指纹 |
| `_finite_float` | [第329–335行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:329) | 输入类型、规范格式与指纹 |
| `_exact_maturity_id` | [第338–342行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:338) | 输入类型、规范格式与指纹 |
| `_source_token` | [第345–355行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:345) | 输入类型、规范格式与指纹 |
| `_exp_is_finite` | [第358–362行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:358) | 输入类型、规范格式与指纹 |
| `_validate_call_schema` | [第365–395行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:365) | 输入类型、规范格式与指纹 |
| `_input_quality_payload` | [第398–404行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:398) | 输入类型、规范格式与指纹 |
| `_effective_node_payload` | [第407–415行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:407) | 输入类型、规范格式与指纹 |
| `_build_fingerprints` | [第418–453行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:418) | 输入类型、规范格式与指纹 |
| `_schema_row_values` | [第456–460行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:456) | 输入类型、规范格式与指纹 |
| `prepare_timestamp_nodes` | [第463–704行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:463) | 逐行校验和节点合并 |
| `_AttemptIdentity` | [第708–716行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:708) | 状态、日历及异常草稿 |
| `_AttemptState` | [第720–728行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:720) | 状态、日历及异常草稿 |
| `_AcceptedExpiry` | [第732–735行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:732) | 状态、日历及异常草稿 |
| `_all_not_run_checks` | [第738–739行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:738) | 状态、日历及异常草稿 |
| `_no_prior_calendar_check` | [第742–753行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:742) | 状态、日历及异常草稿 |
| `_no_overlap_calendar_check` | [第756–767行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:756) | 状态、日历及异常草稿 |
| `_aggregate_calendar_checks` | [第770–789行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:770) | 状态、日历及异常草稿 |
| `_with_calendar_check` | [第792–798行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:792) | 状态、日历及异常草稿 |
| `_not_run_parent_pair` | [第801–821行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:801) | 状态、日历及异常草稿 |
| `_safe_calendar_pair` | [第824–895行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:824) | 状态、日历及异常草稿 |
| `_per_expiry_not_run_metric` | [第898–910行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:898) | 状态、日历及异常草稿 |
| `_skipped_ssvi_parent` | [第913–943行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:913) | 状态、日历及异常草稿 |
| `_ssvi_builder_exception_parent` | [第946–989行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:946) | 状态、日历及异常草稿 |
| `_nonparametric_butterfly_check` | [第992–1003行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:992) | 状态、日历及异常草稿 |
| `_builder_exception_draft` | [第1006–1067行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1006) | 状态、日历及异常草稿 |
| `_deep_plain_mapping` | [第1070–1076行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1070) | 状态、日历及异常草稿 |
| `_materialize_attempt` | [第1079–1129行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1079) | 状态、日历及异常草稿 |
| `_empty_method_counts` | [第1132–1133行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1132) | 状态、日历及异常草稿 |
| `_failed_input_diagnostic` | [第1136–1167行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1136) | 状态、日历及异常草稿 |
| `diagnose_timestamp` | [第1170–1825行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1170) | 正式单时点选择引擎 |
| `_pair_key` | [第1828–1836行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1828) | 正式单时点选择引擎 |
| `validate_timestamp_diagnostic` | [第1839–2479行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:1839) | 状态机证据重放校验 |
| `_option_file_has_read_schema` | [第2500–2505行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2500) | AG读取、profile及确定性抽样 |
| `_month_route` | [第2508–2533行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2508) | AG读取、profile及确定性抽样 |
| `_business_values_equal` | [第2536–2550行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2536) | AG读取、profile及确定性抽样 |
| `_deduplicate_raw_quotes` | [第2553–2578行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2553) | AG读取、profile及确定性抽样 |
| `_adapt_surface_nodes` | [第2581–2589行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2581) | AG读取、profile及确定性抽样 |
| `_source_fingerprint` | [第2592–2601行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2592) | AG读取、profile及确定性抽样 |
| `_load_ag_input` | [第2604–2711行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2604) | AG读取、profile及确定性抽样 |
| `_coerce_timestamp_profile` | [第2714–2737行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2714) | AG读取、profile及确定性抽样 |
| `_eligible_sampling_profiles` | [第2740–2757行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2740) | AG读取、profile及确定性抽样 |
| `select_stratified_timestamps` | [第2760–2840行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2760) | AG读取、profile及确定性抽样 |
| `_nearest_profile_timestamp` | [第2843–2856行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2843) | AG读取、profile及确定性抽样 |
| `_validate_json_value` | [第2872–2891行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2872) | 严格解码及缓存 |
| `_decode_typed` | [第2894–2993行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2894) | 严格解码及缓存 |
| `_validate_closed_attempt_parameters` | [第2996–3042行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:2996) | 严格解码及缓存 |
| `decode_timestamp_diagnostic` | [第3045–3056行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3045) | 严格解码及缓存 |
| `_timestamp_cache_key` | [第3059–3079行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3059) | 严格解码及缓存 |
| `_strict_json_bytes_load` | [第3082–3107行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3082) | 严格解码及缓存 |
| `_decode_cache_record` | [第3110–3142行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3110) | 严格解码及缓存 |
| `_cached_timestamp_diagnostic` | [第3145–3309行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3145) | 严格解码及缓存 |
| `_canonical_diagnostics` | [第3365–3383行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3365) | 规范产物与统计 |
| `_batch_input_fingerprint` | [第3386–3399行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3386) | 规范产物与统计 |
| `_write_canonical_json` | [第3402–3403行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3402) | 规范产物与统计 |
| `_build_diagnostics_payload` | [第3406–3439行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3406) | 规范产物与统计 |
| `_build_sampled_timestamps_payload` | [第3442–3514行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3442) | 规范产物与统计 |
| `_validate_selected_profile_references` | [第3517–3542行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3517) | 规范产物与统计 |
| `write_sampled_timestamps` | [第3566–3578行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3566) | 规范产物与统计 |
| `_compact_json_text` | [第3581–3588行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3581) | 规范产物与统计 |
| `_csv_scalar` | [第3591–3606行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3591) | 规范产物与统计 |
| `_attempt_csv_row` | [第3609–3658行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3609) | 规范产物与统计 |
| `write_attempts_csv` | [第3661–3664行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3661) | 规范产物与统计 |
| `_attempts_csv_bytes` | [第3667–3691行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3667) | 规范产物与统计 |
| `_empty_error_statistics` | [第3694–3695行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3694) | 规范产物与统计 |
| `_error_statistics` | [第3698–3710行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3698) | 规范产物与统计 |
| `build_summary` | [第3713–3869行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3713) | 规范产物与统计 |
| `RuntimePaths` | [第3885–3888行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3885) | 路径边界、能力与manifest |
| `_StagingCapability` | [第3892–3903行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3892) | 路径边界、能力与manifest |
| `_CacheCapability` | [第3910–3922行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3910) | 路径边界、能力与manifest |
| `_project_root` | [第3925–3926行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3925) | 路径边界、能力与manifest |
| `_resolve_path_safely` | [第3929–3946行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3929) | 路径边界、能力与manifest |
| `_lexical_absolute_path` | [第3949–3953行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3949) | 路径边界、能力与manifest |
| `_lexical_chain_has_reparse` | [第3956–3966行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3956) | 路径边界、能力与manifest |
| `_casefold_parts` | [第3969–3971行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3969) | 路径边界、能力与manifest |
| `_paths_overlap` | [第3974–3980行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3974) | 路径边界、能力与manifest |
| `_paths_equal` | [第3983–3984行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3983) | 路径边界、能力与manifest |
| `_is_descendant` | [第3987–3993行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3987) | 路径边界、能力与manifest |
| `_is_drive_root` | [第3996–3997行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:3996) | 路径边界、能力与manifest |
| `_protected_write_targets` | [第4000–4016行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4000) | 路径边界、能力与manifest |
| `_reject_write_root` | [第4019–4082行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4019) | 路径边界、能力与manifest |
| `_validate_runtime_paths` | [第4085–4110行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4085) | 路径边界、能力与manifest |
| `_is_link_or_junction` | [第4113–4124行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4113) | 路径边界、能力与manifest |
| `_validate_cache_internal_path` | [第4127–4139行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4127) | 路径边界、能力与manifest |
| `_nearest_existing_directory` | [第4142–4149行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4142) | 路径边界、能力与manifest |
| `_create_cache_capability` | [第4152–4233行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4152) | 路径边界、能力与manifest |
| `_assert_cache_capability` | [第4236–4276行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4236) | 路径边界、能力与manifest |
| `_finish_cache_capability` | [第4279–4280行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4279) | 路径边界、能力与manifest |
| `_sha256_hex` | [第4283–4288行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4283) | 路径边界、能力与manifest |
| `_runtime_versions` | [第4291–4300行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4291) | 路径边界、能力与manifest |
| `_write_artifact_manifest` | [第4303–4341行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4303) | 路径边界、能力与manifest |
| `_read_canonical_json` | [第4344–4349行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4344) | 路径边界、能力与manifest |
| `_require_exact_regular_artifacts` | [第4407–4416行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4407) | 路径边界、能力与manifest |
| `validate_artifact_bundle` | [第4419–4640行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4419) | 六件产物验证与发布 |
| `_validate_existing_output_names` | [第4643–4650行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4643) | 六件产物验证与发布 |
| `publish_artifact_bundle` | [第4653–4716行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4653) | 六件产物验证与发布 |
| `_utc_now_text` | [第4719–4722行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4719) | 六件产物验证与发布 |
| `_plot_line_values` | [第4725–4734行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4725) | 六件产物验证与发布 |
| `_latest_rejected_parameter_candidate` | [第4737–4753行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4737) | 六件产物验证与发布 |
| `plot_representative_comparison` | [第4756–4902行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4756) | 比较图及staging生命周期 |
| `_validate_created_staging` | [第4905–4927行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4905) | 比较图及staging生命周期 |
| `_directory_identity` | [第4930–4943行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4930) | 比较图及staging生命周期 |
| `_regular_file_identity` | [第4946–4961行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4946) | 比较图及staging生命周期 |
| `_staging_registry_key` | [第4964–4965行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4964) | 比较图及staging生命周期 |
| `_create_staging_capability` | [第4968–5028行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:4968) | 比较图及staging生命周期 |
| `_assert_staging_capability_identity` | [第5031–5067行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:5031) | 比较图及staging生命周期 |
| `_claim_staging_capability` | [第5070–5102行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:5070) | 比较图及staging生命周期 |
| `_finish_staging_capability` | [第5105–5113行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:5105) | 比较图及staging生命周期 |
| `_cleanup_staging` | [第5116–5142行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:5116) | 比较图及staging生命周期 |
| `_write_complete_staging_bundle` | [第5145–5202行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:5145) | 比较图及staging生命周期 |
| `run_ag_fit_diagnostics` | [第5205–5324行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/surface_fit_diagnostics.py:5205) | AG批处理入口 |
