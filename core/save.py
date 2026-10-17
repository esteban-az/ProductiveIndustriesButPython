import json
import os

SAVE_FILE = "game_data.json"

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
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
    }
}


def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
