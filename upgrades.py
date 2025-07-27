import json, os
from typing import Dict

META_FILE = "meta.json"

UPGRADE_MAX_LV = 5
UPGRADE_COST = lambda lv: 100 * (lv + 1)     # 100,200,300,400,500

PLANE_COST = {
    "SCOUT": 300,
    "TANK":  400,
    "NINJA": 500,
    "BOMBER":600,
}

DEFAULT_META = {
    "coins": 0,
    "up": {k:0 for k in ("speed","hitbox","life","slomo","bomb")},
    "unlocked": ["BASIC"],
    "active":   "BASIC"
}

# --------------------------------------------------------
def _load() -> Dict:
    if not os.path.exists(META_FILE):
        with open(META_FILE,"w") as f: json.dump(DEFAULT_META,f)
    with open(META_FILE) as f: return json.load(f)

def _save(meta:Dict):
    with open(META_FILE,"w") as f: json.dump(meta,f,indent=2)

# --------------------------------------------------------
class MetaManager:
    def __init__(self):
        self.meta = _load()

    # --- coin ---
    @property
    def coins(self): return self.meta["coins"]
    def add_coins(self, c): self.meta["coins"] += c; _save(self.meta)

    # --- upgrades ---
    def level(self, key): return self.meta["up"][key]
    def buy_upgrade(self, key):
        lv = self.level(key)
        if lv >= UPGRADE_MAX_LV: return False
        cost = UPGRADE_COST(lv)
        if self.coins < cost: return False
        self.meta["coins"] -= cost
        self.meta["up"][key] += 1
        _save(self.meta); return True

    # --- planes ---
    def unlocked(self): return self.meta["unlocked"]
    def active  (self): return self.meta["active"]
    def buy_plane(self, code):
        if code in self.unlocked(): return False
        cost = PLANE_COST[code]
        if self.coins < cost: return False
        self.meta["coins"] -= cost
        self.meta["unlocked"].append(code)
        _save(self.meta); return True
    def set_active(self, code):
        if code in self.unlocked():
            self.meta["active"] = code; _save(self.meta)
