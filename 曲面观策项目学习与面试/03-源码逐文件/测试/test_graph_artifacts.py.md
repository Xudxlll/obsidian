---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份测试文件防什么错误

测试Notebook、五案例快照、空白人工评分、报告和打包合同。

核心是防报告脱离真实源证据、防合成3级混入业绩、防伪造评分。两个用例额外依赖Jupyter内核/演示数据和PowerShell，不具备环境时可失败，不能将其静默算作通过。

源文件：[test_graph_artifacts.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py>)。

## 输入与输出

测试读取临时或明确指定的样本/结果，输出断言的通过或失败。下面列的是测试函数定义数，参数化会展开多个运行用例；不能把函数数当实际测试case数。此文件有10个test函数。

## 逐项合同索引

### `test_task8_deliverables_exist_and_formal_acceptance_is_unchanged`

[定位第95行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:95>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
all((path.is_file() for path in required))
not REVIEW_SUMMARY.exists()
hashlib.sha256(ACCEPTANCE.read_bytes()).hexdigest().upper() == EXPECTED_ACCEPTANCE_SHA256
```

### `test_notebook_builder_is_deterministic_and_executes_without_errors`

[定位第113行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:113>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
tuple((cell['id'] for cell in notebook.cells)) == EXPECTED_NOTEBOOK_CELL_IDS
notebook.metadata.kernelspec.name == 'python3'
'OptionRiskAgent' in source
'OPTION_RISK_DATA_DIR' in source
```

### `test_delivered_notebook_is_fully_executed_and_matches_builder`

[定位第152行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:152>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
tuple((cell['id'] for cell in delivered.cells)) == EXPECTED_NOTEBOOK_CELL_IDS
[cell.source for cell in delivered.cells] == [cell.source for cell in template.cells]
all((cell.execution_count is not None for cell in code_cells))
not any((output.get('output_type') == 'error' for cell in code_cells for output in cell.get('outputs', [])))
```

### `test_snapshot_is_strict_versioned_traceable_and_covers_five_scenarios`

[定位第167行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:167>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
payload['format_version'] == 'kg-snapshot-v1'
payload['schema_version'] == KG_SCHEMA_VERSION
payload['rule_version'] == KG_RULE_VERSION
payload['formal_acceptance_sha256'] == EXPECTED_ACCEPTANCE_SHA256
```

### `test_review_template_is_blank_and_aggregation_math_is_exact`

[定位第262行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:262>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
len(rows) == 5
all((row[column] == '' for row in rows for column in (*SCORE_COLUMNS, 'reviewer_id', 'comment', 'reviewed_at')))
summary['overall_mean'] == 4.5
summary['reviewer_count'] == 2
```

### `test_review_aggregation_rejects_incomplete_invalid_and_duplicate_rows`

[定位第305行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:305>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
not summary.exists()
pytest.raises(ValueError)
```

### `test_report_reconciles_all_formal_evidence_and_is_offline_safe`

[定位第345行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:345>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
f'data-total-nodes="{total_nodes}"' in html
f'data-total-edges="{total_edges}"' in html
f'data-total-paths="{total_paths}"' in html
'35/35' in html
```

### `test_report_escapes_external_text_and_rejects_inconsistent_acceptance`

[定位第375行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:375>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
'<img src=x onerror="alert(1)">' not in html
'&lt;img src=x onerror=&quot;alert(1)&quot;&gt;' in html
not blocked_output.exists()
pytest.raises(ValueError)
```

### `test_readme_and_problem2_guide_cover_cross_platform_operation_and_boundaries`

[定位第412行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:412>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
all((phrase in combined for phrase in required_phrases))
'python==3.12' not in combined.lower()
not re.search('(?i)(?:[a-z]:[\\\\/]|/Users/|/home/)', combined)
```

### `test_package_manifest_is_explicit_clean_and_contains_problem2_delivery`

[定位第449行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_artifacts.py:449>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
shell is not None
completed.returncode == 0
manifest['audit']['absolute_path_scan_passed'] is True
manifest['audit']['raw_data_scan_passed'] is True
```

## 复习方法与实际执行状态

先说出该测试想防的错误，再改变一个输入，预测哪个断言会失败。所有当前运行记录集中在[[曲面观策项目学习与面试/04-面试与验证/05-本轮验证记录.md|05-本轮验证记录]]；历史文档的751项不能替代本轮实际收集与执行数。
