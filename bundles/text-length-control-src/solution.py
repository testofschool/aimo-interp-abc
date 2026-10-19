"""Problem-text control: robustness from problem length and digit count only (no model loaded)."""
import math
import os
import re

import joblib

_ART = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "text_length.joblib"))
_MODEL = _ART["model"]


def _features(problem: str):
    return [math.log1p(len(problem)), len(re.findall(r"\d", problem))]


def are_robust(model_id: str, reasoning_effort: str, problems: list[str]) -> list[bool]:
    try:
        probs = _MODEL.predict_proba([_features(p) for p in problems])[:, 1]
        return [bool(p >= 0.5) for p in probs]
    except Exception:  # never fail a batch
        return [True for _ in problems]
