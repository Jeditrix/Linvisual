# Linvisual

A simple to use Python library for visualizing linear algebra concepts.

![Matrix Multiplication](assets/matrix_multiply.gif)

![3D Transform](assets/linear_transform_3d.gif)

## Features

- **Vector Visualization**: Display 2D and 3D vectors with arrows on a coordinate grid
- **Matrix Transformations**: Animate how matrices transform vectors and space
- **Arithmetic Animations**: Step-by-step visualization of matrix multiplication, dot products
- **Eigenvector Display**: Visualize eigenvectors and how they behave under transformation
- **Interactive Controls**: Pan, zoom, rotate, pause, and step through animations

## Installation

```bash
git clone https://github.com/Jeditrix/linalg-viz.git
cd linalg-viz
pip install -r requirements.txt
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

The `linalg_viz/examples/` folder contains runnable examples:

### 2D Vectors
| ![Basic Vectors](assets/basic_vectors.gif) | ![Linear Transform](assets/linear_transform.gif) |
|:--:|:--:|
| `python basic_vectors.py` | `python linear_transform.py` |

### 3D Vectors
| ![3D Vectors](assets/basic_3d.gif) | ![3D Transform](assets/linear_transform_3d.gif) |
|:--:|:--:|
| `python basic_3d.py` | `python linear_transform_3d.py` |

### Matrix Arithmetic
| ![Matrix × Vector](assets/matrix_vector.gif) |
|:--:|
| `python matrix_vector_arithmetic.py` |

| ![Matrix × Matrix](assets/matrix_multiply.gif) |
|:--:|
| `python matrix_matrix_arithmetic.py` |

| ![Dot Product](assets/dot_product.gif) |
|:--:|
| `python dot_product_arithmetic.py` |

## GIF Export

Export animations to GIF for documentation or sharing:

```python
from linalg_viz import Vector, Matrix, Scene, MatrixScene
import numpy as np

# --- Matrix Arithmetic ---
scene = MatrixScene()
M = np.array([[2, -1], [0, 4]])
v = np.array([1, 2])
scene.record_matrix_vector_multiply(M, v, "matrix_vector.gif")

# --- Vector Animations ---
M = Matrix([[2, 1], [0, 1]])
scene = Scene(dim=2)
v = Vector(1, 0).color("red").transform(M).animate()
scene.add(v)
scene._add_animation(v._pending_animation)
scene.record_play("transform.gif", fps=20)  # Records until animation ends

# Or record for a fixed duration
scene = Scene(dim=2)
scene.add(Vector(1, 1).color("blue"))
scene.record("static.gif", duration=2.0, fps=15)
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

# Interactive animations (opens window)
scene.show_matrix_vector_multiply(matrix, vector)
scene.show_matrix_multiply(A, B)
scene.show_dot_product(a, b)

# Export to GIF
scene.record_matrix_vector_multiply(matrix, vector, "output.gif")
scene.record_matrix_multiply(A, B, "output.gif")
scene.record_dot_product(a, b, "output.gif")
```

### Scene

```python
Scene(dim=2)                  # Create 2D or 3D scene

# Methods
scene.add(vector)             # Add vector to scene
scene.show()                  # Display (blocking)
scene.play()                  # Play animations

# GIF Export
scene.record("output.gif", duration=3.0, fps=30)  # Record fixed duration
scene.record_play("output.gif", fps=30)           # Record until animations end
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
