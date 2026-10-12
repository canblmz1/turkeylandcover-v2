# TurkeyLandCover V2 — limitations and known failure modes

**Revision:** `v2.0-rc2-docfix` · 12 October 2026.

## 1. What the audit does and does not establish

The earlier independent audit recomputed saved logits, frozen shifts, predictions, metrics and the existing bootstrap procedure. This release revision checks the same numerical chain and file identity without image inference. It does not prove that the images produced those logits, authenticate semantic labels, establish all training item memberships, or certify test-use history. Matching hashes prove file consistency, not authorship or historical exclusivity.

## 2. Spatial uncertainty

The reported intervals use **B=1,000**, seed **20261012**, individual-patch sampling with replacement. No spatial block or province resampling was used. The patch-i.i.d. assumption may be inappropriate for nearby observations. The evidence does not provide a numeric effective sample size or a geography-adjusted interval; neither is invented here. Seven final provinces were tested, while other provinces were assigned to training/development.

## 3. Regional variation and support-zero classes

| Province | N | Top-1 | Macro-F1: present classes | Macro-F1: all 8 | Present classes |
|---|---:|---:|---:|---:|---:|
| Artvin (TR-08) | 8,314 | 85.0373% | 0.708332 | 0.442707 | 5 |
| Edirne (TR-22) | 5,706 | 86.9611% | 0.611896 | 0.535409 | 7 |
| Mersin (TR-33) | 15,155 | 80.8050% | 0.646705 | 0.646705 | 8 |
| Kars (TR-36) | 11,018 | 82.4197% | 0.730947 | 0.548210 | 6 |
| Mardin (TR-47) | 10,217 | 92.8159% | 0.614426 | 0.537622 | 7 |
| Muğla (TR-48) | 12,754 | 90.6225% | 0.619035 | 0.619035 | 8 |
| Nevşehir (TR-50) | 5,394 | 86.6889% | 0.769180 | 0.480738 | 5 |

An absent ground-truth class in a sampled province has support=0; the all-eight convention assigns zero F1. Present-class metrics exclude those classes. Neither convention proves that the class is absent from the real province. Predicted false positives into absent classes can still matter and are reflected in the confusion matrix. Both definitions are reported, not selected after observing favorable values.

Edirne has two shrubland samples and zero correct predictions. Mardin has six shrubland samples and one correct prediction. Artvin's built-up F1=0.5 relies on only three ground-truth examples. These local scores should not be generalized without support counts.

## 4. Classification failure modes

The pooled test contains at least one true positive for each of eight classes; it does not show that every class is detected in every region. Pooled built-up precision is **49.6957%**, bare/sparse precision **30.9595%**, and wetland recall **35.8209%**. Wetland support is 67, shrubland 787. High pooled accuracy must not conceal these errors.

## 5. Data, resolution and external validity

Project records describe Sentinel-2 RGB at 10 m source resolution. The supplied preprocessing produces 128×128 inputs. The patch footprint and source product/radiometry are not independently authenticated here. No fixed 1.28 km footprint follows from a resized input. This system returns a patch class, not a segmentation map, legal land-use category, crop-yield estimate, change detector or airborne sensor capability.

There are 954 image-unresolved rows in the 69,512-row test manifest. Their individual absence causes are unverified. Source labels appear in the saved prediction evidence, but their semantic correctness was not checked against original label rasters.

## 6. Training provenance and comparisons

The checkpoint records prior-weight initialization; the exact initial weight artifact is absent. Actual training manifests, raw successful server records and the NATURAL checkpoint are absent. Complete train/test leakage verification and equal initialization across experiments therefore remain partial. The NATURAL baseline score cited in historical comparisons was not independently reproduced in the available audit.

## 7. Calibration, code and deployment

Prior-shift adjustment changes class scores. No reliability diagram, calibration-error benchmark or probability guarantee is established by these files. `confidence` is a softmax score. `inference/predict.py` was inspected but not run end-to-end, and its environment is not locked. No model-serving, GPU-speed, energy-use or operational-readiness certification is provided.

The prototype is not certified for military, cadastral, ecological enforcement or other safety-critical decisions. No performance on arbitrary aerial photos, all Turkish locations, future seasons or different sensors is claimed.

## 8. Distribution records

The existing license declarations are retained. Missing legal/attribution files and uncertain checkpoint redistribution terms are recorded in `LICENSE_NOTES.md`. This package is not a rights-clearance opinion and has not been publicly uploaded.
