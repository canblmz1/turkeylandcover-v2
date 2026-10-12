"""TurkeyLandCover V2 Standalone Inference Engine.

Integrates:
- YOLO11n-cls base weights (runs/turkeylandcover_v2/exp_v2_balanced_50k_real/best.pt)
- Post-hoc Bayesian logit calibration (tau = 0.50, epsilon = 1e-12)
- Exact 8 canonical land-cover classes
- 128x128 bilinear image preprocessing
"""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from PIL import Image
import torch
from ultralytics import YOLO

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
CONFIG_PATH = ROOT_DIR / "config" / "calibration_config.json"
MODEL_PATH = ROOT_DIR / "model" / "best.pt"


class TurkeyLandCoverClassifier:
    def __init__(self, model_path: Path | str = MODEL_PATH, config_path: Path | str = CONFIG_PATH):
        self.model_path = Path(model_path)
        self.config_path = Path(config_path)

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.cfg = json.load(f)

        self.class_names = self.cfg["class_names"]
        self.tau = float(self.cfg["tau"])
        self.prior_shift = np.array([self.cfg["prior_shift_vector"][c] for c in self.class_names], dtype=np.float32)

        # Load model
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model checkpoint not found at '{self.model_path}'.\n"
                "The binary checkpoint best.pt is withheld from public redistribution per WEIGHTS_DISTRIBUTION_STATUS.md.\n"
                "To run inference, place authorized best.pt (SHA-256: 8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a) in the model/ directory."
            )
        self.yolo = YOLO(str(self.model_path))
        self.model = self.yolo.model
        self.model.eval()

    def preprocess(self, img_input: Image.Image | str | Path | np.ndarray) -> torch.Tensor:
        if isinstance(img_input, (str, Path)):
            img = Image.open(img_input).convert("RGB")
        elif isinstance(img_input, np.ndarray):
            img = Image.fromarray(img_input).convert("RGB")
        elif isinstance(img_input, Image.Image):
            img = img_input.convert("RGB")
        else:
            raise TypeError(f"Unsupported image input type: {type(img_input)}")

        if img.size != (128, 128):
            img = img.resize((128, 128), Image.Resampling.BILINEAR)

        arr = np.array(img, dtype=np.float32) / 255.0  # HWC
        tensor = torch.from_numpy(arr).permute(2, 0, 1).unsqueeze(0)  # 1, C, H, W
        return tensor

    @torch.inference_mode()
    def predict(self, img_input: Image.Image | str | Path | np.ndarray) -> dict:
        inp = self.preprocess(img_input)
        _, raw_logits_t = self.model(inp)
        raw_logits = raw_logits_t.cpu().numpy()[0]

        # Apply calibrated prior shift: logit + tau * shift
        corrected_logits = raw_logits + self.prior_shift

        # Softmax probabilities
        exp_logits = np.exp(corrected_logits - np.max(corrected_logits))
        calibrated_probs = exp_logits / np.sum(exp_logits)

        pred_idx = int(np.argmax(corrected_logits))
        pred_class = self.class_names[pred_idx]
        confidence = float(calibrated_probs[pred_idx])

        return {
            "prediction": pred_class,
            "prediction_index": pred_idx,
            "confidence": confidence,
            "calibrated_probabilities": {c: float(calibrated_probs[i]) for i, c in enumerate(self.class_names)},
            "raw_logits": {c: float(raw_logits[i]) for i, c in enumerate(self.class_names)},
            "corrected_logits": {c: float(corrected_logits[i]) for i, c in enumerate(self.class_names)},
        }
