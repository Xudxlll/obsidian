---
tags: [曲面观策, 源码逆向, 总方差, SSVI, RawSVI, 无套利]
source: src/option_risk/total_variance_fit.py
source_lines: 5106
read_scope: 全文件逐块阅读
---

> [!abstract] 文件定位
> 这是数值内核与严格数据契约：规定方法、状态、失败码，定义曲线和总方差公式，生成确定性多起点，执行参数优化、本地检查并返回候选草稿。它不决定单期限最终采用哪条曲线，不装载业务数据，不写图和诊断文件；期限选择在 `surface_fit_diagnostics.py`。

源文件：[total_variance_fit.py](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1)。长源码逐字档案由知识库统一保存；本篇按真实功能解释，避免用完整源码挤掉学习内容。

## 1. 先画清调用边界

正式曲面入口 `surfaces.surface_grid(metric="iv")` → `surfaces._total_variance_iv_grid` → `surface_fit_diagnostics.diagnose_timestamp` → 本文件四个候选构造器。诊断批处理也复用同一组构造器。返回的 `_LocalFitCandidate` 仍是草稿，包含曲线、误差和本地检查；最终 `attempt_status`、父级阻断和跨期限检查由编排层加入。

主要公共入口：`fit_ssvi_local`、`fit_raw_svi_local`、`build_pchip_local_candidate`、`build_linear_local_candidate`、`evaluate_curve`、`diagnostic_curve_grid`、两个换算函数及 JSON 适配器。构造曲线的 `_create_*` 名称带下划线，统一公开求值口径是 `evaluate_curve`。

**重定义核查**：本文件顶层定义不存在同名函数/类的后段重定义。靠近文件尾部的四个候选入口是实际实现，不存在“上半段实验拟合被同名函数覆盖”的情况。测试会直接调用私有数学函数，但生产链经过编排层调用候选入口；不能把测试专用 `_create_curve_model` 任意曲线当成正式拟合路径。

## 2. 枚举、失败码与不可变策略：为什么前1800行这么长

[22–81行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:22)定义10类封闭枚举。最容易混淆的是：

| 类型 | 意义 | 区别 |
|---|---|---|
| `FitMethod` | 实际尝试的4种方法 | 不包含 UNUSABLE |
| `FinalMethod` | 单期限最终结果 | 多一个 UNUSABLE |
| `AttemptStatus` | skipped/failed/accepted | skipped 仅不够资格的SSVI父级 |
| `CheckStatus` | passed/failed/indeterminate/not_applicable/not_testable | 失败、不确定、未适用、不可比较不能混用 |
| `ForwardSource` | 真实远期/标的代理/未知预计算横轴 | 是经济口径追踪，不是数值拟合方法 |

`CHECK_NAMES` 顺序用于稳定序列化；实际本地硬门顺序是正总方差→价格单调→价格凸性→参数曲线的 $g$ →跳变；日历最后由编排层补齐。表里日历的位置与执行位置不同，不能按字典显示顺序猜调用顺序。

`FitPolicy` [326–462行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:326)冻结默认版本的全部策略。v1 里不能只改网格、容差或种子而保留版本名；要改需新 `policy_version`。内部字典再用 `_FrozenDict` 防修改，解决“冻结dataclass但嵌套dict仍可改”的漏洞。注意新版本对象只跳过v1精确默认值比较，并不代表所有任意新策略已经通过全面合法性验证；展示诊断的其他契约仍有硬编码201点。

### 契约不是普通的数据袋

| 类型与位置 | 承载内容 | 真正检查的相互关系 |
|---|---|---|
| `CheckDiagnostic` [662](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:662) | 单项检查、阈值、计数、标量指标 | 状态↔结论↔原因码的闭合真值表；禁止非有限数 |
| `OptimizerStartSummary` [726](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:726) | 生成、剔除、执行、成功数 | 生成=预检剔除+重复剔除+执行；局部成功数受双重上界约束 |
| `PerExpiryMetric` [781](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:781) | SSVI逐期限误差与检查 | 合并数不超过原始数；支持区间必须正宽 |
| `FitAttemptDiagnostic` [812](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:812) | 一次方法尝试 | optimizer/local/final 成功分层；失败码须匹配首个硬门；父子参数模式 |
| `ExpiryFitResult` [1341](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1341) | 最终期限结果 | 可用时选中引用与数组齐全，不可用时正式拟合数组为空 |
| `InputQuality` [1447](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1447) | 输入计数 | 输入=有效合并前+各排除；合并后≤合并前 |
| `CalendarPairDiagnostic` [1475](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1475) | 两期限检查证据 | 已执行必须有正宽共同区间；无重叠必须空边界 |
| `TimestampSurfaceDiagnostic` [1542](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1542) | 完整时点证据 | 重算ID、选中曲线、计数、矩阵形状、空值掩码与 $\mathrm{IV}=\sqrt{w/T}$ |

这些类是 `frozen=True`，但一般 `list/dict` 字段并未全部深冻结；不要把所有导出的诊断对象称为递归不可变。内部本地候选、策略映射和只读数组做了更强的保护。

`make_attempt_id` [531](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:531)对完整规范身份（输入指纹、产品、时点、范围、期限、方法、顺序、策略版本）做规范JSON和SHA256；`make_calendar_pair_id` [576](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:576)另含阶段、父级及早晚候选引用。它们提供可复现身份，不是加密签名或对数据真实性的证明。

## 3. 总方差与唯一闭域求值

[1853–1868行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1853)：

$$
w=\sigma_{\mathrm{IV}}^2T,\qquad \sigma_{\mathrm{IV}}=\sqrt{w/T}
$$

前向换算允许IV=0；反向换算要求正总方差。正式输入边界要求正IV。

`CurveModel` [1911](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1911)持有方法、期限、支持区间、结点、求值器与可选导数/分段对象，用私有 token 限制构造。`CurveEvaluation` 复制数组并禁止写入。

`evaluate_curve` [2017](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2017)接受有限标量或一维查询；标量转长度1数组。支持掩码严格使用 $k_{\min}\le k\le k_{\max}$。区间外 $w$ 与IV都为None；区间内负/零 $w$ 可以作为诊断数值保留，但IV为空；非有限 $w$ 变None。`supported=True` 仅表示横轴在支持内，不表示拟合值有效。

### 三张网格不能混用

| 名称 | 组成/形状 | 用途 |
|---|---|---|
| `diagnostic_curve_grid` [1877](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1877) | 201均匀点 ∪ 原始合并 $k$，float64精确去重 | 保存候选、画图；因此不一定恰好201点 |
| `_composite_check_grid` [2425](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2425) | 201基点 ∪ 原点 ∪ 结点 ∪ 插值结点双侧邻点 | 本地形状检查与细化起点 |
| 编排层 surface grid | 所有有支持期限的全局最左至最右201点 | 展示矩阵；按每期限闭域置空 |

Greeks 又是第四种路径，默认33点，见 `surfaces.py:190`；没有把这些网格统一成一个复用数组。

## 4. 两种参数模型和非参数模型

SSVI 与Raw SVI的详细推导、符号意义和手算见 [[11-拟合与降级：从SSVI到可解释的失败]]。这里集中说实现差异。

| 函数簇 | 真实行为 |
|---|---|
| `_ssvi_value_derivatives` [2055](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2055) | 幂律 $\varphi=\eta\theta^{-\gamma}$；一次返回 $w,w',w''$ |
| `_raw_svi_value_derivatives` [2082](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2082) | 向量形状必须为5；返回总方差及解析一二阶导 |
| `_ssvi_constraint_slacks` [2100](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2100) | $\theta$地板与非下降、$\rho/\eta/\gamma$边界、两条蝶式屏障；slack≥0才满足 |
| `_raw_svi_constraint_slacks` [2139](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2139) | $b,\sigma_s$正性、$\rho$边界、全域最低值、左右翼上限 |
| `_ssvi_objective` [2162](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2162) | 每期限残差按中位总方差和 $\sqrt n$ 归一化，各期限等权求和 |
| `_raw_svi_objective` [2201](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2201) | 单期限归一化均方误差 |
| `_fit_error_metrics` [2217](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2217) | 总方差RMSE、NRMSE；分母为观察值绝对值中位数和地板之大者 |
| `_create_ssvi_curve` [2249](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2249) | 至少4个递增原节点，原节点首尾必须恰等于支持边界 |
| `_create_raw_svi_curve` [2298](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2298) | 至少5个节点；复制参数向量避免外部数组修改影响曲线 |
| `_create_pchip_curve` [2339](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2339) | 至少4点；总方差插值；显式 `extrapolate=False`；保存分段多项式和导数 |
| `_create_linear_curve` [2364](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2364) | 只接受2或3点；`np.interp`被闭域接口保护；结点导数采用右侧段（右端裁剪） |

SSVI的两个数值屏障为：

$$
\theta\varphi(1+|\rho|)\le4-10^{-8},\qquad
\theta\varphi^2(1+|\rho|)\le4-10^{-8}
$$

它们来自模型无套利结构，但检查只针对输入参与期限的参数。没有对任意未来期限构造出一条已证明无套利的连续期限曲线。Raw SVI的最低值约束也不能代替完整蝶式检查。

## 5. 六项检查的真实硬门与边界

`_run_local_checks` [3348](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3348)顺序执行五个本地门，一旦失败或不确定则后续标记未运行。局部异常被转成不确定，防止默认放行。非参数方法的 $g$ 状态最后会强制补回结构性不适用，即使前面门已失败，仍不能被笼统写成not_run。

- `_check_positive_total_variance` [2626](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2626)：非有限值直接失败；$w\le10^{-10}$失败；靠近地板细化仍不充分则不确定。
- `_normalized_black_call` [2691](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2691)：用 $w$ 与 $k$ 算归一化看涨价格。
- `_check_call_price_monotonic` [2727](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2727)：比较相邻价格绝对增量，阈值 $10^{-8}$。
- `_check_call_price_convex` [2777](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2777)：比较对 $e^k$ 的割线斜率变化，阈值 $-10^{-6}$；不是对 $k$ 的二阶差分。
- `_check_butterfly_g_nonnegative` [2839](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2839)：仅参数曲线执行解析导数形成的 $g$；阈值 $-10^{-8}$。
- `_check_calendar_pair` [2935](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2935)：单对期限纯函数；共同支持无正宽交集时 NOT_TESTABLE；检查余量见下式。
- `_check_jump_reliable` [3250](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3250)：最大IV斜率与原始斜率中位数比例，是额外质量门。

$$
\operatorname{calendar\ margin}=w_2-w_1+10^{-6}+0.005\max(w_1,w_2)
$$

`_adaptive_margin_grid` [2460](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2460)只服务正方差、$g$、日历；检查中点、保留可疑点，最多8轮与最小间隔控制。通过的统一结论字符串是 `sampled_no_violation`；这是代码刻意限定的语义。

数值消减单独处理：`_cancellation_prone_intervals` 用16倍float64机器精度判相邻间隔；`_black_call_limiting_strike_slope` 给出价格导数极限；指数差用expm1稳定计算。它解决的是数值表达问题，不是引入新的金融套利定义。

## 6. 跳变检查比“看两点差”更严格

$$
S(k)=\frac{|w'(k)|}{2\sqrt{Tw(k)}}
$$

参数曲线通过 `_parameter_max_abs_iv_slope` [3076](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3076)调用 SHGO，目标为 $-S(k)^2$，固定256初始采样、3轮、单worker，并检查主解和局部解集完整性；候选集包括两端点、主解、所有局部解。没有成功或结果缺字段时返回分辨率不足，不用不完整最大值作结论。

PCHIP通过 `_pchip_stationary_points` [3183](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3183)逐段构造多项式求根。因为：

$$
S^2=\frac{(w')^2}{4Tw},\qquad
\frac{dS^2}{dk}=\frac{w'[2ww''-(w')^2]}{4Tw^2}
$$

候选包含 $w'=0$、$2ww''-(w')^2=0$ 的段内实根与所有结点。去掉精确零最高次系数，限制虚部容差和区间容差，按精确float64去重，因此非常接近而不相等的根可以同时保留。

线性段通过 `_linear_max_abs_iv_slope` [3233](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3233)取每段较小 $w$ 的端点，因为分子恒定、分母越小斜率越大。例：$T=0.5$，一段从 $(k,w)=(-0.3,0.02)$ 到 $(0,0.08)$，$w'=0.2$，最大IV斜率在左端：$0.2/(2\sqrt{0.5\times0.02})=1$。

## 7. 起点计划、排序和阶段保留

### SSVI起点

`_prepare_ssvi_starts` [3650](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3650)按期限排序；$\theta$上界：

$$
\theta_{\max}=\min\big(100,\max(1,10\max w_{\mathrm{observed}})\big)
$$

平值初值插值或最近节点后做累计最大；$\eta$种子裁剪至两屏障允许上限的80%。固定嵌套循环保证原始索引可审计。

### Raw SVI起点

`_prepare_raw_svi_starts` [3739](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3739)令总方差尺度为 $\max(\operatorname{median}w,10^{-4})$，横轴跨度为 $\max(k_{\max}-k_{\min},0.01)$；据此给 $a,m,\sigma_s$ 的边界。$a$初值是最小观察总方差的一半且至少约束余量；$m$用最小方差所在最左 $k$ 或中位 $k$；$\sigma_s$用两个跨度种子。没有让优化器随机挑参数。

### 五阶段不是五种拟合方法

| `stage_reached` | 已保留证据 | 典型问题 |
|---|---|---|
| 0 | 无有限完整参数 | 优化异常或参数非有限 |
| 1 | 有有限参数 | 曲线/节点求值失败 |
| 2 | 有曲线及有限节点值 | 约束后处理异常 |
| 3 | 约束已处理，指标/检查可能部分完成 | 部分期限指标或检查异常 |
| 4 | 全部本地后处理执行完成 | 仍可因优化器失败或硬门失败不可接受 |

`_evaluate_raw_start_outcome` [3959](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3959)、`_evaluate_ssvi_start_outcome` [4132](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4132)即使优化器 `success=False`，只要参数有限仍尽可能后处理，保留可解释失败曲线。已知RMSE失败不会被后来的检查异常覆盖。SSVI部分期限已完成的指标/检查也不会一股脑清空。

`_select_start_outcome` [3855](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3855)先从真正本地成功中选；无成功则按固定八元组保留失败代表。`_optimizer_summary` [4390](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4390)重算计数；只有 `stage_reached>=2` 计作evaluable。

## 8. 四个最终候选入口与采样失败保护

`fit_raw_svi_local` [4604](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4604)：资格不足返回None；每个保留起点运行SLSQP；选一个代表；转成单期限草稿。一个多起点方法整体产生一条尝试记录，不是每个起点都独立成为最终 `attempt`。

`fit_ssvi_local` [4784](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4784)：筛选至少4点期限；不足2个返回不够期限的父级bundle；完整可求值参数必须生成每期限一个子草稿；父级记录共享参数和逐期限指标。父级优化失败可以有本地看起来正常的子曲线，但选择权要交给编排层，不能私自放行。

非参数构造器 [5000](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:5000)：命中节点后仍算RMSE、价格检查、跳变，返回同一草稿形状。LINEAR只对2–3点有效。

`_expiry_candidate_from_curve` [4539](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4539)在保存诊断曲线采样失败时，若原本本地成功，则主动降为 `check_resolution_limit`，清空候选数组并标记 `candidate_sampling_failed`。它不让“检查已过但无法生成可审查曲线”的状态伪装成成功；若原本已经失败，会保留原始更早失败码。

`to_json_compatible` [5072](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:5072)递归处理枚举、dataclass、数组和numpy标量；保留None；禁止NaN/Infinity；字典键必须字符串。展示上None对应缺数据，JSON里不能把它换成0。

## 9. 最适合答辩演示的数值路径

输入同一期限 $T=0.25$ 的4个节点，$k=[-0.3,-0.1,0.1,0.3]$，IV都20%，因此 $w$ 都0.01。若只有一个合格期限，SSVI父级被跳过；4点不够Raw SVI，尝试PCHIP。PCHIP生成常数总方差曲线：节点RMSE为0、IV斜率0、正方差与价格形状符合方向；$g$结构性不适用；无先前已接受期限，日历为no_prior。若所有适用门通过，最终接受PCHIP。

这个例子同时覆盖：节点资格、拟合坐标、误差、结构性不适用、日历状态、最终选择。你可以不依赖全量白银行情就讲清整条流程。

## 10. 面试问答：必须讲出的差别

**问：有了 SSVI 两屏障，为什么还检查 $g$？**

答：解析参数结构用于约束可行域；独立数值门能捕获后处理、实现、容差及候选形状问题，也让统一诊断契约可审查。最终输出还可能来自Raw或插值方法，因此不能只以SSVI理论替全部方法背书。

**问：PCHIP能求导，为什么原因码叫没有解析g？**

答：这是项目对可适用检查的封闭命名。PCHIP确实保留分段导数，斜率极值搜索还要用它；但项目不把其分段二阶导当成全局光滑参数切片的g门来执行。价格形状门仍生效。

**问：失败代表是不是所有起点中RMSE最低？**

答：不是。优先保留后处理阶段更深、失败数量更少等固定排序的代表；RMSE仅是后续排序项。目的包含可解释性和复现性。

**问：这份实现哪里最值得改进？**

答：可提出报价权重、真实远期、连续域校验或更系统的期限插值；但当前实现没有把这些功能全部做完。尤其多起点SLSQP不提供全局最优证明，有限网格检查也不提供全域无套利证明。

## 11. 验证入口与学习顺序

先读教程10→11→12，再看公式函数、检查函数、起点计划、最终四个入口，最后回头理解庞大契约。测试映射见 [[test_total_variance_fit.py-契约、数值与异常路径的验证地图]]。完整函数定义索引附后，可按原始行号逐个定位。

## 附录：完整顶层定义定位索引

下表覆盖此文件每一个顶层函数/类定义；“所属功能簇”对应正文解释。类内方法随所属类阅读，嵌套闭包随外层函数阅读。

| 定义 | 原始行号 | 所属功能簇 |
|---|---|---|
| `FitMethod` | [第22–26行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:22) | 封闭枚举、代码集合与固定种子 |
| `FinalMethod` | [第29–34行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:29) | 封闭枚举、代码集合与固定种子 |
| `AttemptScope` | [第37–39行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:37) | 封闭枚举、代码集合与固定种子 |
| `AttemptStatus` | [第42–45行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:42) | 封闭枚举、代码集合与固定种子 |
| `CheckStatus` | [第48–53行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:48) | 封闭枚举、代码集合与固定种子 |
| `ResultStatus` | [第56–58行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:56) | 封闭枚举、代码集合与固定种子 |
| `OverallStatus` | [第61–64行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:61) | 封闭枚举、代码集合与固定种子 |
| `TimestampStatus` | [第67–69行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:67) | 封闭枚举、代码集合与固定种子 |
| `SurfaceGridStatus` | [第72–75行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:72) | 封闭枚举、代码集合与固定种子 |
| `ForwardSource` | [第78–81行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:78) | 封闭枚举、代码集合与固定种子 |
| `_FrozenDict` | [第87–107行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:87) | 封闭枚举、代码集合与固定种子 |
| `_dict_ssvi_seeds` | [第296–301行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:296) | 封闭枚举、代码集合与固定种子 |
| `_dict_raw_svi_seeds` | [第304–310行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:304) | 封闭枚举、代码集合与固定种子 |
| `_dict_slsqp_options` | [第313–314行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:313) | 封闭枚举、代码集合与固定种子 |
| `_dict_shgo_options` | [第317–318行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:317) | 封闭枚举、代码集合与固定种子 |
| `_dict_shgo_minimizer_options` | [第321–322行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:321) | 封闭枚举、代码集合与固定种子 |
| `FitPolicy` | [第326–462行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:326) | 策略、身份及导出契约 |
| `_require_enum` | [第465–467行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:465) | 策略、身份及导出契约 |
| `_require_nonempty_string` | [第470–472行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:470) | 策略、身份及导出契约 |
| `_require_count` | [第475–479行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:475) | 策略、身份及导出契约 |
| `_require_finite` | [第482–494行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:482) | 策略、身份及导出契约 |
| `_require_local_timestamp` | [第497–500行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:497) | 策略、身份及导出契约 |
| `_require_attempt_id` | [第503–507行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:503) | 策略、身份及导出契约 |
| `_require_pair_id` | [第510–512行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:510) | 策略、身份及导出契约 |
| `_require_fingerprint` | [第515–517行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:515) | 策略、身份及导出契约 |
| `_identity_digest` | [第520–528行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:520) | 策略、身份及导出契约 |
| `make_attempt_id` | [第531–573行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:531) | 策略、身份及导出契约 |
| `make_calendar_pair_id` | [第576–616行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:576) | 策略、身份及导出契约 |
| `_require_failure_code` | [第619–623行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:619) | 策略、身份及导出契约 |
| `_require_checks` | [第626–631行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:626) | 策略、身份及导出契约 |
| `_require_finite_sequence` | [第634–650行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:634) | 策略、身份及导出契约 |
| `_require_parameter_scalars` | [第653–658行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:653) | 策略、身份及导出契约 |
| `CheckDiagnostic` | [第662–722行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:662) | 策略、身份及导出契约 |
| `OptimizerStartSummary` | [第726–777行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:726) | 策略、身份及导出契约 |
| `PerExpiryMetric` | [第781–808行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:781) | 策略、身份及导出契约 |
| `FitAttemptDiagnostic` | [第812–1337行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:812) | 策略、身份及导出契约 |
| `ExpiryFitResult` | [第1341–1443行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1341) | 策略、身份及导出契约 |
| `InputQuality` | [第1447–1471行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1447) | 策略、身份及导出契约 |
| `CalendarPairDiagnostic` | [第1475–1538行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1475) | 策略、身份及导出契约 |
| `TimestampSurfaceDiagnostic` | [第1542–1850行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1542) | 策略、身份及导出契约 |
| `to_total_variance` | [第1853–1860行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1853) | 换算、网格与闭域求值 |
| `to_implied_volatility` | [第1863–1868行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1863) | 换算、网格与闭域求值 |
| `_readonly_array` | [第1871–1874行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1871) | 换算、网格与闭域求值 |
| `diagnostic_curve_grid` | [第1877–1904行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1877) | 换算、网格与闭域求值 |
| `CurveModel` | [第1911–1964行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1911) | 换算、网格与闭域求值 |
| `_create_curve_model` | [第1967–1992行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1967) | 换算、网格与闭域求值 |
| `CurveEvaluation` | [第1996–2014行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:1996) | 换算、网格与闭域求值 |
| `evaluate_curve` | [第2017–2052行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2017) | 换算、网格与闭域求值 |
| `_ssvi_value_derivatives` | [第2055–2079行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2055) | 模型数学与四类曲线 |
| `_raw_svi_value_derivatives` | [第2082–2097行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2082) | 模型数学与四类曲线 |
| `_ssvi_constraint_slacks` | [第2100–2136行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2100) | 模型数学与四类曲线 |
| `_raw_svi_constraint_slacks` | [第2139–2159行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2139) | 模型数学与四类曲线 |
| `_ssvi_objective` | [第2162–2198行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2162) | 模型数学与四类曲线 |
| `_raw_svi_objective` | [第2201–2214行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2201) | 模型数学与四类曲线 |
| `_fit_error_metrics` | [第2217–2228行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2217) | 模型数学与四类曲线 |
| `_validated_curve_nodes` | [第2231–2246行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2231) | 模型数学与四类曲线 |
| `_create_ssvi_curve` | [第2249–2295行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2249) | 模型数学与四类曲线 |
| `_create_raw_svi_curve` | [第2298–2336行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2298) | 模型数学与四类曲线 |
| `_create_pchip_curve` | [第2339–2361行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2339) | 模型数学与四类曲线 |
| `_create_linear_curve` | [第2364–2396行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2364) | 模型数学与四类曲线 |
| `_curve_values` | [第2399–2406行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2399) | 模型数学与四类曲线 |
| `_knot_neighbor_points` | [第2409–2422行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2409) | 模型数学与四类曲线 |
| `_composite_check_grid` | [第2425–2447行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2425) | 模型数学与四类曲线 |
| `_RefinementResult` | [第2451–2457行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2451) | 数值检查与斜率极值 |
| `_adaptive_margin_grid` | [第2460–2544行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2460) | 数值检查与斜率极值 |
| `_not_run_check` | [第2547–2558行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2547) | 数值检查与斜率极值 |
| `_passed_check` | [第2561–2579行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2561) | 数值检查与斜率极值 |
| `_indeterminate_check` | [第2582–2600行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2582) | 数值检查与斜率极值 |
| `_failed_check_diagnostic` | [第2603–2623行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2603) | 数值检查与斜率极值 |
| `_check_positive_total_variance` | [第2626–2688行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2626) | 数值检查与斜率极值 |
| `_normalized_black_call` | [第2691–2702行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2691) | 数值检查与斜率极值 |
| `_cancellation_prone_intervals` | [第2705–2713行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2705) | 数值检查与斜率极值 |
| `_black_call_limiting_strike_slope` | [第2716–2724行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2716) | 数值检查与斜率极值 |
| `_check_call_price_monotonic` | [第2727–2774行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2727) | 数值检查与斜率极值 |
| `_check_call_price_convex` | [第2777–2823行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2777) | 数值检查与斜率极值 |
| `_butterfly_g_values` | [第2826–2836行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2826) | 数值检查与斜率极值 |
| `_check_butterfly_g_nonnegative` | [第2839–2912行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2839) | 数值检查与斜率极值 |
| `_common_calendar_grid` | [第2915–2932行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2915) | 数值检查与斜率极值 |
| `_check_calendar_pair` | [第2935–3069行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:2935) | 数值检查与斜率极值 |
| `_ResolutionLimit` | [第3072–3073行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3072) | 数值检查与斜率极值 |
| `_parameter_max_abs_iv_slope` | [第3076–3150行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3076) | 数值检查与斜率极值 |
| `_real_polynomial_roots` | [第3153–3180行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3153) | 数值检查与斜率极值 |
| `_pchip_stationary_points` | [第3183–3215行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3183) | 数值检查与斜率极值 |
| `_pchip_max_abs_iv_slope` | [第3218–3230行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3218) | 数值检查与斜率极值 |
| `_linear_max_abs_iv_slope` | [第3233–3247行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3233) | 数值检查与斜率极值 |
| `_check_jump_reliable` | [第3250–3345行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3250) | 数值检查与斜率极值 |
| `_run_local_checks` | [第3348–3406行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3348) | 数值检查与斜率极值 |
| `_LocalExpiryInput` | [第3410–3445行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3410) | 内部输入、起点和草稿 |
| `_IndexedStart` | [第3449–3458行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3449) | 内部输入、起点和草稿 |
| `_PreparedStarts` | [第3462–3479行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3462) | 内部输入、起点和草稿 |
| `_StartPayload` | [第3483–3486行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3483) | 内部输入、起点和草稿 |
| `_StartOutcome` | [第3490–3533行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3490) | 内部输入、起点和草稿 |
| `_LocalFitCandidate` | [第3537–3581行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3537) | 内部输入、起点和草稿 |
| `_LocalSsviBundle` | [第3585–3599行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3585) | 内部输入、起点和草稿 |
| `_freeze_mapping` | [第3602–3608行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3602) | 内部输入、起点和草稿 |
| `_precheck_and_deduplicate_starts` | [第3611–3629行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3611) | 内部输入、起点和草稿 |
| `_bound_slacks` | [第3632–3642行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3632) | 内部输入、起点和草稿 |
| `_all_nonnegative_finite` | [第3645–3647行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3645) | 内部输入、起点和草稿 |
| `_prepare_ssvi_starts` | [第3650–3736行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3650) | 起点计划、选择与误差 |
| `_prepare_raw_svi_starts` | [第3739–3818行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3739) | 起点计划、选择与误差 |
| `_formatted_parameter_key` | [第3821–3829行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3821) | 起点计划、选择与误差 |
| `_finite_or_infinity` | [第3832–3835行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3832) | 起点计划、选择与误差 |
| `_failure_sort_key` | [第3838–3852行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3838) | 起点计划、选择与误差 |
| `_select_start_outcome` | [第3855–3889行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3855) | 起点计划、选择与误差 |
| `_fit_metrics_for_curve` | [第3892–3908行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3892) | 起点计划、选择与误差 |
| `_check_gate_failures` | [第3911–3932行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3911) | 起点计划、选择与误差 |
| `_maximum_constraint_violation` | [第3935–3939行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3935) | 起点计划、选择与误差 |
| `_optimizer_message` | [第3942–3949行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3942) | 起点计划、选择与误差 |
| `_exception_message` | [第3952–3956行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3952) | 起点计划、选择与误差 |
| `_evaluate_raw_start_outcome` | [第3959–4129行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:3959) | 每起点后处理与阶段证据 |
| `_evaluate_ssvi_start_outcome` | [第4132–4387行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4132) | 每起点后处理与阶段证据 |
| `_optimizer_summary` | [第4390–4408行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4390) | 每起点后处理与阶段证据 |
| `_candidate_arrays` | [第4411–4427行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4411) | 草稿物化与失败保护 |
| `_null_fit_metrics` | [第4430–4435行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4430) | 草稿物化与失败保护 |
| `_all_not_run_checks` | [第4438–4439行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4438) | 草稿物化与失败保护 |
| `_fail_closed_local_checks` | [第4442–4453行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4442) | 草稿物化与失败保护 |
| `_candidate_sampling_failure_checks` | [第4456–4477行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4456) | 草稿物化与失败保护 |
| `_resolved_draft_checks` | [第4480–4488行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4480) | 草稿物化与失败保护 |
| `_selected_draft_failure_code` | [第4491–4500行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4491) | 草稿物化与失败保护 |
| `_per_expiry_metric` | [第4503–4521行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4503) | 草稿物化与失败保护 |
| `_local_failure_from_metrics_and_checks` | [第4524–4536行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4524) | 草稿物化与失败保护 |
| `_expiry_candidate_from_curve` | [第4539–4601行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4539) | 草稿物化与失败保护 |
| `fit_raw_svi_local` | [第4604–4697行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4604) | 实际候选入口与JSON输出 |
| `_aggregate_ssvi_parent_checks` | [第4700–4728行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4700) | 实际候选入口与JSON输出 |
| `_not_enough_maturities_bundle` | [第4731–4781行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4731) | 实际候选入口与JSON输出 |
| `fit_ssvi_local` | [第4784–4997行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:4784) | 实际候选入口与JSON输出 |
| `_build_nonparametric_local_candidate` | [第5000–5039行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:5000) | 实际候选入口与JSON输出 |
| `build_pchip_local_candidate` | [第5042–5054行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:5042) | 实际候选入口与JSON输出 |
| `build_linear_local_candidate` | [第5057–5069行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:5057) | 实际候选入口与JSON输出 |
| `to_json_compatible` | [第5072–5106行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/total_variance_fit.py:5072) | 实际候选入口与JSON输出 |
