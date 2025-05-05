import pygame


class TipoffPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        # Jumping & Gravity
        self.gravity = 800
        self.jump_power = -400
        self.velocity_y = 0
        self.is_jumping = False
        self.is_landing = False

        self.ogPos = pos

        self.team = None
        self.frame_index = 0
        self.import_assets()

        self.image = self.idle_animation[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0, 0)

        self.speed = 200
        self.max_speed = 500
        self.min_speed = 200
        self.speed_decay = 100
        self.jumping_inc = 0
        self.landing_inc = 0

        self.jump_sound = pygame.mixer.Sound("images/sounds/jump.wav")
        self.jump_sound.set_volume(0.05)

        self.landing_sound = pygame.mixer.Sound("images/sounds/land.ogg")
        self.landing_sound.set_volume(0.03)

    def import_assets(self):
        if self.team == "knicks":
            self.idle_animation = [
                pygame.image.load(
                    f"images/knicks/brunson/brunson_idle/{frame}.png"
                ).convert_alpha()
                for frame in range(10)
            ]
            self.jump_animation = [
                pygame.image.load(
                    f"images/knicks/brunson/brunson_jump/{frame}.png"
                ).convert_alpha()
                for frame in range(6)
            ]
            self.land_animation = [
                pygame.image.load(
                    f"images/knicks/brunson/brunson_land/{frame}.png"
                ).convert_alpha()
                for frame in range(9)
            ]

            self.animation = self.idle_animation  # Default animation
        else:
            self.idle_animation = [
                pygame.image.load(
                    f"images/lakers/lebron/lebron_idle/{frame}.png"
                ).convert_alpha()
                for frame in range(6)
            ]
            self.jump_animation = [
                pygame.image.load(
                    f"images/lakers/lebron/lebron_jump/{frame}.png"
                ).convert_alpha()
                for frame in range(6)
            ]
            self.land_animation = [
                pygame.image.load(
                    f"images/lakers/lebron/lebron_land/{frame}.png"
                ).convert_alpha()
                for frame in range(9)
            ]

            self.animation = self.idle_animation

    def apply_gravity(self, dt):
        self.velocity_y += self.gravity * dt
        self.pos.y += self.velocity_y * dt

        # Check if player lands on the ground
        if self.pos.y >= 612:
            if self.is_jumping:
                self.is_landing = True
                self.frame_index = 0
            self.pos.y = 612
            self.velocity_y = 0
            self.is_jumping = False

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Gradually decrease speed
        if self.speed > self.min_speed:
            self.speed -= self.speed_decay * dt

        # Update position
        self.pos += self.direction * self.speed * dt
        self.rect.center = round(self.pos.x), round(self.pos.y)

    def input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_SPACE
                    and not self.is_jumping
                    and not self.is_landing
                ):
                    self.velocity_y = self.jump_power
                    self.is_jumping = True  # Prevent double jumping
                    self.animation = self.jump_animation
                    self.frame_index = 0

    def animate(self, dt):
        if self.is_jumping:
            self.landing_inc = 0

            if self.jumping_inc == 0:
                self.jump_sound.play()
                self.jumping_inc = 1

            if self.animation != self.jump_animation:
                self.animation = self.jump_animation
                self.frame_index = 0

            # Play jump animation
            if self.frame_index < len(self.jump_animation) - 1:
                self.frame_index += 10 * dt
            else:
                self.frame_index = len(self.jump_animation) - 1

            self.image = self.jump_animation[int(self.frame_index)]

        elif self.is_landing:
            self.jumping_inc = 0

            if self.landing_inc == 0:
                self.landing_sound.play()
                self.landing_inc = 1

            if self.animation != self.land_animation:
                self.animation = self.land_animation
                self.frame_index = 0

            # Play landing animation
            if self.frame_index < len(self.land_animation) - 1:
                self.frame_index += 20 * dt
            else:
                self.frame_index = len(self.land_animation) - 1
                self.is_landing = False

            self.image = self.land_animation[int(self.frame_index)]

        else:
            if self.animation != self.idle_animation:
                self.animation = self.idle_animation
                self.frame_index = min(self.frame_index, len(self.idle_animation) - 1)

            # Loop idle animation
            self.frame_index += 10 * dt
            if self.frame_index >= len(self.idle_animation):
                self.frame_index = 0

            self.image = self.idle_animation[int(self.frame_index)]

    def update(self, dt, events, team):
        if self.team != team:
            self.team = team
            self.import_assets()  # Only call import_assets when team changes
        self.input(events)
        self.apply_gravity(dt)
        self.move(dt)
        self.animate(dt)

        return (self.is_jumping, self.is_landing)
