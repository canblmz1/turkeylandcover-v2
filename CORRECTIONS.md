# TurkeyLandCover V2 — Corrections and record reconciliation

**Date:** 12 October 2026 · **Revision:** `v2.0-rc2-docfix`  
This is a publication correction after evaluation, not a new preregistration or experiment. Original replaced RC1 files are retained byte-for-byte under `history/rc1/`. Historical frozen configuration files are unchanged.

## 1. Chat summary versus the actual uploaded ZIP

The original RC1 archive already contained Macro-F1 **0.6721**, bootstrap **B=1,000**, and Muğla present-class Macro-F1 **0.6190**. The contradictory values 0.6977, 954 bootstrap repeats and 0.7474 appeared in the pasted agent summary, not in those RC1 publication tables. This revision does not pretend those correct tables required numerical replacement.

The RC1 ZIP contained **26 files**, including `SHA256SUMS.txt`; all **25 listed file hashes** matched. Its SHA-256 was `77ea4d6077a9526f4e46d6e3b039c59ce51dabd98ba03e2ff992ecf3f1f9fe3f`.

## 2. Pretrained initialization and training exposure

`config/v2_50k_frozen.yaml` says `pretrained:false`; checkpoint metadata records `pretrained:true` and a cached `yolo11n-cls.pt` path. The historical file is preserved. Current documentation reports the checkpoint record, does not claim training from scratch, and no longer authenticates a specific ImageNet initialization without the original upstream weight/hash.

The prior independent audit used opcode inspection without `torch.load` or model execution. The RC1 prose incorrectly described unsafe deserialization as that audit's method; it is not.

A selected dataset pool of 50,000 is distinct from the **project-reported 40,253 internal training examples**. The exact source manifests remain unavailable. The 67 training provinces and other platform facts are identified as project-reported, not newly server-verified.

## 3. Platform record and file-path corrections

`metadata_and_splits/v2_evren_dataset_versions.json` contains three HTTP 422 failures with null IDs. It is retained as historical failure evidence, not successful registration evidence. IDs in the frozen configuration remain project records. No current API result or raw successful cluster manifest was added or invented.

Package paths are `model/best.pt`, `config/` and `metadata_and_splits/`, not the historical `models/`, `configs/` or `splits/` locations. The prototype class is `TurkeyLandCoverClassifier`; its result key is `prediction`.

## 4. Validation-manifest lineage

The frozen validation hash is `2a8d29be49c6887094ec8c53f949fdec5b377ee5b11491a7b2884114f601749f`. The current file hash is `edf44566cd51c1263bd371f2a571867b7a039857bbee7079c87981d63c425ae5`.

The earlier audit reproduced the former hash exactly by removing only `canonical_class` and restoring the original serialization. No sample values/order in the original columns changed. See `evidence/independent_audit/validation_manifest_lineage.json`. Both metadata files remain unchanged here.

## 5. Exclusions, uncertainty and geographic claims

**954 image-unresolved manifest rows**, not 954 proven marine/border/cloud exclusions. The supplied code tests membership in the labeled-image archive; it does not establish a separate cause for each omitted row.

Bootstrap is **1,000 patch-level replicates**, seed 20261012. There is no measured effective sample size or quantified geographic-cluster interval in this evidence. The earlier assertions of an effective sample size determined exactly by seven provinces, and of a quantified wider interval for “74 unvisited provinces,” are removed. Many of those other provinces belong to training/development, not unvisited territory.

Support-zero classes are absent from the **evaluated subset**, not established as absent from the province's landscape. Labels such as “zero environmental overlap,” “zero overfitting” and uniform blindness elimination are not current conclusions.

## 6. Source resolution, task and licensing

128×128 is the **model input size after resizing**, not proof of a 1.28×1.28 km footprint. Patch classification is not pixelwise 10 m segmentation. The inconsistent source wording “L2A Top-of-Atmosphere” is removed rather than replaced with an unverified radiometric provenance claim.

`MODEL_CARD.md` previously said MIT, while the supplied `LICENSE` declares Apache-2.0 for code and CC BY 4.0 for dataset material. `LICENSE` is preserved unchanged; the model card now reflects it and explicitly leaves checkpoint/upstream rights unverified. Missing referenced legal documents are listed in `LICENSE_NOTES.md`.

## 7. Inference and numerical identity

The existing inference source adds `prior_shift_vector` once. This is correct for this configuration because that vector **already includes tau=0.50**. No second multiplication is introduced. Weights, config bytes and prediction NPZ are unchanged. The existing prototype inference Python files are unchanged and not executed; no runtime success is asserted.

Final numerator is **59,076**, not the historical chat typo 59,074. Global Macro-F1 remains **0.672094391**. The mathematical verifier included here checks hashes and saved arrays only.

## 8. Historical records and current result metadata

The raw RC1 result JSON is preserved under `history/rc1/results/`. Its numerical fields are unchanged in the current result JSON; only unsupported labels and explanatory metadata are corrected. The old `excluded_nodata_patches` key is replaced by `excluded_unresolved_manifest_rows`. The old generalization-gap field used rounded development references and is retained with an explanation; precise like-for-like values are separately included.

The historical `PUBLICATION_READY` and test pre-open declarations are not presented as a present independent endorsement. Original documents are archived, with scope-labelled pointers at their previous paths. The test has already been used for final evaluation according to project records; this revision does not reopen model development or claim it is still pristine.
