from colorama import Style
from core.colors import MATERIAL_COLORS
from rich import print as rich_print

class Material:
    def __init__(self, key, name, symbol, tier, value, description):
        self.key = key
        self.name = name
        self.symbol = symbol
        self.tier = tier
        self.value = value
        self.description = description
        self.color = MATERIAL_COLORS[key]

    def colored_name(self):
        color = MATERIAL_COLORS[self.key]
        return f"[{color}][{self.symbol}] {self.name}[/{color}]"



materials = {
    "stone": Material(
        key="stone",
        name="Stone",
        symbol="■",
        tier="Primal",
        value=1,
        description="Common material used everywhere."
    ),
    
    "wood": Material(
        key="wood",
        name="Wood",
        symbol="Wd",
        tier="Primal",
        value=2,
        description="One of the primary materials."
    ),
    
    "wooden_planks": Material(
        key="wooden_planks",
        name="Wooden Planks",
        symbol="WP",
        tier="Primal",
        value=5,
        description="Processed wood used for construction."
    ),

    "coal": Material(
        key="coal",
        name="Coal",
        symbol="C",
        tier="Primal",
        value=8,
        description="Carbon-rich fuel material."
    ),
    
    "iron": Material(
        key="iron",
        name="Iron",
        symbol="Fe",
        tier="Basic",
        value=15,
        description="A common metal used for many advanced constructions."
    ),
    
    "steel": Material(
        key="steel",
        name="Steel",
        symbol="CFe",
        tier="Advanced",
        value=25,
        description="Strong alloy made from coal and iron."
    ),


    "gold": Material(
        key="gold",
        name="Gold",
        symbol="Au",
        tier="Advanced",
        value=50,
        description="Precious metal with high value."
    )
}
