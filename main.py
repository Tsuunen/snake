import pygame
import sys


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Snake():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.tete = [20, 0]
        self.body = [pygame.Rect(self.tete[0] - 20, self.tete[1], 20, 20), pygame.Rect(self.tete[0], self.tete[1], 20, 20)]
        self.x_direction = 1
        self.y_direction = 0

    def move(self):
        self.tete[0] += 20 * self.x_direction
        self.tete[1] += 20 * self.y_direction

        self.body.pop(0)
        self.body.append(pygame.Rect(self.tete[0] % 800, self.tete[1] % 600, 20, 20))

    def add_cell(self):
        last_cell = self.body[0]
        self.body.insert(0, pygame.Rect(last_cell.x - 20 * self.x_direction, last_cell.y - 20 * self.y_direction, 20, 20))

    def display(self):
        for rect in self.body:
            pygame.draw.rect(self.screen, "white", rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.player = Snake(self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.player.y_direction != 1:
                            self.player.x_direction = 0
                            self.player.y_direction = -1
                    elif event.key == pygame.K_DOWN:
                        if self.player.y_direction != -1:
                            self.player.x_direction = 0
                            self.player.y_direction = 1
                    elif event.key == pygame.K_LEFT:
                        if self.player.x_direction != 1:
                            self.player.x_direction = -1
                            self.player.y_direction = 0
                    elif event.key == pygame.K_RIGHT:
                        if self.player.x_direction != -1:
                            self.player.x_direction = 1
                            self.player.y_direction = 0
                    elif event.key == pygame.K_a:
                        self.player.add_cell()
                    elif event.key == pygame.K_r:
                        self.player.__init__(self.screen)
                if event.type == pygame.QUIT:
                    running = False

            self.player.move()

            if pygame.Rect.collidelist(self.player.body[-1], self.player.body[:-1]) != -1:
                self.player.__init__(self.screen)

            # Dessiner tout à l'écran
            self.screen.fill((0, 0, 0))
            self.player.display()
            pygame.display.flip()

            # if pygame.Rect.collidelist(self.player.body[-1], self.player.body[:-1]) != -1:
            #     self.player.__init__(self.screen)

            # Contrôle du FPS
            self.clock.tick(10)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
