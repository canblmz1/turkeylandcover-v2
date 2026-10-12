# TurkeyLandCover V2 — Release Notes (v2.0-rc1)

**Release Date:** 2026-10-12  
**Tag:** `v2.0-rc1` (Release Candidate)  

---

### Highlights:
- **Calibrated Multi-Class Land Cover Mapping:** Integration of frozen $\tau = 0.50$ Bayesian logit correction, elevating Macro-F1 to 0.6721 on the 7-province spatial holdout.
- **Complete Elimination of Severe Class Blindness:** F1 scores on marginal Turkish vegetation (shrubland, wetland, bare sparse) raised above 0.41.
- **Audit-Driven Record Reconciliation:** Full disclosure of ImageNet initialization, dataset version logs, validation CSV hash alignment, and patch-level uncertainty limitations.

### Components in this Package:
1. `model/best.pt`: Physical YOLO11n-cls fine-tuned weights (SHA-256: `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`).
2. `config/calibration_config.json`: Frozen logit adjustment parameters and prior shift vectors.
3. `inference/predict.py`: Self-contained, dependency-minimal Python classification module.
4. `results/`: Complete JSON, CSV, and markdown evaluation reports.
5. `metadata_and_splits/`: Benchmark CSV manifests and spatial split definitions.
