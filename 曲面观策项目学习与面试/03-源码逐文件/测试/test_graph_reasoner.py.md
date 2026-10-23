---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份测试文件防什么错误

检查四层合法路径、确定性排序与索引。

节点、边与关系要形成注册的有效链才成为活动路径。路径排序不能称为概率推断，也不估计因果强度。

源文件：[test_graph_reasoner.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py>)。

## 输入与输出

测试读取临时或明确指定的样本/结果，输出断言的通过或失败。下面列的是测试函数定义数，参数化会展开多个运行用例；不能把函数数当实际测试case数。此文件有12个test函数。

## 逐项合同索引

### `test_reasoner_returns_every_legal_four_layer_path`

[定位第31行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:31>)。

Catches omitted legal terminals or traversal outside the approved four layers.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
len(paths) == 3
[graph.nodes[path.conclusion_node_id]['node_type'] for path in paths] == ['RiskConsequence', 'WarningState', 'ConfidenceState']
tuple((graph.nodes[node_id]['node_type'] for node_id in node_ids[:3])) == ('Evidence', 'Anomaly', 'Mechanism')
len(path.edge_ids) == 3
```

### `test_reasoner_carries_registered_identity_and_event_metadata`

[定位第65行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:65>)。

Catches paths losing ordered relations, versioned rule identity, or event data.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[path.relation_semantics for path in paths] == [('EXCEEDS', 'SUPPORTS', 'MAY_AMPLIFY'), ('EXCEEDS', 'SUPPORTS', 'SUPPORTS')]
all((path.rule_ids == (f'{KG_RULE_VERSION}:gamma_hhi',) for path in paths))
all((path.timestamp == pd.Timestamp('2025-04-07 10:15') for path in paths))
all((path.pressure_ratio == 1.6 for path in paths))
```

### `test_reasoner_uses_dynamic_first_relation_and_excludes_inactive_evidence`

[定位第82行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:82>)。

Catches hard-coded threshold semantics or inactive evidence entering paths.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[(_feature_for_path(path), path.relation_semantics[0]) for path in paths] == [('convexity_violation_ratio', 'VIOLATES'), ('atm_iv', 'NEAR_THRESHOLD')]
```

### `test_reasoner_calls_task2_full_validator_before_traversal`

[定位第102行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:102>)。

Catches reasoning over a graph whose registered edge provenance was tampered.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphError, match='rule version')
```

### `test_rank_risk_paths_uses_the_complete_deterministic_total_order`

[定位第112行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:112>)。

Catches quality-first, low-severity-first, registry drift, or terminal drift.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[(_feature_for_path(path), graph.nodes[path.conclusion_node_id]['node_type']) for path in ranked] == [('atm_iv_chg_4', 'RiskConsequence'), ('atm_iv_chg_4', 'WarningState'), ('term_inversion', 'RiskConsequence'), ('term_inversion', 'WarningState'), ('atm_iv', 'RiskConsequence'), ('atm_iv', 'WarningState'), ('coverage_shortfall', 'ConfidenceState')]
[path.path_id for path in ranked] == [path.path_id for path in rank_risk_paths(paths)]
```

### `test_rank_risk_paths_puts_nonfinite_and_missing_pressure_last`

[定位第142行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:142>)。

Catches NaN/None pressure producing an unstable numeric sort order.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[path.path_id for path in rank_risk_paths([not_a_number, missing, finite])] == ['path-z', 'path-a', 'path-b']
```

### `test_build_graph_result_keeps_all_paths_and_builds_ranked_unique_indexes`

[定位第157行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:157>)。

Catches top-three truncation, duplicate roots, or count/index drift.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
result.status == 'ready'
result.node_count == graph.number_of_nodes()
result.edge_count == graph.number_of_edges()
result.active_path_count == 5
```

### `test_build_graph_result_copies_explanations_and_rejects_unknown_path_references`

[定位第193行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:193>)。

Catches mutable explanation input or untraceable explanation path IDs.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
result.explanation_sections == (section,)
result.explanation_text == '说明'
result.explanation_confidence == 'normal'
pytest.raises(KnowledgeGraphError, match='path')
```

### `test_build_graph_result_rejects_non_iterable_or_scalar_missing_evidence`

[定位第221行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:221>)。

Catches scalar missing-evidence input being split or leaking a native TypeError.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphError, match='missing_evidence')
```

### `test_build_graph_result_accepts_any_iterable_of_strings_and_deduplicates_it`

[定位第231行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:231>)。

Catches valid one-shot iterables being rejected or deduplicated unstably.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
result.missing_evidence == ('atm_iv_chg_4', 'vega_hhi')
```

### `test_discovery_is_independent_of_evidence_input_order`

[定位第241行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:241>)。

Catches graph insertion order leaking into path identity or ranking.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[path.to_dict() for path in first_paths] == [path.to_dict() for path in second_paths]
first.graph == second.graph
[rule.order for rule in FEATURE_RULES] == list(range(1, 13))
```

### `test_reasoner_restores_serialized_input_only_through_the_validated_boundary`

[定位第258行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_reasoner.py:258>)。

Catches serialized graph input being rejected or traversed without restoration.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[path.to_dict() for path in actual] == [path.to_dict() for path in expected]
```

## 复习方法与实际执行状态

先说出该测试想防的错误，再改变一个输入，预测哪个断言会失败。所有当前运行记录集中在[[04-面试与验证/05-本轮验证记录]]；历史文档的751项不能替代本轮实际收集与执行数。
