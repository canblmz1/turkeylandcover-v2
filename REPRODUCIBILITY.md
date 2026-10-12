# TurkeyLandCover V2 — reproducibility and evidence scope

**Revision:** `v2.0-rc2-docfix`, 12 October 2026.

## 1. Verified, reported and unresolved information

| Evidence level | What is supported | What is not implied |
|---|---|---|
| Numerically checked | 68,558 unique saved test rows; frozen shift yields stored predictions; confusion matrix and metrics match; file hashes match | No new image-to-checkpoint-to-logit reproduction |
| Checkpoint record | `pretrained=true`, model path, class names, 10 epochs, recorded optimizer/batch/version metadata | No proof of original upstream weight identity or fresh server state |
| Project-reported | EVREN/Slurm IDs; single-GPU execution; 50,000-item pool and 40,253 internal training examples; historical one-time test claim | Not independently authenticated by live API or raw retained cluster logs |
| Unresolved | Original training item lists, source label semantics, source imagery lineage, initial weight hash, complete runtime lock, checkpoint rights | Not silently filled from general knowledge |

The complete earlier independent audit is under `evidence/independent_audit/`. Its scope is saved-logit → correction → prediction → metric. The original scripts in `history/` and the earlier audit scripts are evidence, not instructions to rerun the consumed test.

## 2. Verify this release without a model run

From the extracted release root:

```bash
python tools/verify_release.py --hashes-only
python tools/verify_release.py
```

Hash-only mode uses the standard library. Full numerical mode requires NumPy. The script uses `numpy.load(..., allow_pickle=False)` and never imports PyTorch or Ultralytics, calls a network service, changes files, or computes a new model output.

It checks every entry of `SHA256SUMS.txt`, the saved NPZ schema, finite logits, unique IDs, the exact frozen shift vector, class order, stored argmax agreement, global and provincial metrics, and manifest associations. It does not reselect tau or generate a new confidence interval.

Included evidence:
- `predictions/test_predictions.npz` — unchanged from the earlier evidence package, SHA-256 `d5b63a61813f8ec9ea2d417e3c08ff4b90cf0973efd53b1503351520c9254c64`.
- `model/best.pt` — unchanged, SHA-256 `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`.
- `history/evaluation_source/evaluate_v2_final_test.py` — original source, SHA-256 `982ac6081240089661666c385df35c3625a907096c42e3be3827d9d77c9522d5`; **inspect only, do not rerun the final test**.
- `evidence/independent_audit/independent_audit_results.json` — exact prior audit output, including development comparison and original bootstrap replication.

## 3. Numerical conventions

Global Macro-F1 averages all eight classes. Province tables display both all-eight and locally present-class means with support definitions. Zero denominators use zero for those class metrics. Top-1 is 59,076 / 68,558; Top-5 is 68,548 / 68,558.

Current JSON retains original exact numerical metric fields. Its historical `generalization_gap` used rounded development values; `audit_comparable_dev_to_test_gaps` separately carries the precise prior audit comparisons. Neither is used to retune or classify new models.

The priors and `prior_shift_vector` are unchanged. The vector is float32 and already includes tau. Historical `v2_train_class_counts.json` additionally lists two `Snow and ice` rows; these are outside the frozen eight-class system and **are not added to its prior denominator**. Read priors from the frozen calibration configuration instead of summing every historical class key.

## 4. Environment and inference API

The checkpoint embeds Ultralytics `8.3.0`. No authenticated complete package lock or current wrapper execution is supplied; the previous broad `Ultralytics >= 8.4.0` requirement is not evidence of compatibility. Existing code imports NumPy, Pillow, PyTorch and Ultralytics. No environment was installed or changed in this revision.

`inference/predict.py` is unchanged. It uses the stored class order, the supplied model and prior vector. Its mathematical shift and preprocessing source match the archived evaluation source on inspection. Runtime behavior is not certified, and no assertion of exact reproduction from new images is made.

## 5. Records intentionally preserved

Historical frozen YAML/Markdown, original model, calibration JSON, CSV results and all split files remain byte-for-byte unchanged. Old RC1 text replaced by current corrections is archived under `history/rc1/`. The previous result JSON is archived before changing descriptive labels. Existing license text remains unchanged.

See `CHANGE_MANIFEST.json` for changed/added files and `RELEASE_VALIDATION.json` for completed validation. No new training, image inference, test tuning, publication, email or paid compute was performed.
