# TurkeyLandCover V2 — Scientific Limitations & Known Failure Modes

**Date:** 2026-10-12  
**Purpose:** Explicitly communicate the boundaries, uncertainties, and failure modes of the TurkeyLandCover V2 classification system.

---

## 1. Uncertainty Estimation & Spatial Autocorrelation
- **Bootstrap Method:** The reported 95% confidence intervals (Top-1: `[85.91%, 86.44%]`, Macro-F1: `[0.6557, 0.6876]`) are calculated using a non-parametric patch-level bootstrap ($B=1,000$, seed `20261012`).
- **Critical Limitation:** This assumes independent and identically distributed (i.i.d.) patches. It **does NOT account for spatial clustering** within the 7 evaluated test provinces.
- **Scientific Impact:** Because image patches within a province share local atmospheric conditions, topography, and seasonal Sentinel-2 acquisition dates, the true effective sample size is governed by the 7 held-out province clusters rather than 68,558 independent locations. Real-world uncertainty across the remaining 74 unvisited provinces of Turkey is substantially wider than the reported patch-level confidence intervals.

---

## 2. Geographical Heterogeneity Across Turkey
- Generalization is **not geographically uniform**.
- Performance varies substantially across the 7 tested provinces:
  - Mersin (`TR-33`, Akdeniz): Macro-F1 (present classes) = **0.6467**, Top-1 = 80.81%
  - Muğla (`TR-48`, Ege): Macro-F1 (present classes) = **0.6190**, Top-1 = 90.62%
  - Nevşehir (`TR-50`, İç Anadolu): Macro-F1 (present classes) = **0.7692**, Top-1 = 86.69%
  - Edirne (`TR-22`, Marmara): Macro-F1 (present classes) = **0.6119**, Top-1 = 86.96%
  - Mardin (`TR-47`, Güneydoğu): Macro-F1 (present classes) = **0.6144**, Top-1 = 92.82%
  - Kars (`TR-36`, Doğu Anadolu): Macro-F1 (present classes) = **0.7309**, Top-1 = 82.42%
  - Artvin (`TR-08`, Karadeniz): Macro-F1 (present classes) = **0.7083**, Top-1 = 85.04%
- In areas where marginal vegetation classes have scarce presence (e.g., shrubland in Edirne with 2 patches, Mardin with 6 patches), local class recall degrades severely (Edirne shrubland F1 = 0.0000; Mardin shrubland F1 = 0.0645).

---

## 3. Ecological Absence of Classes in Administrative Holdouts
- Administrative boundaries do not correspond to ecological compartments. Certain provinces naturally lack specific land covers:
  - Artvin lacks cropland, wetland, and shrubland.
  - Kars lacks wetland and shrubland.
  - Nevşehir lacks wetland, shrubland, and tree cover.
- In 8-class macro-averaging, unobserved classes (`support = 0`) receive $F_1 = 0.0$. Users must evaluate regional performance using both "present-only" and "all-8" definitions.

---

## 4. Sensor Scope & Resolution Limits
- **RGB Only:** Inference uses only Sentinel-2 B04 (Red), B03 (Green), and B02 (Blue). Multi-spectral bands (B08 NIR, B11/B12 SWIR, RedEdge) and SAR (Sentinel-1) were not utilized due to public platform constraints.
- **Resolution:** Input patches are 128x128 pixels representing ~1.28 km x 1.28 km footprints. Fine linear structures (canals, narrow roads, scattered settlements) and mixed boundary pixels suffer from aggregation errors.

---

## 5. Non-Operational Status
- The model is an **experimental research prototype**.
- It is NOT certified for operational cartography, cadastral verification, or mission-critical defense/military deployment.
