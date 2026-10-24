---
tags: [曲面观策, 源码逆向, 测试, 数值验证, 故障注入]
source: tests/test_total_variance_fit.py
source_lines: 4391
test_function_count: 109
read_scope: 全文件；前段原文、后段完整AST语句规范化阅读
---

> [!abstract] 测试实际保护什么
> 109个顶层 `test_` 函数分为封闭契约、数学金值、数值边界、起点确定性、异常证据保留几大族。参数化展开后的用例数会更多。它验证数值内核与草稿契约；不能单凭此文件宣称整条AG装载、发布、UI或全量行情已端到端通过。

源文件：[test_total_variance_fit.py](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1)。实现对照：[[曲面观策项目学习与面试/03-源码逐文件/曲面拟合/total_variance_fit.py-总方差公式、优化与本地检查.md|total_variance_fit.py-总方差公式、优化与本地检查]]。

## 1. 先分清辅助夹具和真实测试

文件不是109段独立金融算法。前500多行大多在构造最小合法契约对象：`_check`、`_six_checks`、`_summary`、`_attempt`、`_expiry_result`、`_ready_timestamp`、`_failed_input_timestamp`、`_insufficient_timestamp`。这些夹具刻意提供固定身份和合成数组，服务构造器校验；它们不等同真实 `diagnose_timestamp` 的完整结果。

例如 `_ready_timestamp` 给合成矩阵固定水平值，用于测试dataclass的引用和矩阵约束。不要拿夹具里的所有点数、期限名或参数当作生产资格规则。实际生产maturity_id来自整数dte，夹具为可读性也使用ag2505等字符串。

`monkeypatch` 临时替换本模块导入的 `minimize/shgo/检查函数`，用来强制某个失败阶段；测试结束恢复。这样的测试可以证明“收到该类结果时系统怎样反应”，不能证明真实优化器在所有行情上都会收敛。

## 2. 契约与策略测试族：防止数据自相矛盾

| 原始行号 | 代表测试 | 明确保护的行为 |
|---|---|---|
| [569](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:569) | `test_fit_policy_is_frozen_exact_and_serializes_all_fixed_solver_rules` | 不只检查几个容差，还锁定种子、循环顺序、去重、成功/失败排序、SHGO完整性规则 |
| [690](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:690) | v1策略不许无版本变更 | 改策略必须改版本；测试版可改网格 |
| [713](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:713) | 嵌套映射不可修改 | dataclass冻结不足以保护dict，需额外策略 |
| [721](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:721)、[751](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:751) | attempt/pair身份金值 | 全canonical payload参与哈希，改顺序或期限会改变ID |
| [783](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:783) | 拒绝伪造ID | 时点对象会重算身份，不能只符合字符串正则 |
| [876](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:876)、[1054](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1054) | 枚举顺序和精确字段 | 关闭未知状态/字段漂移；UNUSABLE属于结果方法而非拟合尝试 |
| [1085](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1085) | 起点计数对账 | 生成、丢弃、执行和成功数不能互相矛盾 |
| [1134](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1134)至[1460](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1460) | 封闭状态真值表 | 接受↔success、本地成功所需硬门、父级阻断、首失败优先级、非参数g状态 |

关键思维：不是“给一个好对象能构造”就够，还要对每个重要字段做矛盾修改，断言它必须失败。这个文件大量使用 `dataclasses.replace` 构造近似合法但自相矛盾的对象，这是契约测试的重要手法。

例：`optimizer_success=True`与失败码optimizer_failed同时出现必须拒绝；`local_success=True`却正方差门失败也拒绝；PCHIP的g必须是method_has_no_analytic_g，不能被写成普通not_run蒙混过关。

## 3. 最终引用、矩阵与来源测试族

[1463–1836行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1463)验证：可用结果需要选中记录；不可用结果不能保留正式fit数组；节点不足必须没有任何候选历史；final_checks与数组必须复制对应记录；接受之后不能继续产生可选择候选；method_counts必须从结果重算。

`test_timestamp_validates_every_finite_surface_iv_cell_from_w_and_t` [1688](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1688)仅把一个IV单元格加 $10^{-12}$ 就要求失败，说明这里是精确复算契约，不是用“看起来差不多”的图判定一致性。

来源测试确保failed_input必须多种有效来源且合并数0；ready时有有效节点就必须恰一种匹配来源。日历配对测试区分“已有比较对象却没重叠”与“根本没有先前期限”，并允许父级本地失败时仍保留子引用但配对not_run。

## 4. 公式金值与差分：验证两个不同错误来源

| 测试位置 | 验证办法 | 为什么必要 |
|---|---|---|
| [1839](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1839) | IV→w→IV往返，零IV前向允许 | 单位与正性边界 |
| [1863](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1863) | 参数化负数、非有限、零期限 | 输入合法性不能靠公式自然报错 |
| [2025](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2025) | SSVI三个预先算好的w + 中央差分一二阶导 | 防止公式错误，也防止导数虽自洽却相对真值错误 |
| [2049](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2049) | Raw SVI同样的金值与差分 | 符号、平方、位移和sigma次幂容易写错 |
| [2068](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2068) | 分别触发theta下降、屏障、最低值、翼部违反 | 避免一条约束掩盖其他遗漏 |
| [2099](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2099) | 固定SSVI目标0.10949762428614794、Raw目标0.48744933182676004 | 锁定逐期限等权、标准化与求和口径 |

差分步长为 $h=10^{-5}$，一阶近似 $(w(k+h)-w(k-h))/(2h)$，二阶近似 $(w(k+h)-2w(k)+w(k-h))/h^2$。它是测试参考，不是运行时参数曲线导数的实现方式。

误差算例：观察 $[0.01,0.02,0.09]$ 与拟合 $[0.02,0.01,0.08]$，RMSE=0.01，NRMSE=0.5；这锁定分母是中位数0.02，而非均值0.04或最大值0.09。

## 5. 闭域、插值与浮点数边界族

[1870](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1870)精确验证诊断网格为 `np.unique(linspace∪raw_k)`；只读标志不可写。不是简单测试“长度=201”。

[1888–1956](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1888)给4种方法都喂同一私有测试求值器，用nextafter构造刚越界一个浮点单位的点；要求端点支持而外侧空值。还确认没有可公开打开extrapolate的参数。

[2133](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2133)验证PCHIP和线性在节点命中；[2154](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2154)验证各方法资格，而不假定“节点少一点也可以凑”。[2754](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2754)再专门对参数曲线构造器做闭域回归。

[3093–3160](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3093)构造极近浮点邻点，检验convex割线有限、左右邻点使用正确线性段、单调价格差采用导数极限。金融公式正确但数值相减不稳定也能产生假套利，这组测试直接防此问题。

## 6. 价格形状、g与自适应细化族

[2188](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2188)使用非均匀执行价比例检验价格单调/凸性；坏曲线分别触发价格上涨与割线斜率下降。[2219](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2219)检查复合网格确实包含原节点、结点和左右邻点。

最有教学价值的是 [2259](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2259)：构造一个Raw SVI窄异常，201点基网格的最小g仍为正，复合/自适应检查却发现负g。它具体说明“粗网格未发现”不等于没有违反。该案例验证了一个反例被修复，不是证明所有窄反例都被捕获。

[2233](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2233)把正方差放到地板附近，要求不确定；直接价格形状函数则不因同样原因主动细化。[2600](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2600)锁定恰好最大轮数，[2619](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2619)构造只在禁止的额外一轮才出现异常的点，要求保持resolution_limit，不能偷跑第3轮改变协议。

[2648](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2648)使中点出现NaN：探测点必须留下，正方差检查失败。[2679](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2679)对g与日历也注入非有限中点，结果必须不确定。这三种非有限行为不同：正方差没有合法w属于直接失败；g/日历无法可靠比较属于不确定。

## 7. 日历边界和跳变搜索族

[2324](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2324)用近月w=0.04、远月w=0.05/0.03/0.039799，分别验证通过/失败/不确定；共同区间必须为两曲线支持交集。只在一个端点相接的支持在 [2363](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2363)要求NOT_TESTABLE，不会冒充成功比较。

[2394](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2394)用平坦IV通过、局部1.5的尖峰失败，并验证前门失败关闭后续门，非参数g仍保留结构性不适用。

| 搜索方法 | 核验点 |
|---|---|
| PCHIP [2440](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2440) | 所有驻点候选与50万点密参考最大斜率接近；位置也接近 |
| LINEAR [2460](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2460) | 最大值在每段较小w端点，不只看全局左右端 |
| SHGO [2486](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2486) | success=False、缺局部解、NaN局部目标均不确定 |
| 异常 [2505](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2505) | 求根和SHGO抛错，必须封闭为resolution_limit |
| 真SHGO [2543](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2543) | 记录真实调用参数，匹配密网格最大值 |
| 网格独立 [2581](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2581) | 改base_grid_size不改变跳变检查完整结论 |
| 根集锁定 [2801](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2801) | 精确去重会保留非常近但不同浮点根，候选集不能随意容差合并 |

这里“密网格参考”只用于合成曲线验证。50万点也不是数学证明，但能有效发现驻点求解漏候选和量级错误。

## 8. 固定多起点、并列排序与失败代表族

[2856](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2856)锁定SSVI27种子所有索引、theta初值和边界；[2895](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2895)锁定Raw36起点的尺度、跨度、循环次序和代表索引；[2931](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2931)验证预检后精确去重，正负零合并，而nextafter不同浮点值保留。

[2982](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2982)人为给目标近似并列，验证先用NRMSE、再参数字符串和索引；[2997](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2997)锁定完整失败八元排序与`.15g`格式。特别要知道：失败排序中的primary priority数值小会先选，它是一项确定规则，不可自行解释成“失败越晚越好”替代真实tuple。

[3064](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3064)强制优化器报告失败但返回有限参数，结果仍推进到stage4保留曲线，primary失败仍是optimizer_failed。[3163](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3163)验证只调用固定SLSQP：36生成但因m种子重合去重18，实际执行18。它证明“生成数”与“执行数”必须分开。

[3221](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3221)验证优化成功却RMSE过大仍失败；[3249](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3249)验证SSVI父级优化失败仍保留各期限可求值子草稿；[3328](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3328)对相同模拟结果跑两次，比对参数、摘要、采样数组和失败码的确定性。

## 9. 后处理故障注入族：最接近工程质量的部分

[3382–3475](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3382)逐层把Raw失败停在stage0/1/2/3，核对已经取得的参数、曲线、指标没有丢失；不能把所有异常都笼统归成optimizer_exception。

[3478](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3478)让Raw参数rho=2导致约束后处理异常，全部36个起点继续执行，保留曲线但标记resolution_limit；[3577–3887](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3577)对SSVI同样验证多曲线、多期限指标和规范fail-closed状态。

[3894](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3894)第一期限有已知RMSE失败、第二期限指标异常时：第一子级保持rmse_exceeded，第二子级为check_resolution_limit；父级则按优化器是否成功决定最早已知失败。已知证据不能被后来异常抹平。

[3951](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3951)第一期限检查完成、第二期限检查抛错：保留第一期限真实检查，第二期限关闭为规范不确定；父级聚合保留首个已知失败。它避免“一个期限异常就把全部期限统一清空”的诊断退化。

[4024](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4024)全部27次SSVI优化抛错仍需计数对账，保留父级逐期限键与空指标，无子曲线；[4074](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4074)所有起点预检丢弃时执行数0且selected index为空。

[4176–4391](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4176)把局部检查异常、诊断采样网格异常、evaluate_curve异常转成可以物化为正式 `FitAttemptDiagnostic` 的失败草稿。关键是“失败记录自己也要符合契约”；不能只断言没崩溃。

## 10. 哪些结论还不能由本文件给出

1. 不是完整AG全量数据测试，不足以说明真实行情拟合成功率或性能。
2. 多个优化阶段用假的minimize/shgo结果，是行为契约测试，不能替代真实优化器收敛实验；其中SHGO有单独真实运行对照。
3. 不是UI截图与图像布局验证，不足以证明图表可读性。
4. 没有把一般曲线连续域无套利证明出来；样例通过和理论全域保证不同。
5. 不是缓存/目录能力、六文件发布的全部测试；这些应看诊断编排对应测试与项目整体验证。
6. 本轮笔记生成阶段只读源码，根代理统一执行项目测试；本篇不冒用静态阅读为“109函数全部已通过”的运行结果。真实执行记录应看知识库验证汇总。

## 11. 面试训练：把测试讲成证据链

**问：你怎么确认导数写对？** 答：先对公式输出比预先计算金值，再对一二阶导比中央差分；两个维度分别约束公式本身与导数实现，还分别检查参数屏障。

**问：为什么要测试NaN中点？** 答：自适应算法可能先在中点探到异常，如果不将该点并入最终网格就丢失证据；测试强制保留并核对失败/不确定语义。

**问：为什么不是只测最终可用结果？** 答：失败候选是审计和解释的核心。工程上优化器失败后仍可能有有限曲线，后处理也可能局部失败；需要证明计数、参数、曲线和首个失败原因全部自洽。

**问：怎么设计一个新的有效测试？** 答：找尚未被现有夹具覆盖的真实失败模式，构造最小反例，同时断言行为、证据保留和契约一致性。重复实现同一公式再比对两份相同错误，价值较低。

## 12. 学习练习

尝试解释：一个Raw候选生成36起点，去重18，18次优化都报告成功，但每次NRMSE=0.4。`local_success_count`、`selection_kind`与失败码分别是什么？

> [!success]- 答案
> local_success_count=0；selection_kind=failure_representative；失败码为rmse_exceeded（前提参数与约束已通过，没有更早失败）。优化器成功计数18仍可保留，但不等于18次本地成功，更不等于18条最终接受记录。

附录索引覆盖本文件所有顶层辅助函数与测试函数；参数化装饰器属于对应函数的测试配置。

## 附录：完整顶层定义定位索引

下表覆盖此文件每一个顶层函数/类定义；“所属功能簇”对应正文解释。类内方法随所属类阅读，嵌套闭包随外层函数阅读。

| 定义 | 原始行号 | 所属功能簇 |
|---|---|---|
| `_assert_frozen_dataclass` | [第51–55行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:51) | 合法对象与状态夹具 |
| `test_nonparametric_butterfly_status_survives_an_earlier_failed_gate` | [第58–93行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:58) | 合法对象与状态夹具 |
| `_check` | [第96–131行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:96) | 合法对象与状态夹具 |
| `_six_checks` | [第134–152行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:134) | 合法对象与状态夹具 |
| `_failed_check` | [第155–166行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:155) | 合法对象与状态夹具 |
| `_resolution_check` | [第169–180行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:169) | 合法对象与状态夹具 |
| `_not_run_checks` | [第183–197行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:183) | 合法对象与状态夹具 |
| `_summary` | [第200–211行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:200) | 合法对象与状态夹具 |
| `_per_expiry_metric` | [第214–226行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:214) | 合法对象与状态夹具 |
| `_attempt` | [第229–337行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:229) | 合法对象与状态夹具 |
| `_expiry_result` | [第340–364行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:340) | 合法对象与状态夹具 |
| `_accepted_attempt_and_result` | [第367–404行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:367) | 合法对象与状态夹具 |
| `_ready_timestamp` | [第407–459行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:407) | 合法对象与状态夹具 |
| `_failed_input_timestamp` | [第462–502行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:462) | 合法对象与状态夹具 |
| `_insufficient_timestamp` | [第505–566行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:505) | 合法对象与状态夹具 |
| `test_fit_policy_is_frozen_exact_and_serializes_all_fixed_solver_rules` | [第569–687行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:569) | 策略、身份与封闭状态契约 |
| `test_v1_fit_policy_rejects_strategy_overrides_without_a_new_version` | [第690–700行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:690) | 策略、身份与封闭状态契约 |
| `test_fit_policy_nested_strategy_mappings_are_immutable` | [第713–718行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:713) | 策略、身份与封闭状态契约 |
| `test_attempt_id_uses_the_full_canonical_identity_payload` | [第721–748行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:721) | 策略、身份与封闭状态契约 |
| `test_calendar_pair_id_uses_the_full_canonical_identity_payload` | [第751–780行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:751) | 策略、身份与封闭状态契约 |
| `test_timestamp_rejects_forged_attempt_and_pair_ids` | [第783–841行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:783) | 策略、身份与封闭状态契约 |
| `test_closed_enumerations_preserve_exact_values_and_order` | [第876–879行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:876) | 策略、身份与封闭状态契约 |
| `test_unusable_is_a_final_method_not_a_fit_attempt_method` | [第882–884行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:882) | 策略、身份与封闭状态契约 |
| `test_closed_dataclasses_have_exact_required_fields` | [第1054–1063行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1054) | 策略、身份与封闭状态契约 |
| `test_contract_annotations_keep_required_and_nullable_fields_distinct` | [第1066–1082行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1066) | 策略、身份与封闭状态契约 |
| `test_optimizer_start_summary_enforces_reconciliation_and_upper_bounds` | [第1085–1100行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1085) | 策略、身份与封闭状态契约 |
| `test_attempt_truth_table_accepts_every_closed_row` | [第1134–1163行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1134) | 策略、身份与封闭状态契约 |
| `test_attempt_truth_table_rejects_contradictory_rows` | [第1177–1180行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1177) | 策略、身份与封闭状态契约 |
| `test_attempt_truth_table_rejects_method_and_stage_failure_code_mismatches` | [第1250–1254行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1250) | 策略、身份与封闭状态契约 |
| `test_skipped_ssvi_parent_has_no_parameters_or_executed_checks` | [第1257–1278行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1257) | 策略、身份与封闭状态契约 |
| `test_non_parametric_methods_reject_parameter_and_butterfly_failure_codes` | [第1286–1297行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1286) | 策略、身份与封闭状态契约 |
| `test_failure_code_requires_its_corresponding_method_check_state` | [第1320–1340行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1320) | 策略、身份与封闭状态契约 |
| `_accepted_attempt_for_method` | [第1343–1350行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1343) | 策略、身份与封闭状态契约 |
| `test_accepted_attempt_requires_every_applicable_local_hard_check_to_pass` | [第1357–1366行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1357) | 策略、身份与封闭状态契约 |
| `test_calendar_stage_local_success_rejects_an_earlier_failed_local_gate` | [第1369–1381行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1369) | 策略、身份与封闭状态契约 |
| `test_primary_failure_code_is_the_first_actual_failed_hard_gate` | [第1426–1434行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1426) | 策略、身份与封闭状态契约 |
| `test_non_parametric_butterfly_check_is_never_generic_not_run` | [第1438–1447行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1438) | 策略、身份与封闭状态契约 |
| `test_parameter_method_accepted_attempt_must_execute_analytic_butterfly_gate` | [第1451–1460行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1451) | 策略、身份与封闭状态契约 |
| `test_expiry_result_enforces_usable_and_unusable_reference_rules` | [第1463–1480行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1463) | 结果引用、矩阵与来源契约 |
| `test_insufficient_nodes_result_requires_null_terminal_reference` | [第1483–1491行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1483) | 结果引用、矩阵与来源契约 |
| `test_timestamp_cross_validates_selected_attempt_status_method_and_expiry` | [第1494–1531行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1494) | 结果引用、矩阵与来源契约 |
| `test_timestamp_requires_final_checks_and_arrays_to_copy_selected_attempt` | [第1534–1550行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1534) | 结果引用、矩阵与来源契约 |
| `test_timestamp_requires_unusable_failure_to_copy_terminal_attempt` | [第1553–1600行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1553) | 结果引用、矩阵与来源契约 |
| `test_usable_result_rejects_selection_candidates_after_the_accepted_attempt` | [第1603–1632行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1603) | 结果引用、矩阵与来源契约 |
| `test_insufficient_nodes_rejects_attempts_candidates_and_non_not_run_checks` | [第1635–1666行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1635) | 结果引用、矩阵与来源契约 |
| `test_timestamp_recomputes_method_counts_from_expiry_results` | [第1669–1685行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1669) | 结果引用、矩阵与来源契约 |
| `test_timestamp_validates_every_finite_surface_iv_cell_from_w_and_t` | [第1688–1697行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1688) | 结果引用、矩阵与来源契约 |
| `test_failed_input_requires_zero_merged_nodes_and_multiple_sources` | [第1700–1719行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1700) | 结果引用、矩阵与来源契约 |
| `test_ready_timestamp_requires_one_matching_source_when_valid_nodes_exist` | [第1735–1744行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1735) | 结果引用、矩阵与来源契约 |
| `test_evaluated_calendar_pair_requires_positive_width_common_bounds` | [第1775–1790行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1775) | 结果引用、矩阵与来源契约 |
| `test_expiry_selection_pair_rejects_not_applicable_no_prior_maturity` | [第1793–1806行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1793) | 结果引用、矩阵与来源契约 |
| `test_ssvi_parent_local_failure_pair_retains_child_references_as_not_run` | [第1809–1836行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1809) | 结果引用、矩阵与来源契约 |
| `test_total_variance_and_display_iv_round_trip` | [第1839–1845行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1839) | 换算、闭域和JSON |
| `test_variance_conversions_reject_invalid_inputs` | [第1863–1867行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1863) | 换算、闭域和JSON |
| `test_diagnostic_curve_grid_is_exact_numpy_unique_union` | [第1870–1884行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1870) | 换算、闭域和JSON |
| `test_every_curve_method_uses_one_closed_domain_evaluator` | [第1888–1925行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1888) | 换算、闭域和JSON |
| `test_curve_model_construction_is_private_and_public_api_cannot_enable_extrapolation` | [第1928–1940行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1928) | 换算、闭域和JSON |
| `test_evaluate_curve_preserves_supported_bad_w_as_null_safe_diagnostics` | [第1943–1956行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1943) | 换算、闭域和JSON |
| `test_recursive_json_adapter_normalizes_numpy_scalars_and_preserves_null` | [第1959–1978行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1959) | 换算、闭域和JSON |
| `test_recursive_json_adapter_rejects_non_finite_values` | [第1982–1984行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1982) | 换算、闭域和JSON |
| `test_check_metrics_allow_only_finite_json_scalars_not_arrays` | [第1987–1999行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:1987) | 换算、闭域和JSON |
| `test_check_truth_table_rejects_reason_codes_from_the_wrong_status` | [第2017–2022行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2017) | 换算、闭域和JSON |
| `test_ssvi_formula_and_analytic_derivatives_match_hand_values_and_differences` | [第2025–2046行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2025) | 公式、导数、目标和资格 |
| `test_raw_svi_formula_and_analytic_derivatives_match_hand_values_and_differences` | [第2049–2065行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2049) | 公式、导数、目标和资格 |
| `test_ssvi_and_raw_analytic_constraint_slacks_enforce_every_barrier` | [第2068–2096行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2068) | 公式、导数、目标和资格 |
| `test_golden_ssvi_and_raw_objectives_and_nrmse_scale_are_exact` | [第2099–2126行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2099) | 公式、导数、目标和资格 |
| `test_interpolators_hit_nodes_and_never_extrapolate` | [第2133–2151行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2133) | 公式、导数、目标和资格 |
| `test_curve_builders_reject_method_ineligible_node_counts` | [第2154–2185行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2154) | 公式、导数、目标和资格 |
| `test_normalized_black_checks_use_nonuniform_strike_ratio_monotonicity_and_secants` | [第2188–2216行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2188) | 无套利、跳变和浮点边界 |
| `test_composite_grid_contains_raw_knots_and_both_knot_neighbors` | [第2219–2230行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2219) | 无套利、跳变和浮点边界 |
| `test_positive_refinement_can_be_resolution_limited_but_price_shape_never_is` | [第2233–2256行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2233) | 无套利、跳变和浮点边界 |
| `test_ssvi_and_raw_use_analytic_g_and_interpolators_close_the_gate` | [第2259–2313行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2259) | 无套利、跳变和浮点边界 |
| `test_calendar_pair_uses_one_common_adaptive_grid_and_closed_outcomes` | [第2324–2360行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2324) | 无套利、跳变和浮点边界 |
| `test_calendar_pair_without_public_domain_is_not_testable_no_overlap` | [第2363–2391行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2363) | 无套利、跳变和浮点边界 |
| `test_jump_check_passes_constant_curve_rejects_spike_and_closes_later_gates` | [第2394–2437行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2394) | 无套利、跳变和浮点边界 |
| `test_pchip_enumerates_all_stationary_roots_and_matches_dense_reference` | [第2440–2457行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2440) | 无套利、跳变和浮点边界 |
| `test_linear_jump_maximum_uses_each_segment_minimum_w_endpoint` | [第2460–2469行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2460) | 无套利、跳变和浮点边界 |
| `test_parameter_jump_requires_complete_finite_successful_shgo_result` | [第2486–2502行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2486) | 无套利、跳变和浮点边界 |
| `test_jump_root_or_shgo_exception_is_closed_as_resolution_limit` | [第2505–2540行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2505) | 无套利、跳变和浮点边界 |
| `test_parameter_jump_calls_fixed_shgo_and_matches_dense_reference` | [第2543–2578行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2543) | 无套利、跳变和浮点边界 |
| `test_jump_conclusion_is_independent_of_base_grid_size` | [第2581–2597行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2581) | 无套利、跳变和浮点边界 |
| `test_adaptive_refinement_stops_after_exactly_max_depth_rounds` | [第2600–2616行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2600) | 无套利、跳变和浮点边界 |
| `test_violation_only_on_forbidden_extra_round_remains_resolution_limited` | [第2619–2645行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2619) | 无套利、跳变和浮点边界 |
| `test_nonfinite_midpoint_probe_is_retained_and_positive_check_fails_closed` | [第2648–2676行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2648) | 无套利、跳变和浮点边界 |
| `test_nonfinite_midpoint_probe_makes_g_and_calendar_indeterminate` | [第2679–2750行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2679) | 无套利、跳变和浮点边界 |
| `test_parameter_curve_builders_obey_closed_domain_at_nextafter` | [第2754–2786行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2754) | 无套利、跳变和浮点边界 |
| `test_raw_left_and_right_wing_constraints_fail_independently` | [第2789–2798行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2789) | 无套利、跳变和浮点边界 |
| `test_pchip_stationary_candidate_set_is_complete_and_locked` | [第2801–2823行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2801) | 无套利、跳变和浮点边界 |
| `_local_expiry` | [第2826–2843行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2826) | 起点计划、确定性与候选构造 |
| `_complete_shgo_result` | [第2846–2853行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2846) | 起点计划、确定性与候选构造 |
| `test_ssvi_start_plan_locks_theta_initialization_bounds_and_all_27_indices` | [第2856–2892行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2856) | 起点计划、确定性与候选构造 |
| `test_raw_start_plan_locks_scale_bounds_loop_order_and_all_36_indices` | [第2895–2928行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2895) | 起点计划、确定性与候选构造 |
| `test_start_precheck_then_float64_exact_dedup_keeps_earliest_original_index` | [第2931–2954行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2931) | 起点计划、确定性与候选构造 |
| `_outcome` | [第2957–2979行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2957) | 起点计划、确定性与候选构造 |
| `test_near_tie_success_selection_uses_nrmse_formatted_parameters_then_index` | [第2982–2994行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2982) | 起点计划、确定性与候选构造 |
| `test_failure_representative_uses_the_complete_fixed_tuple_and_15g_key` | [第2997–3061行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:2997) | 起点计划、确定性与候选构造 |
| `test_raw_start_continues_to_stage_four_after_optimizer_reports_failure` | [第3064–3090行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3064) | 起点计划、确定性与候选构造 |
| `test_convex_check_keeps_near_equal_float64_k_strike_intervals_finite` | [第3093–3109行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3093) | 起点计划、确定性与候选构造 |
| `test_convex_cancellation_limit_uses_linear_interval_left_endpoint_segment` | [第3126–3142行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3126) | 起点计划、确定性与候选构造 |
| `test_monotonic_cancellation_interval_uses_limiting_slope_price_change` | [第3145–3160行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3145) | 起点计划、确定性与候选构造 |
| `test_raw_local_fit_uses_only_fixed_slsqp_and_one_draft_for_all_starts` | [第3163–3218行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3163) | 起点计划、确定性与候选构造 |
| `test_optimizer_success_with_failed_rmse_is_a_failure_representative` | [第3221–3246行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3221) | 起点计划、确定性与候选构造 |
| `test_ssvi_failure_representative_builds_one_parent_and_evaluable_child_drafts` | [第3249–3303行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3249) | 起点计划、确定性与候选构造 |
| `test_local_candidate_builders_enforce_method_node_eligibility` | [第3306–3325行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3306) | 起点计划、确定性与候选构造 |
| `test_local_failure_representative_is_bitwise_deterministic_across_two_runs` | [第3328–3354行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3328) | 起点计划、确定性与候选构造 |
| `_raw_stage_expiry` | [第3357–3363行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3357) | 故障注入与证据保留 |
| `_raw_stage_outcome` | [第3366–3379行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3366) | 故障注入与证据保留 |
| `test_start_outcome_stage_zero_requires_no_finite_parameter_vector` | [第3382–3391行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3382) | 故障注入与证据保留 |
| `test_start_outcome_stage_one_keeps_finite_parameters_after_node_evaluation_error` | [第3394–3410行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3394) | 故障注入与证据保留 |
| `test_start_outcome_stage_two_keeps_curve_when_constraint_evaluation_raises` | [第3413–3427行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3413) | 故障注入与证据保留 |
| `test_start_outcome_stage_three_keeps_curve_when_metric_evaluation_raises` | [第3430–3450行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3430) | 故障注入与证据保留 |
| `test_start_outcome_stage_three_keeps_metrics_when_local_check_evaluation_raises` | [第3453–3475行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3453) | 故障注入与证据保留 |
| `test_raw_constraint_postprocess_exception_continues_all_36_starts_and_keeps_curve` | [第3478–3529行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3478) | 故障注入与证据保留 |
| `_ssvi_stage_expiries` | [第3532–3548行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3532) | 故障注入与证据保留 |
| `_assert_canonical_fail_closed_local_checks` | [第3551–3574行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3551) | 故障注入与证据保留 |
| `test_ssvi_constraint_postprocess_exception_reaches_stage_two_with_all_curves` | [第3577–3607行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3577) | 故障注入与证据保留 |
| `test_ssvi_metric_exception_reaches_stage_three_and_keeps_all_curves` | [第3610–3640行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3610) | 故障注入与证据保留 |
| `test_ssvi_check_exception_reaches_stage_three_and_keeps_all_metrics` | [第3643–3673行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3643) | 故障注入与证据保留 |
| `test_ssvi_selected_finite_parameters_and_curves_survive_constraint_exception` | [第3676–3735行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3676) | 故障注入与证据保留 |
| `test_ssvi_stage_two_optimizer_failure_maps_children_to_resolution_limit` | [第3738–3795行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3738) | 故障注入与证据保留 |
| `test_ssvi_stage_three_constraint_failure_keeps_fail_closed_children` | [第3798–3841行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3798) | 故障注入与证据保留 |
| `test_ssvi_rmse_failure_precedes_later_check_exception_for_every_child` | [第3844–3887行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3844) | 故障注入与证据保留 |
| `test_ssvi_partial_metrics_classify_each_child_at_earliest_known_gate` | [第3894–3941行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3894) | 故障注入与证据保留 |
| `test_ssvi_partial_checks_preserve_completed_child_gate_before_exception` | [第3951–4021行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:3951) | 故障注入与证据保留 |
| `test_ssvi_all_27_optimizer_exceptions_reconcile_and_keep_parent_metric_keys` | [第4024–4071行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4024) | 故障注入与证据保留 |
| `test_all_precheck_discarded_starts_reconcile_with_zero_execution` | [第4074–4110行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4074) | 故障注入与证据保留 |
| `_exact_raw_stage_expiry` | [第4113–4117行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4113) | 故障注入与证据保留 |
| `_materialize_failed_local_draft` | [第4120–4166行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4120) | 故障注入与证据保留 |
| `test_raw_check_exception_draft_round_trips_to_fit_attempt_diagnostic` | [第4176–4203行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4176) | 故障注入与证据保留 |
| `test_ssvi_check_exception_parent_and_children_round_trip_to_fit_attempts` | [第4213–4242行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4213) | 故障注入与证据保留 |
| `test_raw_candidate_array_exception_becomes_materializable_local_failure` | [第4246–4296行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4246) | 故障注入与证据保留 |
| `test_ssvi_candidate_array_exception_becomes_materializable_child_failure` | [第4300–4349行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4300) | 故障注入与证据保留 |
| `test_nonparametric_candidate_array_exception_preserves_structural_butterfly_and_materializes` | [第4356–4391行](/Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_total_variance_fit.py:4356) | 故障注入与证据保留 |
