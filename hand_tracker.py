# hand_tracker.py
import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    def __init__(self, max_hands=1):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame_bgr):
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        landmarks = None
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            h, w, _ = frame_bgr.shape
            landmarks = []
            for lm in hand.landmark:
                landmarks.append((int(lm.x * w), int(lm.y * h)))
            self.mp_draw.draw_landmarks(
                frame_bgr,
                hand,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2),
            )
        return frame_bgr, landmarks

    def fingertip(self, landmarks):
        if not landmarks:
            return None
        return landmarks[8]  # index fingertip

    def close(self):
        self.hands.close()
