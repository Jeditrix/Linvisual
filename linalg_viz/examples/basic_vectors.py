"""Basic vector visualization."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from linalg_viz import Vector, show

v1 = Vector(4, 1).color("red")
v2 = Vector(2, 2).color("blue")
v3 = Vector(1, 1.5).color("green")

k = v1 + v2
k.color("yellow")

show(v1, v2, v3, k)
