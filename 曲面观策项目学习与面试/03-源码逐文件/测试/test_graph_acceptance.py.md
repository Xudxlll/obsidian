---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份测试文件防什么错误

测试正式验收、时间安全、缓存、归档与当前结果身份。

这是最大的综合防回归文件之一；大量故意破坏缓存、未来分区、输入成员、策略身份和解释内容，检查是否拒绝错误或保持历史结果不变。用合成fixture验证防未来，不等于每份真实数据的所有历史时点均重放。

源文件：[test_graph_acceptance.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py>)。

## 输入与输出

测试读取临时或明确指定的样本/结果，输出断言的通过或失败。下面列的是测试函数定义数，参数化会展开多个运行用例；不能把函数数当实际测试case数。此文件有64个test函数。

## 逐项合同索引

### `test_single_result_validator_accepts_a_canonical_ready_level_two_graph`

[定位第91行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:91>)。

Catches a validator that rejects the real Task 1-6 canonical result.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
summary == {'status': 'ready', 'product': 'ag', 'timestamp': '2025-04-07T10:15:00', 'schema_version': 'kg-schema-v1', 'rule_version': 'kg-rule-v1', 'node_count': 8, 'edge_count': 6, 'active_path_count': 2, 'alert_path_count': 1, 'quality_path_count': 0, 'missing_evidence_count': 11, 'explanation_status': 'canonical', 'explanation_confidence': 'normal', 'query_record_counts': {'root_evidence': 1, 'paths_to_alert': 1, 'possible_consequences': 1, 'quality_limitations': 0, 'inspect_node': 8, 'paths_
```

### `test_single_result_validator_accepts_level_zero_with_no_active_path`

[定位第126行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:126>)。

Catches formal acceptance inventing a path for sub-attention evidence.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
result.knowledge_graph.active_paths == ()
summary == {'status': 'ready', 'product': 'ag', 'timestamp': '2025-04-07T10:15:00', 'schema_version': 'kg-schema-v1', 'rule_version': 'kg-rule-v1', 'node_count': 5, 'edge_count': 2, 'active_path_count': 0, 'alert_path_count': 0, 'quality_path_count': 0, 'missing_evidence_count': 11, 'explanation_status': 'canonical', 'explanation_confidence': 'normal', 'query_record_counts': {'root_evidence': 0, 'paths_to_alert': 0, 'possible_consequences': 0, 'quality_limitations': 0, 'inspect_node': 5, 'paths_
```

### `test_single_result_validator_accepts_watch_held_without_current_market_path`

[定位第166行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:166>)。

Catches persistence-only level 1 being rejected for lacking a current path.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
result.knowledge_graph.active_paths == ()
'当前市场特征已回落' in result.knowledge_graph.explanation_text
summary == {'status': 'ready', 'product': 'ag', 'timestamp': '2025-04-07T10:15:00', 'schema_version': 'kg-schema-v1', 'rule_version': 'kg-rule-v1', 'node_count': 5, 'edge_count': 2, 'active_path_count': 0, 'alert_path_count': 0, 'quality_path_count': 0, 'missing_evidence_count': 11, 'explanation_status': 'canonical', 'explanation_confidence': 'normal', 'query_record_counts': {'root_evidence': 0, 'paths_to_alert': 0, 'possible_consequences': 0, 'quality_limitations': 0, 'inspect_node': 5, 'paths_
```

### `test_single_result_validator_accepts_quality_only_path_as_limited_confidence`

[定位第208行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:208>)。

Catches a quality limitation being rejected or promoted to market alert.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
all((path.conclusion_node_id.startswith('confidence:') for path in result.knowledge_graph.active_paths))
summary == {'status': 'ready', 'product': 'ag', 'timestamp': '2025-04-07T10:15:00', 'schema_version': 'kg-schema-v1', 'rule_version': 'kg-rule-v1', 'node_count': 7, 'edge_count': 5, 'active_path_count': 1, 'alert_path_count': 0, 'quality_path_count': 1, 'missing_evidence_count': 11, 'explanation_status': 'canonical', 'explanation_confidence': 'limited', 'query_record_counts': {'root_evidence': 1, 'paths_to_alert': 0, 'possible_consequences': 0, 'quality_limitations': 1, 'inspect_node': 7, 'paths
```

### `test_single_result_validator_rejects_an_unavailable_graph`

[定位第251行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:251>)。

Catches formal acceptance silently passing local graph degradation.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='unavailable')
```

### `test_single_result_validator_rejects_ready_graph_with_any_error_payload`

[定位第284行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:284>)。

Catches ready envelopes retaining latent or non-JSON error objects.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='error|错误|ready|JSON')
```

### `test_single_result_validator_rejects_non_builtin_integer_warning_level`

[定位第309行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:309>)。

Catches equality-compatible bool/float/numpy WarningState levels.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='alert_level|预警等级|Warning|整数|类型')
```

### `test_single_result_validator_rejects_non_builtin_warning_boolean`

[定位第335行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:335>)。

Catches equality-compatible integers/numpy booleans in WarningState.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='alert_emitted|通知|Warning|布尔|类型')
```

### `test_single_result_validator_rejects_non_builtin_or_nonfinite_warning_score`

[定位第374行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:374>)。

Catches malformed outer scores collapsing to a legal graph None/number.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='risk_score|风险分|Warning|有限|数值|类型')
```

### `test_single_result_validator_accepts_none_for_feature_numbers`

[定位第392行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:392>)。

Locks legal nulls for all four FeatureEvidence numeric fields.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
summary['status'] == 'ready'
summary['active_path_count'] == 0
```

### `test_single_result_validator_rejects_invalid_feature_number`

[定位第425行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:425>)。

Catches invalid optional Evidence values being collapsed to graph None.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='Evidence|证据|JSON|有限|数值|类型')
```

### `test_single_result_validator_rejects_feature_number_type_drift`

[定位第460行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:460>)。

Catches equality-compatible non-canonical FeatureEvidence scalars.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='Evidence|证据|JSON|有限|数值|类型')
```

### `test_single_result_validator_rejects_feature_string_subclass`

[定位第495行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:495>)。

Catches a validator auditing only FeatureEvidence numeric fields.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='Evidence|证据|JSON|字符串|类型')
```

### `test_single_result_validator_rejects_active_path_numeric_type_drift`

[定位第511行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:511>)。

Catches canonical float 1.0 being accepted as integer 1 in a RiskPath.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
type(paths[0].pressure_ratio) is float and paths[0].pressure_ratio == 1.0
pytest.raises(AssertionError, match='path|路径|类型|规范')
```

### `test_single_result_validator_rejects_list_for_canonical_tuple_field`

[定位第535行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:535>)。

Catches tuple(list_value) comparisons hiding public container drift.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='tuple|元组|类型|规范|路径|索引|missing')
```

### `test_single_result_validator_rejects_string_subclass_in_id_tuple`

[定位第554行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:554>)。

Catches equality-compatible non-builtin IDs in canonical tuple indexes.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
canonical_value
pytest.raises(AssertionError, match='ID|标识|字符串|类型|索引|missing')
```

### `test_single_result_validator_rejects_string_subclass_for_active_path_id`

[定位第584行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:584>)。

Catches dataclass equality hiding a non-builtin canonical path ID.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='path|路径|ID|标识|字符串|类型')
```

### `test_single_result_validator_rejects_evidence_from_after_the_selected_time`

[定位第603行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:603>)。

Catches future Evidence source time entering formal acceptance.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='Evidence|未来|时间')
```

### `test_single_result_validator_rejects_level_two_without_a_market_alert_path`

[定位第619行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:619>)。

Catches a formal level-2 warning unsupported by any current market path.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
result.knowledge_graph.active_path_count == 0
pytest.raises(AssertionError, match='市场|预警路径|alert')
```

### `test_single_result_validator_rejects_version_or_identity_drift`

[定位第690行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:690>)。

Catches stale versions or cross-envelope product/time identity drift.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match=message)
```

### `test_single_result_validator_rejects_cached_structure_count_drift`

[定位第712行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:712>)。

Catches cached node, edge, or path counts replacing recomputed truth.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='数量|count')
```

### `test_single_result_validator_rejects_noncanonical_active_path_order`

[定位第728行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:728>)。

Catches caller-controlled path ordering replacing deterministic ranking.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='路径|path')
```

### `test_single_result_validator_rejects_root_and_consequence_cache_drift`

[定位第746行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:746>)。

Catches cached root/consequence indexes diverging from canonical paths.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='根因|后果|root|consequence')
```

### `test_single_result_validator_rejects_query_index_drift_from_the_graph`

[定位第762行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:762>)。

Catches UI/query caches suppressing a real alert path.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='查询|query')
```

### `test_single_result_validator_rejects_noncanonical_explanation`

[定位第803行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:803>)。

Catches stored prose or confidence replacing a fresh canonical rendering.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='解释|explanation|confidence')
```

### `test_review_r3_accepts_exact_canonical_explanation_sections`

[定位第817行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:817>)。

Locks the exact section and nested scalar/container representation.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
type(sections) is tuple and sections
all((type(section) is ExplanationSection for section in sections))
summary['explanation_status'] == 'canonical'
type(section.section_id) is str
```

### `test_review_r3_rejects_explanation_string_subclass`

[定位第844行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:844>)。

Catches equality-compatible string subclasses in explanation fields.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='解释|explanation|section|字符串|类型|规范')
```

### `test_review_r3_rejects_explanation_path_id_string_subclass`

[定位第861行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:861>)。

Catches equality-compatible string subclasses nested in path_ids.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='解释|explanation|path_ids|路径|字符串|类型')
```

### `test_review_r3_rejects_explanation_list_for_path_ids_tuple`

[定位第885行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:885>)。

Catches a constructible list replacing the canonical path_ids tuple.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='解释|explanation|path_ids|元组|tuple|类型')
```

### `test_review_r3_rejects_explanation_section_subclass`

[定位第905行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:905>)。

Catches an ExplanationSection subclass crossing the formal boundary.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
type(sections[0]) is _ExplanationSectionSubclass
pytest.raises(AssertionError, match='解释|explanation|section|类型|规范')
```

### `test_single_result_validator_rejects_wrong_feature_rules_missing_evidence`

[定位第927行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:927>)。

Catches missing-evidence membership or FEATURE_RULES ordering drift.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
result.knowledge_graph.missing_evidence == ('atm_iv_chg_4', 'term_inversion', 'convexity_violation_ratio', 'max_local_iv_jump', 'put_call_parity_p95_error', 'calendar_variance_violation_ratio', 'gamma_hhi', 'vega_hhi', 'zero_volume_share', 'iv_floor_share', 'coverage_shortfall')
pytest.raises(AssertionError, match='缺失|missing')
```

### `test_single_result_validator_rejects_warning_cross_layer_drift`

[定位第980行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:980>)。

Catches Problem 1 Warning fields disagreeing with WarningState.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='Warning|预警|策略|迁移|risk')
```

### `test_review_r3_rejects_warning_graph_integer_for_outer_float_risk_score`

[定位第998行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:998>)。

Catches JSON integer 1 comparing equal to canonical outer float 1.0.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
type(result.risk_score) is float and result.risk_score == 1.0
type(warning['risk_score']) is float and warning['risk_score'] == 1.0
pytest.raises(AssertionError, match='Warning|risk_score|预警|类型|规范')
```

### `test_single_result_validator_rejects_evidence_cross_layer_drift`

[定位第1030行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1030>)。

Catches graph Evidence values diverging from Problem 1 evidence.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='Evidence|证据')
```

### `test_single_result_validator_rejects_fabricated_graph_evidence`

[定位第1046行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1046>)。

Catches graph Evidence being invented for a feature absent from Problem 1.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='Evidence|证据|缺失')
```

### `test_single_result_validator_rejects_snapshot_cross_layer_drift`

[定位第1066行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1066>)。

Catches RiskSnapshot provenance disagreeing with Problem 1.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='RiskSnapshot|快照|质量|价格')
```

### `test_single_result_validator_rejects_temporal_leakage_or_stale_evidence`

[定位第1124行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1124>)。

Catches future graph data and non-event-time Evidence provenance.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='时间|未来|Evidence|path')
```

### `test_single_result_validator_rejects_non_strict_json_payloads`

[定位第1169行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1169>)。

Catches NaN or default-based serialization hiding invalid graph payloads.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='JSON|序列|有限|NaN')
```

### `test_single_result_validator_rejects_a_quality_path_reaching_warning_state`

[定位第1183行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1183>)。

Catches quality limitations being forged into market-alert support.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='质量|quality|Warning')
```

### `test_single_result_validator_does_not_mutate_the_agent_result`

[定位第1210行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1210>)。

Catches validation normalizing caller-owned graph or query state in place.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
result.to_dict() == before
```

### `test_graph_deployment_sorts_two_products_and_validates_each_exact_last_once`

[定位第1432行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1432>)。

Catches unsorted, repeated, partial, or fabricated deployment validation.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
requested == before_requested
[row['product'] for row in report['products']] == ['ag', 'cu']
agent.list_products_calls == 1
agent.list_timestamp_calls == ['ag', 'cu']
```

### `test_graph_deployment_preserves_problem_one_and_continues_after_graph_failure`

[定位第1495行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1495>)。

Catches one graph failure erasing Problem 1 or stopping later products.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
[row['product'] for row in report['products']] == ['ag', 'cu', 'zn']
agent.list_timestamp_calls == ['ag', 'cu', 'zn']
agent.analyze_calls == [('ag', timestamps['ag'][-1]), ('cu', timestamps['cu'][-1]), ('zn', timestamps['zn'][-1])]
failed['analysis'] == _expected_problem_one_analysis('cu', timestamps['cu'][-1])
```

### `test_graph_deployment_reports_unknown_product_without_catalog_io`

[定位第1558行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1558>)。

Catches an unknown requested product reaching timestamp or analysis I/O.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
report['products'] == [{'product': 'xx', 'status': 'failed', 'error_type': 'AssertionError', 'error': '数据目录不存在品种：xx'}]
report['summary'] == {'status': 'failed', 'product_count': 1, 'passed_products': 0, 'failed_products': 1}
agent.list_timestamp_calls == []
agent.analyze_calls == []
```

### `test_graph_deployment_rejects_an_empty_catalog_without_fabricating_rows`

[定位第1591行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1591>)。

Catches an empty data source being reported as a successful acceptance.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
report['products'] == []
report['summary'] == {'status': 'failed', 'product_count': 0, 'passed_products': 0, 'failed_products': 0}
agent.list_products_calls == 1
agent.list_timestamp_calls == []
```

### `test_review_r3_graph_deployment_fails_without_exact_mandatory_global_checks`

[定位第1656行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1656>)。

Catches nonempty partial/unknown global checks authorizing deployment.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
report['products'][0]['status'] == 'passed'
report['global_checks'] == checks
report['summary'] == {'status': 'failed', 'product_count': 1, 'passed_products': 1, 'failed_products': 0}
```

### `test_review_r3_graph_deployment_accepts_exact_three_passing_global_checks`

[定位第1685行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1685>)。

Keeps the exact mandatory three-check success contract green.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
report['global_checks'] == checks
report['summary'] == {'status': 'passed', 'product_count': 1, 'passed_products': 1, 'failed_products': 0}
```

### `test_graph_deployment_summary_fails_when_any_executed_global_check_fails`

[定位第1712行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1712>)。

Catches all-pass product rows masking a failed executed global check.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
report['products'][0]['status'] == 'passed'
report['global_checks'] == checks
report['summary'] == {'status': 'failed', 'product_count': 1, 'passed_products': 1, 'failed_products': 0}
```

### `test_graph_deployment_executes_all_mandatory_content_safety_phrases`

[定位第1756行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1756>)。

Catches the global check sampling only one unsafe and one safe phrase.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
actual_fixture_outcomes == expected_fixture_outcomes
report['global_checks']['content_safety'] == {'passed': True, 'checked_count': 10, 'scope': '成功图谱1/1；逐个验证生成解释的语言安全，并执行7个不安全与2个安全限制措辞fixture'}
```

### `test_graph_deployment_contains_mapping_runtime_error_at_graph_stage_only`

[定位第1816行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1816>)。

Catches graph Mapping runtime errors aborting later catalog products.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
agent.analyze_calls == [('ag', timestamps['ag'][-1]), ('cu', timestamps['cu'][-1])]
report['products'][0] == {'product': 'ag', 'status': 'failed', 'timestamp_count': 1, 'first_timestamp': '2025-04-07T10:15:00', 'last_timestamp': '2025-04-07T10:15:00', 'analysis': _expected_problem_one_analysis('ag', timestamps['ag'][-1]), 'knowledge_graph': {'status': 'failed', 'error_type': 'RuntimeError', 'error': 'synthetic graph mapping failure'}, 'error_type': 'RuntimeError', 'error': 'synthetic graph mapping failure'}
report['products'][1]['status'] == 'passed'
progress == ['[1/2] ag: failed - synthetic graph mapping failure', '[2/2] cu: passed']
```

### `test_graph_deployment_does_not_swallow_runtime_error_before_graph_stage`

[定位第1874行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:1874>)。

Guards against broadening RuntimeError handling around the whole loop.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(RuntimeError, match='pre-graph analysis bug')
```

### `test_no_future_global_check_replays_real_agent_after_physical_future_append`

[定位第2000行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2000>)。

Catches a graph-tamper fixture that never re-runs the real data pipeline.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
replay_pairs
isinstance(before_state, dict) and isinstance(after_state, dict)
before_state['max_raw_timestamp'] == selected_raw
after_state['max_raw_timestamp'] > selected_raw
```

### `test_query_cli_maps_each_fixed_query_to_exact_real_records`

[定位第2254行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2254>)。

Catches a CLI query name forwarding to the wrong public graph method.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
completed.returncode == 0
payload == {'product': 'ag', 'timestamp': real_query_cli_case['timestamp'].isoformat(), 'schema_version': 'kg-schema-v1', 'rule_version': 'kg-rule-v1', 'query': query, 'record_count': len(records), 'records': records}
'generated_at' not in payload
```

### `test_query_cli_stdout_is_utf8_json_only_and_byte_deterministic`

[定位第2282行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2282>)。

Catches timestamps, progress, or escaping making identical queries unstable.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
first.returncode == second.returncode == 0
first.stdout == second.stdout
b'\r\n' not in first.stdout
json.loads(decoded)['query'] == 'node-detail'
```

### `test_query_cli_usage_errors_exit_two_without_stdout`

[定位第2315行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2315>)。

Catches query/source grammar errors leaking into domain exit code 1.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
completed.returncode == 2
completed.stdout == b''
"can't open file" not in stderr
expected_stderr.lower() in stderr
```

### `test_query_cli_real_domain_errors_exit_one_without_stdout`

[定位第2364行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2364>)。

Catches real catalog/query domain failures becoming usage errors or JSON.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
completed.returncode == 1
completed.stdout == b''
expected_stderr in stderr
```

### `test_query_cli_injected_runtime_failures_exit_one_without_partial_json`

[定位第2409行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2409>)。

Catches graph/serialization failures printing partial stdout or traceback exit.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
exit_code == 1
captured.out == ''
expected_stderr.lower() in captured.err.lower()
```

### `test_validation_cli_writes_the_same_strict_json_it_prints_and_routes_progress`

[定位第2476行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2476>)。

Catches report/stdout drift, wrong status exit, or progress on stdout.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
exit_code == (0 if status == 'passed' else 1)
json.loads(captured.out) == payload
json.loads(report_path.read_text(encoding='utf-8')) == payload
captured.out.rstrip('\r\n').encode('utf-8') == report_path.read_bytes()
```

### `test_validation_cli_exits_one_when_global_check_fails_despite_passed_summary`

[定位第2536行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2536>)。

Catches a crafted passed summary overriding a failed executed check.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
exit_code == 1
json.loads(captured.out) == payload
json.loads(report_path.read_text(encoding='utf-8')) == payload
```

### `test_review_r3_validation_cli_rejects_nonempty_incomplete_global_checks`

[定位第2623行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2623>)。

Catches a passed summary bypassing the exact mandatory check set.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
(helper_allowed, exit_code) == (False, 1)
json.loads(captured.out) == payload
json.loads(report_path.read_text(encoding='utf-8')) == payload
```

### `test_review_r3_validation_cli_preserves_approved_global_check_controls`

[定位第2674行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2674>)。

Locks None/empty compatibility and exact-three-check success.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
(helper_allowed, exit_code) == (True, 0)
json.loads(captured.out) == payload
json.loads(report_path.read_text(encoding='utf-8')) == payload
```

### `test_validation_cli_real_subprocess_keeps_report_and_stdout_bytes_platform_stable`

[定位第2716行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2716>)。

Catches Windows text translation making report/stdout JSON bytes drift.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
completed.returncode == 0
payload['summary'] == {'status': 'passed', 'product_count': 1, 'passed_products': 1, 'failed_products': 0}
b'\r\n' not in completed.stdout
completed.stdout.rstrip(b'\r\n') == report_path.read_bytes()
```

### `test_validation_cli_source_usage_errors_exit_two_without_stdout`

[定位第2765行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2765>)。

Catches missing/ambiguous deployment sources reaching runtime validation.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
completed.returncode == 2
completed.stdout == b''
"can't open file" not in stderr
expected_stderr.lower() in stderr
```

### `test_validation_cli_optional_report_uses_output_default_with_archive_source`

[定位第2779行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2779>)。

Catches optional report or archive configuration ignoring registered defaults.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
exit_code == 0
json.loads(captured.out) == payload
json.loads(default_report.read_text(encoding='utf-8')) == payload
FakeAgent.last_config.archive_path == archive_path.resolve()
```

### `test_validation_cli_rejects_non_strict_json_before_stdout_or_report`

[定位第2832行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_acceptance.py:2832>)。

Catches allow_nan/default serialization emitting an invalid formal artifact.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
exit_code == 1
captured.out == ''
not report_path.exists()
any((word in captured.err.lower() for word in ('json', 'nan', 'finite')))
```

## 复习方法与实际执行状态

先说出该测试想防的错误，再改变一个输入，预测哪个断言会失败。所有当前运行记录集中在[[曲面观策项目学习与面试/04-面试与验证/05-本轮验证记录.md|05-本轮验证记录]]；历史文档的751项不能替代本轮实际收集与执行数。
