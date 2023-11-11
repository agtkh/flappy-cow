import numpy as np
import pygame


class Cow:
    def __init__(self, pos, radius):
        self.pos = np.array(pos)
        self.radius = radius
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -5

        # load image
        self.img = pygame.image.load("cow.png")
        self.img = pygame.transform.scale(self.img, (2 * radius, 2 * radius))

    def update(self):
        self.velocity += self.gravity
        self.pos[1] += self.velocity
        if self.pos[1] > 600:
            self.pos[1] = 600
            self.velocity = 0
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.velocity = 0

    def render(self, screen):
        screen.blit(self.img, (self.pos[0] - self.radius, self.pos[1] - self.radius))

    def up(self):
        self.velocity += self.lift

    def hit(self, pipe):
        if pipe.pos[0] < self.pos[0] < pipe.pos[0] + pipe.size[0]:
            if pipe.pos[1] < self.pos[1] < pipe.pos[1] + pipe.size[1]:
                return True
        return False


class Pipe:
    def __init__(self, pos, size):
        self.pos = np.array(pos)
        self.size = size

        self.img = pygame.image.load("fork_spoon.png")
        self.img = pygame.transform.scale(self.img, self.size)

    def update(self):
        # 毎秒10ピクセル左に移動
        self.pos[0] -= 10

    def render(self, screen):
        screen.blit(self.img, self.pos)


if __name__ == "__main__":
    pygame.init()
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Flappy Cow")

    cow = Cow((100, 300), 50)

    font = pygame.font.Font(None, 100)

    pipes = []

    clock = pygame.time.Clock()
    running = True

    is_gameover = False

    point = 0

    while running:
        clock.tick(30)

        if not is_gameover:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button) == 1 or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                ):
                    cow.up()
            
            screen.fill((0, 127, 0))

            # draw score
            text = font.render(str(point), True, (255, 255, 255))
            screen.blit(text, (400, 50))

            # spown pipe
            if np.random.rand() < 0.01:
                pos = (800, np.random.randint(100, 500))
                size = (100, 400)
                pipes.append(Pipe(pos, size))

            cow.update()
            cow.render(screen)

            for pipe in pipes:
                pipe.update()
                pipe.render(screen)
                if cow.hit(pipe):
                    is_gameover = True
                if pipe.pos[0] < -100:
                    pipes.remove(pipe)
                    point += 1
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button) == 1 or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                ):
                    is_gameover = False
                    cow.pos = np.array([100, 300])
                    cow.velocity = 0
                    point = 0
                    pipes = []
                    break
            
            screen.fill((127, 0, 0))
            text = font.render(f"Game Over {point}", True, (0, 0, 0))
            screen.blit(text, (200, 200))

        pygame.display.flip()
    pygame.quit()
