---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份测试文件防什么错误

检验图构建、节点边Schema、数值与时间一致性。

控制阈值附近、越界、缺失、未知特征、质量压力和序列化输入，确认市场预警与置信度路径不串线。一个事件图的ID规则不等于已实现跨事件图数据库。

源文件：[test_knowledge_graph.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py>)。

## 输入与输出

测试读取临时或明确指定的样本/结果，输出断言的通过或失败。下面列的是测试函数定义数，参数化会展开多个运行用例；不能把函数数当实际测试case数。此文件有53个test函数。

## 逐项合同索引

### `test_builder_uses_deterministic_event_ids_and_graph_metadata`

[定位第109行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:109>)。

Catches random IDs, unsanitized product codes, or a non-event timestamp.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
graph.graph == {'schema_version': KG_SCHEMA_VERSION, 'rule_version': KG_RULE_VERSION, 'product': 'ag', 'timestamp': SNAPSHOT, 'attention_pressure': 0.9, 'policy_parameters': asdict(DecisionPolicy()), 'policy_parameter_hash': DecisionPolicy().parameter_hash}
set(graph.nodes) == {'product:ag', f'snapshot:ag:{STAMP}', f'evidence:ag:{STAMP}:atm_iv', 'anomaly:anomaly_atm_iv', 'mechanism:mechanism_atm_iv', 'consequence:risk_consequence_atm_iv', f'warning:ag:{STAMP}:1', f'confidence:ag:{STAMP}:normal'}
all((node_id == data['node_id'] for node_id, data in graph.nodes(data=True)))
```

### `test_builder_keeps_all_finite_evidence_but_only_activates_attention_pressure`

[定位第140行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:140>)。

Catches normal evidence being dropped or a below-attention path being fabricated.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
{data['feature_name'] for data in evidence_nodes.values()} == {'atm_iv', 'gamma_hhi'}
attached == set(evidence_nodes)
list(graph.out_edges(atm_id, keys=True, data=True)) == []
{data['relation_type'] for _, _, _, data in graph.out_edges(gamma_id, keys=True, data=True)} == {'NEAR_THRESHOLD'}
```

### `test_builder_selects_the_registered_dynamic_evidence_relation`

[定位第194行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:194>)。

Catches wrong 0.90/1.00 boundaries or false constraint violations.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[data['relation_type'] for _, _, data in graph.out_edges(evidence_id, data=True)] == [expected_relation]
```

### `test_nonfinite_pressure_is_retained_as_null_but_never_activates_a_path`

[定位第213行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:213>)。

Catches NaN/inf leaking into JSON or activating an explanatory branch.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
node['reference_value'] is None
node['pressure_ratio'] is None
node['change_rate'] is None
node['direction'] == '不可用'
```

### `test_evidence_direction_comes_only_from_change_rate`

[定位第235行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:235>)。

Catches direction inferred from a fabricated previous raw value.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
evidence_node['direction'] == expected
```

### `test_market_path_has_exact_layers_and_only_supports_a_positive_warning`

[定位第246行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:246>)。

Catches a missing propagation layer or support for a formal level zero.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
node_types.count('Evidence') == 1
node_types.count('Anomaly') == 1
node_types.count('Mechanism') == 1
node_types.count('RiskConsequence') == 1
```

### `test_quality_paths_end_only_at_one_limited_confidence_state`

[定位第268行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:268>)。

Catches quality evidence being used to justify a market warning.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
confidence_id == f'confidence:ag:{STAMP}:limited'
confidence['level'] == 'limited'
confidence['quality_reasons'] == ['zero_volume_share', 'coverage_shortfall']
confidence_id in descendants
```

### `test_builder_rejects_unknown_duplicate_features_and_empty_safe_product`

[定位第297行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:297>)。

Catches ambiguous evidence identity and unsafe product IDs.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_every_node_and_edge_carries_the_required_audit_contract`

[定位第311行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:311>)。

Catches a graph that cannot be inspected without consulting runtime state.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
common_node_fields | type_fields[data['node_type']] <= set(data)
data['product'] == 'ag'
data['source_timestamp'] == SNAPSHOT
required_edge_fields <= set(data)
```

### `test_validator_rejects_a_missing_type_specific_node_attribute`

[定位第387行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:387>)。

Catches validation that checks node type names but not their payloads.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_unknown_node_and_relation_types`

[定位第399行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:399>)。

Catches permissive schema drift in graph records.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_a_missing_edge_audit_attribute`

[定位第425行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:425>)。

Catches partially sourced edges crossing the public audit boundary.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_bad_edge_identity_semantics_and_rule_version`

[定位第435行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:435>)。

Catches edge-key drift, invented semantic classes, and mixed rule registries.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_future_node_and_edge_timestamps`

[定位第456行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:456>)。

Catches future information being attached to the selected event snapshot.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_graph_product_and_timestamp_mismatches`

[定位第472行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:472>)。

Catches a graph envelope describing a different product or event.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_evidence_to_conclusion_shortcuts`

[定位第485行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:485>)。

Catches an explanation that skips the anomaly and mechanism layers.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
template_key == template['edge_id']
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_any_quality_route_to_warning_state`

[定位第507行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:507>)。

Catches a structurally valid SUPPORTS edge laundering quality into risk.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_non_multidigraph_and_non_multigraph_payload`

[定位第530行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:530>)。

Catches loss of parallel-edge keys at validation or deserialization.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_serialization_is_json_safe_sorted_and_deterministic`

[定位第541行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:541>)。

Catches insertion-order output, Timestamp leakage, and unstable multiedges.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
encoded_first == encoded_second
[row['id'] for row in first_payload['nodes']] == sorted(first.nodes)
[(row['source'], row['target'], row['relation_type'], row['edge_id']) for row in first_payload['edges']] == sorted(((row['source'], row['target'], row['relation_type'], row['edge_id']) for row in first_payload['edges']))
first_payload['graph']['timestamp'] == '2025-04-07T10:15:00'
```

### `test_node_link_round_trip_restores_timestamps_keys_and_exact_payload`

[定位第581行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:581>)。

Catches audit payloads that deserialize without their temporal or edge identity.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
isinstance(restored, nx.MultiDiGraph)
restored.graph['timestamp'] == SNAPSHOT
all((isinstance(data['source_timestamp'], pd.Timestamp) for _, data in restored.nodes(data=True)))
all((isinstance(data['source_timestamp'], pd.Timestamp) for _, _, data in restored.edges(data=True)))
```

### `test_validator_rejects_market_mechanism_rewired_to_confidence`

[定位第608行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:608>)。

Catches a market FeatureRule being allowed to terminate as data quality.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_quality_mechanism_rewired_to_risk_consequence`

[定位第629行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:629>)。

Catches a quality FeatureRule being promoted to a market consequence.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_cross_feature_layer_mixing`

[定位第654行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:654>)。

Catches Evidence from one rule feeding another rule's Anomaly.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_warning_support_when_formal_level_is_zero`

[定位第679行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:679>)。

Catches a fabricated alert-support path for an authoritative level zero.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_recomputes_activation_and_first_relation`

[定位第705行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:705>)。

Catches 0.89+NEAR, 0.95+EXCEEDS, and ordinary-feature VIOLATES.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
source == evidence_id
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_noncanonical_node_and_edge_ids`

[定位第726行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:726>)。

Catches IDs that are internally equal but not deterministically derived.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_noncanonical_wording_template`

[定位第744行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:744>)。

Catches a nonempty but unregistered explanatory wording template.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_evidence_field_drift`

[定位第766行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:766>)。

Catches canonical Evidence identity or derived state being overwritten.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_registered_semantic_node_drift`

[定位第793行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:793>)。

Catches semantic nodes that no longer match their FeatureRule.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_builder_rejects_invalid_formal_alert_level`

[定位第806行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:806>)。

Catches out-of-range or bool values masquerading as a formal level.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_builder_rejects_invalid_warning_scalar_types`

[定位第813行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:813>)。

Catches bool/nonfinite risk scores and non-bool emission flags.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_warning_and_confidence_state_drift`

[定位第823行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:823>)。

Catches formal alert names and recomputed quality state being overwritten.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_preflight_rejects_pressure_tamper_with_active_edge`

[定位第839行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:839>)。

Catches raw payload activation drift before returning a graph.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_preflight_rejects_nonfinite_numbers`

[定位第851行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:851>)。

Catches raw NaN being silently converted or accepted as a missing value.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_preflight_rejects_duplicate_edge_records`

[定位第863行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:863>)。

Catches NetworkX overwriting a duplicate multiedge before validation.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_preflight_rejects_duplicate_node_records`

[定位第872行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:872>)。

Catches NetworkX overwriting a duplicate node before validation.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_custom_policy_drives_severity_activation_and_round_trip`

[定位第895行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:895>)。

Catches validation or severity silently falling back to a default policy.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
graph.graph['attention_pressure'] == 0.8
graph.graph['policy_parameters'] == asdict(policy)
graph.graph['policy_parameter_hash'] == policy.parameter_hash
evidence['severity'] == 2
```

### `test_validator_rejects_coordinated_state_tamper_that_ignores_full_policy`

[定位第922行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:922>)。

Catches attention/pressure/status/path edits not bound to policy parameters.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_policy_parameter_or_hash_drift`

[定位第948行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:948>)。

Catches policy metadata that cannot reconstruct the hashed policy.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_binds_optional_snapshot_and_warning_policy_identity`

[定位第971行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:971>)。

Catches optional policy mirrors disagreeing with the reconstructed policy.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_invalid_public_field_types`

[定位第995行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:995>)。

Catches present-but-wrongly-typed public node fields.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_forbidden_causal_or_confidence_weights`

[定位第1021行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1021>)。

Catches prohibited numeric confidence semantics hidden as extra attributes.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_requires_in_memory_contract_times_to_be_timestamps`

[定位第1043行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1043>)。

Catches parseable strings being accepted inside an in-memory graph.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_preflight_rejects_non_string_timestamps`

[定位第1068行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1068>)。

Catches integer nanoseconds and collection values at the ISO boundary.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_preflight_rejects_noncanonical_iso_timestamp`

[定位第1085行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1085>)。

Catches a parseable timestamp string that does not losslessly round-trip.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_preflight_rejects_cyclic_payloads`

[定位第1095行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1095>)。

Catches raw self-references escaping as RecursionError or hanging validation.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_rejects_coordinated_formal_policy_version_tamper`

[定位第1113行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1113>)。

Catches an internally coordinated policy version outside the formal contract.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_builder_rejects_non_authoritative_policy_version`

[定位第1124行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1124>)。

Catches custom thresholds smuggling a non-formal policy version.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_graph_to_node_link_rejects_non_string_mapping_keys`

[定位第1144行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1144>)。

Catches JSON conversion overwriting or renaming Mapping keys.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_preflight_rejects_extra_top_level_keys`

[定位第1155行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1155>)。

Catches top-level data that NetworkX would silently discard.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_node_link_preflight_rejects_missing_top_level_keys`

[定位第1167行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1167>)。

Catches an incomplete node-link envelope before NetworkX defaults fields.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_validator_normalizes_forbidden_weight_key_spellings`

[定位第1191行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1191>)。

Catches camelCase and hyphenated aliases of forbidden numeric weights.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_builder_normalizes_numpy_policy_scalar_errors`

[定位第1216行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_knowledge_graph.py:1216>)。

Catches raw json.dumps TypeError escaping the graph error boundary.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
policy.policy_version == DECISION_POLICY_VERSION
pytest.raises(KnowledgeGraphValidationError)
```

## 复习方法与实际执行状态

先说出该测试想防的错误，再改变一个输入，预测哪个断言会失败。所有当前运行记录集中在[[曲面观策项目学习与面试/04-面试与验证/05-本轮验证记录.md|05-本轮验证记录]]；历史文档的751项不能替代本轮实际收集与执行数。
