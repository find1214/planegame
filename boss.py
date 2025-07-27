from config import (BOSS_DURATION, BOSS_SHOT_INT,
                    BOSS_BURST_COUNT, BOSS_COLOR, SCREEN_WIDTH)
from bullet import radial_burst

class Boss:
    """15초 동안 화면 상단 중앙 고정, 1초마다 원형 탄막."""
    def __init__(self, speed):
        self.x = SCREEN_WIDTH // 2
        self.y = 100
        self.timer = 0.0
        self.time_left = BOSS_DURATION
        self.speed = speed

    def update(self, dt, bullets:list):
        self.time_left -= dt
        self.timer += dt
        if self.timer >= BOSS_SHOT_INT:
            self.timer = 0
            bullets.extend(radial_burst(self.x, self.y, self.speed, BOSS_BURST_COUNT))

    def expired(self):
        return self.time_left <= 0

    def draw(self, surface, ox=0, oy=0):
        import pygame
        pygame.draw.rect(surface, BOSS_COLOR,
                         (self.x-30+ox, self.y-30+oy, 60, 60), 2)
