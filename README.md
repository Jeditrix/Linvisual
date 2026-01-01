# linalg-viz

A Python library for visualizing linear algebra concepts. Perfect for students learning linear algebra or anyone who wants to see vectors, matrices, and transformations in action.

## Features

- **Vector Visualization**: Display 2D and 3D vectors with arrows on a coordinate grid
- **Matrix Transformations**: Animate how matrices transform vectors and space
- **Arithmetic Animations**: Step-by-step visualization of matrix multiplication, dot products
- **Eigenvector Display**: Visualize eigenvectors and how they behave under transformation
- **Interactive Controls**: Pan, zoom, rotate, pause, and step through animations

## Installation

```bash
pip install git+https://github.com/Jeditrix/linalg-viz.git
```

This automatically installs all dependencies (numpy, pygame, PyOpenGL, pillow).

### For Development

```bash
git clone https://github.com/Jeditrix/linalg-viz.git
cd linalg-viz
pip install -e .
```

## Quick Start

### Display Vectors

```python
from linalg_viz import Vector, show

# Show a single vector
show(Vector(3, 2))

# Show multiple vectors with colors
v1 = Vector(1, 0).color("red").label("i")
v2 = Vector(0, 1).color("blue").label("j")
show(v1, v2)

# Vector addition
a = Vector(2, 1).color("red")
b = Vector(1, 2).color("blue")
show(a, b, a + b)
```

### Animate Transformations

```python
from linalg_viz import Vector, Matrix

# Define a transformation matrix
M = Matrix([
    [2, 1],
    [0, 1]
])

# Animate a vector being transformed
Vector(1, 1).transform(M).animate(duration=2.0).show()
```

### 3D Vectors

```python
from linalg_viz import Vector, show

# 3D vectors work the same way
v1 = Vector(1, 0, 0).color("red")
v2 = Vector(0, 1, 0).color("green")
v3 = Vector(0, 0, 1).color("blue")
show(v1, v2, v3)

# Cross product
cross = v1.cross(v2)
show(v1, v2, cross.color("yellow"))
```

### Matrix Arithmetic Visualization

See the actual numbers and step-by-step calculations:

```python
from linalg_viz import MatrixScene
import numpy as np

# Matrix-vector multiplication
M = np.array([
    [2, -1, 3],
    [0, 4, 1],
    [1, 2, -2]
])
v = np.array([1, 2, 3])

scene = MatrixScene(title="Matrix x Vector")
scene.show_matrix_vector_multiply(M, v)
```

```python
# Matrix-matrix multiplication
A = np.array([[1, 2], [3, 4], [5, 6]])
B = np.array([[7, 8, 9], [10, 11, 12]])

scene = MatrixScene(width=1200, title="Matrix x Matrix")
scene.show_matrix_multiply(A, B)
```

```python
# Dot product
a = np.array([2, 3, 4])
b = np.array([1, -2, 3])

scene = MatrixScene(title="Dot Product")
scene.show_dot_product(a, b)
```

### Eigenvectors

```python
from linalg_viz import Vector, Matrix, Scene

# Matrix with real eigenvalues
M = Matrix([
    [3, 1],
    [0, 2]
])

# Get eigenvectors
eigenvectors = M.eigenvectors()

# Visualize - eigenvectors only scale, they don't rotate
scene = Scene(dim=2)
for ev in eigenvectors:
    scene.add(ev.color("yellow"))
    scene.add(ev.transform(M).color("orange"))
scene.show()
```

## Controls

| Key | Action |
|-----|--------|
| **Space** | Pause/resume animation |
| **R** | Restart animation |
| **Left/Right Arrow** | Step backward/forward |
| **Esc** | Close window |
| **Mouse Drag** | Pan view (2D) / Rotate view (3D) |
| **Scroll** | Zoom in/out |

## Examples

The `linalg_viz/examples/` folder contains runnable examples. Just run them directly:

```bash
cd linalg_viz/examples

python basic_vectors.py          # Basic 2D vectors
python linear_transform.py       # Linear transformation animation
python eigenvectors.py           # Eigenvector visualization
python basic_3d.py               # 3D vectors
python cross_product.py          # Cross product
python matrix_vector_arithmetic.py   # Matrix × vector step-by-step
python matrix_matrix_arithmetic.py   # Matrix × matrix step-by-step
python dot_product_arithmetic.py     # Dot product step-by-step
```

## API Reference

### Vector

```python
Vector(*components)           # Create a vector (2D or 3D)
Vector(1, 2)                  # 2D vector
Vector(1, 2, 3)               # 3D vector

# Methods (return new Vector, fluent API)
v.color("red")                # Set color (name or RGB tuple)
v.label("v1")                 # Add text label
v.scale(2)                    # Scale by factor
v.normalize()                 # Unit vector
v.transform(matrix)           # Apply matrix transformation
v.animate(duration=1.0)       # Animate the transformation
v.show()                      # Display in window

# Operations
v1 + v2                       # Vector addition
v1 - v2                       # Vector subtraction
v1.dot(v2)                    # Dot product
v1.cross(v2)                  # Cross product (3D only)
v1.magnitude()                # Length
v1.angle_with(v2)             # Angle between vectors
v1.project_onto(v2)           # Projection
```

### Matrix

```python
Matrix(data)                  # Create from 2D list or numpy array

# Methods
m.eigenvectors()              # List of eigenvector Vectors
m.eigenvalues()               # List of eigenvalues
m.determinant()               # Determinant
m.inverse()                   # Inverse matrix
m.transpose()                 # Transpose
```

### MatrixScene

```python
MatrixScene(width=1000, height=600, title="Matrix Visualization")

# Methods (show animated step-by-step arithmetic)
scene.show_matrix_vector_multiply(matrix, vector)
scene.show_matrix_multiply(A, B)
scene.show_dot_product(a, b)
```

### Scene

```python
Scene(dim=2)                  # Create 2D or 3D scene

# Methods
scene.add(vector)             # Add vector to scene
scene.show()                  # Display (blocking)
scene.play()                  # Play animations
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
