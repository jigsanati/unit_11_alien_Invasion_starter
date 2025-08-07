import pygame
from alien_fleet import Alien
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()

    def create_fleet(self):
        alien = Alien(self, 0, 0)
        alien_width, alien_height = alien.rect.size

        # Spawn aliens in right half of screen
        available_space_x = self.settings.screen_width // 2
        number_aliens_x = available_space_x // (2 * alien_width)

        available_space_y = (self.settings.screen_height - 3 * alien_height) // 2
        number_rows = available_space_y // (2 * alien_height)

        for row in range(number_rows):
            for alien_number in range(number_aliens_x):
                x = self.settings.screen_width // 2 + alien_width + 2 * alien_width * alien_number
                y = alien_height + 2 * alien_height * row
                alien = Alien(self, x, y)
                self.fleet.add(alien)

    def update_fleet(self):
        self.fleet.update()  # Move all aliens vertically

        if self._check_fleet_edges():
            self._change_fleet_direction()

    def _check_fleet_edges(self):
        """Return True if any alien hits top or bottom edge."""
        for alien in self.fleet:
            if alien.check_edges():
                return True
        return False

    def _change_fleet_direction(self):
        # Reverse vertical direction (bounce)
        self.settings.vertical_direction *= -1

        # Move entire fleet one step left
        for alien in self.fleet:
            alien.x -= self.settings.fleet_drop_speed
            alien.rect.x = int(alien.x)

    def check_left_edge(self):
        """Return True if any alien reaches left screen edge (where ship is)."""
        for alien in self.fleet:
            if alien.rect.left <= 0:
                return True
        return False

    def check_collisions(self, bullets):
        return pygame.sprite.groupcollide(self.fleet, bullets, True, True)

    def check_destroyed_status(self):
        return len(self.fleet) == 0

    def draw(self):
        for alien in self.fleet:
            alien.draw_alien()