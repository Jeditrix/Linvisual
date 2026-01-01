"""Matrix-matrix multiplication with numeric display.

Shows the actual numbers and step-by-step calculation:
row of A × column of B = result element
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
from linalg_viz import MatrixScene

# Define two matrices
A = np.array([
    [1, 2],
    [3, 4],
    [5, 6]
])

B = np.array([
    [7, 8, 9],
    [10, 11, 12]
])

print("Matrix A:")
print(A)
print("\nMatrix B:")
print(B)
print("\nResult A×B:")
print(A @ B)

# Show animated visualization
scene = MatrixScene(width=1200, title="Matrix × Matrix Multiplication")
scene.show_matrix_multiply(A, B)
