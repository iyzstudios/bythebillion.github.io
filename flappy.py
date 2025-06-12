import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game constants
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_GAP = 150
PIPE_SPEED = 3

font = pygame.font.SysFont(None, 36)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((34, 24))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped=False):
        super().__init__()
        self.image = pygame.Surface((50, HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midtop=(x, y))
        if flipped:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottom = y

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()


def create_pipes(x):
    gap_y = random.randint(100, HEIGHT - 100)
    top_pipe = Pipe(x, gap_y - PIPE_GAP // 2, flipped=True)
    bottom_pipe = Pipe(x, gap_y + PIPE_GAP // 2)
    return top_pipe, bottom_pipe


def main():
    bird = Bird()
    all_sprites = pygame.sprite.Group(bird)
    pipes = pygame.sprite.Group()
    score = 0
    spawn_pipe_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_pipe_event, 1500)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
            if event.type == spawn_pipe_event:
                top_pipe, bottom_pipe = create_pipes(WIDTH + 50)
                pipes.add(top_pipe, bottom_pipe)
                all_sprites.add(top_pipe, bottom_pipe)
        
        all_sprites.update()

        # Collision detection
        if pygame.sprite.spritecollideany(bird, pipes):
            running = False

        # Score update
        for pipe in pipes:
            if pipe.rect.right < bird.rect.left and not hasattr(pipe, 'scored'):
                pipe.scored = True
                score += 0.5  # Count each pipe once; two pipes per gap

        screen.fill((135, 206, 235))
        all_sprites.draw(screen)
        score_surf = font.render(f"Score: {int(score)}", True, (0, 0, 0))
        screen.blit(score_surf, (10, 10))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
