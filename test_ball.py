import pygame


class TestBall(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.group = groups
        self.original_image = pygame.image.load("images/basketball.png").convert_alpha()

        self.scale_factor = 1.5

        width, height = self.original_image.get_size()
        new_size = (int(width * self.scale_factor), int(height * self.scale_factor))
        self.image = pygame.transform.scale(self.original_image, new_size)

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.midleft)

        self.ball = False

    def update(self, ball):
        self.ball = ball

        # Collision detection
        colliding_sprites = pygame.sprite.spritecollide(
            self, self.group[1], False, pygame.sprite.collide_mask
        )

        # Exclude self and the player group
        colliding_sprites = [
            sprite
            for sprite in colliding_sprites
            if sprite != self and sprite != self.group[1]
        ]

        if colliding_sprites:
            self.ball = True

        return self.ball
