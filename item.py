import pygame, random
from config import (
    ITEM_INTERVAL, SLOW_ITEM_COLOR, BOMB_ITEM_COLOR,
    COIN_COLOR, SHIELD_ITEM_COLOR, POWER_ITEM_COLOR,
    SCREEN_WIDTH, SCREEN_HEIGHT
)

# 아이템 종류별 색상 매핑
KINDS = {
    "slow"  : SLOW_ITEM_COLOR,
    "bomb"  : BOMB_ITEM_COLOR,
    "coin"  : COIN_COLOR,
    "shield": SHIELD_ITEM_COLOR,   # (향후 확장)
    "power" : POWER_ITEM_COLOR,    # (향후 확장)
}

class Item:
    """파워업/코인 등 필드 아이템"""
    def __init__(self, kind: str):
        self.kind   = kind
        self.color  = KINDS[kind]
        self.radius = 10
        self.x      = random.randint(40, SCREEN_WIDTH - 40)
        self.y      = -20
        self.speed  = 120           # 낙하 속도(px/s)

    # ------------------------------------------------
    def update(self, dt: float):
        self.y += self.speed * dt

    def draw(self, surface, ox=0, oy=0):
        pygame.draw.circle(surface, self.color,
                           (int(self.x + ox), int(self.y + oy)), self.radius)

    def offscreen(self) -> bool:
        return self.y > SCREEN_HEIGHT + 20
