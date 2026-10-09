import pygame
import random
from game.player import Player, LANE_W
from game.traffic import make_car
from game.log import Log

LANES = 8
WIDTH = LANES * LANE_W
HEIGHT = 600
FPS = 60
BG = (60, 60, 60)

# A horizontal water crossing; cars are drawn underneath it and do not collide
# with the player while the player is in the water.
WATER_TOP = 220
WATER_BOTTOM = 370
WATER_COLOR = (25, 105, 160)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 19, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.reset()

    def reset(self):
        self.player = Player(WIDTH // 2, HEIGHT - 80)
        self.cars = []
        self.logs = [
            Log(10, WATER_TOP + 18, 145, 2.0, WIDTH),
            Log(245, WATER_TOP + 18, 125, 2.0, WIDTH),
            Log(510, WATER_TOP + 18, 155, 2.0, WIDTH),
            Log(105, WATER_TOP + 92, 155, -2.4, WIDTH),
            Log(370, WATER_TOP + 92, 140, -2.4, WIDTH),
            Log(625, WATER_TOP + 92, 135, -2.4, WIDTH),
        ]
        self.timer = 0
        self.spawn_interval = 50
        self.speed = 3
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.won = False
        self.respawn_invulnerability = 0
        self.riding_log = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
        return True

    def _in_water(self):
        return self.player.rect.centery >= WATER_TOP and self.player.rect.centery < WATER_BOTTOM

    def _lose_life(self):
        """Lose one life once, then respawn outside the hazard area."""
        if self.respawn_invulnerability > 0 or self.game_over:
            return
        self.lives -= 1
        self.riding_log = None
        self.player.rect.center = (WIDTH // 2, HEIGHT - 80)
        self.player.move_cooldown = 12
        self.respawn_invulnerability = 60
        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def update(self):
        if self.game_over or self.won:
            return

        if self.respawn_invulnerability > 0:
            self.respawn_invulnerability -= 1

        # Update platforms first so a player riding one is carried this frame.
        for log in self.logs:
            log.update()

        keys = pygame.key.get_pressed()
        was_in_water = self._in_water()
        previous_player_x = self.player.rect.x
        if was_in_water and self.riding_log is not None:
            # Ride the platform, then allow the player to make a hop.
            dx = self.riding_log.rect.x - getattr(self, "_riding_log_x", self.riding_log.rect.x)
            self.player.rect.x += dx
            self.player.rect.x = max(0, min(WIDTH - self.player.rect.width, self.player.rect.x))
        self.player.move(keys, 0, WIDTH)

        # Determine support only while the player's centre is in the water lane.
        self.riding_log = None
        if self._in_water():
            for log in self.logs:
                if log.rect.colliderect(self.player.rect) and log.rect.left <= self.player.rect.centerx <= log.rect.right:
                    self.riding_log = log
                    break
            if self.riding_log is None:
                self._lose_life()
        self._riding_log_x = self.riding_log.rect.x if self.riding_log else 0

        self.timer += 1
        if self.timer >= self.spawn_interval:
            lane = random.randint(0, LANES - 1)
            self.cars.append(make_car(lane, HEIGHT, self.speed))
            self.timer = 0
            self.spawn_interval = max(22, self.spawn_interval - 0.2)

        for car in self.cars:
            car.update()
            if (self.respawn_invulnerability == 0 and not self._in_water()
                    and car.rect.colliderect(self.player.rect)):
                self._lose_life()
                break
        self.cars = [car for car in self.cars if not car.off_screen(HEIGHT)]

        self.score += 1
        if self.score % 300 == 0:
            self.speed = min(10, self.speed + 0.5)
        if self.player.rect.top <= 30:
            self.won = True

    def draw(self):
        self.screen.fill(BG)

        # Original roadway and lane markings.
        for i in range(LANES + 1):
            pygame.draw.line(self.screen, (100, 100, 100),
                             (i * LANE_W, 0), (i * LANE_W, HEIGHT), 2)
        for y in range(0, HEIGHT, 60):
            for i in range(LANES):
                pygame.draw.rect(self.screen, (200, 200, 100),
                                 pygame.Rect(i * LANE_W + LANE_W // 2 - 3, y, 6, 30))

        pygame.draw.rect(self.screen, (150, 130, 110), pygame.Rect(0, HEIGHT - 50, WIDTH, 50))
        pygame.draw.rect(self.screen, (150, 130, 110), pygame.Rect(0, 0, WIDTH, 30))

        for car in self.cars:
            car.draw(self.screen)

        # Paint the water over the road/cars to make the crossing obvious.
        pygame.draw.rect(self.screen, WATER_COLOR,
                         pygame.Rect(0, WATER_TOP, WIDTH, WATER_BOTTOM - WATER_TOP))
        for y in range(WATER_TOP + 12, WATER_BOTTOM, 24):
            pygame.draw.line(self.screen, (45, 135, 185), (0, y), (WIDTH, y), 1)
        label = self.font.render("WATER: stay on a moving log!", True, (245, 245, 245))
        self.screen.blit(label, (8, WATER_TOP - 22))
        for log in self.logs:
            log.draw(self.screen)

        # Brief flicker after respawn prevents immediate repeat hits.
        if self.respawn_invulnerability == 0 or self.respawn_invulnerability % 8 < 4:
            self.player.draw(self.screen)

        hud = pygame.Rect(0, 0, WIDTH, 30)
        pygame.draw.rect(self.screen, (20, 20, 20), hud)
        status = self.font.render(
            f"Score: {self.score // 10}  Lives: {self.lives}  GOAL: reach top  R=Restart",
            True, (240, 240, 240))
        self.screen.blit(status, (6, 5))

        if self.game_over:
            self._msg("GAME OVER!", (220, 60, 60))
        if self.won:
            self._msg("YOU MADE IT!", (80, 220, 80))
        pygame.display.flip()

    def _msg(self, text, color):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        message = self.big_font.render(text, True, color)
        sub = self.font.render("Press R to Restart", True, (230, 230, 230))
        self.screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 40))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 20))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
