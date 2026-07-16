# stroke_canvas.py
import cv2
import numpy as np
import config


class StrokeCanvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.canvas = np.full((self.height, self.width, 3), config.CANVAS_BG, dtype=np.uint8)
        self.current_stroke = []
        self.strokes = []
        self.history = []

    def start_stroke(self, point):
        self.current_stroke = [point]

    def add_point(self, point):
        if not self.current_stroke:
            self.start_stroke(point)
            return
        prev = self.current_stroke[-1]
        cv2.line(
            self.canvas, prev, point,
            config.STROKE_COLOR, config.STROKE_THICKNESS, cv2.LINE_AA
        )
        self.current_stroke.append(point)

    def end_stroke(self):
        if len(self.current_stroke) >= 2:
            stroke = self.current_stroke.copy()
            self.strokes.append(stroke)
            self.history.append(self.canvas.copy())
            self.current_stroke = []
            return stroke
        self.current_stroke = []
        return None

    def undo(self):
        if not self.strokes:
            return
        self.strokes.pop()
        self.canvas = np.full((self.height, self.width, 3), config.CANVAS_BG, dtype=np.uint8)
        for stroke in self.strokes:
            for i in range(1, len(stroke)):
                cv2.line(
                    self.canvas, stroke[i - 1], stroke[i],
                    config.STROKE_COLOR, config.STROKE_THICKNESS, cv2.LINE_AA
                )

    def get_image(self):
        return self.canvas.copy()
