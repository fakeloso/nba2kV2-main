import pygame


class Background:
    def __init__(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1215, 812
        self.running = True

        # Colors for spotlight effect
        self.spotlight_center = (50, 50, 50)  # Dark Gray (center of light)
        self.spotlight_edge = (0, 0, 0)  # Black (edges and outside light area)

    def generate_background(self):
        background_surface = pygame.Surface(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA
        )
        background_surface.fill((0, 0, 0, 190))  # Transparency level

        return background_surface

    def generate_spotlight(self):
        spotlight_surface = pygame.Surface(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA
        )
        center_x, center_y = self.WINDOW_WIDTH // 2.1, self.WINDOW_HEIGHT // 4
        bottom_y = self.WINDOW_HEIGHT
        top_cone_width = self.WINDOW_WIDTH // 3
        bottom_cone_width = self.WINDOW_WIDTH // 2

        for y in range(self.WINDOW_HEIGHT):
            current_width = top_cone_width + (
                (bottom_cone_width - top_cone_width) * (y / self.WINDOW_HEIGHT)
            )
            left_x = int(center_x - current_width // 2)
            right_x = int(center_x + current_width // 1.5)

            for x in range(left_x, right_x):
                if 0 <= x < self.WINDOW_WIDTH:
                    distance = (y - center_y) / (bottom_y - center_y)
                    ratio = min(distance, 1)
                    color = (
                        max(
                            0,
                            min(
                                255,
                                int(
                                    (1 - ratio) * self.spotlight_center[0]
                                    + ratio * self.spotlight_edge[0]
                                ),
                            ),
                        ),
                        max(
                            0,
                            min(
                                255,
                                int(
                                    (1 - ratio) * self.spotlight_center[1]
                                    + ratio * self.spotlight_edge[1]
                                ),
                            ),
                        ),
                        max(
                            0,
                            min(
                                255,
                                int(
                                    (1 - ratio) * self.spotlight_center[2]
                                    + ratio * self.spotlight_edge[2]
                                ),
                            ),
                        ),
                        max(0, min(255, int(255 * (1 - ratio)))),
                    )
                    spotlight_surface.set_at((x, y), color)

        return spotlight_surface
