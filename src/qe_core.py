import cv2
import numpy as np
import os
from .utils import rgb_to_qe_color, qe_color_to_rgb, get_neighbors

class QeEngine:
    """Core engine for Qe (Quadrante Espacial) image encoding and decoding."""

    def image_to_qe_text(self, img_path):
        """Convert image to textual Qe format."""
        img_bgr = cv2.imread(img_path)
        if img_bgr is None:
            raise FileNotFoundError(f"Image {img_path} not found.")
        
        if len(img_bgr.shape) == 2:
            img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_GRAY2BGR)
        elif img_bgr.shape[2] == 4:
            img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2BGR)
        
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        h, w = img_rgb.shape[:2]
        qe_lines = ["#Qe v1.0"]
        
        for x in range(h):
            for y in range(w):
                r, g, b = img_rgb[x, y]
                center = rgb_to_qe_color(r, g, b)
                neighbors = get_neighbors(img_rgb, x, y, h, w)
                line = f"{x}.{y}-{center},{','.join(neighbors)};"
                qe_lines.append(line)
        
        return "\n".join(qe_lines), h, w

    def qe_text_to_image(self, qe_text):
        """Reconstruct image from textual Qe format."""
        lines = qe_text.strip().split('\n')
        if not lines[0].startswith('#Qe'):
            raise ValueError("Invalid Qe format.")
        
        blocks = []
        max_x = max_y = 0
        for line in lines[1:]:
            if not line.endswith(';'):
                continue
            line = line.rstrip(';')
            if '-' not in line:
                continue
            pos_part, colors = line.split('-', 1)
            x_str, y_str = pos_part.split('.')
            x, y = int(x_str), int(y_str)
            color_list = colors.split(',')
            if len(color_list) != 9:
                continue
            blocks.append((x, y, color_list))
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        
        h, w = max_x + 1, max_y + 1
        img = np.zeros((h, w, 3), dtype=np.uint8)
        for x, y, colors in blocks:
            if 0 <= x < h and 0 <= y < w:
                center_color = colors[0]
                rgb = qe_color_to_rgb(center_color)
                if rgb is not None:
                    img[x, y] = rgb
        return img