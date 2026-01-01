"""Cross product visualization.

Shows how the cross product creates a vector perpendicular to both input vectors.
The magnitude of a×b equals the area of the parallelogram formed by a and b.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from linalg_viz import Vector, show

# Two 3D vectors
a = Vector(1, 0, 0).color("red")
b = Vector(0, 1, 0).color("blue")

# Cross product - perpendicular to both
c = a.cross(b).color("yellow")

print(f"a = ({a.x:.2f}, {a.y:.2f}, {a.z:.2f})")
print(f"b = ({b.x:.2f}, {b.y:.2f}, {b.z:.2f})")
print(f"a × b = ({c.x:.2f}, {c.y:.2f}, {c.z:.2f})")
print(f"|a × b| = {c.magnitude:.2f} (area of parallelogram)")

# Verify perpendicularity
print(f"(a × b) · a = {c.dot(a):.2f} (should be 0)")
print(f"(a × b) · b = {c.dot(b):.2f} (should be 0)")

show(a, b, c)
