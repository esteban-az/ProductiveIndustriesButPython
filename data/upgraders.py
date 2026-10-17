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
        description=""
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
        cost_money=100,
        cost_materials={"stone": 25},
        power_required=5,
        description="Adds +2$ to any drop. No use limit."
    ),
    
    "stone_upgrader": Upgrader(
        key="stone_upgrader",
        name="Stone Upgrader",
        tier="Primal",
        type="mult",          # multiplie la valeur
        value=1.25,           # x1.25
        max_uses=3,           # limite de 3 utilisations
        cost_money=750,
        cost_materials={"stone": 40, "wood": 15},
        power_required=5,
        description="An upgrader made of stone and wood, multiples a drop value by x1.25 up to three times."
    )
}
