# Model Weights Distribution Status

**Status:** WITHHELD FROM PUBLIC REDISTRIBUTION  
**Revision:** `v2.0-rc2-docfix` · 12 October 2026

---

## 1. Checkpoint Identity and Provenance

- **Target Checkpoint:** `model/best.pt`
- **Expected SHA-256:** `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`
- **Architecture:** YOLO11n-cls (input 128×128 RGB)
- **Training Epochs:** 10 epochs, AdamW optimizer, batch 64, seed 20261011

Embedded checkpoint metadata records `pretrained=true` referencing cached Ultralytics weights (`/mnt/evren_data/cache/ultralytics/yolo11n-cls.pt`). The model was fine-tuned from ImageNet initialization rather than trained from random initialization.

---

## 2. Rationale for Withholding Checkpoint Binary

In accordance with strict reproducibility and intellectual property standards:
1. **Upstream Licensing Scope:** Ultralytics YOLO11 incorporates AGPL-3.0 / Enterprise licensing. Upstream redistribution rights and redistribution terms for fine-tuned derivative weights are not accompanied by an explicit upstream license grant in the project records.
2. **Provenance Authentication:** The exact upstream starting-weight artifact SHA-256 and chain of custody cannot be independently authenticated from local records alone.
3. **No Unverified Release:** Per project policy documented in `LICENSE_NOTES.md`, binary model weights are withheld from public distribution rather than distributed under assumed or unverified open-source terms.

---

## 3. What is Fully Released and Audited

The withholding of `best.pt` does **not** impede scientific auditing or reproducibility:
- **Code (Apache License 2.0):** Inference engine (`inference/predict.py`), verification tool (`tools/verify_release.py`), and evaluation scripts.
- **Frozen Calibration System:** Precise Bayesian logit shift configuration ($\tau = 0.50$, class priors, class ordering) in `config/calibration_config.json`.
- **Saved Predictions Array:** Complete 68,558 test sample predictions and raw logits in `predictions/test_predictions.npz` (SHA-256: `d5b63a61813f8ec9ea2d417e3c08ff4b90cf0973efd53b1503351520c9254c64`).
- **Benchmark Results & Audits:** Exact confusion matrices, per-class metrics, provincial breakdowns, and independent audit verification trails.
- **Data Manifests (CC BY 4.0):** 69,512 test manifest rows and 50,000 development manifest rows with spatial province tags.

---

## 4. Local Execution with Authorized Checkpoint

Researchers with legitimate access to the verified model checkpoint can place `best.pt` into the `model/` directory:
```bash
# Verify checksum before execution
sha256sum model/best.pt
# Expected: 8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a

# Run standalone inference
python inference/example_usage.py
```
If `best.pt` is absent, `tools/verify_release.py` will verify all saved arrays, logits, metrics, and manifest linkages without requiring the binary weight file.
