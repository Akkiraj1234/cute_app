import pygame
from typing import (
    Dict, 
    Type, 
    List, 
    Optional
)
from src.utils import (
    WIDTH, 
    HEIGHT, 
    Scene, 
    ExitError
)
from src.homepage import HomePage
from src.propose import Propose
from src.game import Game


class SceneManager:
    """
    Central navigation and lifecycle manager for scenes.

    Responsibilities:
    - Register scene classes (single source of truth)
    - Create scene instances lazily
    - Switch between scenes
    - Maintain navigation history
    - Cleanup scenes on application shutdown
    """
    
    def __init__(self) -> None:
        self._registry: Dict[str, Type[Scene]] = {}
        self._instances: Dict[str, Scene] = {}
        self._history: List[str] = []
        self.current_scene: Optional[Scene] = None

    def register(self, scenes: Dict[str, Type[Scene]]) -> None:
        """
        Register available scene classes.
        """
        self._registry.update(scenes)

    def _get_scene(self, name: str) -> Scene:
        """
        Get an existing scene instance or create it lazily.
        """
        if name not in self._instances:
            self._instances[name] = self._registry[name](manager=self)
        return self._instances[name]
    
    def switch_to(self, name: str) -> None:
        """
        Switch to another scene and record navigation history.
        """
        if self.current_scene is not None:
            self._history.append(self._current_scene_name())
            self.current_scene.cleanup()

        self.current_scene = self._get_scene(name)

    def go_back(self) -> bool:
        """
        Navigate back to the previous scene.

        Returns:
            True if navigation occurred.
            False if no history exists.
        """
        if not self._history:
            return False

        assert self.current_scene is not None

        self.current_scene.cleanup()
        previous = self._history.pop()
        self.current_scene = self._get_scene(previous)
        return True

    def available_scenes(self) -> List[str]:
        """
        Return a list of registered scene names.
        """
        return list(self._registry.keys())

    def _current_scene_name(self) -> str:
        """
        Resolve the name of the current scene.
        """
        for name, scene in self._instances.items():
            if scene is self.current_scene:
                return name
        raise RuntimeError("Current scene is not registered")

    def close_all(self) -> None:
        """
        Cleanup all created scenes.
        Called once when the application exits.
        """
        for scene in self._instances.values():
            scene.cleanup()


class App:
    """
    Root application class.

    Owns:
    - Main game loop
    - Pygame window and clock
    - Event polling and dispatch
    - Global application shutdown

    IMPORTANT:
    - pygame.event.get() is called ONLY here
    """

    SCENES: Dict[str, Type[Scene]] = {
        "home": HomePage,
        "propose": Propose,
        "game": Game,
    }

    def __init__(self, target_fps: int = 60) -> None:
        pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.target_fps = target_fps
        self.is_running: bool = True

        self.scene_manager = SceneManager()
        self._setup_scenes()

    def _setup_scenes(self) -> None:
        """
        Register scenes and load the initial scene.
        """
        self.scene_manager.register(self.SCENES)
        self.scene_manager.switch_to("home")
    
    def _run_frame(self) -> None:
        """
        Run a single frame:
        - Handle events
        - Update scene
        - Render scene
        """
        dt = self.delta

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return

            assert self.scene_manager.current_scene is not None
            self.scene_manager.current_scene.handle_event(event)

        try:
            self.scene_manager.current_scene.update(dt)
        except ExitError:
            # Scene requested application exit
            self.is_running = False
            return

        self.scene_manager.current_scene.draw(self.screen)
        pygame.display.flip()

    @property
    def delta(self) -> float:
        """
        Time elapsed since last frame (in seconds).
        """
        return self.clock.tick(self.target_fps) / 1000.0

    def start(self) -> None:
        """
        Start the main application loop.
        """
        while self.is_running:
            self._run_frame()

        self.scene_manager.close_all()


def main() -> None:
    """
    Application entry point.
    """
    pygame.init()
    pygame.display.set_caption("Cute Application")
    app = App()
    app.start()
    pygame.quit()


if __name__ == "__main__":
    main()
