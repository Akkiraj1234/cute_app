import pygame


class BaseBackground:
    def update(self, dt: float) -> None:
        ...

    def draw(self, screen: pygame.Surface) -> None:
        ...

    def reset(self) -> None:
        ...


class single_cat_bg(BaseBackground):
    pass

class mingle_cat_bg(BaseBackground):
    pass