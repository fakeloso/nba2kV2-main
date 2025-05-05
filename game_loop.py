import pygame, sys
import time


def game_loop(self):
    self.tipoff_music.stop()
    self.game_music.play(loops=-1)
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dt = self.clock.tick() / 1000

        if self.team == "knicks" or self.team == None:
            self.screen.blit(self.knicksbackground, (0, 0))
            self.background = self.knicksbackground
        elif self.team == "lakers":
            self.screen.blit(self.lakersbackground, (0, 0))
            self.background = self.lakersbackground

        self.qtr = self.show_qtr(self.qtr, self.screen)

        self.show_score()

        if self.inbounder_is_active:
            (
                self.inbounder_is_active,
                self.snap,
                self.outOfBounds,
            ) = self.inbounder.update(
                dt,
                events,
                self.outOfBounds,
            )

            self.inbounder.snap_throw_instructions(self.screen)

            # self.testball_group.draw(self.screen)
            self.ball = self.testball.update(self.ball)
            self.ball = self.testball2.update(self.ball)

        else:
            (
                self.inbounder_is_active,
                self.snap,
                self.outOfBounds,
            ) = self.inbounder.update(
                dt,
                events,
                self.outOfBounds,
            )

            self.player_group.customize_draw(
                self.player,
                self.screen,
                self.background,
                self.qtr,
                self.show_qtr,
                self.show_score,
            )

            # self.testball_group.draw(self.screen)
            self.ball = self.testball.update(self.ball)
            self.ball = self.testball2.update(self.ball)

            self.outOfBounds, self.ball = self.player.update(
                dt, events, self.screen, time, self.team, self.winner, self.ball
            )

        if self.outOfBounds:
            self.ball = False
            self.snap = False
            self.qtr += 1

        pygame.display.update()
