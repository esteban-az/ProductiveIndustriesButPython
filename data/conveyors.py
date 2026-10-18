from core.colors import TIER_COLORS

class Conveyor:
    def __init__(
        self,
        key,
        name,
        direction,
        symbol,
        cost_money,
        cost_materials,
        power_required,
        description,
        tier="Basic"
    ):
        self.key = key
        self.name = name
        self.direction = direction  # "right", "left", "up", "down"
        self.symbol = symbol        # "CR", "CL", "CU", "CD"
        self.tier = tier
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.power_required = power_required
        self.description = description

    def colored_name(self):
        color = TIER_COLORS[self.tier]
        return f"[{color}]{self.name}[/{color}]"


conveyors = {
    "conveyor_right": Conveyor(
        key="conveyor_right",
        name="Conveyor Right",
        direction="right",
        symbol="CR",
        cost_money=5000,
        cost_materials={"iron": 15},
        power_required=100,
        description="Moves drops to the right."
    ),

    "conveyor_left": Conveyor(
        key="conveyor_left",
        name="Conveyor Left",
        direction="left",
        symbol="CL",
        cost_money=5000,
        cost_materials={"iron": 15},
        power_required=100,
        description="Moves drops to the left."
    ),

    "conveyor_up": Conveyor(
        key="conveyor_up",
        name="Conveyor Up",
        direction="up",
        symbol="CU",
        cost_money=5000,
        cost_materials={"iron": 15},
        power_required=100,
        description="Moves drops upward."
    ),

    "conveyor_down": Conveyor(
        key="conveyor_down",
        name="Conveyor Down",
        direction="down",
        symbol="CD",
        cost_money=5000,
        cost_materials={"iron": 15},
        power_required=100,
        description="Moves drops downward."
    ),
}
