"""
난이도·탄환 스폰 매니저
────────────────────────────────────────
• Stage  : t(초), spd(px/s), iv(스폰 간격), sp(스폰 함수 리스트)
• update : 경과 시간을 누적, 스테이지 상승 여부(True/False) 반환
• spawn  : interval마다 탄환 또는 JSON 패턴을 bullets 리스트에 추가
           - player 인자를 받아 유도탄 패턴에 전달
"""

import random
from dataclasses import dataclass
from typing import List, Callable

from bullet import (
    spawn_straight,
    spawn_diagonal,
    spawn_fan5,
    spawn_dart,
)
from pattern_loader import load_patterns, spawn_pattern
from config import FPS

# ───────────────────────────────────────────────────
# 1) 스테이지 테이블
#    0~15초 동안 3단계 압축 → 15초 시점에 “1분 난이도”
# ───────────────────────────────────────────────────
@dataclass
class Stage:
    t:   int                # 시작 시점(초)
    spd: float              # 탄 속도(px/s)
    iv:  float              # 발사 간격(초)
    sp:  List[Callable]     # 스폰 함수 리스트

STAGES: List[Stage] = [
    Stage( 0, 240, 0.60, [spawn_straight, spawn_diagonal]),
    Stage( 5, 300, 0.50, [spawn_straight, spawn_diagonal]),
    Stage(15, 360, 0.40, [spawn_straight, spawn_diagonal, spawn_fan5]),
    Stage(30, 420, 0.35, [spawn_straight, spawn_diagonal, spawn_fan5, spawn_dart]),
    Stage(50, 480, 0.30, [spawn_straight, spawn_diagonal, spawn_fan5, spawn_dart]),
]

# 러시(동시 추가 발사) 확률·개수
RUSH_PROB:  float = 0.35
RUSH_COUNT: int   = 4

# JSON 데이터 패턴 불러오기 (앱 최초 1회)
PATTERNS = load_patterns()

# ───────────────────────────────────────────────────
class DifficultyManager:
    def __init__(self) -> None:
        self.elapsed: float = 0.0
        self.idx:     int   = 0
        self.cur:     Stage = STAGES[0]
        self.timer:   float = 0.0

    # ------------------------------------------------
    def update(self, dt: float) -> bool:
        """
        dt : 이번 프레임 경과 시간(초)
        return : 스테이지가 상승한 경우 True (점수 보너스용)
        """
        self.elapsed += dt
        # 스테이지 전환 체크
        if self.idx + 1 < len(STAGES) and self.elapsed >= STAGES[self.idx + 1].t:
            self.idx += 1
            self.cur  = STAGES[self.idx]
            return True
        return False

    # ------------------------------------------------
    def spawn(self, bullets: list, player=None) -> None:
        """
        • 매 프레임 호출
        • 내부 타이머가 current.iv 를 넘으면 탄/패턴을 생성
        • 50 % 확률로 JSON 패턴, 50 % 기존 함수형 스폰
        • RUSH_PROB 확률로 대각선 탄 4발 추가
        """
        self.timer += 1 / FPS
        if self.timer < self.cur.iv:
            return

        # --- ① JSON 패턴 or ② 하드코딩 패턴 선택 ------------
        if PATTERNS and random.random() < 0.5:
            data = random.choice(PATTERNS)
            spawn_pattern(data, self.cur.spd, bullets, player)
        else:
            spawner = random.choice(self.cur.sp)
            spawned = spawner(self.cur.spd)
            bullets.extend(spawned if isinstance(spawned, list) else [spawned])

        # --- 러시 추가 발사 ---------------------------------
        if random.random() < RUSH_PROB:
            for _ in range(RUSH_COUNT):
                bullets.append(spawn_diagonal(self.cur.spd))

        self.timer = 0.0  # 타이머 리셋
