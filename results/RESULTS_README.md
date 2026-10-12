# Results index

`v2_final_test_results.json` keeps all original exact metrics, per-class/per-province numerical values and original rounded-reference generalization gaps. Only descriptive labels and evidence metadata have changed; the original JSON is under `history/rc1/results/`.

`confusion_matrix_raw.csv`, `confusion_matrix_normalized.csv` and `province_metrics_test.csv` are unchanged from RC1. `per_class_metrics.csv` is the earlier independent audit output. `audit_comparable_dev_to_test_gaps` in the JSON gives precise like-for-like gaps; do not mix it with the rounded historical reference field.

The earlier full independent calculation is under `evidence/independent_audit/`. New model execution and recalibration are not part of this release. The saved-prediction consistency verifier is `tools/verify_release.py`.
