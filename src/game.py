import pygame
import random
import math
from typing import List, Tuple
from collections import deque

from src.utils import Scene, WIDTH, HEIGHT


class Game(Scene):
    """
    Maze-based game scene.

    Features:
    - Random perfect maze (DFS backtracking)
    - Guaranteed reachable exit (red)
    - Exit shows sad → happy emoji
    - Player is a cute smiley
    - Collision-safe movement
    - New maze on every play / back
    """

    TILE_SIZE: int = 32
    MOVE_DELAY: float = 0.15

    BG_COLOR = (18, 18, 24)
    WALL_COLOR = (20, 20, 20)
    FLOOR_COLOR = (70, 190, 120)
    EXIT_COLOR = (220, 60, 60)

    PLAYER_COLOR = (255, 220, 80)
    OUTLINE_COLOR = (40, 40, 40)
    EYE_COLOR = (40, 40, 40)

    def __init__(self, manager) -> None:
        super().__init__(manager)

        self.cols = WIDTH // self.TILE_SIZE
        self.rows = HEIGHT // self.TILE_SIZE

        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 36)

        # Exit emojis
        self.exit_sad = self.font.render("😔", True, (0, 0, 0))
        self.exit_happy = self.font.render("😄", True, (0, 0, 0))

        # UI
        self.back_rect = pygame.Rect(10, 10, 100, 36)
        self.back_text = self.font.render("Back", True, (255, 255, 255))
        self.love_text = self.big_font.render(
            "aww baby u love me :)", True, (255, 200, 200)
        )

        self._reset_state()

    # --------------------------------------------------
    # State reset (NEW maze every time)
    # --------------------------------------------------

    def _reset_state(self) -> None:
        self.grid = self._generate_maze(self.cols, self.rows)
        self.exit_x, self.exit_y = self._find_exit()

        self.player_x = 1
        self.player_y = 1

        self.move_timer = 0.0
        self.reached_exit = False

    # --------------------------------------------------
    # Maze generation (DFS Backtracking)
    # --------------------------------------------------

    def _generate_maze(self, w: int, h: int) -> List[List[int]]:
        maze = [[0 for _ in range(w)] for _ in range(h)]

        def carve(x: int, y: int):
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 1 <= nx < w - 1 and 1 <= ny < h - 1 and maze[ny][nx] == 0:
                    maze[y + dy // 2][x + dx // 2] = 1
                    maze[ny][nx] = 1
                    carve(nx, ny)

        maze[1][1] = 1
        carve(1, 1)
        return maze

    # --------------------------------------------------
    # Exit (farthest reachable cell)
    # --------------------------------------------------

    def _find_exit(self) -> Tuple[int, int]:
        start = (1, 1)
        queue = deque([(start, 0)])
        visited = {start}
        farthest = start
        max_dist = 0

        while queue:
            (x, y), dist = queue.popleft()
            if dist > max_dist:
                max_dist = dist
                farthest = (x, y)

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.cols
                    and 0 <= ny < self.rows
                    and self.grid[ny][nx] == 1
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), dist + 1))

        self.grid[farthest[1]][farthest[0]] = 2
        return farthest

    # --------------------------------------------------
    # Input
    # --------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_rect.collidepoint(event.pos):
                if not self.manager.go_back():
                    self.manager.switch_to("home")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            keys = pygame.key.get_pressed()
            dx, dy = self._direction_from_keys(keys)
            self._try_move(dx, dy)

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update(self, dt: float) -> None:
        if self.reached_exit:
            return

        keys = pygame.key.get_pressed()
        dx, dy = self._direction_from_keys(keys)

        if dx or dy:
            self.move_timer += dt
            if self.move_timer >= self.MOVE_DELAY:
                self._try_move(dx, dy)
                self.move_timer = 0.0
        else:
            self.move_timer = 0.0

    # --------------------------------------------------
    # Movement
    # --------------------------------------------------

    def _direction_from_keys(self, keys) -> Tuple[int, int]:
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            return (-1, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            return (1, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            return (0, -1)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            return (0, 1)
        return (0, 0)

    def _try_move(self, dx: int, dy: int) -> None:
        nx = self.player_x + dx
        ny = self.player_y + dy

        if 0 <= nx < self.cols and 0 <= ny < self.rows:
            tile = self.grid[ny][nx]
            if tile in (1, 2):
                self.player_x = nx
                self.player_y = ny

                if tile == 2:
                    self.reached_exit = True

    # --------------------------------------------------
    # Render
    # --------------------------------------------------

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self.BG_COLOR)

        # Maze + Exit emoji
        for y in range(self.rows):
            for x in range(self.cols):
                tile = self.grid[y][x]
                if tile == 1:
                    color = self.FLOOR_COLOR
                elif tile == 2:
                    color = self.EXIT_COLOR
                else:
                    color = self.WALL_COLOR

                rect = pygame.Rect(
                    x * self.TILE_SIZE,
                    y * self.TILE_SIZE,
                    self.TILE_SIZE,
                    self.TILE_SIZE,
                )
                pygame.draw.rect(screen, color, rect)

                if tile == 2:
                    emoji = self.exit_happy if self.reached_exit else self.exit_sad
                    screen.blit(emoji, emoji.get_rect(center=rect.center))

        # Player (cute smiley)
        cx = self.player_x * self.TILE_SIZE + self.TILE_SIZE // 2
        cy = self.player_y * self.TILE_SIZE + self.TILE_SIZE // 2
        radius = self.TILE_SIZE // 2 - 3

        pygame.draw.circle(screen, self.OUTLINE_COLOR, (cx, cy), radius + 2)
        pygame.draw.circle(screen, self.PLAYER_COLOR, (cx, cy), radius)

        # Eyes
        eye_y = cy - radius // 3
        eye_dx = radius // 2
        eye_r = max(3, radius // 6)

        pygame.draw.circle(screen, self.EYE_COLOR, (cx - eye_dx, eye_y), eye_r)
        pygame.draw.circle(screen, self.EYE_COLOR, (cx + eye_dx, eye_y), eye_r)

        # Smile
        points = []
        angles = range(200, 340, 6)
        for a in angles:
            rad = math.radians(a)
            points.append((
                cx + int(math.cos(rad) * radius * 0.6),
                cy + int(math.sin(rad) * radius * 0.6),
            ))
        pygame.draw.lines(screen, self.EYE_COLOR, False, points, 3)

        # Back button
        pygame.draw.rect(screen, (120, 120, 120), self.back_rect, border_radius=8)
        screen.blit(self.back_text, (35, 18))

        # Love message
        if self.reached_exit:
            screen.blit(
                self.love_text,
                self.love_text.get_rect(center=(WIDTH // 2, HEIGHT - 40)),
            )

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def cleanup(self) -> None:
        self._reset_state()
