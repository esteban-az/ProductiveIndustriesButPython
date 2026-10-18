from core.colors import TIER_COLORS
from colorama import Style

class Generator:
    def __init__(self, key, name, tier, power_output, cost_money, cost_materials, description, persistent=False):
        self.key = key
        self.name = name
        self.tier = tier
        self.power_output = power_output  # en u
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.description = description
        self.persistent = persistent

    def colored_name(self):
        color = TIER_COLORS[self.tier]
        return f"[{color}]{self.name}[/{color}]"


generators = {

    "basic_solar_cell": Generator(
        key="basic_solar_cell",
        name="Basic Solar Cell",
        tier="Primal",
        power_output=25,
        cost_money=100,
        cost_materials={"stone": 15},
        description="Produces 25u using sunlight."
    ),
    
    "rusty_coal_generator": Generator(
        key="rusty_coal_generator",
        name="Rusty Coal Generator",
        tier="Primal",
        power_output=300,
        cost_money=3000,
        cost_materials={"stone": 150, "wood": 5},
        description="An old generator that barely produces energy by consuming coal underground."
    ),
    
    "primitive_solar_panel": Generator(
        key="primitive_solar_panel",
        name="Primitive Solar Panel",
        tier="Primal",
        power_output=1000,
        cost_money=10000,
        cost_materials={"stone": 500, "wooden_planks": 100, "wood": 100},
        description="An direct upgrade to the Basic Solar Cell, generating 1ku of energy from sunlight."
    ),
    
    "primitive_thermal_plant": Generator(
        key="primitive_thermal_plant",
        name="Primitive Thermal Plant",
        tier="Basic",
        power_output=7500,
        cost_money=60000,
        cost_materials={"stone": 2000, "wood": 1000, "coal": 100, "iron": 5},
        description="Generates energy from thermal sources deep underground, this is where your real energy generation starts."
    )
}
