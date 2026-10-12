"""Launch, verify pre-epoch runtime gate, and monitor EXP-V2-BALANCED-50K-REAL.

Enforces:
1. Exact dataset version: 01a12cb1-05c8-7c80-b321-2c51ae68b55a (v2-balanced-train-50k)
2. Frozen hyperparams (100% identical to EXP-V2-NATURAL-50K-REAL):
   - model: yolo11n-cls
   - imgsz: 128
   - epochs: 10
   - batch: 64
   - optimizer: AdamW
   - lr0: 0.001
   - lrf: 0.01
   - weight_decay: 0.0005
   - momentum: 0.9
   - seed: 20261011
3. PRE-EPOCH RUNTIME GATE:
   - Server dataset version ID == 01a12cb1-05c8-7c80-b321-2c51ae68b55a
   - Staged images == 50000
   - GPU count == 1
   - If staged images != 50000: IMMEDIATELY ABORT.
4. Downloads best.pt upon completion and computes SHA-256.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.append(r"C:\Users\cumac\OneDrive\Desktop\turkey-landcover\scripts")
from evren_api import call

PID = "01a1256b-d068-7a01-844e-74fe913b4325"
VERSION_ID = "01a12cb1-05c8-7c80-b321-2c51ae68b55a"
RUN_DIR = Path(r"C:\Users\cumac\OneDrive\Desktop\turkey-landcover\runs\turkeylandcover_v2\exp_v2_balanced_50k_real")
RUN_DIR.mkdir(parents=True, exist_ok=True)


def main():
    payload = {
        "architecture": "yolo11n-cls",
        "dataset_version_id": VERSION_ID,
        "hyperparams": {
            "task": "classify",
            "epochs": 10,
            "batch": 64,
            "imgsz": 128,
            "optimizer": "AdamW",
            "lr0": 0.001,
            "lrf": 0.01,
            "weight_decay": 0.0005,
            "momentum": 0.9,
            "seed": 20261011,
        },
    }

    print("Submitting EXP-V2-BALANCED-50K-REAL payload to EVREN...")
    st, res = call("POST", f"/training/jobs?project_id={PID}", body=payload)
    if st not in (200, 201):
        print(f"FAILED to launch job: status={st}, response={res}")
        sys.exit(1)

    job_id = res["id"]
    print(f"Job launched successfully! EVREN Job ID: {job_id}")
    (RUN_DIR / "initial_job_response.json").write_text(json.dumps(res, indent=2), encoding="utf-8")

    # Monitor & Pre-epoch Gate Check
    print("\n--- ENTERING PRE-EPOCH RUNTIME GATE ---")
    gate_passed = False
    seen_events = 0

    while True:
        st_job, job = call("GET", f"/training/jobs/{job_id}")
        st_metrics, metrics = call("GET", f"/training/jobs/{job_id}/metrics")

        if st_job != 200:
            print(f"Warning: HTTP {st_job} querying job status")
            time.sleep(5)
            continue

        status = job.get("status")
        events = metrics if isinstance(metrics, list) else []

        if len(events) > seen_events:
            for ev in events[seen_events:]:
                ev_type = ev.get("type", "")
                phase = ev.get("phase")
                msg = ev.get("message", "")
                ep = ev.get("epoch")
                loss = ev.get("loss")
                val_acc = ev.get("top1") or ev.get("val_top1") or ev.get("metrics/accuracy_top1")
                print(f"[{time.strftime('%H:%M:%S')}] [{ev_type.upper()}] phase={phase} ep={ep} loss={loss} msg={msg}")

                # Check Pre-epoch Runtime Gate
                if not gate_passed:
                    if "direct-to-SHM" in msg or "Direct-to-SHM" in msg:
                        print("\n>>> PRE-EPOCH RUNTIME GATE VERIFICATION <<<")
                        print(f"Server Dataset Version: {job.get('dataset_version_id')}")
                        print(f"Server Item Count:      {job.get('item_count')}")
                        print(f"Allocated GPU Count:    {job.get('gpu_count')}")
                        print(f"Message:                {msg}")

                        if job.get("dataset_version_id") != VERSION_ID:
                            print(f"CRITICAL ERROR: Dataset Version mismatch! Aborting job {job_id}...")
                            call("POST", f"/training/jobs/{job_id}/stop")
                            sys.exit(1)

                        if job.get("item_count") != 50000:
                            print(f"CRITICAL ERROR: Item count {job.get('item_count')} != 50000! Aborting job {job_id}...")
                            call("POST", f"/training/jobs/{job_id}/stop")
                            sys.exit(1)

                        if job.get("gpu_count") != 1:
                            print(f"CRITICAL ERROR: GPU count {job.get('gpu_count')} != 1! Aborting job {job_id}...")
                            call("POST", f"/training/jobs/{job_id}/stop")
                            sys.exit(1)

                        print(">>> PRE-EPOCH RUNTIME GATE PASSED 100%! TRAINING AUTHORIZED TO PROCEED <<<\n")
                        gate_passed = True

            seen_events = len(events)

        (RUN_DIR / "live_job_details.json").write_text(json.dumps(job, indent=2, ensure_ascii=False), encoding="utf-8")
        (RUN_DIR / "live_metrics.json").write_text(json.dumps(events, indent=2, ensure_ascii=False), encoding="utf-8")

        if status in ("COMPLETED", "FAILED", "CANCELLED"):
            print(f"\nJob reached terminal state: {status}")
            print("Final metrics:", job.get("final_metrics"))
            print("Model version ID:", job.get("model_version_id"))
            print("Completed at:", job.get("completed_at"))
            (RUN_DIR / "final_job_details.json").write_text(json.dumps(job, indent=2, ensure_ascii=False), encoding="utf-8")
            break

        time.sleep(10)

    if status != "COMPLETED":
        print(f"Job finished with non-success status: {status}")
        sys.exit(1)

    vid = job.get("model_version_id")
    print(f"\nDownloading weights for model version {vid}...")
    st_pt, res_pt = call("GET", f"/models/versions/{vid}/download?format=pytorch")
    if st_pt == 200 and "download_url" in res_pt:
        pt_url = res_pt["download_url"]
        pt_dest = RUN_DIR / "best.pt"
        print(f"Downloading best.pt from {pt_url[:60]}...")
        req = urllib.request.Request(pt_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(pt_dest, "wb") as f:
            f.write(resp.read())
        sha = hashlib.sha256(pt_dest.read_bytes()).hexdigest()
        print(f"Saved best.pt ({pt_dest.stat().st_size:,} bytes). SHA-256: {sha}")
        (RUN_DIR / "best_pt_sha256.txt").write_text(sha, encoding="utf-8")

    st_ox, res_ox = call("GET", f"/models/versions/{vid}/download?format=onnx")
    if st_ox == 200 and "download_url" in res_ox:
        ox_url = res_ox["download_url"]
        ox_dest = RUN_DIR / "best.onnx"
        print(f"Downloading best.onnx...")
        req = urllib.request.Request(ox_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(ox_dest, "wb") as f:
            f.write(resp.read())
        print(f"Saved best.onnx ({ox_dest.stat().st_size:,} bytes)")

    # Save results.csv
    epochs_data = job.get("final_metrics", {}).get("epochs", [])
    if epochs_data:
        with open(RUN_DIR / "results.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["epoch", "train/loss", "val/loss", "metrics/accuracy_top1", "metrics/accuracy_top5", "lr/pg0"])
            for ep in epochs_data:
                writer.writerow([ep["epoch"], ep["train_loss"], ep["val_loss"], ep["top1"], ep["top5"], ep["lr"]])
        print("Wrote results.csv successfully!")


if __name__ == "__main__":
    main()
