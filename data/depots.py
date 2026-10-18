from colorama import Style
from core.colors import TIER_COLORS

# DEPOTS are the machines that generate your resources

class Depot:
    def __init__(self, key, name, tier, cost_money, cost_materials,
                 production, production_time, power_required, description, persistent=False):
        self.key = key # ID of the item
        self.name = name # Name of the item
        self.tier = tier # Tier of the item
        self.cost_money = cost_money # The money cost of the Depot in the shop
        self.cost_materials = cost_materials # The materials cost of the Depot in the shop
        self.production = production # How many of the material is produced by the Depot
        self.production_time = production_time # The time it takes to produce a material
        self.power_required = power_required # The power consumption of the Depot
        self.description = description # The description of the Depot
        self.persistent = persistent # If the Depot persist across save files
        

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
        production_time=8,
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
        production_time=12,
        power_required=40,
        description="A basic machine that cuts wood automatically."
    ),

    "coal_miner": Depot(
        key="coal_miner",
        name="Coal Miner",
        tier="Primal",
        cost_money=11250,
        cost_materials={"stone": 500, "wood": 100},
        production={"coal": 1},
        production_time=15,
        power_required=1000,
        description="Extracts coal slowly from deep layers."
    ),
    
    "iron_deployer": Depot(
        key="iron_deployer",
        name="Iron Deployer",
        tier="Basic",
        cost_money=20000,
        cost_materials={"stone": 1500, "wooden_planks" : 400, "coal" : 25},
        production={"iron": 1},
        production_time=10,
        power_required=2500,
        description="Mines iron ore veins deep underground."
    ),
}
