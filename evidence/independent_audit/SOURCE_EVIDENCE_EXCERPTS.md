# Kaynak dosya alıntıları

Bunlar ZIP içindeki dosyalardan değiştirilmeden alınmıştır. Kodlar bu denetimde çalıştırılmamıştır.

## configs/v2_50k_frozen.yaml — satır 1–55

```text
1: # TurkeyLandCover V2 50K Frozen Experiment Configuration
2: # Platform: EVREN Public Infrastructure (Zero-Cost / Free Tier)
3: # Model Architecture: YOLO11n-cls (Ultralytics Stock Classification)
4: 
5: experiment_version: "V2_50K_SCIENTIFIC_GATE"
6: date_frozen: "2026-10-11T23:56:00+03:00"
7: 
8: model:
9:   architecture: "yolo11n-cls"
10:   num_classes: 8
11:   input_resolution: 128
12:   pretrained: false
13: 
14: dataset:
15:   parent_dataset_id: "01a11f3a-d114-7922-941b-9e16cd50dea9"
16:   dataset_size: 50000
17:   image_size: 128
18:   num_classes: 8
19:   class_names:
20:     - bare_sparse_vegetation
21:     - built_up
22:     - cropland
23:     - grassland
24:     - herbaceous_wetland
25:     - permanent_water_bodies
26:     - shrubland
27:     - tree_cover
28: 
29:   registered_versions:
30:     natural_train:
31:       tag: "v2-natural-train-50k"
32:       id: "01a12cb1-15b2-7380-9fd8-9d03e48be105"
33:       server_count: 50000
34:       local_csv: "splits/v2_natural_matched_50k.csv"
35:       sha256: "1e73fe657a82412a6ff4d79dbf37bb1ba9501690b1967e1ad533239e42cb71fc"
36: 
37:     balanced_train:
38:       tag: "v2-balanced-train-50k"
39:       id: "01a12cb1-05c8-7c80-b321-2c51ae68b55a"
40:       server_count: 50000
41:       local_csv: "splits/v2_balanced_train_50k.csv"
42:       sha256: "0264a961a75ee74ecdc06c8fe638682dd0708edd9f73e08c5222b6870ffbfa32"
43: 
44:     validation:
45:       tag: "v2-spatial-val-50k"
46:       id: "01a12cb1-223a-7aa0-8ae3-ef298f874b60"
47:       server_count: 50000
48:       local_csv: "splits/v2_spatial_val_50k_fixed.csv"
49:       sha256: "2a8d29be49c6887094ec8c53f949fdec5b377ee5b11491a7b2884114f601749f"
50: 
51:     sealed_test:
52:       local_csv: "splits/v2_spatial_test.csv"
53:       sha256: "6e08a98f777bc3de0c4cb357aa6a21c5d57f880aff8b79a9b09f3a2e55d02171"
54:       status: "SEALED_PRISTINE"
55: 
```

## metadata_and_splits/v2_evren_dataset_versions.json — satır 1–20

```text
1: {
2:   "V2_BALANCED_TRAIN": {
3:     "version_id": null,
4:     "version_tag": "v2-balanced-train",
5:     "item_count": null,
6:     "status_code": 422
7:   },
8:   "V2_NATURAL_TRAIN": {
9:     "version_id": null,
10:     "version_tag": "v2-natural-train",
11:     "item_count": null,
12:     "status_code": 422
13:   },
14:   "V2_SPATIAL_VAL": {
15:     "version_id": null,
16:     "version_tag": "v2-spatial-val",
17:     "item_count": null,
18:     "status_code": 422
19:   }
20: }
```

## scripts/evaluate_v2_final_test.py — satır 175–225

```text
175:         yp_sample = y_pred[idx]
176: 
177:         m = compute_metrics(yt_sample, yp_sample)
178:         top1_list.append(m["top1"])
179:         macro_f1_list.append(m["macro_f1"])
180:         bal_acc_list.append(m["balanced_acc"])
181: 
182:     return {
183:         "top1_ci": [float(np.percentile(top1_list, 2.5)), float(np.percentile(top1_list, 97.5))],
184:         "macro_f1_ci": [float(np.percentile(macro_f1_list, 2.5)), float(np.percentile(macro_f1_list, 97.5))],
185:         "balanced_acc_ci": [float(np.percentile(bal_acc_list, 2.5)), float(np.percentile(bal_acc_list, 97.5))],
186:     }
187: 
188: 
189: def evaluate():
190:     OUT_DIR.mkdir(parents=True, exist_ok=True)
191: 
192:     print("Verifying checkpoint integrity...")
193:     ckpt_hash = compute_sha256(MODEL_PATH)
194:     expected_ckpt = "8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a"
195:     assert ckpt_hash.lower() == expected_ckpt.lower(), f"Checkpoint mismatch: {ckpt_hash}"
196:     print(f"Verified checkpoint: {MODEL_PATH} ({ckpt_hash})")
197: 
198:     print(f"Loading test manifest from {TEST_CSV}...")
199:     df_test_raw = pd.read_csv(TEST_CSV)
200:     print(f"Raw test manifest rows: {len(df_test_raw):,}")
201: 
202:     print("Indexing zip archive (800,020 files)...")
203:     sample_to_zip = {}
204:     sample_to_class = {}
205:     with zipfile.ZipFile(ZIP_PATH, "r") as zf:
206:         for n in zf.namelist():
207:             parts = n.split("/")
208:             if len(parts) >= 3 and parts[-1].endswith(".webp"):
209:                 sid = parts[-1].replace(".webp", "")
210:                 sample_to_zip[sid] = n
211:                 sample_to_class[sid] = parts[1]
212: 
213:     # Resolve valid test images
214:     valid_mask = df_test_raw["sample_id"].isin(sample_to_zip)
215:     df_test = df_test_raw[valid_mask].copy()
216:     df_test["zip_path"] = df_test["sample_id"].map(sample_to_zip)
217:     df_test["canonical_class"] = df_test["sample_id"].map(sample_to_class)
218: 
219:     print(f"Resolved valid test images: {len(df_test):,} (excluded {len(df_test_raw) - len(df_test)} border nodata patches)")
220:     print(f"Test provinces ({df_test['province_code'].nunique()}): {sorted(df_test['province_code'].unique().tolist())}")
221: 
222:     gt_classes = np.array([NAME_TO_IDX[c] for c in df_test["canonical_class"]], dtype=np.int64)
223:     zip_keys = df_test["zip_path"].tolist()
224:     sample_ids = np.array(df_test["sample_id"].tolist())
225:     provinces = np.array(df_test["province_code"].tolist())
```

## scripts/evaluate_v2_final_test.py — satır 245–280

```text
245: 
246:     batch_size = 256
247:     all_raw_logits = []
248:     all_corrected_preds = []
249:     all_top5_preds = []
250: 
251:     print(f"Running ONE-TIME test inference on {len(zip_keys):,} images in batches of {batch_size}...")
252:     t0 = time.time()
253:     with zipfile.ZipFile(ZIP_PATH, "r") as zf:
254:         with torch.inference_mode():
255:             for i in range(0, len(zip_keys), batch_size):
256:                 batch_keys = zip_keys[i : i + batch_size]
257:                 batch_tensors = []
258:                 for k in batch_keys:
259:                     data = zf.read(k)
260:                     img = Image.open(io.BytesIO(data)).convert("RGB")
261:                     if img.size != (128, 128):
262:                         img = img.resize((128, 128), Image.Resampling.BILINEAR)
263:                     arr = np.array(img, dtype=np.float32) / 255.0
264:                     tensor = torch.from_numpy(arr).permute(2, 0, 1)
265:                     batch_tensors.append(tensor)
266: 
267:                 inp = torch.stack(batch_tensors)
268:                 _, raw_logits = model(inp)  # tuple: (probs, logits)
269:                 logits_np = raw_logits.cpu().numpy()
270:                 all_raw_logits.append(logits_np)
271: 
272:                 # Apply frozen prior shift
273:                 corrected_logits = logits_np + prior_shift
274:                 top1_batch = np.argmax(corrected_logits, axis=1)
275:                 all_corrected_preds.extend(top1_batch.tolist())
276: 
277:                 # Top-5 predictions
278:                 for c_log in corrected_logits:
279:                     t5 = list(np.argsort(c_log)[-5:][::-1])
280:                     all_top5_preds.append(t5)
```

## scripts/run_stage3_prior_correction.py — satır 116–145

```text
116:         "worst_f1": worst_f1,
117:         "confusion_matrix": cm,
118:         "per_class": per_class,
119:     }
120: 
121: 
122: def compute_province_macro_f1(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int = 8, active_only: bool = True):
123:     cm = np.zeros((num_classes, num_classes), dtype=np.int64)
124:     for gt, pr in zip(y_true, y_pred):
125:         cm[gt, pr] += 1
126: 
127:     f1s = []
128:     for c in range(num_classes):
129:         tp = int(cm[c, c])
130:         fp = int(cm[:, c].sum() - tp)
131:         fn = int(cm[c, :].sum() - tp)
132:         support = int(cm[c, :].sum())
133: 
134:         if active_only and support == 0:
135:             continue
136: 
137:         prec = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
138:         rec = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
139:         f1 = float(2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
140:         f1s.append(f1)
141: 
142:     return float(np.mean(f1s)) if len(f1s) > 0 else 0.0
143: 
144: 
145: def run():
```

## scripts/run_stage3_prior_correction.py — satır 175–243

```text
175:         preds = np.argmax(corrected_logits, axis=1)
176: 
177:         # Full validation set metrics
178:         global_m = compute_metrics(gt_idx, preds)
179: 
180:         # Per-province Macro-F1
181:         prov_f1s_active = {}
182:         prov_f1s_all8 = {}
183:         for p in unique_provinces:
184:             mask = (provinces == p)
185:             y_p = gt_idx[mask]
186:             pred_p = preds[mask]
187:             prov_f1s_active[p] = compute_province_macro_f1(y_p, pred_p, active_only=True)
188:             prov_f1s_all8[p] = compute_province_macro_f1(y_p, pred_p, active_only=False)
189: 
190:         mean_prov_macro_f1_active = float(np.mean(list(prov_f1s_active.values())))
191:         mean_prov_macro_f1_all8 = float(np.mean(list(prov_f1s_all8.values())))
192: 
193:         # Leave-One-Province-Out (LOPO) cross-validation evaluation:
194:         # For each province p, determine which tau would have been selected based on the other 6 provinces
195:         # We record the other-6 mean for later LOPO simulation
196:         other6_means = {}
197:         for p in unique_provinces:
198:             other6 = [prov_f1s_active[p_other] for p_other in unique_provinces if p_other != p]
199:             other6_means[p] = float(np.mean(other6))
200: 
201:         results_by_tau[tau] = {
202:             "tau": tau,
203:             "global_metrics": global_m,
204:             "prov_f1s_active": prov_f1s_active,
205:             "prov_f1s_all8": prov_f1s_all8,
206:             "mean_prov_macro_f1_active": mean_prov_macro_f1_active,
207:             "mean_prov_macro_f1_all8": mean_prov_macro_f1_all8,
208:             "other6_means": other6_means,
209:         }
210: 
211:         print(
212:             f"tau = {tau:4.2f} | "
213:             f"Top-1: {global_m['top1']*100:6.2f}% | "
214:             f"Global Macro-F1: {global_m['macro_f1']:6.4f} | "
215:             f"Mean Prov Macro-F1: {mean_prov_macro_f1_active:6.4f} | "
216:             f"Balanced Acc: {global_m['balanced_acc']*100:6.2f}% | "
217:             f"Worst F1: {global_m['worst_f1']:6.4f} | "
218:             f"Shrubland F1: {global_m['per_class']['shrubland']['f1']:6.4f} | "
219:             f"Wetland F1: {global_m['per_class']['herbaceous_wetland']['f1']:6.4f}"
220:         )
221: 
222:     # LOPO Cross-Validation Simulation:
223:     # For each province p: choose tau that maximizes other6_means[p], then measure on p
224:     print("\n--- Leave-One-Province-Out (LOPO) Cross-Validation Analysis ---")
225:     lopo_results = {}
226:     for p in unique_provinces:
227:         best_tau_for_p = max(TAU_GRID, key=lambda t: results_by_tau[t]["other6_means"][p])
228:         test_score = results_by_tau[best_tau_for_p]["prov_f1s_active"][p]
229:         lopo_results[p] = {"selected_tau": best_tau_for_p, "held_out_macro_f1": test_score}
230:         print(f"Held out {p:5s} | Selected tau on other 6: {best_tau_for_p:4.2f} | Held-out Macro-F1: {test_score:6.4f}")
231: 
232:     # Primary Selection Rule:
233:     # "Use the frozen primary selection criterion: MEAN PROVINCE MACRO-F1"
234:     # Tie breakers: 1. Worst-Class F1, 2. Balanced Accuracy, 3. Top-1 Accuracy
235:     def selection_key(t):
236:         r = results_by_tau[t]
237:         return (
238:             r["mean_prov_macro_f1_active"],
239:             r["global_metrics"]["worst_f1"],
240:             r["global_metrics"]["balanced_acc"],
241:             r["global_metrics"]["top1"],
242:         )
243: 
```

## results/FINAL_PUBLICATION_CONSISTENCY_AUDIT.md — satır 75–85

```text
75: ## 4. Resolution of Issue 4: Bootstrap Confidence Interval Methodology & Clustering
76: 
77: ### Audit of Bootstrap Implementation:
78: - **Algorithm:** Non-parametric empirical bootstrap resampling ($B = 1,000$ iterations, seed `20261012`) drawing $N = 68,558$ patches with replacement.
79: - **Methodological Limitation:** This procedure treats image patches as **independent and identically distributed (i.i.d.)**. It **does NOT account for spatial clustering** within the 7 holdout provinces.
80: - **Scientific Reality:** Because samples within the same province share local topography, microclimates, and satellite acquisition dates, the effective degrees of freedom are governed primarily by the $7$ held-out clusters, not $68,558$ independent points.
81: - **Reporting Standard:** The reported 95% confidence intervals (Top-1: `[85.91%, 86.44%]`, Macro-F1: `[0.6557, 0.6876]`) represent **patch-level empirical sampling variation conditional on the 7 evaluated provinces**, not out-of-sample geographical uncertainty across the remaining 74 provinces of Turkey.
82: 
83: ---
84: 
85: ## 5. Resolution of Issue 5: Reproducibility Manifest & Artifact Integrity
```
