from colorama import Style
from core.colors import TIER_COLORS

class Depot:
    def __init__(self, key, name, tier, cost_money, cost_materials,
                 production, production_time, power_required, description):
        self.key = key
        self.name = name
        self.tier = tier
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.production = production              # ex: {"stone": 3}
        self.production_time = production_time    # ex: 1 seconde
        self.power_required = power_required
        self.description = description

    def colored_name(self):
        color = TIER_COLORS[self.tier]
        return f"[{color}]{self.name}[/{color}]"

depots = {
    "stone_depot": Depot(
        key="stone_depot",
        name="Stone Depot",
        tier="Primal",
        cost_money=250,
        cost_materials={"stone": 50},
        production={"stone": 1},
        production_time=1,          # produit toutes les 1 seconde
        power_required=10,
        description="Mines stone from ground level."
    ),
    
    "wood_cutter": Depot(
        key="wood_cutter",
        name="Wood Cutter",
        tier="Primal",
        cost_money=1000,
        cost_materials={"stone": 100},
        production={"wood": 1},
        production_time=3,          # produit toutes les 3 seconde
        power_required=25,
        description="A basic machine that cuts wood automatically."
    ),

    "coal_miner": Depot(
        key="coal_miner",
        name="Coal Miner",
        tier="Primal",
        cost_money=2500,
        cost_materials={"stone": 250, "wood": 50},
        production={"coal": 1},
        production_time=5,          # produit toutes les 5 secondes
        power_required=50,
        description="Extracts coal slowly from deep layers."
    ),
    
    "iron_spitter": Depot(
        key="iron_spitter",
        name="Iron Spitter",
        tier="Basic",
        cost_money=7500,
        cost_materials={"stone": 1000, "wooden_planks" : 250, "coal" : 10},
        production={"iron": 1},
        production_time=2,          # produit toutes les 5 secondes
        power_required=500,
        description="Mines iron ore veins deep underground."
    ),
}
