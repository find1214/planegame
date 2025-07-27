# 5종 기체 정의
PLANES = {
    "BASIC":  dict(name="BASIC",  speed=5, hit_r=8, lives=0, bombs=0, slomo=0),
    "SCOUT":  dict(name="SCOUT",  speed=7, hit_r=8, lives=0, bombs=0, slomo=0),
    "TANK":   dict(name="TANK",   speed=4, hit_r=8, lives=2, bombs=0, slomo=0),
    "NINJA":  dict(name="NINJA",  speed=5, hit_r=5, lives=0, bombs=0, slomo=0),
    "BOMBER": dict(name="BOMBER", speed=5, hit_r=8, lives=0, bombs=1, slomo=0),
}
DEFAULT_PLANE = "BASIC"
