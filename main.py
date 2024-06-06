import pygame
import sys
from random import randint


pygame.init()
pygame.font.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

score_font = pygame.font.SysFont('liberation', 70)
old_score_font = pygame.font.SysFont('liberation', 35)

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
        self.body.append(pygame.Rect(self.tete[0] % SCREEN_WIDTH, self.tete[1] % SCREEN_HEIGHT, 20, 20))

    def add_cell(self):
        last_cell = self.body[0]
        self.body.insert(0, pygame.Rect(last_cell.x - 20 * self.x_direction, last_cell.y - 20 * self.y_direction, 20, 20))

    def display(self):
        for rect in self.body:
            pygame.draw.rect(self.screen, "white", rect)


class Apple:
    def __init__(self, screen, snake) -> None:
        self.screen = screen
        self.coords = (randint(0, SCREEN_WIDTH // 20 - 1), randint(0, SCREEN_HEIGHT // 20 - 1))
        self.apple = pygame.Rect(self.coords[0] * 20, self.coords[1] * 20, 20, 20)
        self.snake = snake

    def display(self):
        self.apple.x = self.coords[0] * 20
        self.apple.y = self.coords[1] * 20
        pygame.draw.rect(self.screen, "red", self.apple)

    def change_coords(self):
        self.coords = (randint(0, SCREEN_WIDTH // 20 - 1), randint(0, SCREEN_HEIGHT // 20 - 1))
        self.check_if_spawn_into_snake()

    def check_if_spawn_into_snake(self):
        body_coords = [(rect.x, rect.y) for rect in self.snake.body]
        coords = (self.coords[0] * 20, self.coords[1] * 20)

        if coords in body_coords:
            self.change_coords()

         

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.player = Snake(self.screen)
        self.apple = Apple(self.screen, self.player)
        self.score = 0
        self.old_score = 0

    def draw_bg(self):
        is_drawing = True
        for i in range(0, 600, 20):
            for j in range(0, 800, 20):
                if is_drawing:
                    pygame.draw.rect(self.screen, (60, 60, 60), pygame.Rect(j, i, 20, 20))
                is_drawing = not is_drawing
            is_drawing = not is_drawing

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
                self.old_score = self.score
                self.score = 0

            if pygame.Rect.colliderect(self.player.body[-1], self.apple.apple):
                self.player.add_cell()
                self.apple.change_coords()
                self.score += 1

            # Dessiner tout à l'écran
            self.screen.fill((0, 0, 0))
            self.draw_bg()
            self.apple.display() 
            self.player.display()

            pygame.draw.line(self.screen, "white", (0, 600), (800, 600))
            score_text = score_font.render(str(self.score), True, "white")
            old_score_text = old_score_font.render(str(self.old_score), True, "white")
            self.screen.blit(score_text, (30, 630))
            self.screen.blit(old_score_text, (770, 650))
            pygame.display.flip()

            # Contrôle du FPS
            self.clock.tick(10)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
