"""3D Eigenvector visualization."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from linalg_viz import Vector, Matrix, show

# 3x3 symmetric matrix (guaranteed real eigenvalues)
M = Matrix([
    [2, 1, 0],
    [1, 2, 1],
    [0, 1, 2]
])

# Get and display eigenvectors
print("Eigenvectors of M:")
for val, vec in M.eigenvectors():
    print(f"  λ = {val.real:.2f}, v = ({vec.x:.2f}, {vec.y:.2f}, {vec.z:.2f})")

# Visualize eigenvectors - they only scale under transformation
eigenvecs = []
colors = ["red", "green", "blue"]
for i, (val, vec) in enumerate(M.eigenvectors()):
    v = Vector(vec.x, vec.y, vec.z).color(colors[i])
    eigenvecs.append(v.transform(M).animate())

show(*eigenvecs)
