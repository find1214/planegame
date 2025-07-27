import json, os
# ─ 점수 상수 ─
BASE_PPS = 10
BASE_GRAZE = 20
GRAZE_MULT_INC = 0.1    # 위험할수록(탄속) 가중
COMBO_TIME = 10
# ─────────────────
class ScoreManager:
    def __init__(s):
        s.total=0; s.combo=1; s.ctimer=0
        s.graze_chain=0
    def surv(s,dt,threat): s.total+= (BASE_PPS+threat)*dt
    def graze(s,spd):
        s.graze_chain+=1
        mult=1+ GRAZE_MULT_INC*spd/100
        s.total+= BASE_GRAZE*mult*s.combo
    def hit(s): s.combo=1; s.ctimer=0; s.graze_chain=0
    def step(s,dt):
        s.ctimer+=dt
        if s.ctimer>=COMBO_TIME:
            s.combo+=1; s.ctimer=0
    # ── 보너스 ──
    def stage(s,lvl): s.total+=100*lvl
    # ── 리더보드 ──
    def finalize(s):
        path="scores.json"
        board=[]
        if os.path.exists(path):
            with open(path) as f: board=json.load(f)
        board.append(int(s.total))
        board=sorted(board,reverse=True)[:10]
        with open(path,"w") as f: json.dump(board,f)
        return board
