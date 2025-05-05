import pygame


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.WINDOW_WIDTH = 1215
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player, screen, background, down, show_downs, show_score):

        self.offset.x = player.rect.centerx - self.WINDOW_WIDTH / 2

        if self.offset.x < 0:
            self.offset.x = 0

        if self.offset.x > self.WINDOW_WIDTH - 300:
            self.offset.x = self.WINDOW_WIDTH - 300

        screen.blit(background, -self.offset)
        player.draw_speed_meter(screen)

        show_downs(down, screen)
        show_score()

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
