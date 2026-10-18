from core.colors import TIER_COLORS
from colorama import Style

class Machine:
    def __init__(self, key, name, tier, cost_money, cost_materials, power_required, description, persistent=False):
        self.key = key
        self.name = name
        self.tier = tier
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.power_required = power_required
        self.description = description
        self.persistent = persistent
    
    def colored_name(self):
        color = TIER_COLORS[self.tier]
        return f"[{color}]{self.name}[/{color}]"

machines = {
    
    "wood_sawmill": Machine(
        key="wood_sawmill",
        name="Wood Sawmill",
        tier="Primal",
        cost_money=3000,
        cost_materials={"stone": 300, "wood": 50},
        power_required=100,
        description="A simple machine to cut wood into planks."
    ),
    
    "alloy_factory": Machine(
        key="alloy_factory",
        name="Alloy Factory",
        tier="Advanced",
        cost_money=10_000_000,
        cost_materials={"stone": 5000, "wooden_planks":1000, "iron": 200, "coal": 150},
        power_required=1000000,
        description="High-end industrial machine used to create advanced alloys."
    )

}
