import pygame
from alien import Alien

from typing import TYPE_CHECKING
from bullet import Bullets
if TYPE_CHECKING:
      from alien_invasion import AlienInvasion

class Arsenal:
    def __init__(self, game: 'AlienInvasion') -> None:
        self.game = game
        self.settings = game.settings
        self.bullets = pygame.sprite.Group()

    def fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet = Bullets(self.game)
            self.bullets.add(bullet)
            return True
        return False

    def update_arsenal(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.settings.screen_width:
                self.bullets.remove(bullet)

    def draw(self):
        for bullet in self.bullets:
            bullet.draw_bullet()
        



