# shape_recognizer.py
import math
import numpy as np


class ShapeRecognizer:
    def recognize(self, stroke):
        if not stroke or len(stroke) < 8:
            return None, 0.0

        pts = np.array(stroke, dtype=float)
        start, end = pts[0], pts[-1]
        closed = np.linalg.norm(start - end) < 40

        cx, cy = pts.mean(axis=0)
        dists = np.linalg.norm(pts - np.array([cx, cy]), axis=1)
        circularity = 1.0 - (dists.std() / max(dists.mean(), 1e-6))

        if closed and circularity > 0.75:
            return "Circle", min(0.99, 0.7 + circularity * 0.25)

        # Corner count via angle changes
        corners = 0
        for i in range(2, len(pts) - 2):
            v1 = pts[i] - pts[i - 2]
            v2 = pts[i + 2] - pts[i]
            n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
            if n1 == 0 or n2 == 0:
                continue
            cosang = np.clip(np.dot(v1, v2) / (n1 * n2), -1, 1)
            ang = math.degrees(math.acos(cosang))
            if ang > 35:
                corners += 1

        aspect = self._aspect_ratio(pts)

        if closed and 3 <= corners <= 5 and 0.8 < aspect < 1.2:
            return "Square", 0.88
        if closed and 3 <= corners <= 5 and aspect >= 1.3:
            return "Rectangle", 0.86
        if closed and corners <= 4:
            return "Triangle", 0.84
        if not closed and corners <= 2:
            return "Arrow", 0.80
        if closed and corners >= 8:
            return "Star", 0.82
        if closed and circularity > 0.55:
            return "Heart", 0.75

        return "Polygon", 0.65

    def _aspect_ratio(self, pts):
        xs, ys = pts[:, 0], pts[:, 1]
        w = xs.max() - xs.min()
        h = ys.max() - ys.min()
        if h == 0:
            return 1.0
        return w / h
