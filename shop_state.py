import pygame, sys
from upgrades import MetaManager, UPGRADE_COST, UPGRADE_MAX_LV, PLANE_COST
from planes   import PLANES
from config   import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

class ShopState:
    """
    메뉴에서 'U' 누르면 진입.
    ↑↓ 로 항목 이동, Enter 로 구매/선택, ESC 로 메뉴 복귀
    """
    def __init__(self, game, from_state):
        self.g=game; self.mm=MetaManager(); self.font=pygame.font.SysFont(None,26)
        self.items=[]
        # 업그레이드 항목
        for key,label in [
            ("speed","Speed   +10%/Lv"),
            ("hitbox","HitBox  -1px/Lv"),
            ("life","Lives   +1/Lv"),
            ("slomo","Slomo   +1/Lv"),
            ("bomb","Bomb    +1/Lv")]:
            self.items.append(("up",key,label))
        # 기체 항목
        for code in PLANES:
            if code=="BASIC": continue
            self.items.append(("plane",code,f"Plane {code}"))
        self.idx=0
        self.src=from_state      # 돌아갈 때

    # ------------------------------------------------
    def handle(self,events):
        for e in events:
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE:
                    self.g.change_state(self.src)
                if e.key in (pygame.K_UP,pygame.K_w):
                    self.idx = (self.idx-1)%len(self.items)
                if e.key in (pygame.K_DOWN,pygame.K_s):
                    self.idx = (self.idx+1)%len(self.items)
                if e.key==pygame.K_RETURN:
                    self.activate()

    def activate(self):
        typ,key,_=self.items[self.idx]
        if typ=="up":
            self.mm.buy_upgrade(key)
        else:
            if key in self.mm.unlocked():
                self.mm.set_active(key)
            else:
                self.mm.buy_plane(key)

    # ------------------------------------------------
    def update(self,dt): pass
    def draw(self,s):
        s.fill(BLACK)
        y=40
        title=self.font.render("===  UPGRADES / PLANES  ===",True,WHITE)
        s.blit(title,(SCREEN_WIDTH//2-title.get_width()//2,10))
        coin_txt=self.font.render(f"Coins : {self.mm.coins}",True,WHITE)
        s.blit(coin_txt,(10,10))
        for i,(typ,key,label) in enumerate(self.items):
            selected = (i==self.idx)
            clr = (255,220,0) if selected else WHITE
            if typ=="up":
                lv=self.mm.level(key)
                cost = "-" if lv>=UPGRADE_MAX_LV else UPGRADE_COST(lv)
                txt=f"{label}  Lv {lv}/{UPGRADE_MAX_LV}   Cost {cost}"
            else:
                status="OWNED" if key in self.mm.unlocked() else f"Cost {PLANE_COST[key]}"
                if key == self.mm.active(): status="ACTIVE"
                txt=f"{label:<12} {status}"
            r=self.font.render(txt,True,clr)
            s.blit(r,(40,y)); y+=28
