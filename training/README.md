# TurkeyLandCover V2 — Training Pipeline & Framework Documentation

This directory contains the training pipeline source code corresponding to the `best.pt` model weights (SHA-256: `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`), provided under GNU AGPL-3.0 as part of the Corresponding Source (AGPL-3.0 Section 1 & Section 6).

---

## 1. Upstream Framework Specification

- **Framework:** [Ultralytics](https://github.com/ultralytics/ultralytics)
- **Version:** `8.3.0` (Pinned upstream release: [`https://github.com/ultralytics/ultralytics/tree/v8.3.0`](https://github.com/ultralytics/ultralytics/tree/v8.3.0))
- **Base Architecture:** `yolo11n-cls` (YOLO11 Nano Classifier)
- **License:** GNU AGPL-3.0 (Copyleft)

---

## 2. Training Hyperparameters & Execution Configuration

The exact training parameters embedded in the PyTorch checkpoint header (`checkpoint_embedded_metadata.json`) and used during execution on the EVREN cluster:

| Parameter | Value | Description |
| :--- | :--- | :--- |
| `task` | `classify` | Classification task |
| `architecture` | `yolo11n-cls` | YOLO11 Nano classification head |
| `imgsz` | `128` | 128×128 bilinear input resolution |
| `epochs` | `10` | 10 training epochs |
| `batch` | `64` | Batch size 64 |
| `optimizer` | `AdamW` | AdamW optimizer |
| `lr0` | `0.001` | Initial learning rate |
| `lrf` | `0.01` | Final learning rate ratio |
| `momentum` | `0.9` | Momentum factor |
| `weight_decay` | `0.0005` | Weight decay |
| `seed` | `20261011` | Deterministic training seed |
| `device` | `0` (GPU) | Single NVIDIA GPU cluster node |

---

## 3. Pipeline Components

1. **`v2_training_pipeline.py`:**
   - Implements `MulticlassFocalLoss` ($\gamma=1.5$, $\alpha$ derived from inverse class frequencies) to address severe class imbalance across the 8 land-cover classes.
   - Implements `BalancedFocalClassificationTrainer` subclassing `ultralytics.models.yolo.classify.train.ClassificationTrainer` with `WeightedRandomSampler`.
   - Contains runtime assertions ensuring default Cross-Entropy loss is replaced and balanced sampling is active.

2. **`run_exp_v2_balanced_50k.py`:**
   - Automation script that submitted the training payload to the EVREN cluster API (`/training/jobs`), verified the pre-epoch runtime gate (item count, GPU allocation, dataset version), monitored epoch progression, and retrieved the resulting `best.pt` checkpoint.

---

## 4. Provenance & Dataset Status

- **Training Pool:** 50,000 candidate items staged on EVREN.
- **Reported Training Exposure:** 40,253 items reported by server logs.
- **Training Manifest File List:** `UNKNOWN`. The specific row-by-row subset list of 40,253 patches was not exported from the server database. Note: While desirable for engineering reproducibility, private training datasets and internal manifests are not defined as source code under AGPL-3.0 Section 1, nor mandated by AGPL-3.0 Section 6.
- **Initial Checkpoint:** Upper upstream starting point was `/mnt/evren_data/cache/ultralytics/yolo11n-cls.pt`. Its historical SHA-256 at the moment of training is marked `UNKNOWN` (cannot be backfilled retrospectively).
- **Test & Validation Splits:** Mühürlü test split (`metadata_and_splits/v2_spatial_test.csv`, 68,558 rows) and validation split (`metadata_and_splits/v2_spatial_val_50k_fixed.csv`, 50,000 rows) are fully verified and present in this repository.
