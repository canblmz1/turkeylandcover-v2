# Upstream Citations & Attribution Notices

TurkeyLandCover V2 is a derived research project. It combines satellite data products, open datasets, and open-source machine learning software. It is not produced, endorsed, or validated by ESA, the ESA WorldCover consortium, the European Commission, SSB, EVREN, or Ultralytics.

---

## 1. Satellite Imagery and Map Annotations (CC BY 4.0)

**Mandatory Upstream Notices (verbatim):**

> © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium

> Contains modified Copernicus Sentinel data 2021

- **Upstream License:** Creative Commons Attribution 4.0 International (CC BY 4.0), [https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)
- **Adaptation Notice (CC BY 4.0 §3(a)(1)(B)):**
  - Divided into 120×120 pixel patches on the native 0.01° grid.
  - Surface reflectance bands B04 (Red), B03 (Green), B02 (Blue) linearly stretched (0–0.30) to 8-bit RGB WebP format.
  - Land cover class masks remapped to canonical 8-class system.
  - Patches with >1% nodata excluded.
  - Restricted to geographic boundaries intersecting the Republic of Türkiye.

**Data Citations:**
- Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., Brockmann, C., Kirches, G., Wevers, J., Cartus, O., Santoro, M., Fritz, S., Lesiv, M., Herold, M., Tsendbazar, N.E., Xu, P., Ramoino, F., Arino, O. (2022). *ESA WorldCover 10 m 2021 v200*. Zenodo. [https://doi.org/10.5281/zenodo.7254221](https://doi.org/10.5281/zenodo.7254221)
- *ESA WorldCover Sentinel-1 and Sentinel-2 10 m annual composites 2021*, Registry of Open Data on AWS, [https://registry.opendata.aws/esa-worldcover-vito-composites/](https://registry.opendata.aws/esa-worldcover-vito-composites/)
- *European Commission DG GROW Sentinel Data Legal Notice*, Regulation (EU) No 377/2014 and Delegated Regulation (EU) No 1159/2013.

---

## 2. Geographic Boundaries (Public Domain)

- **Source:** Natural Earth 1:10m Cultural Boundaries (Admin 1 – States, Provinces, v5.1.1).
- **License:** Public Domain ([https://www.naturalearthdata.com/about/terms-of-use/](https://www.naturalearthdata.com/about/terms-of-use/)).
- **Disclaimer:** Natural Earth boundaries represent de facto borders. Boundaries are used solely for spatial sampling and province tagging; no geopolitical claims are made.

---

## 3. Deep Learning Framework & Model Architecture (GNU AGPL-3.0)

- **Software:** Ultralytics YOLO11 (`yolo11n-cls`, framework version `8.3.0`).
- **Copyright:** Copyright © 2020-2026 Glenn Jocher and Ultralytics Inc.
- **License:** GNU Affero General Public License v3.0 (GNU AGPL-3.0).
- **Source Repository:** [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) (Pinned release: `v8.3.0`).
- **Citation:**
  - Jocher, G., Qiu, J., et al. (2024). *Ultralytics YOLO*. [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)
