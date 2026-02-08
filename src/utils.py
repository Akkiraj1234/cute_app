
import pygame

# Defualts
WIDTH, HEIGHT = 800, 500



class Scene:
    def __init__(self, manager):
        self.manager = manager

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass
    
    def cleanup(self):
        pass
    
    
class ExitError(BaseException):
    def __init__(self, *args):
        super().__init__(*args)
        
        

class Particle:
    def __init__(self, image, pos, velocity, lifetime):
        self.image = image
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(velocity)
        self.lifetime = lifetime

    def update(self, dt: float) -> bool:
        self.pos += self.velocity * dt
        self.lifetime -= dt
        return self.lifetime > 0

    def draw(self, screen):
        screen.blit(self.image, self.pos)
class Assets:
    """
    Centralized asset management for the HomePage scene.

    Responsibilities:
    - Load and store fonts, colors, and pre-rendered text
    - Provide easy access to assets for rendering
    - Encapsulate asset-related logic (e.g., text rendering)
    """
    def __init__(self, root_path:str) -> None:
        self.root_path = root_path