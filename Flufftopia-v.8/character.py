import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.spritesheet = pygame.image.load("assets/Player/character.png").convert_alpha()
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = "down"
        self.animations = self.load_animations()

    def get_image(self, frame, direction):
        width = 32
        height = 32
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (frame * width, direction * height, width, height))
        image.set_colorkey((0, 0, 0))
        return image

    def load_animations(self):
        animations = {
            "down": [self.get_image(0, 0), self.get_image(1, 0), self.get_image(2, 0), self.get_image(3, 0)],
            "left": [self.get_image(0, 1), self.get_image(1, 1), self.get_image(2, 1), self.get_image(3, 1)],
            "right": [self.get_image(0, 2), self.get_image(1, 2), self.get_image(2, 2), self.get_image(3, 2)],
            "up": [self.get_image(0, 3), self.get_image(1, 3), self.get_image(2, 3), self.get_image(3, 3)]
        }
        return animations

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.direction = "down"
            self.rect.y += 2
        elif keys[pygame.K_LEFT]:
            self.direction = "left"
            self.rect.x -= 2
        elif keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.rect.x += 2
        elif keys[pygame.K_UP]:
            self.direction = "up"
            self.rect.y -= 2

        self.image = self.animations[self.direction][pygame.time.get_ticks() // 150 % len(self.animations[self.direction])]

# Main loop update
player = Player(100, 100)
all_sprites = pygame.sprite.Group(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill((0, 0, 0))
    draw_map(screen, tmx_data)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
