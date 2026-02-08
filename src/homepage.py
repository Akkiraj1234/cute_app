import pygame
from typing import Tuple
from src.utils import Scene


class HomePage(Scene):
    """
    Home screen scene.

    Responsibilities:
    - Display main menu options
    - Handle user input for navigation
    - Request scene changes via SceneManager

    This scene does NOT:
    - Handle pygame event polling
    - Quit the application directly
    """

    BG_COLOR: Tuple[int, int, int] = (240, 240, 240)
    PROPOSE_COLOR: Tuple[int, int, int] = (200, 100, 120)
    PLAY_COLOR: Tuple[int, int, int] = (100, 160, 220)
    TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)

    def __init__(self, manager) -> None:
        super().__init__(manager)

        self.font = pygame.font.SysFont(None, 48)

        # Button hitboxes (can later be loaded from JSON)
        self.propose_rect = pygame.Rect(300, 200, 200, 60)
        self.play_rect = pygame.Rect(300, 280, 200, 60)

        # Pre-rendered text (performance-friendly)
        self._propose_text = self.font.render(
            "Will you be my…", True, self.TEXT_COLOR
        )
        self._play_text = self.font.render(
            "Play", True, self.TEXT_COLOR
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
        if self.propose_rect.collidepoint(pos):
            self.manager.switch_to("propose")

        elif self.play_rect.collidepoint(pos):
            self.manager.switch_to("game")

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update(self, dt: float) -> None:
        """
        Update scene state.

        HomePage has no time-based logic (yet).
        """
        pass

    # --------------------------------------------------
    # Render
    # --------------------------------------------------

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render the home screen.
        """
        screen.fill(self.BG_COLOR)

        pygame.draw.rect(screen, self.PROPOSE_COLOR, self.propose_rect)
        pygame.draw.rect(screen, self.PLAY_COLOR, self.play_rect)

        screen.blit(self._propose_text, (320, 212))
        screen.blit(self._play_text, (360, 292))

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def cleanup(self) -> None:
        """
        Cleanup resources before leaving the scene.
        """
        pass
