from core.colors import TIER_COLORS
from colorama import Style

class Generator:
    def __init__(self, key, name, tier, power_output, cost_money, cost_materials, description):
        self.key = key
        self.name = name
        self.tier = tier
        self.power_output = power_output  # en u
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.description = description

    def colored_name(self):
        color = TIER_COLORS[self.tier]
        return f"[{color}]{self.name}[/{color}]"


generators = {
    "coal_generator": Generator(
        key="coal_generator",
        name="Coal Generator",
        tier="Primal",
        power_output=50,             # 50u
        cost_money=150,
        cost_materials={"coal": 20},
        description="Basic generator producing 50u of energy."
    ),

    "solar_panel": Generator(
        key="solar_panel",
        name="Solar Panel",
        tier="Primal",
        power_output=20,             # 20u
        cost_money=100,
        cost_materials={"stone": 10},
        description="Produces 20u using sunlight."
    ),
    
    "primitive_thermal_plant": Generator(
        key="primitive_thermal_plant",
        name="Primitive Thermal Plant",
        tier="Basic",
        power_output=500,             # 250u
        cost_money=3000,
        cost_materials={"stone": 500, "wooden_planks": 250},
        description="Generates energy from thermal sources deep underground, very cheap."
    ),
}
