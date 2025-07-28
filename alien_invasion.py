import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:

    def __init__(self) -> None:
        # Initialize the game window
        pygame.init()
        self.settings = Settings()

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

        self.ship = Ship(self)


    def run_game(self) -> None:
        # Game Loop
        while self.running:
            self._check_events()
            self.ship.update()
            self._update_screen()

            # 60 frames per second
            self.clock.tick(self.settings.FPS)

    def _update_screen(self):
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
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
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
