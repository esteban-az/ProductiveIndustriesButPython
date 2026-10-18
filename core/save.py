import json
import os

SAVE_FILE = "game_data.json"

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)

        # === Compatibilité avec anciennes saves ===
        if "packs_opened" not in data:
            data["packs_opened"] = {}

        if "persistent_machines" not in data:
            data["persistent_machines"] = {}

        if "persistent_trophies" not in data:
            data["persistent_trophies"] = {}

        if "placed" not in data:
            data["placed"] = {}

        if "grid" not in data:
            data["grid"] = {}

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

        # Machines placées sur la grille
        "placed": {},

        # Grille (si tu veux l’utiliser plus tard)
        "grid": {},

        # === PACK SYSTEM ===
        "packs_opened": {},          # par save
        "persistent_machines": {},   # global permanent
        "persistent_trophies": {},   # global permanent
    }


def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
