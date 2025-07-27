import sys
import pygame
from settings import Settings

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


    def run_game(self) -> None:
        # Game Loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Set to false to know we are quiting
                    self.running = False
                    pygame.quit()
                    sys.exit()


            self.screen.blit(self.bg, (0,0))
            # Outside if, but inside for loop
            pygame.display.flip()
            # 60 frames per second
            self.clock.tick(self.settings.FPS)


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
