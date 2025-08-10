import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(pygame.sprite.Sprite):
    def __init__(self, fleet: "AlienFleet", x: float, y: float) -> None:
        super().__init__()
        self.fleet = fleet
        self.game = fleet.game
        self.settings = self.game.settings
        self.screen = self.game.screen
        
        self.image = pygame.image.load(str(self.settings.alien_file)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_w, self.settings.alien_h))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)  # track horizontal position
        self.y = float(self.rect.y)  # track vertical position

    def update(self):
        """Move alien vertically only."""
        self.y += self.fleet.settings.vertical_direction * self.settings.fleet_speed
        self.rect.y = int(self.y)
        self.x -= self.fleet.settings.fleet_direction * self.settings.fleet_drop_speed
        self.rect.x = int(self.x)

    def draw_alien(self) -> None:
        self.screen.blit(self.image, self.rect)

    def check_edges(self) -> bool:
        """Return True if alien hits top or bottom edge."""
        return self.rect.top <= 0 or self.rect.bottom >= self.settings.screen_height