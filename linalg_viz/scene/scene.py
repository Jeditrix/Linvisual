"""Scene class - the main container for visualization."""

from __future__ import annotations
from typing import List, Union, TYPE_CHECKING

import pygame
from pygame.locals import *
from OpenGL.GL import glReadPixels, GL_RGB, GL_UNSIGNED_BYTE
from PIL import Image

from linalg_viz.scene.camera import Camera2D, Camera3D
from linalg_viz.scene.grid import Grid2D, Grid3D
from linalg_viz.rendering.renderer2d import Renderer2D
from linalg_viz.rendering.renderer3d import Renderer3D
from linalg_viz.animation.timeline import Timeline
from linalg_viz.animation.animator import Animation, VectorAnimation, GridTransformAnimation

if TYPE_CHECKING:
    from linalg_viz.core.vector import Vector


class Scene:
    """Main scene container for visualization."""

    def __init__(self, dim: int = 2, width: int = 800, height: int = 600, title: str = "linalg-viz"):
        if dim not in (2, 3):
            raise ValueError("Dimension must be 2 or 3")

        self._dim = dim
        self._width = width
        self._height = height
        self._title = title

        self._objects: List[Vector] = []
        self._animations: List[Animation] = []
        self._original_animations: List[Animation] = []
        self._timeline = Timeline()

        # GIF recording
        self._recording = False
        self._frames: List[Image.Image] = []

        if dim == 2:
            self._camera: Union[Camera2D, Camera3D] = Camera2D(width, height)
            self._grid: Union[Grid2D, Grid3D] = Grid2D()
            self._renderer: Union[Renderer2D, Renderer3D] = Renderer2D(width, height)
        else:
            self._camera = Camera3D(width, height)
            self._grid = Grid3D()
            self._renderer = Renderer3D(width, height)

        self._running = False
        self._paused = False
        self._screen = None
        self._clock = None
        self._show_grid = True
        self._step_size = 0.05

        self._dragging = False
        self._last_mouse_pos = (0, 0)

    @property
    def dim(self) -> int:
        return self._dim

    @property
    def camera(self) -> Union[Camera2D, Camera3D]:
        return self._camera

    @property
    def timeline(self) -> Timeline:
        return self._timeline

    def add(self, *objects: 'Vector') -> 'Scene':
        for obj in objects:
            if obj not in self._objects:
                self._objects.append(obj)
                obj._scene = self
        return self

    def remove(self, obj: 'Vector') -> 'Scene':
        if obj in self._objects:
            self._objects.remove(obj)
            obj._scene = None
        return self

    def clear(self) -> 'Scene':
        for obj in self._objects:
            obj._scene = None
        self._objects.clear()
        self._animations.clear()
        return self

    def _add_animation(self, animation: Animation) -> None:
        self._animations.append(animation)
        self._original_animations.append(animation)

    def _replay(self) -> None:
        for anim in self._animations:
            anim.reset()
        for anim in self._original_animations:
            if anim not in self._animations:
                anim.reset()
                self._animations.append(anim)
        self._timeline.stop()
        self._timeline.play()
        self._paused = False

    def _step(self, dt: float) -> None:
        self._timeline.update(dt)
        for anim in self._animations:
            anim.update(dt)

    def _init_pygame(self) -> None:
        pygame.init()
        pygame.display.set_caption(self._title)
        # Request multisampling (MSAA) for anti-aliasing without color bleeding
        # This replaces GL_LINE_SMOOTH which causes color halos
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)  # 4x MSAA
        flags = DOUBLEBUF | OPENGL | RESIZABLE
        self._screen = pygame.display.set_mode((self._width, self._height), flags)
        self._clock = pygame.time.Clock()
        self._renderer.init_gl()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
                elif event.key == K_r:
                    self._replay()
                elif event.key == K_SPACE:
                    self._paused = not self._paused
                elif event.key == K_RIGHT:
                    self._paused = True
                    self._step(self._step_size)
                elif event.key == K_LEFT:
                    self._step_backward()
                elif event.key == K_c:
                    self._camera.reset()

            elif event.type == VIDEORESIZE:
                self._width = event.w
                self._height = event.h
                self._screen = pygame.display.set_mode(
                    (self._width, self._height), DOUBLEBUF | OPENGL | RESIZABLE
                )
                self._camera.resize(self._width, self._height)
                self._renderer.resize(self._width, self._height)

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._dragging = True
                    self._last_mouse_pos = event.pos
                elif event.button == 4:  # Scroll up
                    if self._dim == 2:
                        self._camera.zoom_by(1.1, event.pos)
                    else:
                        self._camera.zoom_by(0.9)
                elif event.button == 5:  # Scroll down
                    if self._dim == 2:
                        self._camera.zoom_by(0.9, event.pos)
                    else:
                        self._camera.zoom_by(1.1)

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self._dragging = False

            elif event.type == MOUSEMOTION:
                if self._dragging:
                    dx = event.pos[0] - self._last_mouse_pos[0]
                    dy = event.pos[1] - self._last_mouse_pos[1]
                    if self._dim == 2:
                        self._camera.pan(dx, dy)
                    else:
                        if pygame.key.get_mods() & KMOD_SHIFT:
                            self._camera.pan(dx, dy)
                        else:
                            self._camera.orbit(dx * 0.01, -dy * 0.01)
                    self._last_mouse_pos = event.pos

    def _step_backward(self) -> None:
        current_progress = self._get_total_progress()
        target_progress = max(0, current_progress - self._step_size)

        for anim in self._animations:
            anim.reset()
        for anim in self._original_animations:
            if anim not in self._animations:
                anim.reset()
                self._animations.append(anim)
        self._timeline.stop()

        if target_progress > 0:
            self._step(target_progress)
        self._paused = True

    def _get_total_progress(self) -> float:
        if self._animations:
            return self._animations[0]._elapsed
        return self._timeline._current_time

    def _update(self, dt: float) -> None:
        if self._paused:
            return
        self._timeline.update(dt)
        finished = []
        for anim in self._animations:
            anim.update(dt)
            if anim.is_finished:
                finished.append(anim)
        for anim in finished:
            self._animations.remove(anim)

    def _render(self) -> None:
        if self._dim == 2:
            self._render_2d()
        else:
            self._render_3d()

    def _render_2d(self) -> None:
        self._renderer.clear()
        self._renderer.setup_2d_projection(self._camera)

        if self._show_grid:
            self._renderer.draw_grid(self._grid, self._camera)

        for anim in self._animations:
            if isinstance(anim, GridTransformAnimation):
                self._renderer.draw_transformed_grid(anim, self._camera)

        for obj in self._objects:
            active_anim = None
            for anim in self._animations:
                if isinstance(anim, VectorAnimation) and anim._end is obj:
                    active_anim = anim
                    break

            if active_anim and not active_anim.is_finished:
                self._renderer.draw_animated_vector(active_anim, self._camera)
            else:
                self._renderer.draw_vector(obj, self._camera)

        self._renderer.draw_controls_hint(self._paused)
        pygame.display.flip()

    def _render_3d(self) -> None:
        self._renderer.clear()
        self._renderer.setup_3d_projection(self._camera)

        if self._show_grid:
            self._renderer.draw_grid(self._grid)

        for anim in self._animations:
            if isinstance(anim, GridTransformAnimation):
                self._renderer.draw_transformed_grid(anim)

        for obj in self._objects:
            active_anim = None
            for anim in self._animations:
                if isinstance(anim, VectorAnimation) and anim._end is obj:
                    active_anim = anim
                    break

            if active_anim and not active_anim.is_finished:
                self._renderer.draw_animated_vector(active_anim)
            else:
                self._renderer.draw_vector(obj)

        self._renderer.draw_controls_hint(self._paused)
        pygame.display.flip()

    def show(self) -> None:
        self._init_pygame()
        self._running = True
        while self._running:
            dt = self._clock.tick(60) / 1000.0
            self._handle_events()
            self._update(dt)
            self._render()
        pygame.quit()

    def play(self) -> None:
        self._timeline.play()
        self.show()

    def _capture_frame(self) -> None:
        """Capture current frame for GIF export."""
        if not self._recording:
            return
        pixels = glReadPixels(0, 0, self._width, self._height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (self._width, self._height), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        self._frames.append(image)

    def _save_gif(self, filename: str, fps: int = 10) -> None:
        """Save recorded frames as GIF."""
        if not self._frames:
            return
        duration = int(1000 / fps)
        self._frames[0].save(
            filename,
            save_all=True,
            append_images=self._frames[1:],
            duration=duration,
            loop=0
        )
        print(f"Saved GIF: {filename} ({len(self._frames)} frames)")

    def record(self, filename: str, duration: float = 3.0, fps: int = 30) -> None:
        """Record the animation to a GIF file.

        Args:
            filename: Output GIF filename
            duration: How long to record in seconds
            fps: Frames per second for the GIF
        """
        self._recording = True
        self._frames = []
        self._init_pygame()
        self._timeline.play()

        frame_time = 1.0 / fps
        total_frames = int(duration * fps)

        for _ in range(total_frames):
            pygame.event.pump()
            self._update(frame_time)
            self._render()
            self._capture_frame()

        self._save_gif(filename, fps)
        pygame.quit()
        self._recording = False

    def record_play(self, filename: str, fps: int = 30) -> None:
        """Record animation until all animations complete.

        Args:
            filename: Output GIF filename
            fps: Frames per second for the GIF
        """
        self._recording = True
        self._frames = []
        self._init_pygame()
        self._timeline.play()

        frame_time = 1.0 / fps
        max_frames = 300  # Safety limit

        frame_count = 0
        while self._animations and frame_count < max_frames:
            pygame.event.pump()
            self._update(frame_time)
            self._render()
            self._capture_frame()
            frame_count += 1

        # Capture a few extra frames at the end
        for _ in range(fps):  # 1 second of final state
            pygame.event.pump()
            self._render()
            self._capture_frame()

        self._save_gif(filename, fps)
        pygame.quit()
        self._recording = False
