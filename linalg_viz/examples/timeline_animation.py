"""Multiple vectors animating together."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from linalg_viz import Vector, Matrix, show

rotation = Matrix.rotation(22.5)

v1 = Vector(1, 0).color("red")
v2 = Vector(0, 3).color("blue")
v3 = Vector(5, 1).color("green")

# All three vectors transform and animate together
show(
    v1.transform(rotation).animate(),
    v2.transform(rotation).animate(),
    v3.transform(rotation).animate()
)
