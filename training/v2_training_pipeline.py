"""[TARİHSEL / UYGULANMAMIŞ DENEY KODU — HISTORICAL / UNAPPLIED EXPERIMENTAL CODE]

ÖNEMLİ UYARI / IMPORTANT NOTICE:
Bu dosya yayımlanan final checkpoint'i (best.pt, SHA-256: 8aa73d67...) ÜRETMEMİŞTİR.
Bu kod, araştırma aşamasında planlanan ancak terk edilen Focal Loss (gamma=1.5)
ve WeightedRandomSampler tasarımını içerir.

GERÇEK V2 EĞİTİM YÖNTEMİ:
1. Veri Düzeyinde Dengeleme: EVREN üzerinde hazırlanan dengeli 50.000 yama havuzu (v2-balanced-train-50k).
2. Sunucu Trainer'ı: EVREN kümesinde çalışan standart Ultralytics stock ClassificationTrainer (varsayılan Cross-Entropy).
3. Çıkarım Düzeltmesi: Eğitim sonrası dondurulmuş Bayesian prior-shift düzeltmesi (tau=0.50).

Bu dosya yalnızca araştırma soykütüğü ve arşivsel şeffaflık amacıyla depoda tutulmaktadır.
"""

from __future__ import annotations

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, WeightedRandomSampler
from ultralytics.models.yolo.classify.train import ClassificationTrainer
from ultralytics.nn.tasks import ClassificationModel

# 8 canonical classes in alphabetical index order:
CANONICAL_CLASSES = [
    "bare_sparse_vegetation",  # index 0
    "built_up",                 # index 1
    "cropland",                 # index 2
    "grassland",                # index 3
    "herbaceous_wetland",       # index 4
    "permanent_water_bodies",   # index 5
    "shrubland",                # index 6
    "tree_cover",               # index 7
]

# Exact training class counts derived strictly from splits/v2_spatial_train.csv:
TRAIN_CLASS_COUNTS = {
    "bare_sparse_vegetation": 10004,
    "built_up": 6652,
    "cropland": 175485,
    "grassland": 298287,
    "herbaceous_wetland": 421,
    "permanent_water_bodies": 12960,
    "shrubland": 924,
    "tree_cover": 175045,
}

# Calculated Alpha (Smoothed Square-Root Inverse Frequency normalized to mean=1.0):
# alpha_c = sqrt(N_total / (C * N_c)), normalized so mean(alpha) = 1.0
CALCULATED_ALPHA = torch.tensor(
    [0.671, 0.822, 0.160, 0.123, 3.269, 0.589, 2.206, 0.160],
    dtype=torch.float32,
)

# Calculated Normalized Sampling Weights (1.0 / N_c, normalized sum=1.0):
CALCULATED_SAMPLING_WEIGHTS = {
    "bare_sparse_vegetation": 0.026307,
    "built_up": 0.039563,
    "cropland": 0.001500,
    "grassland": 0.000882,
    "herbaceous_wetland": 0.625117,
    "permanent_water_bodies": 0.020307,
    "shrubland": 0.284821,
    "tree_cover": 0.001503,
}


class MulticlassFocalLoss(nn.Module):
    """Multiclass Focal Loss with runtime assertion tracking.
    
    Formula:
        FL(p_t) = - alpha_t * (1 - p_t)^gamma * log(p_t)
    where:
        gamma: focusing exponent (default 1.5)
        alpha: 1D tensor of class-specific weighting factors
    """

    def __init__(self, alpha: torch.Tensor, gamma: float = 1.5):
        super().__init__()
        assert isinstance(alpha, torch.Tensor), "alpha must be a torch.Tensor"
        assert alpha.ndim == 1, "alpha must be 1D"
        assert gamma >= 0.0, "gamma must be non-negative"
        self.register_buffer("alpha", alpha)
        self.gamma = float(gamma)
        self.call_count = 0

    def forward(self, preds: torch.Tensor | tuple, batch: dict[str, torch.Tensor]):
        self.call_count += 1
        logits = preds[1] if isinstance(preds, (list, tuple)) else preds
        targets = batch["cls"]

        # Ensure target values are valid class indices
        assert targets.min() >= 0, f"Negative class target: {targets.min()}"
        assert targets.max() < len(self.alpha), f"Target {targets.max()} exceeds alpha classes {len(self.alpha)}"

        # Bring alpha to the device and dtype of logits
        if self.alpha.device != logits.device:
            self.alpha = self.alpha.to(logits.device, dtype=logits.dtype)

        # Standard unweighted per-sample Cross Entropy
        ce_loss = F.cross_entropy(logits, targets, reduction="none")

        # Probability assigned to true class: p_t = exp(-ce_loss)
        p_t = torch.exp(-ce_loss).clamp(min=1e-7, max=1.0)

        # Modulation factor: (1 - p_t)^gamma
        focal_factor = (1.0 - p_t) ** self.gamma

        # Class balance factor: alpha_t
        alpha_t = self.alpha[targets]

        # Modulated focal loss
        focal_loss = alpha_t * focal_factor * ce_loss
        loss = focal_loss.mean()

        # Runtime verification assertion
        assert not torch.isnan(loss), "NaN detected in MulticlassFocalLoss computation"
        assert not torch.isinf(loss), "Inf detected in MulticlassFocalLoss computation"

        return loss, {"loss": loss.detach(), "focal_loss": loss.detach()}

    def __call__(self, preds, batch):
        return self.forward(preds, batch)


class BalancedFocalClassificationTrainer(ClassificationTrainer):
    """Ultralytics ClassificationTrainer with verified Focal Loss & Balanced Sampler."""

    def __init__(self, alpha: torch.Tensor = CALCULATED_ALPHA, gamma: float = 1.5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alpha_weights = alpha
        self.gamma = gamma
        self.focal_loss_activated = False
        self.balanced_sampler_activated = False

    def setup_model(self):
        """Override model setup to inject MulticlassFocalLoss into criterion."""
        ckpt = super().setup_model()
        self.model.criterion = MulticlassFocalLoss(self.alpha_weights, gamma=self.gamma)
        self.focal_loss_activated = True
        
        # Verify replacement assertion
        assert isinstance(self.model.criterion, MulticlassFocalLoss), (
            "FATAL: self.model.criterion was not replaced by MulticlassFocalLoss!"
        )
        assert type(self.model.criterion).__name__ != "v8ClassificationLoss", (
            "FATAL: default v8ClassificationLoss is still active!"
        )
        return ckpt

    def get_dataloader(self, dataset_path: str, batch_size: int = 16, rank: int = 0, mode: str = "train"):
        """Override get_dataloader to attach WeightedRandomSampler for training mode."""
        loader = super().get_dataloader(dataset_path, batch_size, rank, mode)
        if mode == "train":
            dataset = loader.dataset
            # Extract sample labels from dataset
            targets = torch.tensor([s[1] for s in dataset.samples], dtype=torch.long)
            class_counts = torch.bincount(targets, minlength=len(self.alpha_weights))
            
            # Inverse frequency sample weights
            sample_weights = 1.0 / class_counts.float()[targets]
            balanced_sampler = WeightedRandomSampler(
                weights=sample_weights,
                num_samples=len(targets),
                replacement=True,
            )
            
            # Reconstruct loader with balanced sampler
            loader = DataLoader(
                dataset=dataset,
                batch_size=batch_size,
                sampler=balanced_sampler,
                num_workers=self.args.workers,
                pin_memory=True,
                collate_fn=getattr(dataset, "collate_fn", None),
            )
            self.balanced_sampler_activated = True
            assert isinstance(loader.sampler, WeightedRandomSampler), (
                "FATAL: loader.sampler is not WeightedRandomSampler!"
            )
        return loader
