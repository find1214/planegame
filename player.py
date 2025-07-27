import pygame, math
from config import (
    PLAYER_SIZE, PLAYER_COLOR,
    PLAYER_HIT_R, PLAYER_GRAZE_R,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    SLOW_FACTOR
)

class Player:
    """
    · base_speed : Meta 업그레이드/기체에 따라 동적으로 세팅
    · hit_r      : 실제 히트박스 반경 (업그레이드로 감소)
    """
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 90
        self.base_speed = 5
        self.hit_r      = PLAYER_HIT_R

    # ------------------------------------------------
    def update(self, keys):
        spd = self.base_speed
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            spd *= SLOW_FACTOR

        if keys[pygame.K_LEFT] : self.x -= spd
        if keys[pygame.K_RIGHT]: self.x += spd
        if keys[pygame.K_UP]   : self.y -= spd
        if keys[pygame.K_DOWN] : self.y += spd

        self.x = max(0, min(self.x, SCREEN_WIDTH  - PLAYER_SIZE))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - PLAYER_SIZE))

    # ------------------------------------------------
    def draw(self, surface, ox=0, oy=0):
        cx = self.x + PLAYER_SIZE / 2 + ox
        cy = self.y + PLAYER_SIZE / 2 + oy
        tip  = (cx,                 cy - PLAYER_SIZE / 2)
        left = (cx - PLAYER_SIZE/2, cy + PLAYER_SIZE / 2)
        right= (cx + PLAYER_SIZE/2, cy + PLAYER_SIZE / 2)
        pygame.draw.polygon(surface, PLAYER_COLOR, (tip, left, right))

    # ------------------------------------------------
    def _dist(self, b):
        return math.hypot(self.center_x - b.x, self.center_y - b.y)

    def hit_check(self, b):
        return self._dist(b) <= self.hit_r + b.radius

    def graze_check(self, b):
        d = self._dist(b)
        return self.hit_r + b.radius < d <= PLAYER_GRAZE_R + b.radius

    # ------------------------------------------------
    @property
    def center_x(self): return self.x + PLAYER_SIZE / 2
    @property
    def center_y(self): return self.y + PLAYER_SIZE / 2
