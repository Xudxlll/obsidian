---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/README.md](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/README.md>)

SHA-256：`a0052739464b3395973d489f001e0e08e9c7d70a16a66daf68ccf9ef41cbfeb8`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````markdown
# 期权波动率曲面与风险知识图谱单Agent系统

本项目完成比赛问题1，并在其基础上完成问题2。对外始终只有一个业务智能体：`OptionRiskAgent`。

最终用户仍然只做三步：

1. 从数据中已有品种的下拉框选择一个品种；
2. 第二个下拉框自动显示该品种的全部可选时间点；
3. 点击“开始风险分析”。

也就是：品种 → 可选时间点 → 确认。用户不需要填写文件路径、模型、阈值、图谱节点或自由文本问题。

## 完整功能

`OptionRiskAgent` 在一次分析中依次完成：

```text
真实品种 + 真实有效时间点
        ↓
数据清洗、质量检查与严格历史窗口
        ↓
总方差拟合的 IV 曲面 + Delta / Gamma / Vega / Theta 曲面
        ↓
12项风险证据与0—3级动态预警（问题1正式结果）
        ↓
NetworkX事件中心知识图谱（问题2解释层）
        ↓
Evidence → Anomaly → Mechanism → Conclusion
        ↓
固定预设查询 + 五段可追溯解释
```

图谱只解释问题1结果，不重新计算或改写预警等级。质量证据只降低解释置信度，不能把市场风险等级上调。

正式 IV 曲面以 `w(k,T)=IV²T` 为拟合对象，并按 SSVI → 带约束与无套利检查的逐期限 Raw-SVI → PCHIP → 2—3节点总方差线性插值的顺序降级。PCHIP和线性插值不外推；节点不足或检查不可靠时直接标记该期限不可用。每次分析都在 `data_quality.iv_surface_fit` 中保留方法、成功状态、RMSE、节点数、无套利检查和失败原因。Greeks仍使用独立的稳定网格计算，不伪装成总方差拟合结果。

界面提供六个结果页签：Agent决策、风险知识图谱、IV与Greeks曲面、风险特征、预警时间轴、离线回测验证。知识图谱页只提供固定预设查询，不提供自由文本输入框。

## 正式验收结果

当前比赛数据自动识别出35个品种：

```text
a, ag, al, ao, au, b, br, bu, c, cs, cu, eb, eg, fu, i, jd, l,
lc, lh, m, ni, p, pb, pg, pp, ps, rb, ru, sc, si, sn, sp, v, y, zn
```

`outputs/agent_acceptance_full.json` 与 `outputs/knowledge_graph_acceptance_full.json` 均为当前合并代码生成：35/35品种通过，0个失败；每个品种均在最后一个有效时点完成问题1分析、图谱构建、固定查询和解释检查。问题2三项全局门禁为：确定性、无未来数据、内容安全。

## 环境要求与安装

- Python >=3.12；不要求必须恰好是3.12；
- 首次安装通常需要网络，以便安装 `pyproject.toml` 中声明的依赖；
- 安装完成并准备好本地数据后，后续分析、Notebook 与报告可离线运行；
- 主要依赖包括 pandas、NumPy、SciPy、PyArrow、NetworkX、Plotly、Matplotlib、scikit-learn、Streamlit、nbformat 和 nbclient。

Windows PowerShell：

```powershell
cd .\option_risk_warning
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

macOS zsh：

```zsh
cd ./option_risk_warning
python3 -m venv .venv
./.venv/bin/python -m pip install -e '.[dev]'
```

macOS 可以运行本Agent及Notebook；macOS 支持但尚未完成真实 Mac 机器正式认证。提交前的正式全量测试是在Windows环境完成的。

## 数据可以是RAR、ZIP或已解压目录

提交包不携带约7.2GB的比赛源压缩包，也不携带约104MB的原始白银演示Parquet子集。请把数据放在提交包外部，再显式传入。

### 已解压Parquet目录

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m option_risk.cli serve `
  --data-dir ..\比赛数据\期权课题 `
  --cache-dir .\data\agent_cache `
  --output-dir .\outputs
```

macOS zsh：

```zsh
./.venv/bin/python -m option_risk.cli serve \
  --data-dir ../比赛数据/期权课题 \
  --cache-dir ./data/agent_cache \
  --output-dir ./outputs
```

### RAR或ZIP压缩包

压缩包由运行环境中的 `tar/bsdtar` 读取，并按品种安全提取到缓存。RAR和ZIP均可作为 `--archive-path`；若本机工具不支持某种格式，可先用系统解压工具手动解压，再按上一节传入Parquet目录。

Windows PowerShell：

```powershell
.\.venv\Scripts\python.exe -m option_risk.cli serve `
  --archive-path ..\比赛数据\期权课题数据集.rar `
  --cache-dir .\data\agent_cache `
  --output-dir .\outputs
```

macOS zsh：

```zsh
./.venv/bin/python -m option_risk.cli serve \
  --archive-path ../比赛数据/期权课题数据集.zip \
  --cache-dir ./data/agent_cache \
  --output-dir ./outputs
```

若 `tar/bsdtar` 报错，使用 Finder、归档实用工具或其他本机解压软件手动解压，然后改用 `--data-dir`。程序不会下载数据，也不会把压缩包内容写到提交包目录之外的指定缓存以外位置。

浏览器打开本机Streamlit地址。第一次看到Streamlit邮箱提示时直接留空并按回车即可，不影响功能。

## Python接口

```python
from pathlib import Path
from option_risk import AgentConfig, OptionRiskAgent
from option_risk.graph_queries import GraphQueryService

agent = OptionRiskAgent(
    AgentConfig(
        data_source=Path("../比赛数据/期权课题"),
        cache_dir=Path("data/agent_cache"),
        output_dir=Path("outputs"),
    )
)

products = agent.list_products()
product = products[0].code
timestamps = agent.list_timestamps(product)
result = agent.analyze(product, timestamps[-1])

print(result.alert_level, result.alert_name)
print(result.knowledge_graph.schema_version)
print(result.knowledge_graph.rule_version)

query = GraphQueryService(result.knowledge_graph)
print(query.root_evidence(limit=3))
print(query.paths_to_alert())
print(query.possible_consequences())
print(query.quality_limitations())
```

唯一公开业务Agent仍是 `OptionRiskAgent`；`GraphQueryService` 是其结果的只读查询工具，不是第二个Agent。

## 命令行固定查询

```powershell
.\.venv\Scripts\python.exe .\scripts\query_knowledge_graph.py `
  --data-dir ..\比赛数据\期权课题 `
  --product ag `
  --timestamp "2025-04-07 10:15:00" `
  --query root-evidence
```

支持的固定查询包括根证据、到预警路径、可能后果、质量限制、精确节点详情和指定异常路径。命令行拒绝自由文本查询与不存在的节点。

## Notebook、报告与人工评分

使用已解压数据重建并执行问题2 Notebook：

```powershell
$env:OPTION_RISK_DATA_DIR = "..\比赛数据\期权课题"
.\.venv\Scripts\python.exe .\scripts\build_knowledge_graph_notebook.py
```

生成空白人工评分模板和自包含报告：

```powershell
.\.venv\Scripts\python.exe .\scripts\build_explanation_review.py
.\.venv\Scripts\python.exe .\scripts\build_knowledge_graph_report.py
```

当前状态是人工评分待完成。评分模板中的评审人、五项分数、评语和时间均为空。只有真实评审人完成所有字段后，才可以运行：

```powershell
.\.venv\Scripts\python.exe .\scripts\build_explanation_review.py `
  --ratings .\outputs\人工解释评分已填写.csv `
  --summary .\outputs\人工解释评分汇总.csv
```

脚本会拒绝空白、非有限值、1—5范围外分数、缺失评审身份/时间和重复的“评审人×案例”记录。正式总分是全部评审人×案例×五个维度值的算术平均，只有不低于4.0/5.0才标为通过。

## 可复现身份与安全边界

每个图谱结果都保存：

- `schema_version`：图节点和边的契约版本；
- `rule_version`：12项Evidence映射规则版本；
- `policy_version` 与 `policy_parameter_hash`：问题1预警策略身份；
- `source_timestamp`：节点和关系引用的数据时点；
- 品种、所选时间、当前值、动态阈值、压力比和规则ID。

动态阈值只读取所选时点之前的合格历史数据。正式验收还执行“追加未来记录后重放同一历史时点”的测试，既有图、路径、查询和解释必须不变。

系统只说明“哪些证据接近/超过阈值、可能通过什么机理影响风险”；不预测涨跌方向，不提供交易建议，不声称新闻或政策是确定原因，也不把无套利几何违反解释为可执行套利。

比赛数据没有独立期货K线时，标的价格仍由 `strike/moneyness` 重构代理；与代理价格相关的CVaR只能作探索性结果。

## 验证

```powershell
# 全部自动化测试
.\.venv\Scripts\python.exe -m pytest -q

# 先用当前合并代码生成一套完整的问题1离线产物（默认品种ag）
.\.venv\Scripts\python.exe -m option_risk.cli run `
  --data-dir ..\比赛数据\白银演示子集 `
  --output-dir .\outputs\p1-current `
  --product ag

# 再对刚生成的完整产物独立重算；提交包内outputs/demo只是轻量证据目录
.\.venv\Scripts\python.exe .\scripts\validate_outputs.py `
  --data-dir ..\比赛数据\白银演示子集 `
  --output-dir .\outputs\p1-current

# 问题2全品种正式验收
.\.venv\Scripts\python.exe .\scripts\validate_knowledge_graph.py `
  --archive-path ..\比赛数据\期权课题数据集.rar `
  --cache-dir .\data\agent_cache `
  --output-dir .\outputs `
  --report .\outputs\knowledge_graph_acceptance_full.json
```

问题1历史正式报告保留其生成时的源代码树身份；问题2在同一项目新增知识图谱模块后，不应把旧产物的历史源树哈希误当成当前合并代码的哈希。需要验证当前代码时，请按上面的顺序新建输出目录并立即校验，不要覆盖历史正式证据。

主要证据文件：

- `outputs/agent_acceptance_full.json`：当前单Agent第一问与第二问35/35全品种验收；
- `outputs/knowledge_graph_acceptance_full.json`：35/35正式图谱验收；
- `outputs/demo/knowledge_graph_snapshot.json`：真实0/1/2级、真实质量受限和明确标记的3级契约案例；
- `notebooks/02_knowledge_graph_demo.ipynb`：已执行的单Agent演示；
- `outputs/问题2-知识图谱验收报告.html`：无网络依赖的技术验收报告；
- `outputs/人工解释评分模板.csv`：等待真实人工填写的空白模板；
- `docs/问题2-知识图谱设计与运行说明.md`：完整部署、查询和审计说明。
````

</details>
