import pygame


class Log:
    """A horizontally moving raft that carries the player while they stand on it."""

    HEIGHT = 34
    COLOR = (125, 78, 42)
    EDGE_COLOR = (75, 46, 25)

    def __init__(self, x, y, width, speed, screen_width):
        self.rect = pygame.Rect(x, y, width, self.HEIGHT)
        self.speed = speed
        self.screen_width = screen_width

    def update(self):
        """Move horizontally and bounce cleanly at either screen edge."""
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed = abs(self.speed)
        elif self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.speed = -abs(self.speed)

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, self.rect, border_radius=9)
        pygame.draw.rect(screen, self.EDGE_COLOR, self.rect, width=3, border_radius=9)
        # Simple timber details make the raft easy to identify.
        for x in range(self.rect.left + 12, self.rect.right - 6, 22):
            pygame.draw.line(screen, (175, 119, 68),
                             (x, self.rect.top + 5), (x, self.rect.bottom - 5), 2)
