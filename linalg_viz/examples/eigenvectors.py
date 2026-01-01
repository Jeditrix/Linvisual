"""Eigenvector visualization."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from linalg_viz import Vector, Matrix, show

M = Matrix([[2, 1], [1, 2]])

# Get eigenvectors
for val, vec in M.eigenvectors():
    print(f"λ = {val.real:.2f}, v = ({vec.x:.2f}, {vec.y:.2f})")

# Eigenvectors only scale under transformation, they don't rotate
v = Vector(1, 1).color("yellow")  # eigenvector direction
v.transform(M).animate().show()
