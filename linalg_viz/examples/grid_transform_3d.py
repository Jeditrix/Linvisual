"""3D grid transformation animation."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from linalg_viz import Vector, Matrix, Scene
from linalg_viz.animation.animator import GridTransformAnimation
import math

# Create 3D scene
scene = Scene(dim=3)

# Rotation matrix around Y axis
M = Matrix.rotation_y(math.pi / 3)

# Add basis vectors that will be transformed
v1 = Vector(1, 0, 0).color("red").transform(M).animate()
v2 = Vector(0, 1, 0).color("green").transform(M).animate()
v3 = Vector(0, 0, 1).color("blue").transform(M).animate()

scene.add(v1, v2, v3)

# Add vector animations
for v in [v1, v2, v3]:
    if v._pending_animation:
        scene._add_animation(v._pending_animation)

# Animate the grid transformation
grid_anim = GridTransformAnimation(M, duration=2.0)
scene._add_animation(grid_anim)

scene.play()
