import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from game_status import GameStatus
from button import Button
from Spiral_Graph import SpiralGraphics

class AlienInvasion:

    def __init__(self) -> None:
        # Initialize the game window
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()
        self.game_status = GameStatus(self.settings.starting_ships_count)

        # Set display and caption
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_width))
        pygame.display.set_caption(self.settings.name)

        # Set background
        self.bg = pygame.image.load(self.settings.bg_file)
        # Size image
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_width, self.settings.screen_height))


        self.running = True
        # Control frame rate
        self.clock = pygame.time.Clock()

        # Handle sound
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.impact_sound.set_volume(0.7)

        self.ship = Ship(self, Arsenal(self))
        self.spiral_graphics = SpiralGraphics(self)

        self.play_button = Button(self, "Play")
        self.game_active = True 

    def run_game(self) -> None:
        # Game Loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._check_collisions()
            self._update_screen()
            # 60 frames per second
            self.clock.tick(self.settings.FPS)

    def restart_game(self):
        self.settings.initialize_dynamic_settings()
        # setting up dynamic settings
        # reset Game stats
        # update HUB scores
        # reset level
        # recenter the ship
        self.reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)
          
    def _update_screen(self):
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        # Draw HUG

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Set to false to know we are quiting
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()
    def _check_button_clicked(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def new_method(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                # Play the laser sound AND fire
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
                self.ship.fire()
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
