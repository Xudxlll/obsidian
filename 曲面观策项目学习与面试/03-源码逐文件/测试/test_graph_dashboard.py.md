---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份测试文件防什么错误

检查Streamlit图谱页与用户流程。

关注唯一业务Agent、固定查询、图谱展示和审计展开项；有静态源码断言或替身UI测试，不等于真实浏览器在所有尺寸完成操作。

源文件：[test_graph_dashboard.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py>)。

## 输入与输出

测试读取临时或明确指定的样本/结果，输出断言的通过或失败。下面列的是测试函数定义数，参数化会展开多个运行用例；不能把函数数当实际测试case数。此文件有12个test函数。

## 逐项合同索引

### `test_figure_uses_fixed_layers_canonical_path_cap_and_meta_provenance`

[定位第46行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:46>)。

Catches non-layered/random layouts, reordered paths, or untraceable display data.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
tuple(figure.layout.meta['path_ids']) == tuple((path.path_id for path in selected_paths))
tuple(figure.layout.meta['node_ids']) == tuple(expected_nodes)
tuple(figure.layout.meta['edge_ids']) == tuple(expected_edges)
tuple((row[0] for row in points.customdata)) == tuple(expected_nodes)
```

### `test_figure_deduplicates_shared_nodes_edges_and_is_repeatable`

[定位第85行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:85>)。

Catches duplicate shared state nodes/edges or unstable Figure serialization.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
len(points.customdata) == len(tuple(dict.fromkeys((row[0] for row in points.customdata))))
len(first.layout.annotations) == len(first.layout.meta['edge_ids'])
first.to_plotly_json() == second.to_plotly_json() == round_tripped.to_plotly_json()
json.loads(first.to_json()) == json.loads(second.to_json()) == json.loads(round_tripped.to_json())
```

### `test_evidence_hover_and_quality_path_are_registered_and_visible`

[定位第101行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:101>)。

Catches hover values inferred outside graph records or an invisible confidence path.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
points.hovertext[evidence_index] == f"<b>{evidence['label']}</b><br>类型：Evidence<br>品种：{evidence['product']}<br>时间：{evidence['source_timestamp']}<br>当前值：{evidence['current_value']}<br>动态阈值：{evidence['reference_value']}<br>压力：{evidence['pressure_ratio']}<br>方向：{evidence['direction']}<br>数据源：{evidence['source']}<br>规则ID：{evidence['rule_id']}"
evidence_row[1] == 'Evidence'
len(quality_paths) == 1
'置信度路径' in ' '.join((annotation.text for annotation in quality.layout.annotations))
```

### `test_edge_annotations_are_exact_registered_relations_and_quality_label_is_separate`

[定位第131行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:131>)。

Catches a quality badge mutating an edge's registered relation_type text.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
all((item.text in expected for item in arrows))
[item.text for item in quality_arrows] == list(quality_paths[0].relation_semantics)
any((item.text == '置信度路径' and (not item.showarrow) for item in quality.layout.annotations))
```

### `test_figure_rejects_non_strict_or_out_of_range_path_cap`

[定位第155行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:155>)。

Catches bool/float or an unsupported number of rendered canonical paths.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises((TypeError, ValueError))
```

### `test_figure_shows_a_true_empty_state_without_invented_nodes_or_edges`

[定位第161行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:161>)。

Catches a zero-active-path graph being drawn as a synthetic relationship.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
paths == []
figure.layout.meta == {'path_ids': [], 'node_ids': [], 'edge_ids': []}
len(figure.data) == 0
'没有活跃异常/接近阈值证据路径' in figure.layout.annotations[0].text
```

### `test_figure_revalidates_and_rejects_unavailable_or_tampered_results`

[定位第174行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:174>)。

Catches visualization trusting unavailable or forged graph payloads.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_dashboard_preset_queries_and_stale_node_ids_use_only_validated_service`

[定位第187行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:187>)。

Catches preset labels bypassing GraphQueryService or stale Plotly selections crashing.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[row['path_id'] for row in rows[0]] == [path.path_id for path in result.active_paths if path.conclusion_node_id.startswith('warning:')]
[row['node_id'] for row in rows[1]] == list(result.root_evidence[:3])
[row['path_id'] for row in rows[2]] == [path.path_id for path in result.active_paths[:3]]
[row['node_id'] for row in rows[3]] == list(result.possible_consequences)
```

### `test_dashboard_requires_canonical_explanation_before_any_graph_display`

[定位第238行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:238>)。

Catches arbitrary cached prose, titles, section order, or confidence crossing into the UI.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphError, match='解释')
```

### `test_validated_graph_view_cross_checks_problem_one_warning_state`

[定位第269行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:269>)。

Catches the graph tab caption trusting a mismatched outer AgentResult.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
service.paths_to_alert()
sections == graph.explanation_sections
confidence == graph.explanation_confidence
warning['alert_level'] == 2
```

### `test_exact_plotly_selection_round_trip_rejects_malformed_payloads`

[定位第284行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:284>)。

Catches a click selecting anything other than the rendered node-id customdata.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
_selection_node_id(payload) == node_id
_selected_node_detail(GraphQueryService(_ready_result()), _selection_node_id(payload))['node_id'] == node_id
_selection_node_id(AttributeSelection()) == node_id
_selection_node_id({'selection': {'points': [{'customdata': []}]}}) is None
```

### `test_unavailable_graph_isolated_to_its_tab_rendering`

[定位第300行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_dashboard.py:300>)。

Catches graph validation failure preventing existing Problem 1 content from rendering.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
len(app.exception) == 0
any(('问题一仍可用' in item.value for item in app.markdown))
any(('风险知识图谱暂不可用' in item.value for item in app.warning))
```

## 复习方法与实际执行状态

先说出该测试想防的错误，再改变一个输入，预测哪个断言会失败。所有当前运行记录集中在[[04-面试与验证/05-本轮验证记录]]；历史文档的751项不能替代本轮实际收集与执行数。
