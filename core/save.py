import json
import os

SAVE_FILE = "game_data.json"

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        # === FIX GRID ===
        if "grid" not in data or not isinstance(data["grid"], list):
            # Si aucune grille → créer une grille vide 20x20
            data["grid"] = [["." for _ in range(20)] for _ in range(20)]


        # === FIX PLACED ===
        if "placed" not in data or not isinstance(data["placed"], dict):
            data["placed"] = {}

        # === FIX PACK SYSTEM ===
        if "packs_opened" not in data:
            data["packs_opened"] = {}

        if "persistent_machines" not in data:
            data["persistent_machines"] = {}

        if "persistent_trophies" not in data:
            data["persistent_trophies"] = {}

        return data

    # === Nouvelle sauvegarde ===
    return {
        "inventory": {},
        "machines": {
            "depots": {},
            "droppers": {},
            "upgraders": {},
            "collectors": {},
            "special": {}
        },
        "power": {
            "generators": {},
            "total_power": 0
        },
        "grid": [["." for _ in range(10)] for _ in range(10)],
        "placed": {},
        "packs_opened": {},
        "persistent_machines": {},
        "persistent_trophies": {}
    }


def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
