# gesture_detector.py
import math


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _finger_extended(landmarks, tip_id, pip_id, mcp_id):
    tip, pip, mcp = landmarks[tip_id], landmarks[pip_id], landmarks[mcp_id]
    return _dist(tip, mcp) > _dist(pip, mcp) * 1.1


class GestureDetector:
    """
    Gestures:
    - open_palm: start writing
    - fist: stop writing
    - two_fingers: space
    - thumb_up: confirm
    - ok_sign: save
    - five_fingers_reset: reset canvas
    """

    def detect(self, landmarks):
        if not landmarks or len(landmarks) < 21:
            return None

        thumb = _finger_extended(landmarks, 4, 3, 2)
        index = _finger_extended(landmarks, 8, 6, 5)
        middle = _finger_extended(landmarks, 12, 10, 9)
        ring = _finger_extended(landmarks, 16, 14, 13)
        pinky = _finger_extended(landmarks, 20, 18, 17)

        extended = [thumb, index, middle, ring, pinky]
        count = sum(extended)

        # OK sign: thumb + index close, others folded
        thumb_tip, index_tip = landmarks[4], landmarks[8]
        if _dist(thumb_tip, index_tip) < 35 and not middle and not ring and not pinky:
            return "ok_sign"

        if thumb and not index and not middle and not ring and not pinky:
            return "thumb_up"

        if index and middle and not ring and not pinky:
            return "two_fingers"

        if count == 5:
            return "open_palm"

        if count == 0:
            return "fist"

        if count == 5:
            return "five_fingers_reset"

        if index and not middle and not ring and not pinky:
            return "one_finger"

        return None
