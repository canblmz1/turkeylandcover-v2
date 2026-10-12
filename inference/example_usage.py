"""Example usage for TurkeyLandCover V2 Calibrated Classifier."""

from pathlib import Path
import numpy as np
from PIL import Image
from predict import TurkeyLandCoverClassifier

if __name__ == "__main__":
    clf = TurkeyLandCoverClassifier()
    # Dummy Sentinel-2 RGB patch test
    dummy_patch = Image.fromarray(np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8))
    result = clf.predict(dummy_patch)
    print("Dummy test inference completed:")
    print("Predicted class:", result["prediction"])
    print("Confidence:", f"{result['confidence']:.4f}")
    print("Probabilities:", result["calibrated_probabilities"])
