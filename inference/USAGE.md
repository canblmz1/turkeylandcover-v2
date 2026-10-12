# Prototype inference API — inspected, not executed in this revision

The original `predict.py` and `example_usage.py` are preserved byte-for-byte. No image inference was run to validate them. The standalone example generates a random image, not a scientific test; it was not run here and must not be reported as accuracy evidence.

Actual class and keys:

```python
from inference.predict import TurkeyLandCoverClassifier
classifier = TurkeyLandCoverClassifier()
result = classifier.predict("sample_patch.png")
print(result["prediction"])
print(result["confidence"])
```

Default checkpoint: `model/best.pt`, not `models/best.pt`. Default configuration: `config/calibration_config.json`.

The model output is expected by the source to be `(probabilities, raw_logits)`. The wrapper takes raw logits and adds the already tau-scaled frozen prior vector once. The evaluation source uses the same mathematical operation and RGB/bilinear-resize/float32-divide-by-255/CHW preprocessing. Do not apply tau a second time or change preprocessing to a generic library default without a new validation protocol.

The checkpoint and environment must be trusted. A full package lock, cross-version compatibility test, device/dtype compatibility test, or end-to-end proof is not supplied. `confidence` and `calibrated_probabilities` are API field names for softmax scores; their reliability as calibrated probabilities is unverified.

For a verified no-model operation, run `python tools/verify_release.py` from the release root. It checks the frozen saved-prediction arithmetic without PyTorch, Ultralytics, network, GPU or new image inference.
