# TurkeyLandCover V2 — Audit Corrections & Record Reconciliation

**Date:** 2026-10-12  
**Purpose:** Formally document and reconcile all historical discrepancies, parameter mismatches, and platform recording gaps identified during independent audit.

---

## 1. Pretrained Initialization vs. Historical Frozen YAML

### Historical Record in `configs/v2_50k_frozen.yaml`:
Line 12 states: `pretrained: false`.

### Physical Reality in Checkpoint `best.pt`:
Inspection of `best.pt` metadata (`torch.load('best.pt', weights_only=False)['train_args']`) proves:
- `pretrained`: `True`
- `model`: `/mnt/evren_data/cache/ultralytics/yolo11n-cls.pt` (ImageNet-pretrained YOLO11n-cls weights).

### Correction:
The historical frozen YAML file is preserved unmodified for audit traceability. However, all public documentation is corrected:
- **The model was NOT trained from scratch.**
- The model was fine-tuned from standard ImageNet-pretrained YOLO11n-cls weights on the EVREN platform.
- Any prior claims of "trained from scratch" are retracted.

---

## 2. EVREN Dataset Version Registration Logs & Provenance

### Historical Record in `splits/v2_evren_dataset_versions.json`:
Contains `HTTP 422` error responses with `null` IDs resulting from an early failed attempt to use deprecated version tags (`v2-balanced-train`, `v2-natural-train`).

### Physical Reality in Execution Records:
The actual successful EVREN jobs were submitted and executed with dataset version IDs:
- Balanced Training: `01a12cb1-05c8-7c80-b321-2c51ae68b55a` (EVREN Job ID: `01a12f84-8c82-7d92-8d15-05d042eea100`)
- Natural Training: `01a12cb1-15b2-7380-9fd8-9d03e48be105` (EVREN Job ID: `01a12cc3-e897-74c1-8e6c-1fa672d8acde`)
- Validation: `01a12cb1-223a-7aa0-8ae3-ef298f874b60`

### Correction & Independent Audit Status:
While the job response records confirm that EVREN accepted these version IDs, the original API response logs capturing the raw server-side manifest hash and registration body were not retained locally.
- **Audit Assessment:** *Platform kökeni bağımsız olarak tam doğrulanamadı* (Platform dataset version provenance cannot be independently re-verified from local logs beyond job submission metadata).
- The obsolete 422 error file is not presented as a successful registration record.

---

## 3. Validation CSV Hash Discrepancy

### Discrepancy:
- `configs/v2_50k_frozen.yaml` records: `2a8d29be49c6887094ec8c53f949fdec5b377ee5b11491a7b2884114f601749f`
- Physical file `splits/v2_spatial_val_50k_fixed.csv` has SHA-256: `edf44566cd51c1263bd371f2a571867b7a039857bbee7079c87981d63c425ae5`

### Independent Audit Verification:
- The hash `2a8d29...` corresponds exactly to `splits/v2_spatial_val_50k.csv` (9 columns).
- Both CSV files contain the **exact same 50,000 sample IDs in the exact same row order**.
- The only change in `v2_spatial_val_50k_fixed.csv` is the append of the 10th column (`canonical_class`) to enable local ground truth label mapping for evaluation scripts.
- Zero samples, coordinates, or province assignments were altered.

---

## 4. Test Sample Exclusions (68,558 vs. 69,512)

### Record:
The pristine spatial test grid manifest (`splits/v2_spatial_test.csv`) contains 69,512 rows. The physical test evaluation executed on 68,558 patches.

### Correction & Clarification:
The 954 excluded rows are strictly documented as **"görüntüsü çözümlenemeyen manifest satırları"** (grid cell coordinate rows for which no physical image tile was generated in the labeled dataset archive due to marine/border buffer exclusions).

---

## 5. Test Accuracy Numerator Reconciliation (59,076 vs. 59,074)

### Record:
A typographical slip in chat summary prose cited `59,074 / 68,558` correct predictions.

### Empirical Proof:
- Immutable tensor `artifacts/final_test/test_predictions.npz`: `(gt == pred).sum() = 59,076`.
- Confusion matrix diagonal: `413 + 490 + 13869 + 22186 + 24 + 630 + 328 + 21136 = 59,076`.
- Exact authoritative Top-1 accuracy: `59,076 / 68,558 = 86.169375%` (86.17%).
- All publication artifacts are synchronized to 59,076.
