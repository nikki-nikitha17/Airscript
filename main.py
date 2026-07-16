# ui.py
import cv2
import numpy as np


class UIOverlay:
    def render(self, frame, canvas, state):
        h, w = frame.shape[:2]
        panel_h = 180
        combined = np.zeros((h + panel_h, w, 3), dtype=np.uint8)
        combined[:h] = frame
        combined[h:] = (30, 30, 30)

        canvas_small = cv2.resize(canvas, (w // 2, panel_h - 20))
        combined[h + 10:h + 10 + canvas_small.shape[0], 10:10 + canvas_small.shape[1]] = canvas_small

        x = w // 2 + 20
        y = h + 30
        lines = [
            f"Mode: {state['mode']}",
            f"Writing Active: {state['writing_active']}",
            f"Gesture: {state.get('gesture', 'None')}",
            f"Last Letter: {state.get('last_letter', '')} ({state.get('last_conf', 0):.0%})",
            f"Current Word: {state.get('current_word', '')}",
            f"Sentence: {state.get('sentence', '')}",
        ]
        if state.get("shape"):
            lines.append(f"Shape: {state['shape']} ({state.get('shape_conf', 0):.0%})")

        for i, line in enumerate(lines):
            cv2.putText(
                combined, line, (x, y + i * 24),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA
            )

        help_text = "Open palm=start | Fist=stop | 2 fingers=space | OK=save | Q=quit | R=reset | U=undo"
        cv2.putText(combined, help_text, (10, h + panel_h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1, cv2.LINE_AA)
        return combined
