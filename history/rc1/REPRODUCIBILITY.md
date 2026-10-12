# TurkeyLandCover V2 — Reproducibility & Epistemic Audit Manifest

**Date:** 2026-10-12  
**Purpose:** Delineate verified facts, platform-reported metadata, and unverified elements, with exact instructions for independent re-execution.

---

## 1. Three-Tier Epistemic Audit Classification

### 1.1 Independently Verified Artifacts & Metrics
The following elements have been physically validated on disk with matching hashes and tensor computations:
- Model checkpoint `model/best.pt` (SHA-256: `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`).
- Predictions tensor `test_predictions.npz` (SHA-256: `d5b63a61813f8ec9ea2d417e3c08ff4b90cf0973efd53b1503351520c9254c64`).
- Evaluation script `scripts/evaluate_v2_final_test.py` (SHA-256: `982ac6081240089661666c385df35c3625a907096c42e3be3827d9d77c9522d5`).
- Exact test patch count: **68,558** across 7 test provinces (`TR-08`, `TR-22`, `TR-33`, `TR-36`, `TR-47`, `TR-48`, `TR-50`).
- Exact correct predictions: **59,076** (`Top-1 = 86.17%`).
- Exact test metrics: Macro-F1 = **0.6721**, Balanced Accuracy = **73.98%**, Worst-Class F1 = **0.4138**.
- 8x8 confusion matrix and per-province metrics.

### 1.2 Reported in Project Records (Platform-Dependent)
The following metadata are documented in EVREN platform execution logs:
- Training job ID `01a12f84-8c82-7d92-8d15-05d042eea100`, Slurm job ID `5645`.
- Single GPU allocation (`WORLD_SIZE = 1`, 200.2 seconds wall-clock time).
- Internal EVREN dataset split resolution: 40,253 train, 4,413 val, 5,334 test patches staged to `/dev/shm`.

### 1.3 Unverified Platform Elements
- Server-side raw API response logs for dataset version creation (`POST /datasets/.../versions`).
- Provenance of `/mnt/evren_data/cache/ultralytics/yolo11n-cls.pt` pre-training weights beyond stock Ultralytics ImageNet release.

---

## 2. Exact Execution Environment & Instructions

### Requirements:
- Python >= 3.10
- PyTorch >= 2.1.0
- Ultralytics >= 8.4.0
- Pillow, NumPy, Pandas

### Running Standalone Calibrated Inference:
```bash
cd release/v2/inference
python example_usage.py
```

### Reproducing Test Metrics from Saved Predictions:
```python
import numpy as np

npz = np.load("predictions/test_predictions.npz")
gt = npz["ground_truth_idx"]
pred = npz["pred_idx"]
print("Top-1 Accuracy:", (gt == pred).sum() / len(gt))  # 0.86169375
```
