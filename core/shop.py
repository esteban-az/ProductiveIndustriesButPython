from rich import print as rich_print
from rich.panel import Panel

from core.save import save_game
from core.colors import MATERIAL_COLORS
from data.depots import depots
from data.droppers import droppers
from data.upgraders import upgraders
from data.collectors import collectors
from data.machines import machines
from data.generators import generators
from data.materials import materials
from core.power import format_resource, format_money, format_power
from core.packs_system import buy_pack
from data.packs import packs



def shop_menu(data):
    while True:
        rich_print("\n[bold cyan]=== SHOP ===[/bold cyan]")
        print("1. Depots")
        print("2. Droppers")
        print("3. Upgraders")
        print("4. Collectors")
        print("5. Special Machines")
        print("6. Generators")
        print("7. Packs")
        print("8. Back")

        choice = input("Choisis une catégorie : ")

        if choice == "1":
            shop_category(data, depots, "Depot")
        elif choice == "2":
            shop_category(data, droppers, "Dropper")
        elif choice == "3":
            shop_category(data, upgraders, "Upgrader")
        elif choice == "4":
            shop_category(data, collectors, "Collector")
        elif choice == "5":
            shop_category(data, machines, "Special Machine")
        elif choice == "6":
            shop_category(data, generators, "Generator")
        elif choice == "7":
            show_packs_menu(data)
        elif choice == "8":
            break
        else:
            rich_print("[red]❌ Option invalide.[/red]")


def shop_category(data, category_dict, category_name):
    rich_print(f"\n[bold cyan]=== {category_name} Shop ===[/bold cyan]")

    keys = list(category_dict.keys())

    for i, key in enumerate(keys, 1):
        item = category_dict[key]
        rich_print(f"{i}. {item.colored_name()}")

    print(f"{len(keys)+1}. Back")

    try:
        choice = int(input("Choisis un item : "))
    except:
        rich_print("[red]❌ Choix invalide.[/red]")
        return

    if choice == len(keys) + 1:
        return

    if choice < 1 or choice > len(keys):
        rich_print("[red]❌ Choix invalide.[/red]")
        return

    selected_key = keys[choice - 1]
    item = category_dict[selected_key]

    show_preview(data, item)


def show_preview(data, item):
    text = ""

    # === Tier ===
    if hasattr(item, "tier"):
        text += f"Tier : {item.tier}\n"

    # === Base Value (droppers) ===
    if hasattr(item, "base_value"):
        text += f"Base Value : {format_money(item.base_value)}\n"

    # === Upgrader details ===
    if item in upgraders.values():

        # Type d'amélioration
        if item.type == "mult":
            text += f"Upgrade Value : x{item.value}\n"

        elif item.type == "add":
            text += f"Upgrade Value : +{item.value}$\n"

        elif item.type == "conditional_mult":
            text += f"Upgrade Value : x{item.value}\n"

        elif item.type == "conditional_add":
            text += f"Upgrade Value : +{item.value}$\n"

        # Conditions
        if item.condition:
            cond_parts = []

            if "min_value" in item.condition:
                cond_parts.append(f">= {format_money(item.condition['min_value'])}")

            if "max_value" in item.condition:
                cond_parts.append(f"<= {format_money(item.condition['max_value'])}")

            cond_text = " and ".join(cond_parts)
            text += f"Condition : {cond_text}\n"

        # Limite d'utilisation
        if item.max_uses is not None:
            text += f"Use Limit : {item.max_uses}\n"

    # === Collector multiplier ===
    if hasattr(item, "multiplier"):
        text += f"Multiplier : x{item.multiplier}\n"

    # === Power Required ===
    if hasattr(item, "power_required"):
        text += f"Power Required : {format_power(item.power_required)}\n"

    # === Drop Time ===
    if hasattr(item, "drop_time"):
        text += f"Drop Time : {item.drop_time}s\n"
    
    # === Depot Production ===
    if item in depots.values():
        # Un dépôt produit toujours une seule ressource pour l'instant
        # On récupère la quantité produite (ex: {"stone": 1})
        produced_amount = list(item.production.values())[0]

        formatted_amount = format_resource(produced_amount)

        text += f"Production : {formatted_amount} / {item.production_time}s\n"


    text += "\n"

    # === Cost Money ===
    if hasattr(item, "cost_money"):
        text += f"Cost Money : {format_money(item.cost_money)}\n"

    # === Cost Materials ===
    if hasattr(item, "cost_materials") and item.cost_materials:
        text += "Cost Materials :\n"
        for mat_key, amt in item.cost_materials.items():
            mat = materials[mat_key]
            owned = data["inventory"].get(mat_key, 0)

            colored_symbol = f"[{mat.color}][{mat.symbol}][/{mat.color}]"
            colored_name = f"[{mat.color}]{mat.name}[/{mat.color}]"

            text += (
                f"  {colored_symbol} {colored_name} : "
                f"{format_resource(owned)} / {format_resource(amt)}\n"
            )

    text += "\n"

    # === Power Output (generators) ===
    if hasattr(item, "power_output"):
        text += f"Power Output : {format_power(item.power_output)}\n"

    # === Description ===
    if hasattr(item, "description"):
        text += f"Description : {item.description}\n"

    # === Panel ===
    panel = Panel(
        text,
        title=item.colored_name(),
        border_style="cyan",
        expand=False
    )

    rich_print(panel)

    buy = input("Acheter ? (y/n) : ").lower()

    if buy == "y":
        buy_item(data, item)

def show_pack_preview(data, pack):
    text = ""

    # === Tier ===
    text += f"Tier : {pack.tier}\n"

    # === Guaranteed Item ===
    text += f"Guaranteed Item : {pack.guaranteed_item}\n"

    # === Exclusive Machines ===
    text += "Exclusive Machines :\n"
    for m in pack.pool:
        text += f"  - {m}\n"

    text += "\n"

    # === Slot Chances ===
    text += "Slot Chances :\n"
    for i, chance in enumerate(pack.slot_chances, 1):
        pct = int(chance * 100)
        text += f"  Slot {i} : {pct}%\n"

    text += "\n"

    # === Cost Money ===
    text += f"Cost Money : {format_money(pack.cost_money)}\n"

    # === Cost Materials ===
    if pack.cost_materials:
        text += "Cost Materials :\n"
        for mat_key, amt in pack.cost_materials.items():
            owned = data["inventory"].get(mat_key, 0)
            text += (
                f"  {mat_key} : "
                f"{format_resource(owned)} / {format_resource(amt)}\n"
            )

    text += "\n"

    # === Max Uses per save ===
    used = data["packs_opened"].get(pack.key, 0)
    text += f"Max Uses (per save) : {pack.max_uses}\n"
    text += f"Used in this save : {used}\n"

    # === Panel ===
    panel = Panel(
        text,
        title=f"[cyan]{pack.name}[/cyan]",
        border_style="cyan",
        expand=False
    )

    rich_print(panel)

    buy = input("Acheter ce pack ? (y/n) : ").lower()
    if buy == "y":
        buy_pack(data, pack)


def show_packs_menu(data):
    print("\n=== Packs ===")
    for key, pack in packs.items():
        print(f"- {pack.name} ({key})")

    sel = input("Quel pack acheter ? (key) : ")

    if sel in packs:
        show_pack_preview(data, packs[sel])



def buy_item(data, item):

    if data["inventory"]["money"] < item.cost_money:
        rich_print("[red]❌ Pas assez d'argent.[/red]")
        return

    for mat_key, needed in item.cost_materials.items():
        if data["inventory"].get(mat_key, 0) < needed:
            rich_print(f"[red]❌ Pas assez de {mat_key}[/red]")
            return

    data["inventory"]["money"] -= item.cost_money
    for mat_key, needed in item.cost_materials.items():
        data["inventory"][mat_key] -= needed

    added = False

    for category in data["machines"]:
        if item.key in data["machines"][category]:
            data["machines"][category][item.key] += 1
            added = True
            break

    if not added:
        if item.key in droppers:
            data["machines"]["droppers"][item.key] = 1
        elif item.key in upgraders:
            data["machines"]["upgraders"][item.key] = 1
        elif item.key in collectors:
            data["machines"]["collectors"][item.key] = 1
        elif item.key in depots:
            data["machines"]["depots"][item.key] = 1
        elif item.key in machines:
            data["machines"]["special"][item.key] = 1
        elif item.key in generators:
            data["power"]["generators"][item.key] = (
                data["power"]["generators"].get(item.key, 0) + item.power_output
            )
            data["power"]["total_power"] += item.power_output

    rich_print(f"[green]✔ {item.name} acheté ![/green]")
    save_game(data)
