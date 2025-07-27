import sys
import pygame

class AlienInvasion:

    def __init__(self) -> None:
        # Initialize the game window
        pygame.init()

        # Set display and caption
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption("Alien Invasion")

        self.running = True


    def run_game(self) -> None:
        # Game Loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Set to false to know we are quiting
                    self.running = False
                    pygame.quit()
                    sys.exit()

            # Outside if, but inside for loop
            pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
