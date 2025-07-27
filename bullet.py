import pygame, math, random
from config import (
    BULLET_OUTER, BULLET_INNER,
    SCREEN_WIDTH, SCREEN_HEIGHT
)

# ───────────────────────────────────────────────
class Bullet:
    """기본 탄: 여러 모양 지원"""
    SHAPES = ("circle", "diamond", "triangle")

    def __init__(self, x, y, angle_deg, speed):
        self.x, self.y = x, y
        self.speed = speed
        rad = math.radians(angle_deg)
        self.vx = math.cos(rad) * speed
        self.vy = math.sin(rad) * speed
        self.radius = 8
        self.shape = random.choice(self.SHAPES)

    # --------------------------
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    # --------------------------
    def draw(self, s, ox=0, oy=0):
        cx, cy = int(self.x + ox), int(self.y + oy)
        r = self.radius
        if self.shape == "circle":
            pygame.draw.circle(s, BULLET_OUTER, (cx, cy), r)
            pygame.draw.circle(s, BULLET_INNER, (cx, cy), r - 3)
        elif self.shape == "diamond":
            pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
            pygame.draw.polygon(s, BULLET_OUTER, pts)
        else:  # triangle
            pts = [(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)]
            pygame.draw.polygon(s, BULLET_OUTER, pts)

    # --------------------------
    def offscreen(self):
        return (
            self.x < -self.radius or self.x > SCREEN_WIDTH + self.radius or
            self.y < -self.radius or self.y > SCREEN_HEIGHT + self.radius
        )

# ───────────────────────────────────────────────
class HomingBullet(Bullet):
    """플레이어를 서서히 향하는 곡선 유도탄"""
    def __init__(self, x, y, speed, player, turn_rate):
        super().__init__(x, y, 90, speed)
        self.player = player
        self.turn_rate = turn_rate  # °/s

    def update(self, dt):
        # 현재·목표 각도 계산
        target = math.degrees(math.atan2(
            self.player.center_y - self.y,
            self.player.center_x - self.x))
        current = math.degrees(math.atan2(self.vy, self.vx))
        diff = (target - current + 540) % 360 - 180   # -180~180

        # 회전 제한
        delta = max(-self.turn_rate * dt, min(self.turn_rate * dt, diff))
        new_ang = current + delta
        rad = math.radians(new_ang)
        self.vx = math.cos(rad) * self.speed
        self.vy = math.sin(rad) * self.speed
        super().update(dt)

# ───────────────────────────────────────────────
# 스폰 헬퍼들 : difficulty.py · JSON 패턴에서 호출
def spawn_straight(speed):
    edge = random.choice(("top", "left", "right"))
    if edge == "top":
        x = random.randint(0, SCREEN_WIDTH)
        return Bullet(x, -10, 90, speed)
    elif edge == "left":
        y = random.randint(0, SCREEN_HEIGHT // 2)
        return Bullet(-10, y, 0, speed)
    else:
        y = random.randint(0, SCREEN_HEIGHT // 2)
        return Bullet(SCREEN_WIDTH + 10, y, 180, speed)

def spawn_diagonal(speed):
    x = random.randint(0, SCREEN_WIDTH)
    ang = random.choice((45, 135))
    return Bullet(x, -10, ang, speed)

def spawn_fan5(speed):
    x = random.randint(0, SCREEN_WIDTH)
    angles = (70, 80, 90, 100, 110)
    return [Bullet(x, -10, a, speed * 0.8) for a in angles]

def spawn_dart(speed):
    x = random.randint(0, SCREEN_WIDTH)
    return Bullet(x, -10, 90, speed * 1.6)

def radial_burst(cx, cy, speed, count):
    """보스용 원형 발사 (360° / count)"""
    step = 360 / count
    return [Bullet(cx, cy, i * step, speed) for i in range(count)]
