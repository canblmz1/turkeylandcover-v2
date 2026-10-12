"""Verify a TurkeyLandCover V2 review package without model execution.

Uses only the standard library for hashes and NumPy for saved-array arithmetic.
No network, torch.load, model inference, training, file writes or tau search.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def verify_hashes(root: Path) -> dict:
    entries = []
    for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        require(len(expected) == 64 and all(c in "0123456789abcdef" for c in expected), "Invalid SHA entry")
        require(relative not in entries, f"Duplicate manifest entry: {relative}")
        path = (root / relative).resolve()
        require(root in path.parents, f"Unsafe manifest path: {relative}")
        require(path.is_file(), f"Missing file: {relative}")
        require(file_hash(path) == expected, f"Hash mismatch: {relative}")
        entries.append(relative)
    actual = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and not any(part.startswith(".") for part in p.relative_to(root).parts)
    }
    require(set(entries) == actual - {"SHA256SUMS.txt"}, "File coverage differs from hash manifest")
    return {"listed_files": len(entries), "matching_files": len(entries), "complete_coverage": True}


def verify_saved_predictions(root: Path) -> dict:
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("NumPy is required for saved-array checks; --hashes-only needs no NumPy.") from exc

    cfg = read_json(root / "config/calibration_config.json")
    recorded = read_json(root / "results/v2_final_test_results.json")
    names = cfg["class_names"]
    require(len(names) == 8 and len(set(names)) == 8, "Invalid frozen class order")
    require(cfg["tau"] == 0.50 and cfg["epsilon"] == 1e-12, "Frozen scalar mismatch")
    model_file = root / "model/best.pt"
    if model_file.is_file():
        require(file_hash(model_file) == cfg["checkpoint_sha256"], "Checkpoint identity mismatch")
    require(file_hash(root / "predictions/test_predictions.npz") == recorded["test_pred_npz_sha256"], "Prediction identity mismatch")

    with np.load(root / "predictions/test_predictions.npz", allow_pickle=False) as arrays:
        require(set(arrays.files) == {"sample_id", "province", "ground_truth_idx", "pred_idx", "raw_logits", "class_names"}, "Unexpected NPZ schema")
        sid = arrays["sample_id"].copy()
        provinces = arrays["province"].copy()
        gt = arrays["ground_truth_idx"].copy()
        pred = arrays["pred_idx"].copy()
        logits = arrays["raw_logits"].copy()
        require(arrays["class_names"].tolist() == names, "NPZ class-order mismatch")
    n = len(gt)
    require(n == recorded["test_samples_total"] == 68558, "Sample count mismatch")
    require(len(sid) == len(provinces) == len(pred) == n and logits.shape == (n, 8), "Array shape mismatch")
    require(np.issubdtype(gt.dtype, np.integer) and np.issubdtype(pred.dtype, np.integer), "Noninteger labels")
    require(bool(np.all((gt >= 0) & (gt < 8))) and bool(np.all((pred >= 0) & (pred < 8))), "Out-of-range labels")
    require(len(np.unique(sid)) == n, "Duplicate test sample IDs")
    require(bool(np.isfinite(logits).all()), "Nonfinite saved logits")

    pt = np.asarray([cfg["p_target"][c] for c in names], dtype=np.float64)
    pb = np.asarray([cfg["p_train_balanced"][c] for c in names], dtype=np.float64)
    require(bool(np.all(pt > 0)) and bool(np.all(pb > 0)), "Nonpositive prior")
    require(abs(float(pt.sum()) - 1) < 1e-12 and abs(float(pb.sum()) - 1) < 1e-12, "Prior normalization mismatch")
    expected_shift = (cfg["tau"] * (np.log(pt + cfg["epsilon"]) - np.log(pb + cfg["epsilon"]))).astype(np.float32)
    supplied_shift = np.asarray([cfg["prior_shift_vector"][c] for c in names], dtype=np.float32)
    require(bool(np.array_equal(expected_shift, supplied_shift)), "Frozen shift mismatch")
    # The stored shift already includes tau. Do not apply tau again.
    corrected = logits + supplied_shift
    reproduced_pred = np.argmax(corrected, axis=1)
    mismatch = int(np.count_nonzero(reproduced_pred != pred))
    require(mismatch == 0, f"Frozen correction disagrees with {mismatch} saved predictions")

    def metrics(y, p):
        cm = np.bincount(y * 8 + p, minlength=64).reshape(8, 8)
        support = cm.sum(axis=1)
        predicted = cm.sum(axis=0)
        tp = np.diag(cm)
        precision = np.divide(tp, predicted, out=np.zeros(8, dtype=float), where=predicted > 0)
        recall = np.divide(tp, support, out=np.zeros(8, dtype=float), where=support > 0)
        f1 = np.divide(2*tp, support + predicted, out=np.zeros(8, dtype=float), where=(support+predicted) > 0)
        present = support > 0
        return cm, support, precision, recall, f1, present

    cm, support, precision, recall, f1, present = metrics(gt, pred)
    top5 = np.argsort(corrected, axis=1)[:, -5:]
    top5_correct = int(np.count_nonzero(np.any(top5 == gt[:, None], axis=1)))
    calculated = {
        "top1": float(np.trace(cm) / n), "top5": top5_correct / n,
        "macro_f1": float(f1.mean()), "balanced_acc": float(recall.mean()),
        "worst_f1": float(f1.min()), "micro_f1": float(np.trace(cm) / n),
        "weighted_f1": float(np.sum(f1 * support) / n),
    }
    for key, value in calculated.items():
        require(abs(value - recorded["metrics"][key]) < 1e-12, f"Metric mismatch: {key}")
    require(np.array_equal(cm, recorded["metrics"]["confusion_matrix"]), "JSON confusion matrix mismatch")
    with (root / "results/confusion_matrix_raw.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    require(rows[0][1:] == names and [row[0] for row in rows[1:]] == names, "CSV class-order mismatch")
    require(np.array_equal(cm, np.asarray([row[1:] for row in rows[1:]], dtype=np.int64)), "CSV confusion matrix mismatch")
    for i, c in enumerate(names):
        ref = recorded["metrics"]["per_class"][c]
        require(int(support[i]) == ref["support"], f"Class support mismatch: {c}")
        for k, v in (("precision", precision[i]), ("recall", recall[i]), ("f1", f1[i])):
            require(abs(float(v) - ref[k]) < 1e-12, f"Class metric mismatch: {c}/{k}")

    with (root / "results/province_metrics_test.csv").open(encoding="utf-8-sig", newline="") as f:
        saved_provinces = {row["province_code"]: row for row in csv.DictReader(f)}
    require(set(np.unique(provinces)) == set(saved_provinces), "Province membership mismatch")
    per_province = {}
    for code in sorted(saved_provinces):
        mask = provinces == code
        pc, ps, pp, pr, pf, present = metrics(gt[mask], pred[mask])
        row = saved_provinces[code]
        calculated_row = {
            "samples": int(mask.sum()), "correct": int(np.trace(pc)),
            "top1_accuracy": float(np.trace(pc)/mask.sum()),
            "present_classes_count": int(present.sum()), "absent_classes_count": int((~present).sum()),
            "macro_f1_present_only": float(pf[present].mean()), "macro_f1_all8_classes": float(pf.mean()),
            "balanced_accuracy_present": float(pr[present].mean()),
            "worst_class_f1_present": float(pf[present].min()), "worst_class_f1_all8": float(pf.min()),
        }
        for k,v in calculated_row.items():
            require(abs(v-float(row[k])) < 1e-12, f"Province metric mismatch: {code}/{k}")
        per_province[code] = calculated_row

    with (root / "metadata_and_splits/v2_spatial_test.csv").open(encoding="utf-8-sig", newline="") as f:
        test_rows = list(csv.DictReader(f))
    mapping = {row["sample_id"]: row["province_code"] for row in test_rows}
    require(len(mapping) == len(test_rows) == 69512, "Test manifest row or uniqueness mismatch")
    require(all(mapping.get(str(s)) == str(p) for s,p in zip(sid,provinces)), "NPZ-to-test-manifest association mismatch")
    with (root / "metadata_and_splits/v2_spatial_val_50k_fixed.csv").open(encoding="utf-8-sig", newline="") as f:
        val_rows = list(csv.DictReader(f))
    val_ids = {row["sample_id"] for row in val_rows}
    val_provs = {row["province_code"] for row in val_rows}
    require(len(val_rows) == len(val_ids) == 50000, "Development manifest count mismatch")
    require(not set(mapping).intersection(val_ids), "Development/test sample overlap")
    require(not set(mapping.values()).intersection(val_provs), "Development/test province overlap")

    return {
        "samples": n, "unique_sample_ids": n, "correct": int(np.trace(cm)),
        "top5_correct": top5_correct, "saved_prediction_mismatches": mismatch,
        "metrics": calculated,
        "mean_province_macro_f1_present": float(np.mean([v["macro_f1_present_only"] for v in per_province.values()])),
        "mean_province_macro_f1_all8": float(np.mean([v["macro_f1_all8_classes"] for v in per_province.values()])),
        "province_tables_match": True, "development_test_sample_overlap": 0,
        "development_test_province_overlap": 0, "unresolved_manifest_rows": len(mapping)-n,
        "training_membership_independently_verified": False,
        "image_inference_performed": False, "bootstrap_recomputed_in_this_revision": False,
        "model_checkpoint_present": model_file.is_file(),
        "weights_distribution_status": "WITHHELD_FROM_PUBLIC_REDISTRIBUTION" if not model_file.is_file() else "VERIFIED_PRESENT",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hashes-only", action="store_true", help="Use only the standard library; skip NPZ arithmetic")
    args = parser.parse_args()
    root = ROOT.resolve()
    result = {"hashes": verify_hashes(root)}
    if not args.hashes_only:
        result["saved_prediction_checks"] = verify_saved_predictions(root)
    result["status"] = "PASS_WITH_DOCUMENTED_SCOPE_LIMITS"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, RuntimeError, KeyError) as exc:
        print(f"VERIFICATION_FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
