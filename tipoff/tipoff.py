import pygame
import time
from tipoff.tipoff_player import TipoffPlayer
from tipoff.tipoff_cpu import TipoffCPU
from tipoff.tipoff_background import Background
from tipoff.drop_ball import DropBall


class TipOff:
    def __init__(self):
        pygame.init()

        # Constants
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1215, 812
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # Sprite Groups
        self.tipoff_player_group = pygame.sprite.Group()
        self.tipoff_cpu_group = pygame.sprite.Group()
        self.dropBall_group = pygame.sprite.Group()

        # Create Players
        self.player = TipoffPlayer((570, 612), self.tipoff_player_group)
        self.cpu = TipoffCPU(
            (670, 612),
            self.tipoff_cpu_group,
        )

        # Create DropBall
        self.dropBall = DropBall((617, -50), self.dropBall_group)

        self.team = None

        # Load background
        self.background = None
        self.transparent_background, self.spotlight = (
            Background().generate_background(),
            Background().generate_spotlight(),
        )

        # Sounds
        self.highlight_sound = pygame.mixer.Sound("images/sounds/highlight.ogg")
        self.highlight_sound.set_volume(0.05)

        self.confirm_sound = pygame.mixer.Sound("images/sounds/confirm.ogg")
        self.confirm_sound.set_volume(0.05)

        self.tipoff_win_sound = pygame.mixer.Sound("images/sounds/tipoff_win.ogg")
        self.tipoff_win_sound.set_volume(0.05)

        self.tipoff_lose_sound = pygame.mixer.Sound("images/sounds/tipoff_lose.ogg")
        self.tipoff_lose_sound.set_volume(0.05)

        # Game state variables
        self.start = True
        self.knicks_turn = True
        self.drop = False
        self.jumping = False
        self.landing = False
        self.winner = None
        self.score = [0, 0]

        self.continue_item = ["Continue", "Quit"]
        self.selected_index = 0

        self.game_loop = None

        self.spacebar_enabled = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False

        return True

    def show_score(self):
        my_font = pygame.font.Font("images/font.ttf", 60)

        score_surface = my_font.render(f"{self.score[0]}", True, "white")

        score_surface2 = my_font.render(f"{self.score[1]}", True, "white")

        score_rect = score_surface.get_rect()
        score_rect.midtop = (480, 445)

        score_rect2 = score_surface.get_rect()
        score_rect2.midtop = (748, 445)

        self.screen.blit(score_surface, score_rect)
        self.screen.blit(score_surface2, score_rect2)

    def draw(self):
        self.screen.blit(self.background, (-462, 80))
        self.screen.blit(self.transparent_background, (0, 0))
        self.screen.blit(self.spotlight, (0, 0))

        self.show_score()

        self.tipoff_player_group.draw(self.screen)
        self.tipoff_cpu_group.draw(self.screen)
        self.dropBall_group.draw(self.screen)

        pygame.display.update()

    def update(self, dt, events):
        self.jumping, self.landing = self.player.update(dt, events, self.team)
        self.cpu.update(dt, self.dropBall, self.team)

        # Ball drops after the player starts the game and after jumping and landing animations complete.
        if not self.start and not self.drop and not self.jumping and not self.landing:
            self.drop = True
            self.dropBall.reset()

        elif self.drop:
            self.score = self.dropBall.update(
                dt, self.tipoff_player_group, self.tipoff_cpu_group, self.score
            )
            if self.dropBall.is_dropped:
                self.drop = False
                self.dropBall.reset()

    def run(self, team, background, continue_menu):
        self.team = team
        self.start = False
        running = True
        self.background = background

        while running:
            dt = self.clock.tick(60) / 1000

            events = pygame.event.get()
            running = self.handle_events(events)

            self.update(dt, events)

            self.draw()

            if self.score[0] == 5 or self.score[1] == 5:
                if self.score[0] == 5:
                    self.winner = True
                    self.tipoff_win_sound.play()
                elif self.score[1] == 5:
                    self.winner = False
                    self.tipoff_lose_sound.play()
                else:
                    self.winner = None

                time.sleep(1)
                continue_menu()

                return self.winner

        pygame.quit()


if __name__ == "__main__":
    game = TipOff()
    game.run()
