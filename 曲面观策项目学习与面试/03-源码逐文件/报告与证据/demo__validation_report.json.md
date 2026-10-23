---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 文件作用

第一问完整产物曾通过验证的历史记录。

有all_boolean_checks_pass=true和多项身份/指标/报告/Notebook检查。当前demo只留3个JSON，已不含原先被验证的全部文件；这些true是历史记录，不能宣称在当前目录重新执行仍全绿。

源文件：[validation_report.json](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/outputs/demo/validation_report.json>)。

## 顶层结构

`all_required_outputs_exist`, `validator_pipeline_config_valid`, `validator_primary_policy_identity_valid`, `decision_source_matches_current_policy_version`, `decision_source_matches_warning_policy_version`, `identity_present`, `identity_version_matches`, `identity_generated_at_is_utc`, `identity_package_version_matches`, `identity_feature_schema_version_matches`, `identity_ordered_feature_columns_match`, `identity_pressure_column_contract_matches`, `identity_history_column_contract_matches`, `identity_26_column_exclusion_contract_matches`, `identity_decision_policy_version_matches`, `identity_decision_policy_is_pre_registered_fixed`, `identity_decision_policy_parameters_match`, `identity_pipeline_config_matches`, `identity_forward_label_boundary_purge_matches_config`, `identity_input_files_match`, `identity_source_tree_matches`, `decision_policy_replay_index_matches`, `decision_policy_alert_levels_replay_exactly`, `decision_policy_alert_emissions_replay_exactly`, `decision_policy_version_matches_exactly`, `decision_policy_parameter_hash_matches_exactly`, `fixed_holdout_protocol_identity_matches_model_bundle`, `fixed_holdout_primary_policy_is_pre_registered_fixed`, `fixed_holdout_primary_policy_identity_is_current`, `fixed_holdout_model_has_no_test_label_reuse`, `fixed_holdout_ablation_model_has_no_test_label_reuse`, `fixed_holdout_split_boundary_labels_are_purged`, `fixed_holdout_alert_policies_have_no_test_label_reuse`, `fixed_holdout_all_calibration_precedes_test_start`, `fixed_holdout_no_test_label_reuse`, `feature_index_unique`, `feature_index_sorted`, `warning_index_matches_features`, `alert_levels_valid`, `warning_explanations_complete`, `no_trading_instruction_in_explanations`, `test_months`, `test_has_three_consecutive_months`, `surface_grids_have_finite_values`, `summary_test_rows_match`, `primary_model_excludes_label_derived_features`, `threshold_feasibility_is_explicit`, `cvar_has_random_baseline`, `official_event_file_was_evaluated`, `primary_policy_is_pre_registered_fixed`, `primary_predictions_identify_decision_source`, `recomputed_test_metrics_match_summary`, `quality_clean_rate_reconciles`, `no_duplicate_primary_key_rows`, `surface_snapshot_count_matches_features`, `test_range_is_three_consecutive_months`, `recomputed_long_short_cvar_matches_summary`, `delivery_artifacts_exist`, `all_35_products_pass_full_agent_query`, `all_products_have_complete_problem_one_payload`, `report_metrics_match_run_summary`, `report_product_coverage_matches_acceptance`, `html_report_exists`, `html_report_exactly_matches_current_artifact`, `html_report_is_self_contained`, `notebook_exists`, `notebook_is_parseable`, `notebook_all_code_cells_executed`, `notebook_has_no_error_outputs`, `notebook_contains_current_policy_identity`, `notebook_contains_current_test_metrics`, `all_boolean_checks_pass`。

## 上下游

由Agent验收、离线pipeline或快照脚本生成，报告脚本读取；正式在线决策不从报告反向学习参数。身份、时间、来源和统计分母必须一起核对。

## 面试自测

为什么不能只截一张“passed”的图作为泛化能力证明？

> [!success]- 答案
> passed取决于具体检查合同、品种、时点、数据和代码版本。功能可用性、数值一致性、预测效果、因果解释和实际经济收益是不同主张。
