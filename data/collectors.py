from core.colors import TIER_COLORS
from colorama import Style

class Collector:
    def __init__(self, key, name, tier, multiplier, cost_money, cost_materials, power_required, description):
        self.key = key
        self.name = name
        self.tier = tier
        self.multiplier = multiplier
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.power_required = power_required
        self.description = description

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
        description="A basic collector made of wood, process ore at x1.2 their value"
    ),
    
    "basic_furnace": Collector(
        key="basic_furnace",
        name="Basic Furnace",
        tier="Basic",
        multiplier=2.0,
        cost_money=1000,
        cost_materials={"stone" : 50, "wood" : 50},
        power_required=100,
        description="Consumes drops and doubles their value."
    )
}
