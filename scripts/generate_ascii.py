from PIL import Image, ImageOps
from pathlib import Path

# ===========================
# CONFIG
# ===========================

IMAGE_PATH = Path("../assets/images/profile.png")
OUTPUT_PATH = Path("../portrait.txt")

WIDTH = 85

ASCII_CHARS = "@%#*+=-:. "

# ===========================
# LOAD IMAGE
# ===========================

img = Image.open(IMAGE_PATH).convert("RGBA")

# Transparent background -> Black
background = Image.new("RGBA", img.size, (0, 0, 0, 255))
img = Image.alpha_composite(background, img)

# Convert to grayscale
img = img.convert("L")

# Auto contrast
img = ImageOps.autocontrast(img) 

# Auto crop dark background
bbox = img.point(lambda p: 255 if p > 20 else 0).getbbox()

if bbox:
    img = img.crop(bbox)

# Resize
w, h = img.size
aspect_ratio = h / w
new_height = int(WIDTH * aspect_ratio * 0.60)
img = img.resize((WIDTH, new_height))

# ===========================
# ASCII
# ===========================

pixels = list(img.getdata())

ascii_str = ""

for pixel in pixels:
    index = pixel * (len(ASCII_CHARS) - 1) // 255
    ascii_str += ASCII_CHARS[::-1][index]

ascii_img = ""

for i in range(0, len(ascii_str), WIDTH):
    ascii_img += ascii_str[i:i + WIDTH] + "\n"

OUTPUT_PATH.write_text(ascii_img, encoding="utf-8")

print("✅ portrait.txt generated")