# TurkeyLandCover V2 — release notes

## v2.0-rc2-docfix — 12 October 2026

**Same model, corrected publication records.** This is not V3, a retraining, a second test benchmark, or a new model-selection result.

### Preserved

Checkpoint, tau=0.50, priors, preprocessing implementation, inference Python files, historical freeze files, split manifests, numeric CSVs, and original LICENSE. The saved test predictions were brought forward unchanged from the previously uploaded evidence ZIP.

### Corrected

Evidence scope, 50,000-pool versus reported 40,253-training exposure, unverified upstream ImageNet claims, exclusion causes, geographic uncertainty/absence wording, patch versus pixel resolution, inconsistent MIT declaration, package paths and API examples. Unsupported blanket `PUBLICATION_READY` and `STRONG_GENERALIZATION` labels no longer serve as current independent audit conclusions.

### Numbers

The original ZIP already had the correct 0.6721 Macro-F1, B=1000 bootstrap and Muğla 0.6190 present-class F1; different numbers appeared only in the agent's chat summary. The current exact test metrics remain Top-1 0.8616937483590537, Macro-F1 0.6720943913308772 and balanced accuracy 0.7398264353147572.

### Added

A no-inference saved-metric verifier, prior independent audit artifacts, a source/history trail, Turkish start guide, license-record notes, corrected result metadata and a regenerated hash manifest.

### Remaining boundaries

End-to-end image inference, full training/source-label provenance, dependency lock and checkpoint rights were not established. No external distribution was performed. See `LIMITATIONS.md`, `LICENSE_NOTES.md` and `REPRODUCIBILITY.md`.
