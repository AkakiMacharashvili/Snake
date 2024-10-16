#extensions:
#1) Forbid 180 degree turns - If the snake is moving upwards and the player presses `S` or `Down Arrow` it should not be counted as collision and the snake should continue moving in the initial direction. These rules should apply to all 4 directions.
#2) Score - Add scoring system to the game. Every time snake eats food player earns some points which should be displayed at the upper part of the screen.
#3) End screen - Instead of closing the application on colliding, display the ending screen.
#4) Replay - Ask if the player wants to replay the game and if so start over. For example: if the player presses the space bar, you can start the game again.
#5) Display Score - Display achieved a score on the end screen.
import pygame
import random


class Snake:
    def __init__(self, pos, direction, nextdir, body, screen, speed):
        self.speed = speed
        self.screen = screen
        self.pos = pos
        self.direction = direction
        self.nextdir = nextdir
        self.body = body

    def render(self):
        for pos in self.body:
            pygame.draw.circle(self.screen, pygame.Color(0, 0, 255), (pos[0] + 5, pos[1] + 5), 5, 3)


class App:
    pygame.init()

    fps = pygame.time.Clock()

    fruit = [random.randrange(1, (1200 // 10)) * 10,
             random.randrange(1, (700 // 10)) * 10]
    presents = True
    score = 0

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        while True:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_n]:
                    quit()
                elif keys[pygame.K_y]:
                    self.score = 0
                    self.run()
            self.end()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))

        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = Snake([100, 50], "right", "right", [[90, 30], [80, 30], [70, 30], [60, 30], [50, 30]],
                           self.screen, 25)

    def update(self):
        self.events()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake.nextdir = 'up'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake.nextdir = 'down'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake.nextdir = 'left'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake.nextdir = 'right'
        if self.snake.nextdir == 'down' and self.snake.direction != 'up':
            self.snake.direction = 'down'
            self.snake.pos[1] += 10
        elif self.snake.nextdir == 'down' and self.snake.direction == 'up':
            self.snake.direction = 'up'
            self.snake.pos[1] -= 10

        elif self.snake.nextdir == 'up' and self.snake.direction != 'down':
            self.snake.direction = 'up'
            self.snake.pos[1] -= 10
        elif self.snake.nextdir == 'up' and self.snake.direction == 'down':
            self.snake.direction = 'down'
            self.snake.pos[1] += 10

        elif self.snake.nextdir == 'left' and self.snake.direction != 'right':
            self.snake.direction = 'left'
            self.snake.pos[0] -= 10
        elif self.snake.nextdir == 'right' and self.snake.direction != 'left':
            self.snake.direction = 'right'
            self.snake.pos[0] += 10

        elif self.snake.nextdir == 'left' and self.snake.direction == 'right':
            self.snake.direction = 'right'
            self.snake.pos[0] += 10
        elif self.snake.nextdir == 'right' and self.snake.direction == 'left':
            self.snake.direction = 'left'
            self.snake.pos[0] -= 10

        self.snake.body.insert(0, list(self.snake.pos))

        if self.snake.pos[1] == self.fruit[1] and self.snake.pos[0] == self.fruit[0]:
            self.score += 1
            self.fruit = [random.randrange(1, (1200 // 10)) * 10, random.randrange(1, (700 // 10)) * 10]
        else:
            self.snake.body.pop()

        self.render()

        pygame.draw.rect(self.screen, pygame.Color(255, 0, 0), pygame.Rect(self.fruit[0], self.fruit[1], 10, 10))

        if self.snake.pos[0] < 0 or self.snake.pos[0] > 1200:
            self.running = False
        if self.snake.pos[1] < 0 or self.snake.pos[1] > 700:
            self.running = False
        for block in self.snake.body[1:]:
            if self.snake.pos[0] == block[0] and self.snake.pos[1] == block[1]:
               self.running = False


        self.Score(pygame.Color(255, 255, 255), 'normal', 25)
        pygame.display.update()
        self.fps.tick(self.snake.speed)

    def Score(self, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        string = score_font.render('Score : ' + str(self.score), True, (0, 0, 0))
        rect = string.get_rect()
        self.screen.blit(string, rect)

    def end(self):
        self.screen.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont("roman", 35)


        end_surface = font.render(
             'Game Over,Your score:' + str(self.score) +' Do you want to play again (y/n)? ', True, (0, 255, 0))
        rect = end_surface.get_rect()
        rect.midtop = (1200 / 2, 700 / 2)
        self.screen.blit(end_surface, rect)
        pygame.display.flip()


    def render(self):
        self.screen.fill((200, 200, 200))

        self.snake.render()

    def cleanup(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.font.init()
        font = pygame.font.SysFont("roman", 35)

        end_surface = font.render(
            'Game Over,Your score:' + str(self.score) +' Do you want to play again (y/n)? ', True, (0, 255, 0))
        rect = end_surface.get_rect()
        rect.midtop = (1200 / 2, 700 / 2)
        self.screen.blit(end_surface, rect)
        pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
