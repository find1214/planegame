import json, random, math
from pathlib import Path
from bullet import Bullet, HomingBullet     # (bullet.py 에 추가된 클래스)

PATTERN_DIR = Path("patterns")   # 폴더

def load_patterns():
    patterns = []
    for path in PATTERN_DIR.glob("*.json"):
        with open(path) as f:
            data = json.load(f)
        patterns.append(data)
    return patterns

# --------------------------------------------------
def spawn_pattern(data, speed, bullets, player=None):
    """
    data : 패턴 dict (JSON)
    speed: 난이도 가중 속도
    bullets: bullet 리스트 (PlayState.bullets)
    player : HomingBullet용 플레이어 참조 (optional)
    """
    kind = data["kind"]
    if kind == "spray":
        cx = random.randint(20, 460)
        cy = -10
        for ang in data["angles"]:
            bullets.append(Bullet(cx, cy, ang, speed))
    elif kind == "ring":
        cx = random.randint(40, 440); cy = -30
        n   = data["count"]
        step= 360/n
        for i in range(n):
            bullets.append(Bullet(cx, cy, i*step, speed))
    elif kind == "wall":
        y = -10
        for x in range(0, 480, int(data["gap"])):
            bullets.append(Bullet(x, y, 90, speed))
    elif kind == "homing":
        # player 필수
        cx = random.randint(20,460); cy=-15
        for _ in range(data["count"]):
            bullets.append(HomingBullet(cx, cy, speed*0.8, player, data["turn_rate"]))
