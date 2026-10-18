from core.colors import TIER_COLORS
from colorama import Style

class Upgrader:
    def __init__(
        self,
        key,
        name,
        tier,
        type,               # "add", "mult", "conditional_add", "conditional_mult"
        value,              # +2 ou x1.2
        max_uses,           # None = pas de limite
        condition=None,     # fonction ou dict décrivant la condition
        cost_money=0,
        cost_materials=None,
        power_required=0,
        description="",
        persistent=False
    ):
        self.key = key
        self.name = name
        self.tier = tier
        self.type = type
        self.value = value
        self.max_uses = max_uses
        self.condition = condition
        self.cost_money = cost_money
        self.cost_materials = cost_materials or {}
        self.power_required = power_required
        self.description = description
        self.persistent = persistent
        # compteur d'utilisation
        self.uses = 0

    def colored_name(self):
        color = TIER_COLORS[self.tier]
        return f"[{color}]{self.name}[/{color}]"

upgraders = {
    "primitive_stone_refiner": Upgrader(
        key="primitive_stone_refiner",
        name="Primitive Stone Refiner",
        tier="Primal",
        type="add",              # ajoute une valeur fixe
        value=2,                 # +2$
        max_uses=None,           # pas de limite
        cost_money=125,
        cost_materials={"stone": 25},
        power_required=5,
        description="Adds +2$ to any drop. No use limit."
    ),
    
    "stone_upgrader": Upgrader(
        key="stone_upgrader",
        name="Stone Upgrader",
        tier="Primal",
        type="mult",
        value=1.25,           
        max_uses=5,           
        cost_money=750,
        cost_materials={"stone": 40},
        power_required=20,
        description="An upgrader made of stone and wood, multiples a drop value by x1.25 up to three times."
    ),
    
    "primal_magnifier": Upgrader(
        key="primal_magnifier",
        name="Primal Magnifier",
        tier="Primal",
        type="mult",
        value=2,           
        max_uses=1,           
        cost_money=1500,
        cost_materials={"stone": 100},
        power_required=100,
        description="Magnifies your drops by multiplying their value by x2 once."
    ),
    
    "wooden_infuser": Upgrader(
        key="wooden_infuser",
        name="Wooden Infuser",
        tier="Primal",
        type="add",
        value=15,           
        max_uses=None,           
        cost_money=8000,
        cost_materials={"stone": 350, "wood": 50},
        power_required=500,
        description="Infuses your drops with wood, adding 15$ to their value."
    ),
    
    "basic_ore_refiner": Upgrader(
        key="basic_ore_refiner",
        name="Basic Ore Refiner",
        tier="Basic",
        type="conditional_mult",
        value=2.5,                     # x3
        max_uses=None,               # pas de limite
        condition={
            "max_value": 1000        # fonctionne uniquement si drop <= 1k$
        },
        cost_money=20000,
        cost_materials={"stone": 600, "coal": 35, "iron": 10},
        power_required=5000,         # 1ku
        description=(
            "Multiplies drop value by x3 as long as the drop is worth <= 1k$. "
            "Stops working once the drop exceeds 1k$."
        )
    )
}
