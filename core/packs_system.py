# core/packs_system.py

import random
from rich import print as rich_print
from data.packs import packs
from core.power import format_money, format_resource


RARITY_COLORS = {
    "Common": "white",
    "Rare": "cyan",
    "Epic": "magenta",
    "Legendary": "yellow",
    "Mythical": "red",
    "Godly": "green"
}


def rarity_from_chance(chance):
    if chance >= 0.7:
        return "Common"
    elif chance >= 0.5:
        return "Rare"
    elif chance >= 0.25:
        return "Epic"
    elif chance >= 0.1:
        return "Legendary"
    elif chance >= 0.02:
        return "Mythical"
    else:
        return "Godly"


def can_open_pack(data, pack):
    # Vérifie si déjà ouvert trop de fois dans cette save
    if data["packs_opened"].get(pack.key, 0) >= pack.max_uses:
        return False, "[red]❌ Tu as déjà ouvert ce pack dans cette save.[/red]"

    # Vérifie argent
    if data["inventory"]["money"] < pack.cost_money:
        return False, "[red]❌ Pas assez d'argent.[/red]"

    # Vérifie matériaux
    for mat, amt in pack.cost_materials.items():
        if data["inventory"].get(mat, 0) < amt:
            return False, f"[red]❌ Pas assez de {mat}.[/red]"

    return True, ""


def open_pack(data, pack):
    obtained = []

    # Slot 1 : trophée garanti
    obtained.append(pack.guaranteed_item)

    # Slot 2 : machine exclusive garantie
    obtained.append(random.choice(pack.pool))

    # Slots suivants
    for chance in pack.slot_chances[2:]:
        if random.random() <= chance:
            obtained.append(random.choice(pack.pool))

    return obtained


def apply_pack_rewards(data, rewards):
    for machine_key in rewards:
        if "pylon" in machine_key:
            # Trophée persistant
            data["persistent_trophies"][machine_key] = \
                data["persistent_trophies"].get(machine_key, 0) + 1
        else:
            # Machine persistante
            data["persistent_machines"][machine_key] = \
                data["persistent_machines"].get(machine_key, 0) + 1


def buy_pack(data, pack):
    ok, msg = can_open_pack(data, pack)
    if not ok:
        rich_print(msg)
        return

    # Paiement
    data["inventory"]["money"] -= pack.cost_money
    for mat, amt in pack.cost_materials.items():
        data["inventory"][mat] -= amt

    # Marquer pack ouvert dans cette save
    data["packs_opened"][pack.key] = data["packs_opened"].get(pack.key, 0) + 1

    # Ouvrir pack
    rewards = open_pack(data, pack)
    apply_pack_rewards(data, rewards)

    # Affichage simple
    rich_print(f"[bold cyan]Pack ouvert : {pack.name}[/bold cyan]\n")

    for item in rewards:
        rarity = rarity_from_chance(random.random())
        color = RARITY_COLORS[rarity]
        rich_print(f"[{color}]{rarity} → {item}[/{color}]")

    rich_print("\n[green]Les récompenses ont été ajoutées à tes machines persistantes ![/green]")
