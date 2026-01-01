"""Basic 3D vector visualization."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from linalg_viz import Vector, Matrix, show

# 3D vectors
v1 = Vector(1, 0, 0).color("red")
v2 = Vector(0, 1, 0).color("green")
v3 = Vector(0, 0, 1).color("blue")
v4 = Vector(1, 1, 1).color("yellow")

show(v1, v2, v3, v4)
