import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship(pygame.sprite.Sprite):
    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal') -> None:
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(str(self.settings.ship_file))
        self.image = pygame.transform.scale(self.image, (self.settings.ship_w, self.settings.ship_h))

        if self.settings.ship_side == "left":
            self.image = pygame.transform.rotate(self.image, -90)
        else:
            self.image = pygame.transform.rotate(self.image, 90)

        self.side = self.settings.ship_side
        self.rect = self.image.get_rect()

        if self.side == "left":
            self.rect.left = 0
        else:
            self.rect.right = self.boundaries.right
            self.image = pygame.transform.flip(self.image, True, False)

        self._center_ship()

        self.moving_up = False
        self.moving_down = False
        self.y = float(self.rect.y)

        self.arsenal = arsenal

    def _center_ship(self) -> None:
        self.rect.centery = self.boundaries.centery
        self.y = float(self.rect.y)

    def update(self) -> None:
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self) -> None:
        speed = self.settings.ship_speed
        if self.moving_up and self.rect.top > self.boundaries.top:
            self.y -= speed
        if self.moving_down and self.rect.bottom < self.boundaries.bottom:
            self.y += speed
        self.rect.y = int(self.y)

    def draw(self) -> None:
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)

    def fire(self) -> bool:
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, aliens):
        return pygame.sprite.spritecollideany(self, aliens)