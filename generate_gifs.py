"""Generate GIFs for README documentation."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import math
import numpy as np
from linalg_viz import Vector, Matrix, Scene, MatrixScene

# Create assets folder
assets = Path(__file__).parent / "assets"
assets.mkdir(exist_ok=True)

print("Generating GIFs...")

# --- Matrix Arithmetic GIFs ---

# Matrix-vector multiplication
print("  matrix_vector.gif...")
M = np.array([
    [2, -1, 3],
    [0, 4, 1],
    [1, 2, -2]
])
v = np.array([1, 2, 3])
scene = MatrixScene()
scene.record_matrix_vector_multiply(M, v, str(assets / "matrix_vector.gif"))

# Matrix-matrix multiplication
print("  matrix_multiply.gif...")
A = np.array([[1, 2], [3, 4], [5, 6]])
B = np.array([[7, 8, 9], [10, 11, 12]])
scene = MatrixScene(width=1200)
scene.record_matrix_multiply(A, B, str(assets / "matrix_multiply.gif"))

# Dot product
print("  dot_product.gif...")
a = np.array([2, 3, 4])
b = np.array([1, -2, 3])
scene = MatrixScene()
scene.record_dot_product(a, b, str(assets / "dot_product.gif"))

# --- Vector Transform GIFs ---

# 2D Linear transform
print("  linear_transform.gif...")
M = Matrix([[2, 1], [0, 1.5]])
scene = Scene(dim=2)
v1 = Vector(1, 0).color("red").transform(M).animate()
v2 = Vector(0, 1).color("blue").transform(M).animate()
scene.add(v1, v2)
scene._add_animation(v1._pending_animation)
scene._add_animation(v2._pending_animation)
scene.record_play(str(assets / "linear_transform.gif"), fps=20)

# 3D Linear transform
print("  linear_transform_3d.gif...")
M = Matrix.rotation_y(math.pi / 4)
scene = Scene(dim=3)
v1 = Vector(1, 0, 0).color("red").transform(M).animate()
v2 = Vector(0, 1, 0).color("green").transform(M).animate()
v3 = Vector(0, 0, 1).color("blue").transform(M).animate()
scene.add(v1, v2, v3)
scene._add_animation(v1._pending_animation)
scene._add_animation(v2._pending_animation)
scene._add_animation(v3._pending_animation)
scene.record_play(str(assets / "linear_transform_3d.gif"), fps=20)

# Basic vectors (static)
print("  basic_vectors.gif...")
scene = Scene(dim=2)
v1 = Vector(2, 1).color("red")
v2 = Vector(1, 2).color("blue")
v3 = Vector(3, 3).color("green")
scene.add(v1, v2, v3)
scene.record(str(assets / "basic_vectors.gif"), duration=1.0, fps=10)

# Basic 3D
print("  basic_3d.gif...")
scene = Scene(dim=3)
v1 = Vector(1, 0, 0).color("red")
v2 = Vector(0, 1, 0).color("green")
v3 = Vector(0, 0, 1).color("blue")
v4 = Vector(1, 1, 1).color("yellow")
scene.add(v1, v2, v3, v4)
scene.record(str(assets / "basic_3d.gif"), duration=1.0, fps=10)

print("Done! GIFs saved to assets/")
