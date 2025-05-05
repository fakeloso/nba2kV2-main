import pygame
import time
from player import Player
from inbounder import Inbounder
#we in this bitch
from game_loop import game_loop
from all_sprites import AllSprites
from test_ball import TestBall

from menus import (
    start_menu,
    render_teamselect_menu,
    teamselect_menu,
    render_playerselect_menu,
    playerselect_menu,
    howto_menu,
    render_start_screen,
    render_continue_menu,
    start_screen,
    continue_menu,
)
from tipoff.tipoff import TipOff
from tipoff.tipoff_background import Background


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1215, 812
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("NBA 2K25")
        self.clock = pygame.time.Clock()

        # groups
        self.player_group = AllSprites()
        self.inbounder_group = pygame.sprite.Group()
        self.testball_group = pygame.sprite.Group()

        # variables
        self.outOfBounds = False
        self.inbounder_is_active = True
        self.snap = False
        self.menu = False
        self.team = None
        self.selectedplayer = None
        self.winner = None
        self.ball = False

        # Menu variables
        self.selected_index3 = None
        self.team_selected_index = 0
        self.continue_selected_index = 0
        self.teamselect_menu_items = ["KNICKS", "LAKERS"]
        self.teamselect_instructions = [
            "CHOOSE YOUR TEAM:",
            "",
            "USE ARROW KEYS TO SELECT",
            "PRESS ENTER TO CONTINUE",
        ]
        self.continue_item = ["Continue", "Quit"]

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.HIGHLIGHT = "green"
        self.start = True

        # fonts
        self.font = pygame.font.Font("images/font.ttf", 74)

        # data
        self.qtr = 1
        self.score = [0, 0]
        self.white = pygame.Color(255, 255, 255)

        # Backgrounds
        self.knicksbackground = pygame.image.load(
            "images/courts/knicks_court_alt.png"
        ).convert()
        self.lakersbackground = pygame.image.load(
            "images/courts/lakers_court_alt.png"
        ).convert()

        # Classes
        self.tipoff = TipOff()

        self.player = Player((250, 450), self.player_group)
        self.inbounder = Inbounder(
            (250, 350),
            self.inbounder_group,
            self.inbounder_is_active,
            self.snap,
        )

        self.testball = TestBall(
            (200, 700),
            (self.testball_group, self.player_group),
        )
        self.testball2 = TestBall(
            (1960, 700),
            (self.testball_group, self.player_group),
        )

        # channels
        if not hasattr(self, "start_channel"):
            self.start_channel = pygame.mixer.Channel(0)

        if not hasattr(self, "tipoff_channel"):
            self.tipoff_channel = pygame.mixer.Channel(1)

        if not hasattr(self, "game_channel"):
            self.game_channel = pygame.mixer.Channel(2)

        # Instructions
        self.instructions = [
            "HOW TO PLAY:",
            "",
            "OFFENSIVE MOVES:",
            "-PASS | A KEY",
            "-SHOOT | W KEY",
            "-SPIN | S AND LEFT OR RIGHT ARROW KEYS",
            "-HALF SPIN | AS AND LEFT OR RIGHT ARROW KEYS",
            "-PUMP | SHIFT KEY",
            "-SIDE STEP | SPACEBAR AND UP OR DOWN KEY",
            "-STEP BACK | SHIFT AND LEFT OR RIGHT KEY",
            "-DUNK | D KEY",
            "-EUROSTEP | SPACEBAR AND SHIFT KEYS",
            "FLOP | WAD KEYS",
            "BALL BEHIND THE BACK | SA KEYS",
            "SWITCH HANDS | SD KEYS" "",
            "DEFENSIVE MOVES:",
            "-BLOCK | W KEY",
            "-SUMMON 2ND MAN | A KEY",
            "-STEAL | D AND LEFT OR RIGHT ARROW KEYS",
            "-DRAYMOND | S KEY",
        ]

        # images/sounds
        self.start_music = pygame.mixer.Sound("images/sounds/start.ogg")
        self.start_music.set_volume(0.2)

        self.game_music = pygame.mixer.Sound("images/sounds/game_music.ogg")
        self.game_music.set_volume(0.2)

        self.highlight_sound = pygame.mixer.Sound("images/sounds/highlight.ogg")
        self.highlight_sound.set_volume(0.05)

        self.confirm_sound = pygame.mixer.Sound("images/sounds/confirm.ogg")
        self.confirm_sound.set_volume(0.05)

        self.start_sound = pygame.mixer.Sound("images/sounds/start_sound.ogg")
        self.start_sound.set_volume(0.05)

        self.tipoff_music = pygame.mixer.Sound("images/sounds/tipoff_music.ogg")
        self.tipoff_music.set_volume(0.2)

        self.tipoff_win_sound = pygame.mixer.Sound("images/sounds/tipoff_win.ogg")
        self.tipoff_win_sound.set_volume(0.05)

        self.tipoff_lose_sound = pygame.mixer.Sound("images/sounds/tipoff_lose.ogg")
        self.tipoff_lose_sound.set_volume(0.05)

        # Load background (Tipoff)
        self.background = None
        self.transparent_background = Background().generate_background()

    # Functions
    def show_qtr(self, qtr, screen):
        self.qtr = qtr % 4
        my_font = pygame.font.Font("images/font.ttf", 50)
        if self.qtr == 1:
            down_surface = my_font.render("1ST QTR", True, "white")
        elif self.qtr == 2:
            down_surface = my_font.render("2ND QTR", True, "white")
        elif self.qtr == 3:
            down_surface = my_font.render("3RD QTR", True, "white")
        elif self.qtr == 0:
            down_surface = my_font.render("4TH QTR", True, "white")

        down_rect = down_surface.get_rect()
        down_rect.midtop = (615, 5)
        screen.blit(down_surface, down_rect)

        return self.qtr

    def show_score(self):
        my_font = pygame.font.Font("images/font.ttf", 50)
        score_surface = my_font.render(
            f"SCORE: {self.score[0]} vs {self.score[1]}", True, self.white
        )
        score_rect = score_surface.get_rect()
        score_rect.midtop = (1050, 5)
        self.screen.blit(score_surface, score_rect)

    def show_startscreen(self):

        my_font = pygame.font.Font("images/font.ttf", 45)
        speed_surface = my_font.render("NBA 2K25", True, "yellow")
        speed_rect = speed_surface.get_rect()
        speed_rect.midtop = (320, 480)
        self.screen.blit(speed_surface, speed_rect)

    def show_startscreensub(self):

        my_font = pygame.font.Font("images/font.ttf", 30)
        speed_surface = my_font.render("A DN INDUSTRIES PRODUCT", True, "yellow")
        speed_rect = speed_surface.get_rect()
        speed_rect.midtop = (320, 515)
        self.screen.blit(speed_surface, speed_rect)

    def show_startscreensub1(self):
        if int(time.time() * 2) % 2 == 0:
            my_font = pygame.font.Font("images/font.ttf", 55)
            speed_surface = my_font.render("PRESS S TO START THE GAME", True, "white")
            speed_rect = speed_surface.get_rect()
            speed_rect.midtop = (806, 605)
            self.screen.blit(speed_surface, speed_rect)

    def logo(self):
        implogo = pygame.image.load("images/logo.png").convert_alpha()
        self.screen.blit(
            implogo,
            pygame.Rect(105, 100, 10, 10),
        )

    def logolakers(self):
        implogolakers = pygame.image.load("images/logolakers.png").convert_alpha()
        self.screen.blit(
            implogolakers,
            pygame.Rect(700, 225, 40, 10),
        )

    def logolakers1(self):
        implogolakers = pygame.image.load("images/logolakers.png").convert_alpha()
        self.screen.blit(
            implogolakers,
            pygame.Rect(150, 175, 10, 10),
        )

    def logoknx(self):
        implogoknx = pygame.image.load("images/logoknx.png").convert_alpha()
        self.screen.blit(
            implogoknx,
            pygame.Rect(210, 225, 10, 10),
        )

    def logoknx1(self):
        implogoknx = pygame.image.load("images/logoknx.png").convert_alpha()
        self.screen.blit(
            implogoknx,
            pygame.Rect(170, 125, 10, 10),
        )

    def howto(self, lines, color, start_pos, line_spacing=5):
        font = pygame.font.Font("images/font.ttf", 30)
        x, y = start_pos
        for line in lines:
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (x, y))
            y += font.get_height() + line_spacing

    def game_loop(self):
        game_loop(self)

    def start_menu(self):
        start_menu(self)

    def playerselect_menu(self):
        playerselect_menu(self)

    def render_playerselect_menu(self):
        render_playerselect_menu(self)

    def teamselect_menu(self):
        teamselect_menu(self)

    def render_teamselect_menu(self):
        render_teamselect_menu(self)

    def howto_menu(self):
        howto_menu(self)

    """Tipoff"""

    def win_condition(self):
        my_font = pygame.font.Font("images/font.ttf", 50)
        score_surface = my_font.render("First to 5 Wins", True, "white")
        score_rect = score_surface.get_rect()
        score_rect.midtop = (1030, 5)
        self.screen.blit(score_surface, score_rect)

    def gameplay_instructions(self):
        my_font = pygame.font.Font("images/font.ttf", 50)
        score_surface = my_font.render("Jump: Spacebar", True, "white")
        score_rect = score_surface.get_rect()
        score_rect.midtop = (190, 5)
        self.screen.blit(score_surface, score_rect)

    def render_start_screen(self):
        render_start_screen(self)

    def start_screen(self):
        start_screen(self)

    def render_continue_menu(self):
        render_continue_menu(self)

    def continue_menu(self):
        continue_menu(self)

    def run(self):
        self.start_menu()
        """
        self.game_loop()
        """


if __name__ == "__main__":
    game = Game()
    game.run()
