# Model Card — TurkeyLandCover V2

**Publication revision:** `v2.0-rc2-docfix` (same frozen model).  
**Evidence status:** saved-prediction numerical consistency verified; end-to-end image inference and complete training provenance not independently verified here.

## Model summary

- **Type:** YOLO11n-cls patch classifier with fixed prior-shift logit adjustment.
- **Input:** RGB image converted to 128×128 using the supplied evaluation preprocessing. The source is described in project records as Sentinel-2 10 m imagery. Exact source-raster radiometry, acquisition metadata and per-patch georeferencing are not independently established by this package.
- **Output:** one of eight patch classes and softmax scores after adjustment; no segmentation mask.
- **Initialization:** checkpoint metadata records `pretrained=true` and `/mnt/evren_data/cache/ultralytics/yolo11n-cls.pt`. The initial weight file/hash is absent. Random initialization is not supported; a specific upstream ImageNet artifact is not independently authenticated.
- **Parameter count:** not newly measured in this documentation revision; no assumed 2.6M count is asserted.
- **License:** see the unchanged `LICENSE` and `LICENSE_NOTES.md`; no blanket MIT or checkpoint redistribution clearance is claimed.

## Intended use and exclusions

Research on Turkish Sentinel-2 RGB patch classification and reproducible analysis of saved predictions. Not validated for arbitrary aerial photographs, different sensors, pixelwise mapping, temporal change detection, cadastral decisions or safety-critical/military deployment. No claim of probability calibration quality is established by the name “prior-shift calibration.”

## Recorded training and system identity

Project reports: a 50,000-item balanced pool; 40,253 internal training, 4,413 internal validation and 5,334 internal test items. The actual item lists and raw cluster logs are absent from the supplied evidence; complete exposure/leakage auditing remains partial.

Checkpoint metadata: 10 epochs, batch 64, 128 input, AdamW, lr0 0.001, lrf 0.01, weight_decay 0.0005, seed 20261011; recorded Ultralytics version 8.3.0. These are metadata inside the checkpoint, not live cluster verification. Historical `pretrained:false` remains in the frozen YAML and is explicitly corrected in `CORRECTIONS.md` rather than silently rewritten.

Final identity: `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a` plus the unchanged `config/calibration_config.json`, including tau=0.50, priors, class order, and preprocessing. The shift vector is already tau-scaled.

## Evaluation

The saved test artifact has 68,558 unique sample IDs; the manifest has 69,512 rows. The 954 unmatched rows are **image-unresolved manifest rows**; per-row marine/cloud/border causes are not proven by the files. Test and development sample/province separation is supported by the prior audit; actual training item membership could not be independently rechecked.

Top-1 **86.169375%**; global eight-class Macro-F1 **0.672094391**; balanced accuracy **73.982644%**; worst-class F1 **0.413793103**. These numerical results were reconstructed from saved logits, not a new image forward pass. The one-time evaluation history remains a project declaration rather than something hashes alone prove.

| Class | Support | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| `bare_sparse_vegetation` | 661 | 0.309595 | 0.624811 | 0.414035 |
| `built_up` | 515 | 0.496957 | 0.951456 | 0.652898 |
| `cropland` | 15,483 | 0.848101 | 0.895757 | 0.871278 |
| `grassland` | 27,981 | 0.918865 | 0.792895 | 0.851245 |
| `herbaceous_wetland` | 67 | 0.489796 | 0.358209 | 0.413793 |
| `permanent_water_bodies` | 674 | 0.763636 | 0.934718 | 0.840560 |
| `shrubland` | 787 | 0.431012 | 0.416773 | 0.423773 |
| `tree_cover` | 22,390 | 0.876831 | 0.943993 | 0.909173 |

## Geographic and statistical scope

Mean province Macro-F1 over locally present classes: development **0.681884**, final **0.671503**. Over all eight classes: development **0.592506**, final **0.544347**. Global Macro-F1: development **0.670588**, final **0.672094**. These definitions must not be interchanged.

| Province | N | Top-1 | Macro-F1: present classes | Macro-F1: all 8 | Present classes |
|---|---:|---:|---:|---:|---:|
| Artvin (TR-08) | 8,314 | 85.0373% | 0.708332 | 0.442707 | 5 |
| Edirne (TR-22) | 5,706 | 86.9611% | 0.611896 | 0.535409 | 7 |
| Mersin (TR-33) | 15,155 | 80.8050% | 0.646705 | 0.646705 | 8 |
| Kars (TR-36) | 11,018 | 82.4197% | 0.730947 | 0.548210 | 6 |
| Mardin (TR-47) | 10,217 | 92.8159% | 0.614426 | 0.537622 | 7 |
| Muğla (TR-48) | 12,754 | 90.6225% | 0.619035 | 0.619035 | 8 |
| Nevşehir (TR-50) | 5,394 | 86.6889% | 0.769180 | 0.480738 | 5 |

Reported 95% intervals use patch-level resampling, B=1000, seed=20261012. They do not account for geographic clustering. “Support zero” means no ground-truth examples in this sampled holdout, not that the land-cover class is ecologically absent from the entire province.

## Audit limits

Saved-logit arithmetic and artifact identity are verified. Actual training examples, source labels, upstream initial weights, live platform provenance, calibrated probability reliability, legal clearance for all components, and end-to-end wrapper execution are not established here. See `LIMITATIONS.md` and `REPRODUCIBILITY.md`.
