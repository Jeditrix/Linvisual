"""3D linear transformation with animation."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from linalg_viz import Vector, Matrix, show
import math

# 3D rotation matrix around Y axis
M = Matrix.rotation_y(math.pi / 4)

# Unit vectors along each axis
v1 = Vector(1, 0, 0).color("red")
v2 = Vector(0, 1, 0).color("green")
v3 = Vector(0, 0, 1).color("blue")

# Transform and animate
show(
    v1.transform(M).animate(),
    v2.transform(M).animate(),
    v3.transform(M).animate()
)
