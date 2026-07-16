# letter_recognizer.py
import math
import numpy as np


def _resample(points, n=64):
    if len(points) < 2:
        return np.zeros((n, 2))
    pts = np.array(points, dtype=float)
    dists = [0.0]
    for i in range(1, len(pts)):
        dists.append(dists[-1] + np.linalg.norm(pts[i] - pts[i - 1]))
    total = dists[-1]
    if total == 0:
        return np.tile(pts[0], (n, 1))
    target = np.linspace(0, total, n)
    resampled = []
    j = 1
    for t in target:
        while j < len(dists) and dists[j] < t:
            j += 1
        if j >= len(pts):
            resampled.append(pts[-1])
        else:
            ratio = (t - dists[j - 1]) / max(dists[j] - dists[j - 1], 1e-6)
            resampled.append(pts[j - 1] + ratio * (pts[j] - pts[j - 1]))
    return np.array(resampled)


def _normalize(points):
    pts = _resample(points)
    pts -= pts.mean(axis=0)
    scale = np.max(np.linalg.norm(pts, axis=1))
    if scale > 0:
        pts /= scale
    return pts.flatten()


def _cosine_distance(a, b):
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 1.0
    return 1.0 - np.dot(a, b) / denom


# Simple stroke templates for uppercase letters (normalized paths)
LETTER_TEMPLATES = {
    "A": [(0, 1), (0.5, 0), (1, 1), (0.25, 0.55), (0.75, 0.55)],
    "B": [(0, 0), (0, 1), (0.6, 1), (0.8, 0.85), (0.6, 0.65), (0, 0.65), (0.6, 0.65), (0.8, 0.45), (0.6, 0), (0, 0)],
    "C": [(1, 0.2), (0.6, 0), (0.2, 0.2), (0, 0.5), (0.2, 0.8), (0.6, 1), (1, 0.8)],
    "D": [(0, 0), (0, 1), (0.5, 1), (0.9, 0.7), (0.9, 0.3), (0.5, 0), (0, 0)],
    "E": [(1, 0), (0, 0), (0, 1), (1, 1), (0, 0.5), (0.7, 0.5)],
    "H": [(0, 0), (0, 1), (0, 0.5), (1, 0.5), (1, 0), (1, 1)],
    "I": [(0.5, 0), (0.5, 1)],
    "L": [(0, 0), (0, 1), (1, 1)],
    "O": [(0.5, 0), (0.1, 0.2), (0, 0.5), (0.1, 0.8), (0.5, 1), (0.9, 0.8), (1, 0.5), (0.9, 0.2), (0.5, 0)],
    "S": [(1, 0.1), (0.5, 0), (0.1, 0.2), (0.9, 0.5), (0.1, 0.8), (0.5, 1), (1, 0.9)],
    "T": [(0, 0), (1, 0), (0.5, 0), (0.5, 1)],
    "U": [(0, 0), (0, 0.8), (0.2, 1), (0.8, 1), (1, 0.8), (1, 0)],
    "V": [(0, 0), (0.5, 1), (1, 0)],
    "W": [(0, 0), (0.25, 1), (0.5, 0.4), (0.75, 1), (1, 0)],
    "X": [(0, 0), (1, 1), (0, 1), (1, 0)],
    "Y": [(0, 0), (0.5, 0.5), (1, 0), (0.5, 0.5), (0.5, 1)],
    "Z": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "0": [(0.5, 0), (0.1, 0.2), (0, 0.5), (0.1, 0.8), (0.5, 1), (0.9, 0.8), (1, 0.5), (0.9, 0.2), (0.5, 0)],
    "1": [(0.3, 0.2), (0.5, 0), (0.5, 1)],
}


class LetterRecognizer:
    def __init__(self):
        self.templates = {
            k: _normalize([(x * 200, y * 200) for x, y in v])
            for k, v in LETTER_TEMPLATES.items()
        }

    def recognize(self, stroke):
        if not stroke or len(stroke) < 3:
            return None, 0.0

        xs = [p[0] for p in stroke]
        ys = [p[1] for p in stroke]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        norm_stroke = [
            ((x - min_x) / max(max_x - min_x, 1), (y - min_y) / max(max_y - min_y, 1))
            for x, y in stroke
        ]
        probe = _normalize([(x * 200, y * 200) for x, y in norm_stroke])

        best_char, best_score = None, -1.0
        for ch, tmpl in self.templates.items():
            score = 1.0 - _cosine_distance(probe, tmpl)
            if score > best_score:
                best_char, best_score = ch, score

        return best_char, float(best_score)
