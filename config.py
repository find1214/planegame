# ── 화면 & FPS ──────────────────────────────────────
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 640
FPS = 60

# ── 색상 팔레트 ─────────────────────────────────────
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)

PLAYER_COLOR   = ( 80, 200, 255)

BULLET_OUTER   = (180,  30,  30)   # 적탄 테두리
BULLET_INNER   = (255, 180, 180)   # 적탄 내부
BOSS_COLOR     = (180, 180,   0)   # 보스 본체

GRAZE_COLOR    = (255, 220,   0)   # 히트박스 / Graze 링

# 파워업 아이템 색
SLOW_ITEM_COLOR  = (  0, 255, 255)
BOMB_ITEM_COLOR  = (255, 255,   0)
COIN_COLOR       = (255, 215,   0)
SHIELD_ITEM_COLOR= (120, 255, 120)
POWER_ITEM_COLOR = (255, 120, 255)

# ── 플레이어 기본 ───────────────────────────────────
PLAYER_SIZE     = 30          # 삼각형 크기(밑변)
PLAYER_HIT_R    = 6           # 기본 히트박스 반경
PLAYER_GRAZE_R  = 22          # Graze 판정 반경
SHOW_HITBOX_DEF = False       # H 키로 토글

BASE_SPEED   = 5              # 업그레이드 이전 기본 속도
SLOW_FACTOR  = 0.4            # Shift 저속 이동 배수

# ── 파워업 스폰 ─────────────────────────────────────
ITEM_INTERVAL = 18            # 파워업/코인 등장 주기(초)

# ── 플레이 특수자원(초기값) ─────────────────────────
SLOMO_FACTOR, SLOMO_DURATION, SLOMO_CHARGES = 0.4, 3.0, 1
BOMB_COUNT   = 0              # 폭탄 초기 0– 아이템/업글로 추가

# ── 연출 효과 ──────────────────────────────────────
FLASH_DURATION = 0.15         # 피격 시 화면 번쩍
SHAKE_DURATION = 0.30         # 폭탄/피격 흔들림
SHAKE_MAG      = 6            # 흔들림 강도(px)

# ── 보스 / 이벤트 ──────────────────────────────────
BOSS_INTERVAL     = 60        # 60초마다 등장
BOSS_DURATION     = 15        # 머무는 시간
BOSS_SHOT_INT     = 1.0       # 탄막 발사 간격
BOSS_BURST_COUNT  = 16        # 한 번에 16발
