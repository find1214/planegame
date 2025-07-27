import pygame
import sys

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from state import MenuState  # state.py 안의 첫 진입 상태(메뉴)


class Game:
    """
    ‣ PyGame 초기화
    ‣ 상태(State) 관리 : MenuState → PlayState → GameOverState …
    ‣ 메인 루프 : 이벤트 → 업데이트 → 렌더 → 화면 스왑
    """

    def __init__(self) -> None:
        pygame.init()
        # ── 창 생성 ──
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Plane Dodge – Minimal Bullet‑Hell")

        # ── 전역 상태 ──
        self.clock = pygame.time.Clock()
        self.state = MenuState(self)  # state 객체는 자신이 Game을 받아 내부에서 change_state 호출

    # 외부(각 State)에서 상태 전환 시 사용 ------------------
    def change_state(self, new_state):
        """현재 state 객체를 새로운 state로 교체"""
        self.state = new_state

    # ── 메인 루프 ──────────────────────────────────────────
    def run(self) -> None:
        while True:
            dt_sec = self.clock.tick(FPS) / 1000  # 이번 프레임 경과 시간(초)

            events = pygame.event.get()  # 모든 이벤트 가져오기
            self.state.handle(events)  # 현재 상태에 이벤트 전달
            self.state.update(dt_sec)  # 게임 로직 업데이트
            self.state.draw(self.screen)  # 화면 그리기
            pygame.display.flip()  # 더블 버퍼 스왑


# ── 엔트리 포인트 ─────────────────────────────────────────
if __name__ == "__main__":
    try:
        Game().run()
    except Exception as e:
        # 예외 발생 시 PyGame 종료 후 traceback 표시
        pygame.quit()
        raise e
