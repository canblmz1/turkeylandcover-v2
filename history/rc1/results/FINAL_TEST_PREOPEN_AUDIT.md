# TurkeyLandCover V2 — Final Test Pre-Open Integrity Audit
## Gate Verification Protocol Before Sealed Test Access

**Timestamp:** 2026-10-12T13:31:00+03:00  
**Audit Purpose:** Prove total pre-evaluation integrity, zero data leakage, and uncompromised holdout sealing prior to opening `splits/v2_spatial_test.csv`.

---

## 1. Authoritative Pre-Open Verification Checklist

| # | Integrity Condition | Verified Value | Status |
| :---: | :--- | :--- | :---: |
| 1 | **Base Checkpoint SHA-256** | `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a` | **PASS** |
| 2 | **Config Freeze SHA-256** | `3227810623582f3222ea95e84990a2579c77caf53298e198ef0d21378bbec9df` | **PASS** |
| 3 | **Evaluation Script SHA-256** | `982ac6081240089661666c385df35c3625a907096c42e3be3827d9d77c9522d5` | **PASS** |
| 4 | **Pristine Test CSV SHA-256** | `6e08a98f777bc3de0c4cb357aa6a21c5d57f880aff8b79a9b09f3a2e55d02171` | **PASS** |
| 5 | **Pristine Test Row Count** | **69,512** rows | **PASS** |
| 6 | **Exact 7 Test Provinces** | `TR-08` (Artvin), `TR-22` (Edirne), `TR-33` (Mersin), `TR-36` (Kars), `TR-47` (Mardin), `TR-48` (Muğla), `TR-50` (Nevşehir) | **PASS** |
| 7 | **Train / Test Province Overlap** | **0** (Empty intersection across 67 train provinces) | **PASS** |
| 8 | **Validation / Test Province Overlap** | **0** (Empty intersection across 7 validation provinces) | **PASS** |
| 9 | **Previous Prediction Artifacts** | **None** (`artifacts/final_test` does not exist prior to run) | **PASS** |
| 10 | **Test Evaluation Count Prior to Run** | **0** (Zero previous inference passes executed) | **PASS** |

---

## 2. Integrity Gate Verdict

**ALL 10 INTEGRITY CHECKS PASSED UNANIMOUSLY.**

- No parameters, thresholds, or logit calibrations may be adjusted after opening.
- The model will be evaluated **EXACTLY ONCE** on the pristine holdout test set using the frozen `tau = 0.50` prior-shift correction.
- The evaluation script `scripts/evaluate_v2_final_test.py` is permanently hashed and authorized for execution.
