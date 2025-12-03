import numpy as np

def rgb_to_qe_color(r, g, b):
    """Convert RGB (0-255) to Qe format 'R.G.B'."""
    return f"{int(r)}.{int(g)}.{int(b)}"

def qe_color_to_rgb(color_str):
    """Convert Qe color string to RGB tuple or None."""
    if color_str == 'f':
        return None
    r, g, b = map(int, color_str.split('.'))
    return (r, g, b)

def get_neighbors(img, x, y, h, w):
    """Get 8 neighbors in clockwise order (starting from top)."""
    directions = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < h and 0 <= ny < w:
            r, g, b = img[nx, ny]
            neighbors.append(rgb_to_qe_color(r, g, b))
        else:
            neighbors.append('f')
    return neighbors