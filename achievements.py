class Achievements:
    LIST=[
        ("FIRST_STEP",   "30초 생존",                lambda g: g.time_surv>=30),
        ("ONE_MIN_ND",   "노데미지 60초",           lambda g: g.no_hit>=60),
        ("POWER_COL_3",  "아이템 3개 획득",          lambda g: g.item_col>=3),
        ("SLOW_MASTER",  "슬로모 3회 사용",          lambda g: g.slo_used>=3),
        ("BOMB_USED",    "폭탄 사용",               lambda g: g.bomb_used>=1),
        ("BOSS_HUNTER",  "보스 1회 생존",            lambda g: g.boss_surv>=1),
        ("BOSS_SLAYER",  "보스 2회 생존",            lambda g: g.boss_surv>=2),
        ("GRAZE_100",    "Graze 100회",             lambda g: g.graze_total>=100),
        ("SCORE_10K",    "점수 10,000 도달",        lambda g: g.score.total>=10000),
        ("SCORE_30K",    "점수 30,000 도달",        lambda g: g.score.total>=30000),
    ]
    def __init__(s): s.unlocked=set()
    def check(s,game):
        for key,name,cond in s.LIST:
            if key not in s.unlocked and cond(game):
                s.unlocked.add(key)
                game.messages.append(f"업적 달성: {name}")
