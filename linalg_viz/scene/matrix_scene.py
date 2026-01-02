"""Scene for visualizing matrix/vector arithmetic with numbers."""

from __future__ import annotations
from typing import Optional, List, Callable
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from PIL import Image

from linalg_viz.rendering.matrix_display import MatrixDisplay
from linalg_viz.rendering.colors import Colors


class MatrixScene:
    """Scene for displaying matrix operations with actual numbers."""

    def __init__(self, width: int = 1000, height: int = 600, title: str = "Matrix Visualization"):
        self._width = width
        self._height = height
        self._title = title
        self._display = MatrixDisplay(width, height)
        self._running = False
        self._clock = None
        self._screen = None

        # Animation state
        self._animation_step = 0
        self._animation_timer = 0.0
        self._step_duration = 1.0  # seconds per step
        self._paused = False

        # GIF recording state
        self._recording = False
        self._frames: List[Image.Image] = []

    def _init_pygame(self) -> None:
        pygame.init()
        pygame.display.set_caption(self._title)
        self._screen = pygame.display.set_mode((self._width, self._height), DOUBLEBUF | OPENGL)
        self._clock = pygame.time.Clock()

        # Setup 2D orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self._width, self._height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self._display.init()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
                elif event.key == K_SPACE:
                    self._paused = not self._paused
                elif event.key == K_r:
                    self._animation_step = 0
                    self._animation_timer = 0.0
                elif event.key == K_RIGHT:
                    self._animation_step += 1
                elif event.key == K_LEFT:
                    self._animation_step = max(0, self._animation_step - 1)

    def _capture_frame(self) -> None:
        """Capture current frame for GIF export."""
        if not self._recording:
            return
        # Read pixels from OpenGL framebuffer
        pixels = glReadPixels(0, 0, self._width, self._height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (self._width, self._height), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL is bottom-up
        self._frames.append(image)

    def _save_gif(self, filename: str, fps: int = 10) -> None:
        """Save recorded frames as GIF."""
        if not self._frames:
            return
        duration = int(1000 / fps)  # ms per frame
        self._frames[0].save(
            filename,
            save_all=True,
            append_images=self._frames[1:],
            duration=duration,
            loop=0
        )
        print(f"Saved GIF: {filename} ({len(self._frames)} frames)")

    def record_matrix_vector_multiply(self, matrix: np.ndarray, vector: np.ndarray,
                                       filename: str, fps: int = 2) -> None:
        """Record matrix-vector multiplication animation to GIF."""
        self._recording = True
        self._frames = []
        self._init_pygame()

        rows, cols = matrix.shape
        result = matrix @ vector
        total_steps = rows + 2  # Extra frame at end

        for step in range(total_steps):
            pygame.event.pump()  # Process events to prevent freeze
            self._animation_step = step

            # Clear and render
            glClearColor(*Colors.BACKGROUND)
            glClear(GL_COLOR_BUFFER_BIT)
            self._render_matrix_vector(matrix, vector, result, rows, cols)
            pygame.display.flip()
            self._capture_frame()

        self._save_gif(filename, fps)
        pygame.quit()
        self._recording = False

    def record_matrix_multiply(self, A: np.ndarray, B: np.ndarray,
                                filename: str, fps: int = 2) -> None:
        """Record matrix-matrix multiplication animation to GIF."""
        self._recording = True
        self._frames = []
        self._init_pygame()

        rows_a, cols_a = A.shape
        rows_b, cols_b = B.shape
        result = A @ B
        total_steps = rows_a * cols_b + 2  # Extra frame at end

        for step in range(total_steps):
            pygame.event.pump()  # Process events to prevent freeze
            self._animation_step = step

            # Clear and render
            glClearColor(*Colors.BACKGROUND)
            glClear(GL_COLOR_BUFFER_BIT)
            self._render_matrix_multiply(A, B, result, rows_a, cols_a, cols_b)
            pygame.display.flip()
            self._capture_frame()

        self._save_gif(filename, fps)
        pygame.quit()
        self._recording = False

    def record_dot_product(self, a: np.ndarray, b: np.ndarray,
                           filename: str, fps: int = 2) -> None:
        """Record dot product animation to GIF."""
        self._recording = True
        self._frames = []
        self._init_pygame()

        n = len(a)
        result = np.dot(a, b)
        total_steps = n + 2  # Extra frame at end

        for step in range(total_steps):
            pygame.event.pump()  # Process events to prevent freeze
            self._animation_step = step

            # Clear and render
            glClearColor(*Colors.BACKGROUND)
            glClear(GL_COLOR_BUFFER_BIT)
            self._render_dot_product(a, b, result, n)
            pygame.display.flip()
            self._capture_frame()

        self._save_gif(filename, fps)
        pygame.quit()
        self._recording = False

    def _render_matrix_vector(self, matrix, vector, result, rows, cols) -> None:
        """Render matrix-vector multiplication frame."""
        start_x = 50
        start_y = 100
        spacing = 40

        calc_row = self._animation_step - 1 if self._animation_step > 0 else -1

        self._display._draw_text("Matrix × Vector = Result", start_x, 30, (200, 200, 200),
                                 self._display._font_large)

        highlight_row = calc_row if 0 <= calc_row < rows else -1
        mw, mh = self._display.draw_matrix(matrix, start_x, start_y, highlight_row=highlight_row)

        x = start_x + mw + spacing
        self._display.draw_multiply(x, start_y, mh)

        x += spacing + 20
        vw, vh = self._display.draw_vector(vector, x, start_y, highlight_idx=highlight_row)

        x += vw + spacing
        self._display.draw_equals(x, start_y, mh)

        x += spacing + 20
        result_partial = np.zeros_like(result)
        for i in range(min(self._animation_step, rows)):
            result_partial[i] = result[i]

        if self._animation_step > 0:
            self._display.draw_vector(result_partial, x, start_y, color=(100, 255, 100),
                                      highlight_idx=highlight_row)

        if 0 <= calc_row < rows:
            calc_y = start_y + mh + 60
            terms = []
            for j in range(cols):
                m_val = self._display._format_number(matrix[calc_row, j])
                v_val = self._display._format_number(vector[j])
                terms.append(f"{m_val}×{v_val}")
            result_val = self._display._format_number(result[calc_row])
            calc_str = f"Row {calc_row + 1}: " + " + ".join(terms) + f" = {result_val}"
            self._display._draw_text(calc_str, start_x, calc_y, (255, 255, 100))

    def _render_matrix_multiply(self, A, B, result, rows_a, cols_a, cols_b) -> None:
        """Render matrix-matrix multiplication frame."""
        start_x = 30
        start_y = 100
        spacing = 30

        calc_idx = self._animation_step - 1 if self._animation_step > 0 else -1
        calc_row = calc_idx // cols_b if calc_idx >= 0 else -1
        calc_col = calc_idx % cols_b if calc_idx >= 0 else -1

        self._display._draw_text("Matrix × Matrix = Result", start_x, 30, (200, 200, 200),
                                 self._display._font_large)

        highlight_r = calc_row if 0 <= calc_idx < rows_a * cols_b else -1
        mw_a, mh_a = self._display.draw_matrix(A, start_x, start_y, highlight_row=highlight_r)

        x = start_x + mw_a + spacing
        self._display.draw_multiply(x, start_y, mh_a)

        x += spacing + 10
        highlight_c = calc_col if 0 <= calc_idx < rows_a * cols_b else -1
        mw_b, mh_b = self._display.draw_matrix(B, x, start_y, highlight_col=highlight_c)

        x += mw_b + spacing
        self._display.draw_equals(x, start_y, mh_a)

        x += spacing + 10
        result_partial = np.zeros_like(result)
        for idx in range(min(self._animation_step, rows_a * cols_b)):
            r, c = idx // cols_b, idx % cols_b
            result_partial[r, c] = result[r, c]

        if self._animation_step > 0:
            self._display.draw_matrix(result_partial, x, start_y, color=(100, 255, 100),
                                      highlight_row=highlight_r, highlight_col=highlight_c)

        if 0 <= calc_idx < rows_a * cols_b:
            calc_y = start_y + max(mh_a, mh_b) + 60
            terms = []
            for k in range(cols_a):
                a_val = self._display._format_number(A[calc_row, k])
                b_val = self._display._format_number(B[k, calc_col])
                terms.append(f"{a_val}×{b_val}")
            result_val = self._display._format_number(result[calc_row, calc_col])
            calc_str = f"C[{calc_row+1},{calc_col+1}]: " + " + ".join(terms) + f" = {result_val}"
            self._display._draw_text(calc_str, start_x, calc_y, (255, 255, 100))

    def _render_dot_product(self, a, b, result, n) -> None:
        """Render dot product frame."""
        start_x = 100
        start_y = 150
        spacing = 40

        calc_idx = self._animation_step - 1 if self._animation_step > 0 else -1
        highlight_idx = calc_idx if 0 <= calc_idx < n else -1

        self._display._draw_text("Vector Dot Product: a · b", start_x, 50, (200, 200, 200),
                                 self._display._font_large)

        self._display._draw_text("a =", start_x, start_y + 10, (255, 150, 150))
        x = start_x + 50
        aw, ah = self._display.draw_vector(a, x, start_y - 20, color=(255, 150, 150),
                                           highlight_idx=highlight_idx)

        x += aw + spacing
        self._display._draw_text("·", x, start_y + 10, (200, 200, 200), self._display._font_large)

        x += spacing + 20
        self._display._draw_text("b =", x, start_y + 10, (150, 150, 255))
        x += 50
        bw, bh = self._display.draw_vector(b, x, start_y - 20, color=(150, 150, 255),
                                           highlight_idx=highlight_idx)

        x += bw + spacing
        self._display.draw_equals(x, start_y - 20, ah)

        x += spacing + 20
        if self._animation_step > n:
            result_text = self._display._format_number(result)
            self._display._draw_text(result_text, x, start_y + 10, (100, 255, 100),
                                     self._display._font_large)

        calc_y = start_y + ah + 80
        if self._animation_step > 0:
            terms = []
            running_sum = 0.0
            for i in range(min(self._animation_step, n)):
                a_val = self._display._format_number(a[i])
                b_val = self._display._format_number(b[i])
                terms.append(f"{a_val}×{b_val}")
                running_sum += a[i] * b[i]

            result_val = self._display._format_number(running_sum)
            calc_str = " + ".join(terms) + f" = {result_val}"
            self._display._draw_text(calc_str, start_x, calc_y, (255, 255, 100))

    def show_matrix_vector_multiply(self, matrix: np.ndarray, vector: np.ndarray) -> None:
        """Animate matrix-vector multiplication step by step."""
        self._init_pygame()
        self._running = True

        rows, cols = matrix.shape
        result = matrix @ vector
        total_steps = rows + 1  # One step per row + final result

        while self._running:
            dt = self._clock.tick(60) / 1000.0
            self._handle_events()

            if not self._paused:
                self._animation_timer += dt
                if self._animation_timer >= self._step_duration:
                    self._animation_timer = 0.0
                    if self._animation_step < total_steps:
                        self._animation_step += 1

            # Clear
            glClearColor(*Colors.BACKGROUND)
            glClear(GL_COLOR_BUFFER_BIT)

            # Layout
            start_x = 50
            start_y = 100
            spacing = 40

            # The row we're currently calculating (0-indexed)
            calc_row = self._animation_step - 1 if self._animation_step > 0 else -1

            # Draw title
            self._display._draw_text("Matrix × Vector = Result", start_x, 30, (200, 200, 200),
                                     self._display._font_large)

            # Draw matrix with highlighted row (matches calculation)
            highlight_row = calc_row if 0 <= calc_row < rows else -1
            mw, mh = self._display.draw_matrix(matrix, start_x, start_y, highlight_row=highlight_row)

            # Draw multiply sign
            x = start_x + mw + spacing
            self._display.draw_multiply(x, start_y, mh)

            # Draw vector with highlighted element (matches calculation)
            x += spacing + 20
            vw, vh = self._display.draw_vector(vector, x, start_y, highlight_idx=highlight_row)

            # Draw equals
            x += vw + spacing
            self._display.draw_equals(x, start_y, mh)

            # Draw result vector (progressively revealed)
            x += spacing + 20
            result_partial = np.zeros_like(result)
            for i in range(min(self._animation_step, rows)):
                result_partial[i] = result[i]

            if self._animation_step > 0:
                self._display.draw_vector(result_partial, x, start_y, color=(100, 255, 100),
                                          highlight_idx=highlight_row)

            # Show current calculation
            if 0 <= calc_row < rows:
                calc_y = start_y + mh + 60

                # Build calculation string with clean formatting
                terms = []
                for j in range(cols):
                    m_val = self._display._format_number(matrix[calc_row, j])
                    v_val = self._display._format_number(vector[j])
                    terms.append(f"{m_val}×{v_val}")
                result_val = self._display._format_number(result[calc_row])
                calc_str = f"Row {calc_row + 1}: " + " + ".join(terms) + f" = {result_val}"
                self._display._draw_text(calc_str, start_x, calc_y, (255, 255, 100))

            # Draw controls hint
            controls = "Space:Pause  R:Restart  ←→:Step  Esc:Exit"
            self._display._draw_text(controls, 10, self._height - 30, (150, 150, 150))

            pygame.display.flip()

        pygame.quit()

    def show_matrix_multiply(self, A: np.ndarray, B: np.ndarray) -> None:
        """Animate matrix-matrix multiplication step by step."""
        self._init_pygame()
        self._running = True

        rows_a, cols_a = A.shape
        rows_b, cols_b = B.shape
        result = A @ B
        total_steps = rows_a * cols_b + 1

        while self._running:
            dt = self._clock.tick(60) / 1000.0
            self._handle_events()

            if not self._paused:
                self._animation_timer += dt
                if self._animation_timer >= self._step_duration:
                    self._animation_timer = 0.0
                    if self._animation_step < total_steps:
                        self._animation_step += 1

            # Clear
            glClearColor(*Colors.BACKGROUND)
            glClear(GL_COLOR_BUFFER_BIT)

            # Layout
            start_x = 30
            start_y = 100
            spacing = 30

            # The cell we're currently calculating (0-indexed)
            calc_idx = self._animation_step - 1 if self._animation_step > 0 else -1
            calc_row = calc_idx // cols_b if calc_idx >= 0 else -1
            calc_col = calc_idx % cols_b if calc_idx >= 0 else -1

            # Draw title
            self._display._draw_text("Matrix × Matrix = Result", start_x, 30, (200, 200, 200),
                                     self._display._font_large)

            # Draw matrix A with highlighted row (matches calculation)
            highlight_r = calc_row if 0 <= calc_idx < rows_a * cols_b else -1
            mw_a, mh_a = self._display.draw_matrix(A, start_x, start_y, highlight_row=highlight_r)

            # Draw multiply sign
            x = start_x + mw_a + spacing
            self._display.draw_multiply(x, start_y, mh_a)

            # Draw matrix B with highlighted column (matches calculation)
            x += spacing + 10
            highlight_c = calc_col if 0 <= calc_idx < rows_a * cols_b else -1
            mw_b, mh_b = self._display.draw_matrix(B, x, start_y, highlight_col=highlight_c)

            # Draw equals
            x += mw_b + spacing
            self._display.draw_equals(x, start_y, mh_a)

            # Draw result matrix (progressively revealed)
            x += spacing + 10
            result_partial = np.zeros_like(result)
            for idx in range(min(self._animation_step, rows_a * cols_b)):
                r, c = idx // cols_b, idx % cols_b
                result_partial[r, c] = result[r, c]

            if self._animation_step > 0:
                self._display.draw_matrix(result_partial, x, start_y, color=(100, 255, 100),
                                          highlight_row=highlight_r,
                                          highlight_col=highlight_c)

            # Show current calculation
            if 0 <= calc_idx < rows_a * cols_b:
                calc_y = start_y + max(mh_a, mh_b) + 60

                # Build calculation string with clean formatting
                terms = []
                for k in range(cols_a):
                    a_val = self._display._format_number(A[calc_row, k])
                    b_val = self._display._format_number(B[k, calc_col])
                    terms.append(f"{a_val}×{b_val}")
                result_val = self._display._format_number(result[calc_row, calc_col])
                calc_str = f"C[{calc_row+1},{calc_col+1}]: " + " + ".join(terms) + f" = {result_val}"
                self._display._draw_text(calc_str, start_x, calc_y, (255, 255, 100))

            # Draw controls hint
            controls = "Space:Pause  R:Restart  ←→:Step  Esc:Exit"
            self._display._draw_text(controls, 10, self._height - 30, (150, 150, 150))

            pygame.display.flip()

        pygame.quit()

    def show_dot_product(self, a: np.ndarray, b: np.ndarray) -> None:
        """Animate dot product calculation step by step."""
        self._init_pygame()
        self._running = True

        n = len(a)
        result = np.dot(a, b)
        total_steps = n + 1

        while self._running:
            dt = self._clock.tick(60) / 1000.0
            self._handle_events()

            if not self._paused:
                self._animation_timer += dt
                if self._animation_timer >= self._step_duration:
                    self._animation_timer = 0.0
                    if self._animation_step < total_steps:
                        self._animation_step += 1

            # Clear
            glClearColor(*Colors.BACKGROUND)
            glClear(GL_COLOR_BUFFER_BIT)

            # Layout
            start_x = 100
            start_y = 150
            spacing = 40

            # The element we're currently calculating (0-indexed)
            calc_idx = self._animation_step - 1 if self._animation_step > 0 else -1
            highlight_idx = calc_idx if 0 <= calc_idx < n else -1

            # Draw title
            self._display._draw_text("Vector Dot Product: a · b", start_x, 50, (200, 200, 200),
                                     self._display._font_large)

            # Draw vector a (as row)
            self._display._draw_text("a =", start_x, start_y + 10, (255, 150, 150))
            x = start_x + 50
            aw, ah = self._display.draw_vector(a, x, start_y - 20,
                                               color=(255, 150, 150),
                                               highlight_idx=highlight_idx)

            # Draw dot
            x += aw + spacing
            self._display._draw_text("·", x, start_y + 10, (200, 200, 200), self._display._font_large)

            # Draw vector b
            x += spacing + 20
            self._display._draw_text("b =", x, start_y + 10, (150, 150, 255))
            x += 50
            bw, bh = self._display.draw_vector(b, x, start_y - 20,
                                               color=(150, 150, 255),
                                               highlight_idx=highlight_idx)

            # Draw equals and result
            x += bw + spacing
            self._display.draw_equals(x, start_y - 20, ah)

            x += spacing + 20
            if self._animation_step > n:
                result_text = self._display._format_number(result)
                self._display._draw_text(result_text, x, start_y + 10, (100, 255, 100),
                                         self._display._font_large)

            # Show current calculation
            calc_y = start_y + ah + 80
            if self._animation_step > 0:
                terms = []
                running_sum = 0.0
                for i in range(min(self._animation_step, n)):
                    a_val = self._display._format_number(a[i])
                    b_val = self._display._format_number(b[i])
                    terms.append(f"{a_val}×{b_val}")
                    running_sum += a[i] * b[i]

                result_val = self._display._format_number(running_sum)
                calc_str = " + ".join(terms) + f" = {result_val}"
                self._display._draw_text(calc_str, start_x, calc_y, (255, 255, 100))

            # Draw controls hint
            controls = "Space:Pause  R:Restart  ←→:Step  Esc:Exit"
            self._display._draw_text(controls, 10, self._height - 30, (150, 150, 150))

            pygame.display.flip()

        pygame.quit()
