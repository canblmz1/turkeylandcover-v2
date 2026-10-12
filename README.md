# TurkeyLandCover V2 — corrected release candidate
## Sentinel-2 RGB patch classification with frozen prior-shift adjustment

**Release:** `v2.0` · **Date:** 12 October 2026  
**Status:** research prototype; saved-prediction numerical consistency verified, complete training provenance only partially verifiable.

This revision corrects publication records. It is **not a new model or experiment**. The checkpoint, historical frozen configurations, prior vectors, tau, and saved test predictions are unchanged. No training, image inference, or external platform calls were performed for this revision.

Türkçe başlangıç: [BASLA_BURADAN.md](BASLA_BURADAN.md).

## Verified results and their scope

The previously saved predictions contain **68,558** unique sample IDs from seven designated test provinces: Artvin, Edirne, Mersin, Kars, Mardin, Muğla and Nevşehir.

| Metric | Value |
|---|---:|
| Correct / evaluated samples | 59,076 / 68,558 |
| Top-1 accuracy | 86.169375% |
| Macro-F1, all eight classes | 0.672094391 |
| Balanced accuracy, all eight classes | 73.982644% |
| Worst-class F1 | 0.413793103 |
| Top-5 accuracy | 99.985414% |

These are **recomputed from saved logits and predictions**, not from a new image-to-model run. Hashes identify files but do not independently prove their entire history or the correctness of their source labels. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

The reported 95% intervals are patch-level bootstrap intervals, with **B=1,000**, seed `20261012`: Top-1 [85.905292%, 86.443595%], Macro-F1 [0.655683, 0.687631]. They are not geographic-cluster confidence intervals.

## What the system is

The recorded architecture is **YOLO11n-cls**. The checkpoint records `pretrained=true` and a cached `yolo11n-cls.pt` path; the exact upstream initialization artifact is not included. Therefore this release does not claim random initialization or independently verified ImageNet provenance.

Project records describe a **50,000-item selected pool**, of which **40,253 items** were assigned to internal training, 4,413 to internal validation, and 5,334 to internal test. Those counts are project-reported, not a fresh server verification. A 50,000-item pool is not 50,000 examples used for gradient updates.

This is a patch classifier, **not pixel-level segmentation**. The model input is 128×128 RGB after the preprocessing written in the evaluation source. The source imagery is described by the project as Sentinel-2 10 m; resizing to 128×128 does not establish a 1.28 km square footprint or improve the source ground resolution.

## Frozen inference identity

- Checkpoint: `model/best.pt`, SHA-256 `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a` *(GNU AGPL-3.0 ve Apache-2.0 birleşik lisansı kapsamında yayımlandı; bkz. [WEIGHTS_DISTRIBUTION_STATUS.md](WEIGHTS_DISTRIBUTION_STATUS.md))*.
- Parameters: `config/calibration_config.json`, tau `0.50`, epsilon `1e-12`.
- Class order: the eight names in that JSON, not an inferred alphabetical mapping.
- Formula: `corrected_logits = raw_logits + 0.50 * (log(p_target + epsilon) - log(p_train_balanced + epsilon))`.
- **Important:** `prior_shift_vector` in the JSON already includes tau. Add that vector once; do not multiply it by tau again.

The provided `inference/predict.py` uses RGB conversion, bilinear resizing when needed, float32 division by 255, and CHW layout. Its source was compared with the archived evaluation source; it was **not executed end-to-end** during this documentation revision. Its `confidence` field is a softmax score, not an independently validated probability of correctness.

## Inspect or verify without training

From the extracted release root:

```bash
python tools/verify_release.py --hashes-only
python tools/verify_release.py
```

The first command uses Python's standard library. The second additionally requires NumPy and checks saved predictions, class order, frozen shifts, metrics and province tables. Neither loads the checkpoint, downloads weights, launches a GPU job, nor evaluates new images.

For the current prototype API, source usage is:

```python
from inference.predict import TurkeyLandCoverClassifier

classifier = TurkeyLandCoverClassifier()  # default: model/best.pt
result = classifier.predict("sample_patch.png")
print(result["prediction"])
print(result["confidence"])  # softmax score, not a certified confidence estimate
```

Use only a compatible existing environment and trusted weights. This example was not run in this revision; no universal dependency/version compatibility is claimed. See `inference/USAGE.md`.

## Package and provenance

- `results/`: corrected result metadata, unchanged numerical results, class/province tables.
- `predictions/`: unchanged saved predictions, added from the earlier evidence package.
- `evidence/independent_audit/`: the earlier independent audit and its exact outputs.
- `history/`: original RC1 files replaced by corrections and original evaluation source; historical claims are not current release endorsements.
- `CORRECTIONS.md`, `LIMITATIONS.md`, `LICENSE_NOTES.md`: corrections, known limits and incomplete licensing records.
- `SSB_EVREN_TEKNIK_NOT.md`: restrained Turkish technical summary; not sent to any organization.

The provided `LICENSE` is preserved unchanged. Its code declaration is Apache-2.0 and its dataset declaration is CC BY 4.0, **not MIT**. This revision does not establish a license for the checkpoint or supply missing upstream licensing documents. No publication, repository visibility change, EVREN update, or email transmission has been performed.
