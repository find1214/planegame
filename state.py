import pygame, sys, random, math

# 내부 모듈
from config        import *
from player        import Player
from difficulty    import DifficultyManager
from score         import ScoreManager
from bullet        import Bullet
from boss          import Boss
from item          import Item
from achievements  import Achievements
from upgrades      import MetaManager
from planes        import PLANES
from shop_state    import ShopState         # ← 별도 파일

# ───────────────────────────────────────────────────
class State:         # 간단 추상 기반
    def __init__(self, game): self.game = game
    def handle(self, events): ...
    def update(self, dt): ...
    def draw  (self, surf):  ...

# ───────────────────────────────────────────────────
class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.fb = pygame.font.SysFont(None, 56)
        self.fs = pygame.font.SysFont(None, 24)

    def handle(self, events):
        for e in events:
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:      # ▶ 게임 시작
                    self.game.change_state(PlayState(self.game))
                if e.key == pygame.K_u:           # ▶ 업그레이드/기체 상점
                    self.game.change_state(ShopState(self.game, self))

    def update(self, dt): pass

    def draw(self, s):
        s.fill(BLACK)
        title = self.fb.render("PLANE  DODGE", True, WHITE)
        s.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 60)))

        # 키 안내
        msgs = [
            "ENTER :  Start Game",
            "U     :  Upgrades / Planes",
            "Arrow :  Move      |  Shift : Slow Move",
            "Space :  Slomo     |  X : Bomb",
            "H     :  Show/Hide HitBox",
            "ESC   :  Quit (in‑game over screen)",
        ]
        for i, m in enumerate(msgs):
            txt = self.fs.render(m, True, WHITE)
            s.blit(txt, (SCREEN_WIDTH/2 - txt.get_width()/2, SCREEN_HEIGHT/2 + 10 + i*24))

# ───────────────────────────────────────────────────
class PlayState(State):
    def __init__(self, game):
        super().__init__(game)

        # --- 메타 정보 & 기체 능력 반영 -------------------
        self.mm = MetaManager()
        p_cfg   = PLANES[self.mm.active()]

        self.player   = Player()
        self.player.base_speed = p_cfg["speed"] * (1 + 0.1*self.mm.level("speed"))
        self.player.hit_r      = max(3, p_cfg["hit_r"] - self.mm.level("hitbox"))

        # 시작 자원
        self.lives  = 3 + p_cfg["lives"] + self.mm.level("life")
        self.slo    = SLOMO_CHARGES + p_cfg["slomo"] + self.mm.level("slomo")
        self.bombs  = BOMB_COUNT + p_cfg["bombs"] + self.mm.level("bomb")

        # 매니저
        self.diff   = DifficultyManager()
        self.score  = ScoreManager()
        self.achv   = Achievements()

        # 엔티티
        self.bullets=[]; self.items=[]
        self.boss   = None

        # 상태 변수
        self.slo_timer = 0.0; self.time_scale = 1.0
        self.flash = 0.0; self.shake = 0.0; self.show_hit = SHOW_HITBOX_DEF

        # 타이머
        self.next_boss = BOSS_INTERVAL
        self.item_timer= 0.0

        # 통계(업적)
        self.time_surv = 0.0; self.no_hit = 0.0
        self.item_col  = 0;   self.slo_used=0; self.bomb_used=0
        self.boss_surv = 0;   self.graze_total=0

        self.font_ui = pygame.font.SysFont(None, 22)
        self.messages=[]

    # --------------------------------------------------
    def handle(self, events):
        for e in events:
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                # 슬로모
                if e.key == pygame.K_SPACE and self.slo > 0 and self.slo_timer <= 0:
                    self.time_scale = SLOMO_FACTOR
                    self.slo_timer  = SLOMO_DURATION
                    self.slo       -= 1; self.slo_used+=1
                # 폭탄
                if e.key == pygame.K_x and self.bombs > 0:
                    self.bullets.clear()
                    self.bombs     -= 1; self.bomb_used+=1
                    self.shake = SHAKE_DURATION
                # 히트박스 토글
                if e.key == pygame.K_h:
                    self.show_hit = not self.show_hit

    # --------------------------------------------------
    def update(self, dt):
        # ----- 슬로모/타임스케일 -----
        if self.slo_timer > 0:
            self.slo_timer -= dt
            if self.slo_timer <= 0: self.time_scale = 1.0
        dtt = dt * self.time_scale

        # ----- 시간 누적 -----
        self.time_surv += dtt; self.no_hit += dtt

        # ----- 난이도/스폰 -----
        if self.diff.update(dtt): self.score.stage(self.diff.idx)
        self.diff.spawn(self.bullets, self.player)

        # ----- 보스 -----
        if self.diff.elapsed >= self.next_boss and self.boss is None:
            self.boss = Boss(self.diff.cur.spd * 0.8)
        if self.boss:
            self.boss.update(dtt, self.bullets)
            if self.boss.expired():
                self.boss_surv += 1
                self.boss = None
                self.next_boss += BOSS_INTERVAL

        # ----- 아이템 스폰 -----
        self.item_timer += dtt
        if self.item_timer >= ITEM_INTERVAL:
            kind = random.choice(("slow", "bomb", "coin"))
            self.items.append(Item(kind))
            self.item_timer = 0.0

        # ----- 플레이어 이동 -----
        self.player.update(pygame.key.get_pressed())

        # ----- 탄환 충돌 -----
        graze_frame = False
        for b in self.bullets[:]:
            b.update(dtt)
            if b.offscreen():
                self.bullets.remove(b); continue

            if self.player.hit_check(b):
                self.lives -= 1
                self.no_hit = 0
                self.score.hit()
                self.flash, self.shake = FLASH_DURATION, SHAKE_DURATION
                self.bullets.remove(b)
                if self.lives <= 0:
                    self.end_run(); return

            elif self.player.graze_check(b):
                graze_frame = True
                self.score.graze(abs(b.vy))
                self.graze_total += 1

        # ----- 점수·콤보 -----
        self.score.surv(dtt, self.diff.idx * 10)
        self.score.step(dtt)

        # ----- 아이템 충돌 -----
        for it in self.items[:]:
            it.update(dtt)
            if it.offscreen():
                self.items.remove(it); continue
            dist= math.hypot(self.player.center_x - it.x, self.player.center_y - it.y)
            if dist <= it.radius + PLAYER_SIZE/2:
                self.items.remove(it); self.item_col += 1
                if it.kind=="slow":   self.slo  += 1; self.messages.append("SLOW +1")
                elif it.kind=="bomb": self.bombs+= 1; self.messages.append("BOMB +1")
                elif it.kind=="coin": self.mm.add_coins(20); self.messages.append("COIN +20")

        # ----- 연출 타이머 -----
        if self.flash>0: self.flash-=dt
        if self.shake>0: self.shake-=dt

        # ----- 업적 체크 -----
        self.achv.check(self)

    # --------------------------------------------------
    def draw(self, s):
        ox = random.randint(-SHAKE_MAG,SHAKE_MAG) if self.shake>0 else 0
        oy = random.randint(-SHAKE_MAG,SHAKE_MAG) if self.shake>0 else 0
        s.fill(BLACK)

        # 히트박스 / Graze 링
        if self.show_hit:
            pygame.draw.circle(s, GRAZE_COLOR, (int(self.player.center_x+ox),int(self.player.center_y+oy)),
                               self.player.hit_r, 1)
        pygame.draw.circle(s, GRAZE_COLOR, (int(self.player.center_x+ox),int(self.player.center_y+oy)),
                           PLAYER_GRAZE_R, 1)

        # 엔티티
        if self.boss: self.boss.draw(s,ox,oy)
        self.player.draw(s,ox,oy)
        for b  in self.bullets: b.draw(s,ox,oy)
        for it in self.items:  it.draw(s,ox,oy)

        # UI
        ui = f"S{int(self.score.total)}  L{self.lives}  Sl{self.slo}  B{self.bombs}  ₵{self.mm.coins}"
        s.blit(self.font_ui.render(ui, True, WHITE), (10, 8))

        # 최근 메시지
        if self.messages:
            msg = self.font_ui.render(self.messages[-1], True, COIN_COLOR)
            s.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 40))

        # 피격 플래시
        if self.flash>0 and int(self.flash*20)%2==0:
            overlay=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
            overlay.fill((255,50,50,120)); s.blit(overlay,(0,0))

    # --------------------------------------------------
    def end_run(self):
        # 코인 적립 = 점수 //10
        earned = int(self.score.total)//10
        self.mm.add_coins(earned)
        board = self.score.finalize()
        self.game.change_state(GameOverState(self.game, int(self.score.total), earned, board))

# ───────────────────────────────────────────────────
class GameOverState(State):
    def __init__(self, game, sc: int, earned: int, board: list[int]):
        super().__init__(game)
        self.sc=sc; self.earned=earned; self.board=board
        self.big=pygame.font.SysFont(None,64)
        self.sm =pygame.font.SysFont(None,24)

    def handle(self,events):
        for e in events:
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_r: self.game.change_state(PlayState(self.game))
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()

    def update(self,dt): pass
    def draw(self,s):
        s.fill(BLACK)
        s.blit(self.big.render("GAME  OVER",True,WHITE),(SCREEN_WIDTH/2-160,60))
        s.blit(self.sm .render(f"SCORE : {self.sc}",True,WHITE),(SCREEN_WIDTH/2-90,140))
        s.blit(self.sm .render(f"COINS +{self.earned}",True,COIN_COLOR),(SCREEN_WIDTH/2-90,170))
        s.blit(self.sm.render("TOP  10",True,WHITE),(SCREEN_WIDTH/2-40,210))
        for i,val in enumerate(self.board):
            t=self.sm.render(f"{i+1:>2}.  {val}",True,WHITE)
            s.blit(t,(SCREEN_WIDTH/2-60,240+i*24))
        hint=self.sm.render("R:Restart    ESC:Quit",True,WHITE)
        s.blit(hint,hint.get_rect(center=(SCREEN_WIDTH/2,520)))
