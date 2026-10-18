from core.colors import TIER_COLORS
from colorama import Style

class Dropper:
    def __init__(self, key, name, tier, base_value, cost_money, cost_materials, power_required, description, drop_time, persistent=False):
        self.key = key
        self.name = name
        self.tier = tier
        self.base_value = base_value
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.power_required = power_required
        self.description = description
        self.drop_time = drop_time
        self.persistent = persistent

    def colored_name(self):
        color = TIER_COLORS[self.tier]
        return f"[{color}]{self.name}[/{color}]"

droppers = {
    "stone_dropper": Dropper(
        key="stone_dropper",
        name="Stone Dropper",
        tier="Primal",
        base_value=1,                 # valeur du drop
        cost_money=100,               # coût en argent
        cost_materials={"stone": 25}, # coût en matériaux
        power_required=10,            # énergie nécessaire
        drop_time=5,                   # temps de drop
        description="Drops basic stone fragments worth 1$."
    ),
    
    "reinforced_stone_dropper": Dropper(
        key="reinforced_stone_dropper",
        name="Reinforced Stone Dropper",
        tier="Primal",
        base_value=15,                 # valeur du drop
        cost_money=2500,               # coût en argent
        cost_materials={"stone": 40, "wooden_planks" : 25, "wood" : 10}, # coût en matériaux
        power_required=150,            # énergie nécessaire
        drop_time=3,
        description="A reinforced version of the Stone Dropper, drops bigger stone fragments worth 15$ each."
    ),
    
    "trash_thrower": Dropper(
        key="trash_thrower",
        name="Thrash Thrower",
        tier="Primal",
        base_value=100,                 
        cost_money=15000,               
        cost_materials={"stone": 1000, "coal": 100,"iron": 15},
        power_required=3000,           
        drop_time=6,
        description="A man's trash is one's treasure, drops trashbags that are worth 100$ every 6 seconds."
    ),
}
