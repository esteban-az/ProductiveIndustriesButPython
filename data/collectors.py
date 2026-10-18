from core.colors import TIER_COLORS
from colorama import Style

class Collector:
    def __init__(self, key, name, tier, multiplier, cost_money, cost_materials, power_required, description, persistent=False):
        self.key = key
        self.name = name
        self.tier = tier
        self.multiplier = multiplier
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.power_required = power_required
        self.description = description
        self.persistent = persistent

    def colored_name(self):
        color = TIER_COLORS[self.tier]
        return f"[{color}]{self.name}[/{color}]"

collectors = {
    
    "wooden_collector": Collector(
        key="wooden_collector",
        name="Wooden Collector",
        tier="Primal",
        multiplier=1.2,
        cost_money=25,
        cost_materials={},
        power_required=5,
        description="A basic collector made of wood, process drops at x1.2 their value"
    ),
    
    "stone_collector": Collector(
        key="stone_collector",
        name="Stone Collector",
        tier="Primal",
        multiplier=1.5,
        cost_money=500,
        cost_materials={"stone" : 60},
        power_required=45,
        description="Slightly better than the Wooden Collector, process drops at x1.5 their value."
    ),
    
    "basic_furnace": Collector(
        key="basic_furnace",
        name="Basic Furnace",
        tier="Basic",
        multiplier=2.1,
        cost_money=4000,
        cost_materials={"stone" : 100, "wood" : 50},
        power_required=300,
        description="The first real furnace to process drops, multiplies drops value by x2.1."
    )
}
