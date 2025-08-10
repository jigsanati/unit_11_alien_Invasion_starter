import sys
import pygame
from settings import Settings
from ship import Ship
from game_status import GameStats
from arsenal import Arsenal
from alien_fleet import AlienFleet
from time import sleep
from button import Buttons
from hud import HUD


class AlienInvasion:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
                (self.settings.screen_width, self.settings.screen_height))
        
        self.game_stats = GameStats(self) 
        self.HUD = HUD(self)

        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(str(self.settings.laser_sound))
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(str(self.settings.impact_sound))
        self.impact_sound.set_volume(0.7)
               
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()
        self.play_button = Buttons(self, 'Play')
        self.game_active = False

        # Position ship on left border, centered vertically
        self.ship.rect.x = 0
        self.ship.rect.y = self.settings.screen_height // 2

    def run_game(self):
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self) -> None:
        # Check if aliens reached left edge — game over
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()

        if self.alien_fleet.check_left_edge():
            self.restart_game()

        # Check if aliens collided with ship — game over
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self.restart_game()

        # Check bullets vs aliens collisions
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.bullets)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)

            self.game_stats.update(collisions) 

            self.HUD.update_scores()

        # Check if all aliens destroyed (win condition)
        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()

            #Update game stats level

            self.game_stats.update_level()

    def _check_game_status (self)->None:
        if self.game_stats.ship_left >= 0:
            self.game_stats.ship_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

    def _reset_level(self) -> None:
        self.ship.arsenal.bullets.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def restart_game(self)->None:

        #Setting dynamic 
        self.settings.initialize_dynamic_settings()

        #reset Game stats
        self.game_stats.reset_stats()

        #Update HUD scores
        self.HUD.update_scores()

        #reset_level
        #recenter the ship
        self._reset_level
        self.ship._center_ship  
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _update_screen(self) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.ship.arsenal.update_arsenal()
        self.ship.arsenal.draw()
        self.HUD.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.init_saved_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _check_keyup_events(self, event) -> None:
        if event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _check_keydown_events(self, event):
        if event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
