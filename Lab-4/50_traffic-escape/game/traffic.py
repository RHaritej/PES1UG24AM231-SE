import pygame
import random

LANE_W = 80
COLORS = [(220, 60, 60), (220, 140, 40), (140, 60, 180),
          (60, 180, 80), (180, 180, 40), (60, 80, 200)]

# Cached translucent light cones: constructed once, not every frame.
_HEADLIGHT_CONES = {}


def _headlight_cone(direction):
    """Return a cached transparent cone extending in the car's travel direction."""
    if direction not in _HEADLIGHT_CONES:
        width, height = 110, 155
        cone = pygame.Surface((width, height), pygame.SRCALPHA)
        # Subtle broad beam, brightest near the lamps and transparent farther away.
        if direction == 1:
            pygame.draw.polygon(cone, (255, 226, 135, 24),
                                [(width // 2 - 13, 0), (width // 2 + 13, 0),
                                 (width - 3, height), (3, height)])
            pygame.draw.ellipse(cone, (255, 236, 175, 24),
                                pygame.Rect(14, 0, width - 28, 45))
        else:
            pygame.draw.polygon(cone, (255, 226, 135, 24),
                                [(3, 0), (width - 3, 0),
                                 (width // 2 + 13, height), (width // 2 - 13, height)])
            pygame.draw.ellipse(cone, (255, 236, 175, 24),
                                pygame.Rect(14, height - 45, width - 28, 45))
        _HEADLIGHT_CONES[direction] = cone
    return _HEADLIGHT_CONES[direction]


class Car:
    def __init__(self, lane_x, y, direction, speed):
        self.rect = pygame.Rect(lane_x + 10, y, 60, 80)
        self.direction = direction  # 1=down, -1=up
        self.speed = speed
        self.color = random.choice(COLORS)

    def update(self):
        self.rect.y += self.direction * self.speed

    def off_screen(self, height):
        return self.rect.top > height + 100 or self.rect.bottom < -100

    def draw(self, screen, night=False):
        # Draw the cone before the vehicle so the lamps and car body stay crisp.
        if night:
            cone = _headlight_cone(self.direction)
            cone_x = self.rect.centerx - cone.get_width() // 2
            if self.direction == 1:
                cone_y = self.rect.bottom - 2
            else:
                cone_y = self.rect.top - cone.get_height() + 2
            screen.blit(cone, (cone_x, cone_y))

        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (180, 220, 240),
                         pygame.Rect(self.rect.x + 8, self.rect.y + 10, 44, 22),
                         border_radius=4)
        for wx in [self.rect.x + 6, self.rect.right - 16]:
            for wy in [self.rect.y + 4, self.rect.bottom - 16]:
                pygame.draw.rect(screen, (30, 30, 30),
                                 pygame.Rect(wx, wy, 10, 12), border_radius=3)

        if night:
            # Headlamp dots are intentionally bright against the night palette.
            lamp_y = self.rect.bottom - 4 if self.direction == 1 else self.rect.top + 1
            lamp_color = (255, 246, 190)
            for lamp_x in (self.rect.left + 12, self.rect.right - 18):
                pygame.draw.circle(screen, (255, 221, 105),
                                   (lamp_x + 5, lamp_y + (1 if self.direction == 1 else 0)), 7)
                pygame.draw.circle(screen, lamp_color,
                                   (lamp_x + 5, lamp_y + (1 if self.direction == 1 else 0)), 3)


def make_car(lane_idx, height, speed):
    x = lane_idx * LANE_W
    direction = 1 if lane_idx % 2 == 0 else -1
    y = -90 if direction == 1 else height + 10
    return Car(x, y, direction, speed)
