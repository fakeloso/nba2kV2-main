import pygame, sys
import time


def start_menu(self):
    # self.win_music.stop()
    # self.lose_music.stop()
    time.sleep(0.4)
    if not self.start_channel.get_busy():
        self.start_channel.play(self.start_music, loops=-1)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.start_sound.play()
                    self.teamselect_menu()

        self.screen.fill(self.BLACK)
        self.logo()
        self.howto(self.instructions, self.WHITE, (575, 50), line_spacing=5)

        self.show_startscreen()
        self.show_startscreensub()
        self.show_startscreensub1()
        pygame.display.flip()

def render_playerselect_menu(self):

    self.screen.fill(self.BLACK)
    teamselect_font = pygame.font.Font("images/font.ttf", 150)
    select_font = pygame.font.Font("images/font.ttf", 50)

    score_surface = teamselect_font.render("PICK UR PLAYER", True, "yellow")
    score_rect = score_surface.get_rect()
    score_rect.midtop = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 10)
    self.screen.blit(score_surface, score_rect)
    
    menu_items = None
    print(self.team)

    if self.team == "LAKERS":
        menu_items = self.playerselectlakers_menu_items
    elif self.team == "KNICKS":
        menu_items = self.playerselectknicks_menu_items

    for index, item in enumerate(menu_items):
        if index == self.selected_index3:
            text_color = self.HIGHLIGHT
            if menu_items[self.selected_index3] != "":
                text_color = "yellow"
        else:
            text_color = self.WHITE

        menu_text = select_font.render(item, True, text_color)
        

        text_rect = menu_text.get_rect(
            center=(
                self.WINDOW_WIDTH / 2 + (index - len(menu_items) // 2) * 200,
                self.WINDOW_HEIGHT // 1.8,
            )
        )
        self.screen.blit(menu_text, text_rect)
        if self.team == "KNICKS":
            self.ps_brunson()
            self.ps_melo()
        elif self.team == "LAKERS":
            self.ps_lebron()


def playerselect_menu(self):

    self.selected_index3 = 0
    running = True

    menu_items = None
    if self.team == "LAKERS":
        menu_items = self.playerselectlakers_menu_items
    elif self.team == "KNICKS":
        menu_items = self.playerselectknicks_menu_items

    # Disable spacebar for a few seconds when the menu is rendered
    self.spacebar_enabled = False
    pygame.time.set_timer(pygame.USEREVENT, 100)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                self.spacebar_enabled = True
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer

            if event.type == pygame.KEYDOWN:
                if not self.spacebar_enabled and event.key == pygame.K_SPACE:
                    continue  # Ignore spacebar presses if disabled

                self.highlight_sound.play()
                if event.key == pygame.K_LEFT:
                    self.highlight_sound.play()
                    self.selected_index3 = (self.selected_index3 - 1) % len(menu_items)
                elif event.key == pygame.K_RIGHT:
                    self.highlight_sound.play()
                    self.selected_index3 = (self.selected_index3 + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:

                    if menu_items[self.selected_index3] == "BRUNSON":
                        self.selectedplayer = "brunson"
                        
                    elif menu_items[self.selected_index3] == "LEBRON":
                        self.selectedplayer = "lebron"
                        
                    elif menu_items[self.selected_index3] == "MELO":
                        self.selectedplayer = "melo"

                    self.confirm_sound.play()
                    self.player.update_selectedplayer(self.selectedplayer)
                    self.inbounder.update_selectedplayer(self.selectedplayer)
                    self.tipoff.update_selectedplayer(self.selectedplayer)
                    self.howto_menu()
                    self.confirm_sound.play()
  
        self.render_playerselect_menu()
        pygame.display.flip()                


def render_teamselect_menu(self):
    self.screen.fill(self.BLACK)
    teamselect_font = pygame.font.Font("images/font.ttf", 150)
    select_font = pygame.font.Font("images/font.ttf", 100)

    score_surface = teamselect_font.render("PICK UR TEAM", True, "yellow")
    score_rect = score_surface.get_rect()
    score_rect.midtop = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 10)
    self.screen.blit(score_surface, score_rect)

    for index, item in enumerate(self.teamselect_menu_items):
        if index == self.team_selected_index:
            text_color = self.HIGHLIGHT
            if self.teamselect_menu_items[self.team_selected_index] == "LAKERS":
                text_color = "purple"
            elif self.teamselect_menu_items[self.team_selected_index] == "KNICKS":
                text_color = "blue"
        else:
            text_color = self.WHITE

        menu_text = select_font.render(item, True, text_color)

        text_rect = menu_text.get_rect(
            center=(
                self.WINDOW_WIDTH / 1.43
                + (index - len(self.teamselect_menu_items) // 2) * 480,
                self.WINDOW_HEIGHT // 1.35,
            )
        )
        self.screen.blit(menu_text, text_rect)
        self.logoknx()
        self.logolakers()


def teamselect_menu(self):
    running = True

    # Disable spacebar for a few seconds when the menu is rendered
    self.spacebar_enabled = False
    pygame.time.set_timer(pygame.USEREVENT, 100)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                self.spacebar_enabled = True
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer

            if event.type == pygame.KEYDOWN:
                if not self.spacebar_enabled and event.key == pygame.K_SPACE:
                    continue  # Ignore spacebar presses if disabled

                self.highlight_sound.play()
                if event.key == pygame.K_LEFT:
                    self.highlight_sound.play()
                    self.team_selected_index = (self.team_selected_index - 1) % len(
                        self.teamselect_menu_items
                    )
                elif event.key == pygame.K_RIGHT:
                    self.highlight_sound.play()
                    self.team_selected_index = (self.team_selected_index + 1) % len(
                        self.teamselect_menu_items
                    )
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:

                    if self.teamselect_menu_items[self.team_selected_index] == "KNICKS":
                        self.team = "knicks"

                    elif (
                        self.teamselect_menu_items[self.team_selected_index] == "LAKERS"
                    ):
                        self.team = "lakers"

                    self.confirm_sound.play()
                    self.playerselect_menu()
                    self.confirm_sound.play()

        self.render_teamselect_menu()
        pygame.display.flip()

def howto_menu(self):
    if not self.start_channel.get_busy():
        self.start_channel.play(self.start_music, loops=-1)
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.start_sound.play()
                    self.start_channel.stop()
                    self.tipoff_music.play(loops=-1)
                    self.start_screen()

        self.screen.fill(self.BLACK)

        if self.team == "knicks":
            self.logoknx1()
        elif self.team == "lakers":
            self.logolakers1()

        self.howto(self.instructions, self.WHITE, (575, 50), line_spacing=5)
        self.show_startscreen()
        self.show_startscreensub()
        self.show_startscreensub1()
        pygame.display.flip()


"""Tipoff"""


def render_start_screen(self):
    self.screen.blit(self.background, (-462, 80))
    self.screen.blit(self.transparent_background, (0, 0))

    # Create a semi-transparent overlay
    overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)

    # Set the overlay color and transparency (RGBA format)
    overlay.fill((0, 0, 0, 128))  # Black with 50% transparency

    continue_font = pygame.font.Font("images/font.ttf", 120)
    select_font = pygame.font.Font("images/font.ttf", 100)

    select_font2 = pygame.font.Font("images/font.ttf", 40)

    if self.team == "knicks":
        menu_text = "GET READY!"
        menu_color = "orange"
    else:
        menu_text = "GET READY!"
        menu_color = "yellow"

    menu_surface = continue_font.render(menu_text, True, menu_color)
    menu_rect = menu_surface.get_rect(
        midtop=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 5)
    )
    self.screen.blit(overlay, (0, 0))
    self.screen.blit(menu_surface, menu_rect)

    continue_surface = select_font.render("Start", True, menu_color)
    continue_rect = continue_surface.get_rect(
        center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 2)
    )
    continue_surface2 = select_font2.render("(Press Spacebar)", True, menu_color)
    continue_rect2 = continue_surface2.get_rect(
        center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 1.7)
    )
    self.screen.blit(continue_surface, continue_rect)
    self.screen.blit(continue_surface2, continue_rect2)


def start_screen(self):
    if self.team == "knicks":
        self.background = pygame.image.load(
            "images/courts/knicks_court_alt.png"
        ).convert()
    else:
        self.background = pygame.image.load(
            "images/courts/lakers_court_alt.png"
        ).convert()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pygame.K_SPACE = 32
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):

                    self.winner = self.tipoff.run(
                        self.team, self.background, self.continue_menu
                    )

        self.render_start_screen()
        self.win_condition()
        self.gameplay_instructions()

        pygame.display.update()

        pygame.display.flip()


def render_continue_menu(self):
    self.screen.fill("black")

    continue_font = pygame.font.Font("images/font.ttf", 150)
    select_font = pygame.font.Font("images/font.ttf", 100)

    if self.winner:
        if self.team == "knicks":
            menu_text = "KNICKS BALL"
            menu_color = "orange"
        elif self.team == "LAKERS":
            menu_text = "LAKERS BALL"
            menu_color = "yellow"
    elif not self.winner:
        if self.team == "lakers":
            menu_text = "LAKERS BALL"
            menu_color = "yellow"
        elif self.team == "knicks":
            menu_text = "KNICKS BALL"
            menu_color = "orange"
    else:
        menu_text = "DRAW"
        menu_color = "red"

    menu_surface = continue_font.render(menu_text, True, menu_color)
    menu_rect = menu_surface.get_rect(
        midtop=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT / 5)
    )
    self.screen.blit(menu_surface, menu_rect)

    base_y = self.WINDOW_HEIGHT / 2 + 10  # Start lower on the screen
    spacing = 120  # Adjust spacing between items

    for index, item in enumerate(self.continue_item):
        text_color = (
            "red"
            if item == "Quit" and index == self.continue_selected_index
            else "green" if index == self.continue_selected_index else "white"
        )

        menu_text = select_font.render(item, True, text_color)
        text_rect = menu_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, base_y + index * spacing)
        )
        self.screen.blit(menu_text, text_rect)


def continue_menu(self):
    self.spacebar_enabled = False
    pygame.time.set_timer(pygame.USEREVENT, 100)

    running = True
    while running:
        self.render_continue_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT:
                self.spacebar_enabled = True
                pygame.time.set_timer(pygame.USEREVENT, 0)

            if event.type == pygame.KEYDOWN:
                if not self.spacebar_enabled and event.key == pygame.K_SPACE:
                    continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.highlight_sound.play()
                    self.continue_selected_index = (
                        self.continue_selected_index - 1
                    ) % len(self.continue_item)

                elif event.key == pygame.K_DOWN:
                    self.highlight_sound.play()
                    self.continue_selected_index = (
                        self.continue_selected_index + 1
                    ) % len(self.continue_item)

                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.confirm_sound.play()
                    if self.continue_item[self.continue_selected_index] == "Quit":
                        pygame.quit()
                        sys.exit()

                    elif self.continue_item[self.continue_selected_index] == "Continue":
                        self.game_loop()

        pygame.display.flip()
