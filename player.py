import pygame
import time
from basketball import Basketball


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.group = groups
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1215, 812
        self.winner = None
        self.team = None
        self.status = "right"
        self.frame_index = 0
        self.direction = pygame.math.Vector2(1, 0)
        self.position = pygame.math.Vector2(pos)
        self.rect = None

        self.import_assets()
        self.animation = self.animations["idle"]
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.height = 0
        self.velocity = 0
        self.jump_speed = 400
        self.jump_start = 1
        self.gravity = -800

        self.speed = 200
        self.max_speed = 500
        self.min_speed = 200
        self.speed_decay = 100

        self.stop = 0
        self.ball = False
        self.pass_steal = False
        self.stealing = False
        self.landing = None
        self.is_animation_playing = False
        self.before_jump = None
        self.is_idle = False
        self.basketball = None
        self.scale_factor = 1.0

        self.jump_sound = pygame.mixer.Sound("images/sounds/jump.wav")
        self.jump_sound.set_volume(0.05)

        self.landing_sound = pygame.mixer.Sound("images/sounds/land.ogg")
        self.landing_sound.set_volume(0.02)

    def load_animation(self, path, frame_count):
        images = []

        for i in range(frame_count):
            image_path = f"{path}{i}.png"
            image = pygame.image.load(image_path).convert_alpha()

            images.append(image)

        return images

    def import_assets(self):
        # Define animation types and frame counts
        animation_data = {
            "run_right": ("run/", 8),
            "run_left": ("run_left/", 8),
            "jump": ("jump/", 6),
            "jump_left": ("jump_left/", 6),
            "land_right": ("land/", 9),
            "land_left": ("land_left/", 9),
            "idle": ("idle/", 10),
            "idle_left": ("idle_left/", 10),
            "dribble_right": ("dribble/", 8),
            "dribble_left": ("dribble_left/", 8),
            "shoot": ("shoot/", 2),
            "shoot_left": ("shoot_left/", 2),
            "pass": ("pass/", 7),
            "pass_left": ("pass_left/", 7),
            "steal": ("steal/", 8),
            "steal_left": ("steal_left/", 8),
        }

        # Determine which player's animations to load
        if self.winner:
            if self.team == "knicks":
                team = "knicks"
                player = "brunson"
            else:
                team = "lakers"
                player = "lebron"
        else:
            if self.team == "lakers":
                team = "lakers"
                player = "lebron"
            else:
                team = "knicks"
                player = "brunson"

        # Generate the base path dynamically
        base_path = f"images/{team}/{player}/{player}_"

        # Load animations dynamically
        self.animations = {
            key: self.load_animation(base_path + path, frames)
            for key, (path, frames) in animation_data.items()
        }

        # Store animation lengths
        self.animation_lengths = {
            key: len(anim) for key, anim in self.animations.items()
        }

    def outofbounds(self, screen, time):
        screen.fill((0, 0, 0))
        my_font = pygame.font.Font("images/font.ttf", 100)

        message = "OUT OF BOUNDS"
        color = "red"

        downs_surface = my_font.render(message, True, color)
        downs_rect = downs_surface.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
        )
        screen.blit(downs_surface, downs_rect)
        pygame.display.flip()
        time.sleep(1)

        self.speed = 0
        self.outOfBounds = True
        self.direction = pygame.math.Vector2(1, 0)

    def reset_position(self):
        self.status = "right"
        self.speed = 0
        self.position = pygame.math.Vector2(250, 450)
        self.rect.center = round(self.position.x), round(self.position.y)

    def move(self, dt, screen, time):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Gradually decrease speed
        if self.speed > self.min_speed:
            self.speed -= self.speed_decay * dt

        # Update position
        self.position += self.direction * self.speed * dt
        if self.height != 0:
            self.velocity += self.gravity * dt
            self.height += self.velocity * dt

            if self.height < 0:
                self.height = 0
                self.velocity = 0
                self.frame_index = 0
                self.landing = True
                self.stop = 0

        self.rect.center = round(self.position.x), round(self.position.y - self.height)

        # Adjust the scale factor based on the vertical position (y-coordinate)
        # The higher the y position, the smaller the sprite becomes, the lower the y position, the bigger the sprite.
        self.scale_factor = max(
            1.0, min(1.5, 1 + (self.position.y - 400) / 500)
        )  # Adjust the divisor and constants to fine-tune size changes

        self.speed = max(self.min_speed, min(self.speed, self.max_speed))

        if self.landing:
            self.ball = False
            self.pass_steal = False

        if self.position.x < 20:
            self.position.x = 20

        if self.position.x > 2000 and not self.height != 0:
            self.outofbounds(screen, time)
            self.reset_position()
            self.direction.y = 0

        if (self.position.y < 350 or self.position.y > 775) and not self.height != 0:
            self.outofbounds(screen, time)
            self.reset_position()
            self.direction.y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.speed += 50

                if event.key == pygame.K_w and self.height == 0:
                    self.jump_sound.play()
                    self.velocity = self.jump_speed
                    self.height = self.jump_start
                    self.animation = self.animation
                    self.frame_index = 0
                    self.direction = pygame.math.Vector2(0, 0)

                if event.key == pygame.K_d and not self.pass_steal and self.ball:
                    self.pass_steal = True
                    self.frame_index = 0
                elif event.key == pygame.K_d and not self.pass_steal and not self.ball:
                    self.pass_steal = True
                    self.frame_index = 0

        keys = pygame.key.get_pressed()

        if not self.ball:
            # Reset direction
            self.is_idle = True
            self.direction.x = 0
            self.direction.y = 0

            # Horizontal movement
            if keys[pygame.K_RIGHT]:
                self.is_idle = False
                self.status = "right"
                self.direction.x = 1
            elif keys[pygame.K_LEFT]:
                self.is_idle = False
                self.status = "left"
                self.direction.x = -1

            # Vertical movement
            if keys[pygame.K_UP]:
                self.is_idle = False
                self.direction.y = -1
            if keys[pygame.K_DOWN]:
                self.is_idle = False
                self.direction.y = 1
        else:
            if not self.pass_steal:
                if keys[pygame.K_RIGHT]:
                    self.status = "right"
                    self.direction.x = 1
                elif keys[pygame.K_LEFT]:
                    self.status = "left"
                    self.direction.x = -1

                # Vertical movement
                if keys[pygame.K_UP]:
                    self.direction.y = -1
                if keys[pygame.K_DOWN]:
                    self.direction.y = 1

    def animate(self, dt):
        if self.height != 0:
            if self.ball:

                if self.status == "right":
                    self.animation = self.animations["shoot"]
                elif self.status == "left":
                    self.animation = self.animations["shoot_left"]
            else:
                if self.status == "right":
                    self.animation = self.animations["jump"]
                elif self.status == "left":
                    self.animation = self.animations["jump_left"]
        else:
            if self.ball:
                if self.status == "right":
                    if self.landing:
                        self.is_idle = False
                        self.animation = self.animations["land_right"]
                    else:
                        self.animation = self.animations["dribble_right"]
                        self.direction.x = 1
                    if self.pass_steal:
                        self.animation = self.animations["pass"]
                elif self.status == "left":
                    if self.landing:
                        self.is_idle = False
                        self.animation = self.animations["land_left"]
                    else:
                        self.animation = self.animations["dribble_left"]
                        self.direction.x = -1
                    if self.pass_steal:
                        self.animation = self.animations["pass_left"]
            else:
                if self.status == "right":
                    self.animation = self.animations["run_right"]
                    self.direction.x = 1
                    if self.landing:
                        self.is_idle = False
                        self.animation = self.animations["land_right"]
                    if self.is_idle:
                        self.animation = self.animations["idle"]
                        self.direction.x = 0

                    if self.pass_steal:
                        self.animation = self.animations["steal"]

                elif self.status == "left":
                    self.animation = self.animations["run_left"]
                    self.direction.x = -1

                    if self.landing:
                        self.is_idle = False
                        self.animation = self.animations["land_left"]

                    if self.is_idle:
                        self.animation = self.animations["idle_left"]
                        self.direction.x = 0

                    if self.pass_steal:
                        self.animation = self.animations["steal_left"]

        if self.landing:
            self.frame_index += 15 * dt
        else:
            self.frame_index += 10 * dt

        if self.animation in [
            self.animations["jump"],
            self.animations["jump_left"],
            self.animations["shoot"],
            self.animations["shoot_left"],
            self.animations["pass"],
            self.animations["pass_left"],
            self.animations["land_right"],
            self.animations["land_left"],
            self.animations["steal"],
            self.animations["steal_left"],
        ]:

            if self.frame_index > len(self.animation) - 2:
                self.frame_index = len(self.animation) - 1

                if self.stop == 0:
                    self.stop += 1

                self.is_animation_playing = False
                if self.ball:
                    self.speed = 0
                self.pass_steal = False
                self.landing = False

            else:
                self.is_animation_playing = True
                self.pass_steal = True
                if self.ball or self.landing or self.pass_steal:
                    self.speed = 0
                else:
                    self.speed = self.speed

        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]

        # Applys the scale factor to the image
        width, height = self.image.get_size()
        new_width = int(width * self.scale_factor)
        new_height = int(height * self.scale_factor)
        self.image = pygame.transform.scale(
            self.animation[int(self.frame_index)], (new_width, new_height)
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw_speed_meter(self, screen):
        bar_width = 200
        bar_height = 20
        bar_x = 170
        bar_y = 20
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))

        # Calculate the width of the green bar based on the player's speed
        green_bar_width = int(
            (self.speed - self.min_speed)
            / (self.max_speed - self.min_speed)
            * bar_width
        )

        pygame.draw.rect(
            screen, (0, 255, 0), (bar_x, bar_y, green_bar_width, bar_height)
        )
        my_font = pygame.font.Font("images/font.ttf", 50)
        speed_surface = my_font.render("SPEED:", True, pygame.Color(255, 255, 255))
        speed_rect = speed_surface.get_rect()
        speed_rect.midtop = (100, 10)
        screen.blit(speed_surface, speed_rect)

    def move_basketball(self, dt):
        if self.ball:
            if not self.pass_steal and self.height != 0:
                if self.frame_index == len(self.animation) - 1:
                    if self.stop == 1:

                        if self.status == "right":
                            self.basketball = Basketball(
                                (
                                    self.rect.topright[0] - 50,
                                    self.rect.topright[1] + 10,
                                ),
                                self,
                                time,
                                pygame.math.Vector2(1, 0),
                            )
                        elif self.status == "left":
                            self.basketball = Basketball(
                                (self.rect.topleft[0] + 50, self.rect.topleft[1] + 10),
                                self,
                                time,
                                pygame.math.Vector2(-1, 0),
                            )
                        self.stop += 1
            else:
                if self.frame_index == len(self.animation) - 1:

                    if self.status == "right":
                        self.basketball = Basketball(
                            (self.rect.midright[0] - 50, self.rect.midright[1] + 10),
                            self,
                            time,
                            pygame.math.Vector2(1, 0),
                        )
                    elif self.status == "left":
                        self.basketball = Basketball(
                            (self.rect.midleft[0] + 50, self.rect.midleft[1] + 10),
                            self,
                            time,
                            pygame.math.Vector2(-1, 0),
                        )
                    self.ball = False

        if self.basketball:
            self.basketball.update(dt)

    def update(self, dt, events, screen, time, team, winner, ball):
        self.ball = ball
        self.winner = winner
        self.team = team
        self.outOfBounds = False
        self.input(events)
        self.move(dt, screen, time)
        self.move_basketball(dt)
        self.animate(dt)
        self.import_assets()

        return (self.outOfBounds, self.ball)
