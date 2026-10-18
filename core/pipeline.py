from data.droppers import droppers
from data.upgraders import upgraders
from data.collectors import collectors
from data.conveyors import conveyors

def run_pipeline(data, dropper_pos):
    grid = data["grid"]

    x, y = dropper_pos
    dropper_key = data["placed"][f"{x},{y}"]
    dropper = droppers[dropper_key]

    value = dropper.base_value

    dx, dy = 1, 0
    cx, cy = x + dx, y + dy

    visited = set()

    # compteur d'utilisation par upgrader
    upgrader_usage = {}

    while True:

        if cx < 0 or cy < 0 or cy >= len(grid) or cx >= len(grid[0]):
            return None

        pos = (cx, cy)
        if pos in visited:
            return None
        visited.add(pos)

        cell = grid[cy][cx]

        # Conveyor
        if cell in ["CR", "CL", "CU", "CD"]:
            key = data["placed"][f"{cx},{cy}"]
            conv = conveyors[key]

            if conv.direction == "right":
                dx, dy = 1, 0
            elif conv.direction == "left":
                dx, dy = -1, 0
            elif conv.direction == "up":
                dx, dy = 0, -1
            elif conv.direction == "down":
                dx, dy = 0, 1

            cx += dx
            cy += dy
            continue

        # Upgrader
        if cell == "U":
            key = data["placed"][f"{cx},{cy}"]
            upgrader = upgraders[key]

            # init compteur
            if key not in upgrader_usage:
                upgrader_usage[key] = 0

            # max uses
            if upgrader.max_uses is not None and upgrader_usage[key] >= upgrader.max_uses:
                cx += dx
                cy += dy
                continue

            # conditions
            cond_ok = True
            if upgrader.condition:
                if "min_value" in upgrader.condition and value < upgrader.condition["min_value"]:
                    cond_ok = False
                if "max_value" in upgrader.condition and value > upgrader.condition["max_value"]:
                    cond_ok = False

            if cond_ok:
                if upgrader.type == "add":
                    value += upgrader.value
                elif upgrader.type == "mult":
                    value *= upgrader.value
                elif upgrader.type == "conditional_add":
                    value += upgrader.value
                elif upgrader.type == "conditional_mult":
                    value *= upgrader.value

                upgrader_usage[key] += 1

            cx += dx
            cy += dy
            continue

        # Collector
        if cell == "C":
            key = data["placed"][f"{cx},{cy}"]
            collector = collectors[key]
            value *= collector.multiplier
            return value

        # Case vide → drop tombe
        if cell == ".":
            return None

        # Autre machine → stop
        return None
