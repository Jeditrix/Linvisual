"""Dot product with numeric display.

Shows the actual numbers and step-by-step calculation:
a₁×b₁ + a₂×b₂ + ... = result
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from linalg_viz import MatrixScene

# Define two vectors
a = np.array([2, 3, 4])
b = np.array([1, -2, 3])

print(f"Vector a: {a}")
print(f"Vector b: {b}")
print(f"Dot product a·b: {np.dot(a, b)}")

# Show animated visualization
scene = MatrixScene(title="Dot Product Calculation")
scene.show_dot_product(a, b)
