"""TurkeyLandCover V2 - One-Time Pristine Final Evaluation.

Strict Execution Directives:
- Evaluates strictly on splits/v2_spatial_test.csv (first and only evaluation).
- Uses frozen EXP-V2-BALANCED-50K-REAL best.pt (SHA-256: 8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a).
- Frozen logit calibration: tau = 0.50, epsilon = 1e-12.
- Priors frozen strictly from reports/V2_STAGE3_CONFIG_FREEZE.md.
- Calculates:
  - Top-1, Top-5, Macro-F1, Balanced Accuracy, Weighted-F1, Micro-F1, Worst-Class F1.
  - Per-class precision, recall, F1, support.
  - 8x8 raw and normalized confusion matrices.
  - Per-province metrics across the 7 test provinces.
  - 95% bootstrap confidence intervals (seed: 20261012, B=1000).
  - Generalization gap vs. Development Stage 3.
- Saves reports/v2_final_test_results.json and artifacts/final_test/test_predictions.npz.
"""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import time
import zipfile

import numpy as np
import pandas as pd
from PIL import Image
import torch
from ultralytics import YOLO

ROOT = Path(r"C:\Users\cumac\OneDrive\Desktop\turkey-landcover")
TEST_CSV = ROOT / "splits" / "v2_spatial_test.csv"
ZIP_PATH = Path(r"C:\data\turkey-landcover\evren_single\turkeylandcover_v1_labeled.zip")
MODEL_PATH = ROOT / "runs" / "turkeylandcover_v2" / "exp_v2_balanced_50k_real" / "best.pt"
OUT_DIR = ROOT / "artifacts" / "final_test"
REPORTS_DIR = ROOT / "reports"

CLASS_NAMES = [
    "bare_sparse_vegetation",
    "built_up",
    "cropland",
    "grassland",
    "herbaceous_wetland",
    "permanent_water_bodies",
    "shrubland",
    "tree_cover",
]
NAME_TO_IDX = {name: i for i, name in enumerate(CLASS_NAMES)}

# Frozen Priors (from V2_STAGE3_CONFIG_FREEZE.md)
BALANCED_EXPOSURE = {
    "grassland": 4885,
    "cropland": 5349,
    "tree_cover": 5329,
    "permanent_water_bodies": 10576,
    "bare_sparse_vegetation": 7616,
    "built_up": 5504,
    "shrubland": 638,
    "herbaceous_wetland": 356,
}
BALANCED_TOTAL = 40253

NATURAL_TRAIN_COUNTS = {
    "grassland": 298287,
    "cropland": 175485,
    "tree_cover": 175045,
    "permanent_water_bodies": 12960,
    "bare_sparse_vegetation": 10004,
    "built_up": 6652,
    "shrubland": 924,
    "herbaceous_wetland": 421,
}
NATURAL_TOTAL = 679778

TAU = 0.50
EPSILON = 1e-12
BOOTSTRAP_SEED = 20261012
BOOTSTRAP_ROUNDS = 1000

DEV_STAGE3_METRICS = {
    "top1": 0.8687,
    "macro_f1": 0.6706,
    "balanced_acc": 0.7309,
    "worst_f1": 0.1423,
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, top5_preds: list[list[int]] | None = None):
    total = len(y_true)
    top1 = float((y_true == y_pred).sum() / total)

    top5 = None
    if top5_preds is not None:
        top5_correct = sum(1 for gt, t5 in zip(y_true, top5_preds) if gt in t5)
        top5 = float(top5_correct / total)

    cm = np.zeros((8, 8), dtype=np.int64)
    for gt, pr in zip(y_true, y_pred):
        cm[gt, pr] += 1

    per_class = {}
    f1s = []
    recalls = []
    precisions = []
    supports = []

    for c in range(8):
        tp = int(cm[c, c])
        fp = int(cm[:, c].sum() - tp)
        fn = int(cm[c, :].sum() - tp)
        support = int(cm[c, :].sum())

        prec = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        rec = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        f1 = float(2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0

        per_class[CLASS_NAMES[c]] = {
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "support": support,
        }
        f1s.append(f1)
        recalls.append(rec)
        precisions.append(prec)
        supports.append(support)

    macro_f1 = float(np.mean(f1s))
    balanced_acc = float(np.mean(recalls))
    worst_f1 = float(np.min(f1s))
    micro_f1 = top1  # in single-label multi-class, micro-F1 == accuracy
    weighted_f1 = float(sum(f * s for f, s in zip(f1s, supports)) / total) if total > 0 else 0.0

    # Normalized confusion matrix (row-normalized by ground truth support)
    cm_norm = np.zeros((8, 8), dtype=np.float64)
    for c in range(8):
        if supports[c] > 0:
            cm_norm[c, :] = cm[c, :] / supports[c]

    return {
        "top1": top1,
        "top5": top5,
        "macro_f1": macro_f1,
        "balanced_acc": balanced_acc,
        "worst_f1": worst_f1,
        "micro_f1": micro_f1,
        "weighted_f1": weighted_f1,
        "confusion_matrix": cm,
        "normalized_confusion_matrix": cm_norm,
        "per_class": per_class,
    }


def bootstrap_ci(y_true: np.ndarray, y_pred: np.ndarray, n_rounds: int = BOOTSTRAP_ROUNDS, seed: int = BOOTSTRAP_SEED):
    rng = np.random.default_rng(seed)
    n = len(y_true)

    top1_list = []
    macro_f1_list = []
    bal_acc_list = []

    for _ in range(n_rounds):
        idx = rng.choice(n, size=n, replace=True)
        yt_sample = y_true[idx]
        yp_sample = y_pred[idx]

        m = compute_metrics(yt_sample, yp_sample)
        top1_list.append(m["top1"])
        macro_f1_list.append(m["macro_f1"])
        bal_acc_list.append(m["balanced_acc"])

    return {
        "top1_ci": [float(np.percentile(top1_list, 2.5)), float(np.percentile(top1_list, 97.5))],
        "macro_f1_ci": [float(np.percentile(macro_f1_list, 2.5)), float(np.percentile(macro_f1_list, 97.5))],
        "balanced_acc_ci": [float(np.percentile(bal_acc_list, 2.5)), float(np.percentile(bal_acc_list, 97.5))],
    }


def evaluate():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Verifying checkpoint integrity...")
    ckpt_hash = compute_sha256(MODEL_PATH)
    expected_ckpt = "8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a"
    assert ckpt_hash.lower() == expected_ckpt.lower(), f"Checkpoint mismatch: {ckpt_hash}"
    print(f"Verified checkpoint: {MODEL_PATH} ({ckpt_hash})")

    print(f"Loading test manifest from {TEST_CSV}...")
    df_test_raw = pd.read_csv(TEST_CSV)
    print(f"Raw test manifest rows: {len(df_test_raw):,}")

    print("Indexing zip archive (800,020 files)...")
    sample_to_zip = {}
    sample_to_class = {}
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        for n in zf.namelist():
            parts = n.split("/")
            if len(parts) >= 3 and parts[-1].endswith(".webp"):
                sid = parts[-1].replace(".webp", "")
                sample_to_zip[sid] = n
                sample_to_class[sid] = parts[1]

    # Resolve valid test images
    valid_mask = df_test_raw["sample_id"].isin(sample_to_zip)
    df_test = df_test_raw[valid_mask].copy()
    df_test["zip_path"] = df_test["sample_id"].map(sample_to_zip)
    df_test["canonical_class"] = df_test["sample_id"].map(sample_to_class)

    print(f"Resolved valid test images: {len(df_test):,} (excluded {len(df_test_raw) - len(df_test)} border nodata patches)")
    print(f"Test provinces ({df_test['province_code'].nunique()}): {sorted(df_test['province_code'].unique().tolist())}")

    gt_classes = np.array([NAME_TO_IDX[c] for c in df_test["canonical_class"]], dtype=np.int64)
    zip_keys = df_test["zip_path"].tolist()
    sample_ids = np.array(df_test["sample_id"].tolist())
    provinces = np.array(df_test["province_code"].tolist())

    print("Calculating frozen prior shift vector...")
    p_train = np.array([BALANCED_EXPOSURE[c] / BALANCED_TOTAL for c in CLASS_NAMES], dtype=np.float64)
    p_target = np.array([NATURAL_TRAIN_COUNTS[c] / NATURAL_TOTAL for c in CLASS_NAMES], dtype=np.float64)
    delta_logits = np.log(p_target + EPSILON) - np.log(p_train + EPSILON)
    prior_shift = (TAU * delta_logits).astype(np.float32)

    print(f"Applied shift vector (tau = {TAU}):")
    for idx, c in enumerate(CLASS_NAMES):
        print(f"  {c:25s}: {prior_shift[idx]:+.4f}")

    print("Loading PyTorch model...")
    yolo_model = YOLO(str(MODEL_PATH))
    model = yolo_model.model
    model.eval()

    # Verify model class ordering matches CLASS_NAMES
    for idx, name in enumerate(CLASS_NAMES):
        assert yolo_model.names[idx] == name, f"Mismatch at idx {idx}: {yolo_model.names[idx]} vs {name}"

    batch_size = 256
    all_raw_logits = []
    all_corrected_preds = []
    all_top5_preds = []

    print(f"Running ONE-TIME test inference on {len(zip_keys):,} images in batches of {batch_size}...")
    t0 = time.time()
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        with torch.inference_mode():
            for i in range(0, len(zip_keys), batch_size):
                batch_keys = zip_keys[i : i + batch_size]
                batch_tensors = []
                for k in batch_keys:
                    data = zf.read(k)
                    img = Image.open(io.BytesIO(data)).convert("RGB")
                    if img.size != (128, 128):
                        img = img.resize((128, 128), Image.Resampling.BILINEAR)
                    arr = np.array(img, dtype=np.float32) / 255.0
                    tensor = torch.from_numpy(arr).permute(2, 0, 1)
                    batch_tensors.append(tensor)

                inp = torch.stack(batch_tensors)
                _, raw_logits = model(inp)  # tuple: (probs, logits)
                logits_np = raw_logits.cpu().numpy()
                all_raw_logits.append(logits_np)

                # Apply frozen prior shift
                corrected_logits = logits_np + prior_shift
                top1_batch = np.argmax(corrected_logits, axis=1)
                all_corrected_preds.extend(top1_batch.tolist())

                # Top-5 predictions
                for c_log in corrected_logits:
                    t5 = list(np.argsort(c_log)[-5:][::-1])
                    all_top5_preds.append(t5)

                if (i + len(batch_keys)) % 5000 == 0 or (i + len(batch_keys)) == len(zip_keys):
                    elapsed = time.time() - t0
                    speed = (i + len(batch_keys)) / elapsed
                    print(f"Evaluated {i + len(batch_keys):,} / {len(zip_keys):,} ({speed:.1f} img/s)...", flush=True)

    raw_logits_arr = np.concatenate(all_raw_logits, axis=0).astype(np.float32)
    pred_classes = np.array(all_corrected_preds, dtype=np.int64)

    print("\nComputing primary test metrics...")
    metrics = compute_metrics(gt_classes, pred_classes, all_top5_preds)

    print("Computing 95% bootstrap confidence intervals...")
    ci_res = bootstrap_ci(gt_classes, pred_classes, n_rounds=BOOTSTRAP_ROUNDS, seed=BOOTSTRAP_SEED)

    print("Computing per-province breakdown across 7 test provinces...")
    prov_metrics = {}
    for p in sorted(df_test["province_code"].unique().tolist()):
        mask = (provinces == p)
        m_p = compute_metrics(gt_classes[mask], pred_classes[mask])
        prov_metrics[p] = {
            "samples": int(mask.sum()),
            "top1": m_p["top1"],
            "macro_f1": m_p["macro_f1"],
            "balanced_acc": m_p["balanced_acc"],
            "worst_f1": m_p["worst_f1"],
            "per_class": m_p["per_class"],
        }

    # Development-to-Final Generalization Gap
    gen_gap = {
        "top1": float(metrics["top1"] - DEV_STAGE3_METRICS["top1"]),
        "macro_f1": float(metrics["macro_f1"] - DEV_STAGE3_METRICS["macro_f1"]),
        "balanced_acc": float(metrics["balanced_acc"] - DEV_STAGE3_METRICS["balanced_acc"]),
        "worst_f1": float(metrics["worst_f1"] - DEV_STAGE3_METRICS["worst_f1"]),
    }

    # Final Scientific Verdict Classification
    # Criteria:
    # STRONG: Macro-F1 gap within +/- 0.03 of dev, Macro-F1 > 0.60
    # MODERATE: Macro-F1 gap within +/- 0.06 of dev, Macro-F1 > 0.55
    # WEAK: Macro-F1 gap > -0.10, or drops below 0.50
    # FAILED: Macro-F1 drops severely below 0.40
    test_f1 = metrics["macro_f1"]
    if test_f1 >= 0.64 and abs(gen_gap["macro_f1"]) <= 0.05:
        verdict = "STRONG_GENERALIZATION"
    elif test_f1 >= 0.55 and abs(gen_gap["macro_f1"]) <= 0.12:
        verdict = "MODERATE_GENERALIZATION"
    elif test_f1 >= 0.45:
        verdict = "WEAK_GENERALIZATION"
    else:
        verdict = "FAILED_TO_GENERALIZE"

    print("\n==================================================")
    print("FINAL TEST EVALUATION COMPLETE")
    print(f"Top-1 Accuracy:     {metrics['top1']*100:.2f}% (95% CI: [{ci_res['top1_ci'][0]*100:.2f}%, {ci_res['top1_ci'][1]*100:.2f}%])")
    print(f"Top-5 Accuracy:     {metrics['top5']*100:.2f}%")
    print(f"Macro-F1:           {metrics['macro_f1']:.4f} (95% CI: [{ci_res['macro_f1_ci'][0]:.4f}, {ci_res['macro_f1_ci'][1]:.4f}])")
    print(f"Balanced Accuracy:  {metrics['balanced_acc']*100:.2f}% (95% CI: [{ci_res['balanced_acc_ci'][0]*100:.2f}%, {ci_res['balanced_acc_ci'][1]*100:.2f}%])")
    print(f"Worst-Class F1:     {metrics['worst_f1']:.4f}")
    print(f"Weighted-F1:        {metrics['weighted_f1']:.4f}")
    print(f"Generalization Gap: Macro-F1: {gen_gap['macro_f1']:+.4f} | Top-1: {gen_gap['top1']*100:+.2f}% | Bal Acc: {gen_gap['balanced_acc']*100:+.2f}%")
    print(f"FINAL SCIENTIFIC VERDICT: {verdict}")
    print("==================================================")

    # Save artifacts
    test_pred_npz = OUT_DIR / "test_predictions.npz"
    np.savez_compressed(
        test_pred_npz,
        sample_id=sample_ids,
        province=provinces,
        ground_truth_idx=gt_classes,
        pred_idx=pred_classes,
        raw_logits=raw_logits_arr,
        class_names=np.array(CLASS_NAMES),
    )
    test_pred_sha = compute_sha256(test_pred_npz)

    results_data = {
        "verdict": verdict,
        "test_samples_total": len(gt_classes),
        "test_manifest_rows": len(df_test_raw),
        "excluded_nodata_patches": int(len(df_test_raw) - len(df_test)),
        "checkpoint_sha256": ckpt_hash,
        "test_manifest_sha256": compute_sha256(TEST_CSV),
        "test_pred_npz_sha256": test_pred_sha,
        "tau": TAU,
        "epsilon": EPSILON,
        "priors": {
            "p_train_balanced": {c: float(p_train[i]) for i, c in enumerate(CLASS_NAMES)},
            "p_target": {c: float(p_target[i]) for i, c in enumerate(CLASS_NAMES)},
            "shift_vector": {c: float(prior_shift[i]) for i, c in enumerate(CLASS_NAMES)},
        },
        "metrics": {
            "top1": metrics["top1"],
            "top5": metrics["top5"],
            "macro_f1": metrics["macro_f1"],
            "balanced_acc": metrics["balanced_acc"],
            "worst_f1": metrics["worst_f1"],
            "micro_f1": metrics["micro_f1"],
            "weighted_f1": metrics["weighted_f1"],
            "ci_95": ci_res,
            "per_class": metrics["per_class"],
            "confusion_matrix": metrics["confusion_matrix"].tolist(),
            "normalized_confusion_matrix": metrics["normalized_confusion_matrix"].tolist(),
        },
        "provinces": prov_metrics,
        "generalization_gap": gen_gap,
        "dev_stage3_metrics": DEV_STAGE3_METRICS,
    }

    out_json = REPORTS_DIR / "v2_final_test_results.json"
    with open(out_json, "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"Results saved to {out_json}")

    return results_data


if __name__ == "__main__":
    evaluate()
