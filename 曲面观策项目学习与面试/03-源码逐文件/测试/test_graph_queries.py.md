---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份测试文件防什么错误

验证根证据、到预警路径、后果、质量与节点等固定查询。

对序列化图重建查询服务，并测试篡改、非法节点与结果漂移。只读查询从当前图重新计算，不相信缓存中的伪答案。

源文件：[test_graph_queries.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py>)。

## 输入与输出

测试读取临时或明确指定的样本/结果，输出断言的通过或失败。下面列的是测试函数定义数，参数化会展开多个运行用例；不能把函数数当实际测试case数。此文件有12个test函数。

## 逐项合同索引

### `test_quality_paths_never_appear_as_alert_support`

[定位第32行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:32>)。

Catches a quality-confidence limitation being promoted to alert support.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
service.paths_to_alert() == []
len(limitations) == 1
limitations[0]['relation_semantics'][-1] == 'REDUCES_CONFIDENCE'
```

### `test_preset_queries_return_ranked_flat_json_safe_records`

[定位第47行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:47>)。

Catches nested node wrappers, non-JSON timestamps, or query ordering drift.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[row['feature_name'] for row in roots] == ['term_inversion', 'atm_iv']
all((row['node_type'] == 'Evidence' and 'properties' not in row for row in roots))
all((isinstance(row['source_timestamp'], str) for row in roots))
all((path['conclusion_node_id'].startswith('warning:') for path in alerts))
```

### `test_root_evidence_requires_a_strict_non_negative_integer`

[定位第76行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:76>)。

Catches coercion of booleans, floats, strings, nulls, or negative limits.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises((TypeError, ValueError))
```

### `test_exact_node_and_anomaly_queries_reject_unknown_or_wrong_types`

[定位第84行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:84>)。

Catches fuzzy matching, silent fallback, or non-Anomaly path lookup.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
service.inspect_node(anomaly_id)['node_id'] == anomaly_id
all((row['anomaly_node_id'] == anomaly_id for row in service.paths_from_anomaly(anomaly_id)))
pytest.raises(UnknownGraphNodeError)
pytest.raises(UnknownGraphNodeError)
```

### `test_query_results_are_deep_copies_isolated_from_service_and_result`

[定位第103行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:103>)。

Catches callers mutating cached node/path data through query return values.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
service.inspect_node(snapshot_id)['data_quality']['clean_rate'] == 1.0
service.paths_to_alert()[0]['relation_semantics'][0] in {'NEAR_THRESHOLD', 'EXCEEDS', 'VIOLATES'}
result.graph_json == original_graph_json
```

### `test_service_requires_a_ready_result_and_restores_only_valid_node_link_data`

[定位第128行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:128>)。

Catches unavailable results or serialized graph tampering crossing the boundary.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphError, match='ready')
pytest.raises(KnowledgeGraphError, match='rule version')
```

### `test_service_rejects_tampered_result_contract`

[定位第200行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:200>)。

Catches trust in cached result metadata, indexes, or noncanonical paths.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphError)
```

### `test_result_and_service_require_the_exact_canonical_five_key_query_index`

[定位第242行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:242>)。

Catches query-index fields, IDs, or ranked ordering drifting from the graph.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
result.query_index == _canonical_query_index()
[row['node_id'] for row in service.root_evidence()] == result.query_index['root_evidence']
```

### `test_service_rejects_any_noncanonical_cached_query_index`

[定位第294行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:294>)。

Catches trust-boundary acceptance of malformed or forged cached indexes.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphError)
```

### `test_service_does_not_consume_query_index_after_validation`

[定位第300行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:300>)。

Catches query methods retaining the caller-owned query-index cache as truth.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
service.root_evidence()[0]['node_id'] == result.root_evidence[0]
[path['path_id'] for path in service.paths_to_alert()] == ['path:ag:20250407T101500:term_inversion:warningstate:warning_2', 'path:ag:20250407T101500:atm_iv:warningstate:warning_2']
```

### `test_service_rejects_malformed_cached_records_with_a_graph_domain_error`

[定位第322行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:322>)。

Catches malformed cached records leaking AttributeError past the trust boundary.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphError)
```

### `test_public_query_api_has_only_the_six_preset_methods_and_no_question_input`

[定位第330行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_queries.py:330>)。

Catches accidental exposure of a free-form natural-language query surface.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
set(public) == {'inspect_node', 'paths_from_anomaly', 'paths_to_alert', 'possible_consequences', 'quality_limitations', 'root_evidence'}
str(inspect.signature(public['root_evidence'])) == '(self, limit=3)'
str(inspect.signature(public['inspect_node'])) == '(self, node_id)'
str(inspect.signature(public['paths_from_anomaly'])) == '(self, anomaly_id)'
```

## 复习方法与实际执行状态

先说出该测试想防的错误，再改变一个输入，预测哪个断言会失败。所有当前运行记录集中在[[04-面试与验证/05-本轮验证记录]]；历史文档的751项不能替代本轮实际收集与执行数。
