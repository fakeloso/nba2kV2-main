import pygame
from random import randint


class DropBall(pygame.sprite.Sprite):

    def __init__(self, pos, groups):
        super().__init__(groups)
        self.ball_surf = pygame.image.load("images/basketball.png").convert_alpha()
        self.image = self.ball_surf
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, 1)
        self.speed = randint(200, 300)

        self.rotation = 0
        self.rotation_speed = randint(20, 50)

        self.is_dropped = False

        self.player_sound = pygame.mixer.Sound("images/sounds/player_success.wav")
        self.player_sound.set_volume(0.04)

        self.cpu_sound = pygame.mixer.Sound("images/sounds/cpu_success.wav")
        self.cpu_sound.set_volume(0.03)

    def rotate(self, dt):
        # Uncomment the line below to add rotation to the ball
        # self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.ball_surf, self.rotation, 1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

        self.is_dropped = False

    def reset(self):
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = randint(200, 300)
        self.rect.center = (617, -50)
        self.is_dropped = False

    def update(self, dt, player_group, cpu_group, score):
        score
        self.rotate(dt)
        if not self.is_dropped:
            self.pos += self.direction * self.speed * dt
            self.rect.center = (round(self.pos.x), round(self.pos.y))

            # Check if the ball has collided with the player or CPU
            if pygame.sprite.spritecollide(
                self, player_group, False, pygame.sprite.collide_mask
            ):
                if score[0] < 4:
                    self.player_sound.play()
                score[0] += 1
                self.is_dropped = True

            if pygame.sprite.spritecollide(
                self, cpu_group, False, pygame.sprite.collide_mask
            ):
                if score[1] < 4:
                    self.cpu_sound.play()
                score[1] += 1
                self.is_dropped = True

        return score
