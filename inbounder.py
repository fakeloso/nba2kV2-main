import pygame
import time


class Inbounder(pygame.sprite.Sprite):

    def __init__(self, pos, groups, inbounder_is_active, snap):
        super().__init__(groups)
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1215, 812
        self.inbounder_is_active = inbounder_is_active
        self.import_assets()
        self.frame_index = 0
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.snap = snap
        self.spacebar_pressed = 0

        self.position = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1, 0)
        self.speed = 200

    def import_assets(self):
        path = "images/inbounder/"

        self.animation = []
        for frame in range(3):
            surf = pygame.image.load(f"{path}{frame}.png").convert_alpha()
            self.animation.append(surf)

    def outofbounds(self, screen, time):
        my_font = pygame.font.Font("images/font.ttf", 100)
        downs_surface = my_font.render("INCOMPLETE PASS", True, "red")
        downs_rect = downs_surface.get_rect()
        downs_rect.midtop = (self.WINDOW_WIDTH / 2, 300)
        screen.blit(downs_surface, downs_rect)
        pygame.display.flip()
        self.football_outOfBounds = True
        time.sleep(1)

    def move(self, dt):

        self.position += self.direction * self.speed * dt
        self.rect.center = round(self.position.x), round(self.position.y)

        if self.position.x < 50:
            self.position.x = 50
        if self.position.x > 150:
            self.position.x = 150

        if self.position.y < 100:
            self.position.y = 100
        if self.position.y > 575:
            self.position.y = 575

        if self.position.x > self.WINDOW_WIDTH:
            self.position.x = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.spacebar_pressed < 3:
                        self.spacebar_pressed += 1
                        self.direction.x = -1
                        if self.spacebar_pressed == 1:
                            # self.snap = True
                            self.spacebar_pressed = 4
                            self.inbounder_is_active = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        if keys[pygame.K_UP]:
            self.direction.y = -1
        if keys[pygame.K_DOWN]:
            self.direction.y = 1

    def animate(self):
        if self.snap:
            self.frame_index = 1
        if self.spacebar_pressed == 3:
            self.frame_index = 2

        self.image = self.animation[int(self.frame_index)]

    def snap_throw_instructions(self, screen):
        if self.snap:
            if int(time.time() * 2) % 2 == 0:
                my_font = pygame.font.Font("images/font.ttf", 50)
                speed_surface = my_font.render("SPACEBAR TO THROW", True, "yellow")
                speed_rect = speed_surface.get_rect()
                speed_rect.midtop = (215, 5)
                screen.blit(speed_surface, speed_rect)

        else:
            if int(time.time() * 2) % 2 == 0:
                my_font = pygame.font.Font("images/font.ttf", 50)
                speed_surface = my_font.render("SPACEBAR TO START", True, "white")
                speed_rect = speed_surface.get_rect()
                speed_rect.midtop = (200, 5)
                screen.blit(speed_surface, speed_rect)

    def update(
        self,
        dt,
        events,
        outOfBounds,
    ):

        self.input(events)
        self.move(dt)
        self.animate()

        self.outOfBounds = outOfBounds

        # Reset inbounder position if out of bounds
        if outOfBounds:
            self.position.x = 250
            self.position.y = 350
            self.rect.center = round(self.position.x), round(self.position.y)
            self.inbounder_is_active = True
            self.snap = False
            self.spacebar_pressed = 0
            self.frame_index = 0
            outOfBounds = False

        return self.inbounder_is_active, self.snap, outOfBounds
