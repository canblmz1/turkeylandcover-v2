# Licensing and attribution record — not a new license

The original `LICENSE` file is preserved byte-for-byte. It declares:

- Dataset material: CC BY 4.0, with ESA WorldCover / modified Copernicus Sentinel notices.
- Code: Apache License 2.0.

The RC1 model card's separate MIT assertion contradicted that file and was removed. This correction does not authorize a license change, assign rights for others' work, or authenticate an upstream license.

## Incomplete records

The original `LICENSE` references `legal/archive/cc_by_4.0_legalcode.txt` and `legal/ATTRIBUTION.md`; neither path is present in the reviewed main tree. A root-level `ATTRIBUTION.md` was added by commit `7579554`; it supplies attribution notices but does not repair those literal paths. Its code scope mentions `src/`, `scripts/`, and `tests/`, while this release also has an `inference/` directory. The declaration's exact coverage of that directory and of added documentation needs owner confirmation.

The checkpoint is publicly available: GitHub release `v2.0`, published on 12 October 2026, includes `best.pt` (3,201,787 bytes); GitHub reports SHA-256 `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`. Commit `7579554` added `model/best.pt`, `LICENSE_AGPL.txt`, `ATTRIBUTION.md`, and training source, and declared GNU AGPL-3.0 for the weights and combined distribution. Thus the earlier statements that no checkpoint license was declared and that the package was unpublished are superseded.

That project declaration and the presence of a license text do not authenticate the historical starting-weight artifact or establish a complete dependency/weight licensing dossier, sufficient Corresponding Source, commercial-use clearance, or compliance of the entire distribution. The exact scope of the original Apache-2.0 declaration remains unresolved. EVREN contractual permission is not independently established by the repository's assertions. This correction neither changes existing license grants nor determines that distribution is prohibited. See [WEIGHTS_DISTRIBUTION_STATUS.md](WEIGHTS_DISTRIBUTION_STATUS.md) for evidence and remaining limits.

## Notices copied from the supplied LICENSE

© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium  
Contains modified Copernicus Sentinel data 2021

The supplied source says the dataset is adapted from ESA WorldCover 2021 and boundaries are from Natural Earth. These are preserved source declarations, not an independent provenance investigation. No endorsement by ESA, the ESA WorldCover consortium, the European Commission, SSB or EVREN is claimed.

No license text is changed by this documentation correction. Keep this limitation with any review copy; do not relabel the entire package MIT.
