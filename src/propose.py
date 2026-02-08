import pygame
from typing import Tuple

from src.utils import Scene


class Propose(Scene):
    """
    Proposal scene.

    Responsibilities:
    - Display proposal content
    - Allow user to navigate back
    - Handle its own input and rendering

    This scene does NOT:
    - Quit the application directly
    - Access pygame.event.get()
    """

    BG_COLOR: Tuple[int, int, int] = (250, 245, 240)
    BUTTON_COLOR: Tuple[int, int, int] = (120, 120, 120)
    TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)
    TITLE_COLOR: Tuple[int, int, int] = (0, 0, 0)

    def __init__(self, manager) -> None:
        super().__init__(manager)

        self.font = pygame.font.SysFont(None, 36)

        # UI elements (later JSON-driven)
        self.back_rect = pygame.Rect(20, 20, 120, 40)

        # Pre-rendered text
        self._back_text = self.font.render("Back", True, self.TEXT_COLOR)
        self._title_text = self.font.render(
            "💌 Proposal Screen 💌", True, self.TITLE_COLOR
        )

    # --------------------------------------------------
    # Input
    # --------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle input events forwarded by the App.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)

    def _handle_click(self, pos: Tuple[int, int]) -> None:
        """
        Handle mouse click at a given position.
        """
        if self.back_rect.collidepoint(pos):
            # Prefer back navigation if history exists
            if not self.manager.go_back():
                # Fallback (shouldn't happen, but safe)
                self.manager.switch_to("home")

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update(self, dt: float) -> None:
        """
        Update scene state.

        Placeholder for future animations.
        """
        pass

    # --------------------------------------------------
    # Render
    # --------------------------------------------------

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render the proposal scene.
        """
        screen.fill(self.BG_COLOR)

        pygame.draw.rect(screen, self.BUTTON_COLOR, self.back_rect)
        screen.blit(self._back_text, (50, 28))

        screen.blit(self._title_text, (260, 200))

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def cleanup(self) -> None:
        """
        Cleanup resources before leaving the scene.
        """
        pass
