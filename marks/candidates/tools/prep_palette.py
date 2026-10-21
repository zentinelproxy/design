"""Palette sampled from marks/source/zentinel-mascot-1024.png (histogram of a
16-colour quantise plus point samples of the nose, tongue, ball and ring).
Shared by prep.py (raster remap) and assemble.py (snapping vtracer's fills)."""

PALETTE = {
    "outline": "#200b22",
    "disc": "#492c4f",
    "orange": "#fe8a27",
    "orange-shade": "#e56c26",
    "orange-light": "#fcac2a",
    "cream": "#fedaa9",
    "cream-shade": "#e59c5b",
    "nose": "#885135",
    "tongue": "#ba5760",
    "white": "#ffffff",
    "ball": "#96749a",
    "ball-shade": "#664879",
    "ball-light": "#d7bdc7",
}
# Not used for the remap (the ring is painted out and redrawn as circles).
RING = "#84566a"
