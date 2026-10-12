# Model Card — TurkeyLandCover V2

## Model Summary
- **Model Name:** TurkeyLandCover V2 (YOLO11n-cls + Bayesian Logit Calibration)
- **Model Description:** Turkey-scale Sentinel-2 RGB land-cover classification model with geographically disjoint evaluation and prior-shift calibration.
- **Model Type:** Fine-tuned convolutional classifier (nano scale, ~2.6M parameters)
- **Modality:** Single-temporal Sentinel-2 L2A Top-of-Atmosphere RGB patches (128x128 pixels, 10m ground sampling distance).
- **License:** MIT License (with ESA WorldCover & Copernicus Sentinel attribution).

## Intended Use
- **Primary Domain:** Automated 10-meter land-cover patch classification over the Republic of Turkey across 8 canonical classes: `bare_sparse_vegetation`, `built_up`, `cropland`, `grassland`, `herbaceous_wetland`, `permanent_water_bodies`, `shrubland`, `tree_cover`.
- **Out of Scope:** Sub-meter aerial imagery, multi-spectral band inference beyond RGB, temporal time-series segmentation, or direct deployment outside Turkey without prior recalibration.
- **Operational Status:** Experimental research prototype. Not certified for critical cadastral or military surveying.

## Training & Initialization Details
- **Base Architecture:** YOLO11n-cls (Ultralytics).
- **Initialization:** ImageNet-pretrained weights (`/mnt/evren_data/cache/ultralytics/yolo11n-cls.pt`).
- **Optimization:** AdamW (lr0 = 0.001, lrf = 0.01, weight_decay = 0.0005, momentum = 0.9, 10 epochs, batch size 64).
- **Training Data:** 50,000 deterministically balanced Sentinel-2 patches across 67 Turkish provinces.

## Performance & Evaluation
- **Benchmark:** Evaluated strictly once on a geographically disjoint test set consisting of 68,558 physical patches across 7 held-out provinces (Artvin, Edirne, Mersin, Kars, Mardin, Muğla, Nevşehir).
- **Top-1 Accuracy:** 86.17% (59,076 / 68,558) [95% patch CI: 85.91%, 86.44%]
- **Macro-F1:** 0.6721 [95% patch CI: 0.6557, 0.6876]
- **Balanced Accuracy:** 73.98% [95% patch CI: 72.47%, 75.66%]
- **Worst-Class F1:** 0.4138 (Herbaceous wetland)
