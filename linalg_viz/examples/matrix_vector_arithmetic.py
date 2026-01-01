"""Matrix-vector multiplication with numeric display.

Shows the actual numbers and step-by-step calculation:
row × column = result element
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from linalg_viz import MatrixScene

# Define matrix and vector
M = np.array([
    [2, -1, 3],
    [0, 4, 1],
    [1, 2, -2]
])

v = np.array([1, 2, 3])

print("Matrix M:")
print(M)
print(f"\nVector v: {v}")
print(f"\nResult M×v: {M @ v}")

# Show animated visualization
scene = MatrixScene(title="Matrix × Vector Multiplication")
scene.show_matrix_vector_multiply(M, v)
