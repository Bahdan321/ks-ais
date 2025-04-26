# styles/colors.py

# Pink Shades
TEXT = "#000000"
PINK_LIGHT = "#FFC0CB"  # Light Pink
PINK_MEDIUM = "#FF69B4"  # Hot Pink
PINK_DARK = "#C71585"  # Medium Violet Red

# Yellow Shades
YELLOW_LIGHT = "#FFFFE0"  # Light Yellow
YELLOW_MEDIUM = "#FFFF00"  # Yellow
YELLOW_DARK = "#FFD700"  # Gold

# Gradients (Example: Linear gradient from light pink to light yellow)
# Note: Actual gradient implementation depends on the UI framework (e.g., CSS, Tkinter, Kivy, etc.)
# This is a conceptual representation.
PINK_YELLOW_GRADIENT = f"linear-gradient(to right, {PINK_LIGHT}, {YELLOW_LIGHT})"
PINK_GRADIENT = f"linear-gradient(to right, {PINK_LIGHT}, {PINK_DARK})"
YELLOW_GRADIENT = f"linear-gradient(to right, {YELLOW_LIGHT}, {YELLOW_DARK})"


# You might need specific color formats depending on your UI library (e.g., hex, rgb, rgba)
# Example for RGB conversion (if needed):
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


# PINK_LIGHT_RGB = hex_to_rgb(PINK_LIGHT)
# YELLOW_LIGHT_RGB = hex_to_rgb(YELLOW_LIGHT)
