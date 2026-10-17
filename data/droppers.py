from core.colors import TIER_COLORS
from colorama import Style

class Dropper:
    def __init__(self, key, name, tier, base_value, cost_money, cost_materials, power_required, description):
        self.key = key
        self.name = name
        self.tier = tier
        self.base_value = base_value
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.power_required = power_required
        self.description = description

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
        description="Drops basic stone fragments worth 1$."
    ),
    
    "reinforced_stone_dropper": Dropper(
        key="reinforced_stone_dropper",
        name="Reinforced Stone Dropper",
        tier="Primal",
        base_value=10,                 # valeur du drop
        cost_money=2500,               # coût en argent
        cost_materials={"stone": 300, "wooden_planks" : 200, "wood" : 100}, # coût en matériaux
        power_required=100,            # énergie nécessaire
        description="A reinforced version of the Stone Dropper, drops bigger stone fragments worth 10$ each."
    )
}
