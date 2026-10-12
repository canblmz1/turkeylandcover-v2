# TurkeyLandCover V2 — Stage 3 Configuration Freeze
## Frozen Post-Hoc Prior Correction Parameters

**Date:** 2026-10-12T13:20:00+03:00  
**Candidate Status:** `V2_STAGE3_DEVELOPMENT_CANDIDATE`  
**Base Checkpoint:** `runs/turkeylandcover_v2/exp_v2_balanced_50k_real/best.pt`  
**Base Checkpoint SHA-256:** `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`  
**Logits Source:** `artifacts/stage3/balanced_val_logits.npz`  
**Logits SHA-256:** `cf11a22bd5ab6ec481035df0d01d61070b36cb896312f71642d35b3d3d8e9732`  

---

## 1. Frozen Hyperparameters

- **Selected Prior Scaling ($\tau$):** `0.50`
- **Numerical Epsilon ($\epsilon$):** `1e-12`
- **Selection Basis:** Maximum Mean Province Macro-F1 across 7 validation provinces (**0.6819**)
- **Tie-Breaker Performance:** Maximum Worst-Class F1 across all evaluated $\tau$ values (**0.1423**)

---

## 2. Frozen Class Priors & Shift Vector ($\Delta$)

Formula:
$$\text{corrected\_logit}_c = \text{raw\_logit}_c + \tau \cdot \Delta_c$$
where:
$$\Delta_c = \log(P_{\text{target}}(c) + \epsilon) - \log(P_{\text{train\_balanced}}(c) + \epsilon)$$

| Index | Class Name | $P_{\text{train\_balanced}}$ | $P_{\text{target}}$ | Full Delta ($\tau=1.0$) | Applied Shift ($\tau=0.50$) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 0 | `bare_sparse_vegetation` | 0.189203 | 0.014717 | -2.5538 | **-1.2769** |
| 1 | `built_up` | 0.136735 | 0.009786 | -2.6371 | **-1.3186** |
| 2 | `cropland` | 0.132885 | 0.258150 | +0.6641 | **+0.3320** |
| 3 | `grassland` | 0.121357 | 0.438801 | +1.2853 | **+0.6427** |
| 4 | `herbaceous_wetland` | 0.008844 | 0.000619 | -2.6589 | **-1.3294** |
| 5 | `permanent_water_bodies` | 0.262738 | 0.019065 | -2.6233 | **-1.3117** |
| 6 | `shrubland` | 0.015850 | 0.001359 | -2.4562 | **-1.2281** |
| 7 | `tree_cover` | 0.132388 | 0.257503 | +0.6653 | **+0.3326** |

---

## 3. Verified Frozen Development Metrics (Validation Set)

- **Macro-F1 (Frozen Primary):** **0.6706**
- **Balanced Accuracy:** **73.09%**
- **Top-1 Accuracy:** **86.87%**
- **Worst-Class F1:** **0.1423**
- **Mean Province Macro-F1:** **0.6819**

---

## 4. Execution Directives

1. **NO Retraining:** Model weights remain strictly frozen (`best.pt`).
2. **NO Parameter Tuning:** $\tau = 0.50$ is permanently frozen. No further search or grid adjustment.
3. **Pristine Test Seal:** `splits/v2_spatial_test.csv` must remain completely sealed until the user authorizes the single final test evaluation run.
