# config.py
import os

# Webcam
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Drawing
STROKE_COLOR = (0, 255, 255)      # yellow ink
STROKE_THICKNESS = 4
CANVAS_BG = (20, 20, 20)

# Gesture / writing thresholds
MIN_STROKE_POINTS = 8
LETTER_PAUSE_FRAMES = 18          # pause ends a letter
WORD_PAUSE_FRAMES = 45            # longer pause ends a word
GESTURE_COOLDOWN_FRAMES = 20

# Recognition
LETTER_CONFIDENCE_THRESHOLD = 0.55
SHAPE_CONFIDENCE_THRESHOLD = 0.60

# Export folder
EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

# Modes
MODE_WRITING = "writing"
MODE_DRAWING = "drawing"
