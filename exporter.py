# exporter.py
import os
from datetime import datetime
from PIL import Image
import config


class Exporter:
    def __init__(self):
        self.dir = config.EXPORT_DIR

    def save_txt(self, text):
        path = os.path.join(self.dir, f"text_{self._stamp()}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def save_png(self, image_bgr):
        path = os.path.join(self.dir, f"drawing_{self._stamp()}.png")
        rgb = image_bgr[:, :, ::-1]
        Image.fromarray(rgb).save(path)
        return path

    def save_session(self, text, image_bgr, shape_info=None):
        txt_path = self.save_txt(text)
        img_path = self.save_png(image_bgr)
        meta_path = os.path.join(self.dir, f"session_{self._stamp()}.txt")
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(f"Text: {text}\n")
            if shape_info:
                f.write(f"Shape: {shape_info}\n")
        return txt_path, img_path, meta_path

    def _stamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")
