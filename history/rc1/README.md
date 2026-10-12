# TurkeyLandCover V2 — Release Candidate (v2.0-rc1)
## Geographically Disjoint Land-Cover Classification Model with Prior-Shift Calibration

TurkeyLandCover V2 is an experimental research model designed for 10-meter land-cover classification across Turkey from Sentinel-2 RGB imagery. It combines a fine-tuned YOLO11n-cls backbone with post-hoc Bayesian logit calibration ($\\tau = 0.50$) to alleviate minority-class blindness while maintaining strong majority-class accuracy.

---

## Key Verified Results (Pristine Geographically Disjoint Holdout)
Evaluated on **68,558** physical Sentinel-2 patches across 7 completely held-out provinces (Artvin, Edirne, Mersin, Kars, Mardin, Muğla, Nevşehir):

- **Top-1 Accuracy:** **86.17%** (59,076 / 68,558 correct predictions)
  - 95% patch-level bootstrap CI: [85.91%, 86.44%]
- **Macro-F1 (Primary Metric):** **0.6721**
  - 95% patch-level bootstrap CI: [0.6557, 0.6876]
  - Development benchmark (Val 50K): 0.6706 (Generalization gap: +0.0015)
- **Balanced Accuracy:** **73.98%** (Macro recall across all 8 classes)
- **Worst-Class F1:** **0.4138** (Herbaceous wetland: 0.4138, Bare vegetation: 0.4140, Shrubland: 0.4238)
- **Top-5 Accuracy:** **99.99%**

---

## Architecture & Calibration System
The system consists of two tightly coupled components:
1. **Backbone (`model/best.pt`):** YOLO11n-cls (~2.6M parameters), fine-tuned from ImageNet on 50,000 balanced Turkish Sentinel-2 patches on the EVREN platform.
2. **Calibrated Head (`config/calibration_config.json`):** Post-hoc logit adjustment:
   $$\\text{corrected\\_logit}_c = \\text{raw\\_logit}_c + 0.50 \\cdot [\\log(P_{\\text{target}}(c) + 10^{-12}) - \\log(P_{\\text{train\\_balanced}}(c) + 10^{-12})]$$

---

## Release Candidate Contents
- `model/best.pt`: Physical model checkpoint (SHA-256: `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`)
- `config/`: Dondurulmuş öncül shift vektörleri ve YAML konfigürasyonu
- `inference/`: `predict.py` ve örnek kullanım scripti
- `results/`: Test sonuçları JSON, karmaşıklık matrisleri ve denetim raporları
- `metadata_and_splits/`: 7 test ilinin koordinatlı manifesti ve bölme özetleri
- `CORRECTIONS.md`: Bağımsız denetim düzeltmeleri ve parametre mutabakatı
- `LIMITATIONS.md`: Uzamsal kümelenme, bölgesel dağılım ve kapsam sınırları
- `REPRODUCIBILITY.md`: Üç seviyeli epistemik durum ve yeniden üretim rehberi
