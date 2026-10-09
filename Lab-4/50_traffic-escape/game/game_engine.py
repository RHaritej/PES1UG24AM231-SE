import pygame
import random
import time
from game.player import Player, LANE_W
from game.traffic import make_car
from game.log import Log
from game.high_scores import load_scores, record_score

LANES = 8
WIDTH = LANES * LANE_W
HEIGHT = 600
FPS = 60
BG = (60, 60, 60)
DAY_NIGHT_INTERVAL = 30.0  # Required 30-second interval per README

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
        self.small_font = pygame.font.SysFont("monospace", 17, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 44, bold=True)
        self.high_scores = load_scores()
        self.cycle_start_time = time.monotonic()
        self.is_night = False
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
        self._riding_log_x = 0
        self.score_recorded = False

    def _update_day_night(self, elapsed_seconds=None):
        """Update the day/night phase using elapsed real seconds.

        elapsed_seconds is optional to make the 30-second transition easy to
        verify in tests without changing the production interval.
        """
        if elapsed_seconds is None:
            elapsed_seconds = time.monotonic() - self.cycle_start_time
        phase = int(max(0.0, elapsed_seconds) // DAY_NIGHT_INTERVAL) % 2
        self.is_night = (phase == 1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
        return True

    def _in_water(self):
        return self.player.rect.centery >= WATER_TOP and self.player.rect.centery < WATER_BOTTOM

    def _record_finished_run(self):
        """Persist a run exactly once, when it ends by loss or victory."""
        if self.score_recorded:
            return
        # The HUD's score is measured in tenths of a second/frame groups.
        self.high_scores = record_score(self.score // 10)
        self.score_recorded = True

    def _lose_life(self):
        """Lose one life once, then respawn outside the hazard area."""
        if self.respawn_invulnerability > 0 or self.game_over:
            return
        self.lives -= 1
        self.riding_log = None
        if self.lives <= 0:
            self.lives = 0
            self.game_over = True
            self._record_finished_run()
            return
        self.player.rect.center = (WIDTH // 2, HEIGHT - 80)
        self.player.move_cooldown = 12
        self.respawn_invulnerability = 60

    def update(self):
        self._update_day_night()
        if self.game_over or self.won:
            return

        if self.respawn_invulnerability > 0:
            self.respawn_invulnerability -= 1

        # Update platforms first so a player riding one is carried this frame.
        for log in self.logs:
            log.update()

        keys = pygame.key.get_pressed()
        was_in_water = self._in_water()
        if was_in_water and self.riding_log is not None:
            dx = self.riding_log.rect.x - self._riding_log_x
            self.player.rect.x += dx
            self.player.rect.x = max(0, min(WIDTH - self.player.rect.width, self.player.rect.x))
        self.player.move(keys, 0, WIDTH)

        # Determine support only while the player's centre is in the water lane.
        self.riding_log = None
        if self._in_water():
            for log in self.logs:
                if (log.rect.colliderect(self.player.rect)
                        and log.rect.left <= self.player.rect.centerx <= log.rect.right):
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
            self._record_finished_run()

    def draw(self):
        # Keep the same layout, but use a strong palette change at night.
        background = (12, 17, 32) if self.is_night else BG
        road_marking = (65, 76, 105) if self.is_night else (100, 100, 100)
        lane_paint = (105, 105, 75) if self.is_night else (200, 200, 100)
        sidewalk = (65, 68, 82) if self.is_night else (150, 130, 110)
        water_color = (8, 35, 83) if self.is_night else WATER_COLOR
        water_ripple = (24, 65, 125) if self.is_night else (45, 135, 185)
        self.screen.fill(background)

        # Original roadway and lane markings.
        for i in range(LANES + 1):
            pygame.draw.line(self.screen, road_marking,
                             (i * LANE_W, 0), (i * LANE_W, HEIGHT), 2)
        for y in range(0, HEIGHT, 60):
            for i in range(LANES):
                pygame.draw.rect(self.screen, lane_paint,
                                 pygame.Rect(i * LANE_W + LANE_W // 2 - 3, y, 6, 30))

        pygame.draw.rect(self.screen, sidewalk, pygame.Rect(0, HEIGHT - 50, WIDTH, 50))
        pygame.draw.rect(self.screen, sidewalk, pygame.Rect(0, 0, WIDTH, 30))

        for car in self.cars:
            car.draw(self.screen, night=self.is_night)

        # Paint the water over the road/cars to make the crossing obvious.
        pygame.draw.rect(self.screen, water_color,
                         pygame.Rect(0, WATER_TOP, WIDTH, WATER_BOTTOM - WATER_TOP))
        for y in range(WATER_TOP + 12, WATER_BOTTOM, 24):
            pygame.draw.line(self.screen, water_ripple, (0, y), (WIDTH, y), 1)
        label = self.font.render("WATER: stay on a moving log!", True, (245, 245, 245))
        self.screen.blit(label, (8, WATER_TOP - 22))
        phase_label = "NIGHT" if self.is_night else "DAY"
        phase_color = (255, 222, 130) if self.is_night else (255, 255, 255)
        phase_surface = self.small_font.render(phase_label, True, phase_color)
        self.screen.blit(phase_surface, (WIDTH - phase_surface.get_width() - 8, 42))
        for log in self.logs:
            log.draw(self.screen)

        # Brief flicker after respawn prevents immediate repeat hits.
        if self.respawn_invulnerability == 0 or self.respawn_invulnerability % 8 < 4:
            self.player.draw(self.screen)

        hud = pygame.Rect(0, 0, WIDTH, 30)
        pygame.draw.rect(self.screen, (5, 8, 18) if self.is_night else (20, 20, 20), hud)
        status = self.font.render(
            f"Score: {self.score // 10}  Lives: {self.lives}  GOAL: reach top  R=Restart",
            True, (240, 240, 240))
        self.screen.blit(status, (6, 5))

        if self.game_over:
            self._msg("GAME OVER!", (220, 60, 60))
        elif self.won:
            self._msg("YOU MADE IT!", (80, 220, 80))
        pygame.display.flip()

    def _msg(self, text, color):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))
        message = self.big_font.render(text, True, color)
        self.screen.blit(message, (WIDTH // 2 - message.get_width() // 2, 125))

        final_score = self.small_font.render(
            f"Your score: {self.score // 10}", True, (245, 245, 245))
        self.screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 190))

        title = self.font.render("TOP 5 HIGH SCORES", True, (255, 220, 100))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 235))
        if not self.high_scores:
            empty = self.small_font.render("No scores saved yet", True, (220, 220, 220))
            self.screen.blit(empty, (WIDTH // 2 - empty.get_width() // 2, 275))
        else:
            for index, score in enumerate(self.high_scores[:5], start=1):
                row = self.small_font.render(f"{index}.  {score}", True, (245, 245, 245))
                self.screen.blit(row, (WIDTH // 2 - row.get_width() // 2, 270 + (index - 1) * 27))

        sub = self.font.render("Press R to Restart", True, (200, 200, 200))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 440))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
