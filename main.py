import time
from rich import print as rich_print

from core.save import load_game, save_game
from core.power import PowerSystem, format_power, format_money, format_resource
from core.colors import TIER_COLORS, MATERIAL_COLORS
from data.materials import materials
from data.depots import depots
from data.droppers import droppers
from data.upgraders import upgraders
from data.collectors import collectors
from data.machines import machines
from data.generators import generators
from core.pipeline import process_drop
from core.machine_actions import process_wood_sawmill, process_alloy_factory



# ============================
#   INITIALISATION DU JEU
# ============================

def init_game():
    data = load_game()

    if "inventory" not in data:
        data["inventory"] = {}

    base_inventory = {
        "stone": 0,
        "coal": 0,
        "wood": 0,
        "money": 0
    }

    for key, value in base_inventory.items():
        if key not in data["inventory"]:
            data["inventory"][key] = value

    if "machines" not in data:
        data["machines"] = {}

    base_machines = {
        "depots": {},
        "droppers": {},
        "upgraders": {},
        "collectors": {},
        "special": {}
    }

    for key, value in base_machines.items():
        if key not in data["machines"]:
            data["machines"][key] = value

    if "power" not in data:
        data["power"] = {}

    base_power = {
        "generators": {},
        "total_power": 0
    }

    for key, value in base_power.items():
        if key not in data["power"]:
            data["power"][key] = value

    if "depot_timers" not in data:
        data["depot_timers"] = {}
    
    # Grille 10x10
    if "grid" not in data:
        data["grid"] = [["." for _ in range(10)] for _ in range(10)]

    # Machines placées
    if "placed" not in data:
        data["placed"] = {}  # (x,y) -> machine_key


    save_game(data)
    return data


# ============================
#   AFFICHAGES
# ============================

def show_inventory(data):
    rich_print("\n[bold cyan]=== INVENTORY ===[/bold cyan]")

    money = data["inventory"].get("money", 0)
    if money > 0:
        rich_print(f"[green]{format_money(money)}[/green]")

    for key, mat in materials.items():
        amount = data["inventory"].get(key, 0)
        if amount > 0:
            rich_print(f"{mat.colored_name()} : {format_resource(amount)}")


def show_base(data):
    from rich import print as rich_print
    from rich.panel import Panel

    rich_print("\n[bold cyan]=== BASE ===[/bold cyan]")

    # Depots
    rich_print("\n[bold]Depots :[/bold]")
    for key, count in data["machines"]["depots"].items():
        depot = depots.get(key)
        if depot:
            rich_print(f"{depot.colored_name()} x {count}")

    # Droppers
    rich_print("\n[bold]Droppers :[/bold]")
    for key, count in data["machines"]["droppers"].items():
        dropper = droppers.get(key)
        if dropper:
            rich_print(f"{dropper.colored_name()} x {count}")

    # Upgraders
    rich_print("\n[bold]Upgraders :[/bold]")
    for key, count in data["machines"]["upgraders"].items():
        upgrader = upgraders.get(key)
        if upgrader:
            rich_print(f"{upgrader.colored_name()} x {count}")

    # Collectors
    rich_print("\n[bold]Collectors :[/bold]")
    for key, count in data["machines"]["collectors"].items():
        collector = collectors.get(key)
        if collector:
            rich_print(f"{collector.colored_name()} x {count}")

    # Special Machines
    rich_print("\n[bold]Special Machines :[/bold]")
    for key, count in data["machines"]["special"].items():
        machine = machines.get(key)
        if machine:
            rich_print(f"{machine.colored_name()} x {count}")

    # Generators
    rich_print("\n[bold]Generators :[/bold]")
    for key, total_power in data["power"]["generators"].items():
        gen = generators.get(key)
        if gen:
            count = total_power // gen.power_output
            rich_print(f"{gen.colored_name()} x {count} → {format_power(total_power)}")

    # ============================
    #   ENERGY PANEL
    # ============================

    # Calcul consommation totale
    total_consumption = 0

    # Depots
    for key, count in data["machines"]["depots"].items():
        depot = depots.get(key)
        if depot:
            total_consumption += depot.power_required * count

    # Droppers
    for key, count in data["machines"]["droppers"].items():
        dropper = droppers.get(key)
        if dropper:
            total_consumption += dropper.power_required * count

    # Upgraders
    for key, count in data["machines"]["upgraders"].items():
        upgrader = upgraders.get(key)
        if upgrader:
            total_consumption += upgrader.power_required * count

    # Collectors
    for key, count in data["machines"]["collectors"].items():
        collector = collectors.get(key)
        if collector:
            total_consumption += collector.power_required * count

    # Special machines (si power_required)
    for key, count in data["machines"]["special"].items():
        machine = machines.get(key)
        if machine and hasattr(machine, "power_required"):
            total_consumption += machine.power_required * count

    production = data["power"]["total_power"]

    # Déterminer le statut
    if production > total_consumption:
        status = "[green]Stable[/green]"
    elif production == total_consumption:
        status = "[yellow]Balanced[/yellow]"
    else:
        status = "[red]Deficit[/red]"

    # Construire le panneau Rich
    energy_text = (
        f"[green]Production : {production}u[/green]\n"
        f"[red]Consumption : {total_consumption}u[/red]\n"
        f"Status : {status}"
    )

    panel = Panel(
        energy_text,
        title="Energy Status",
        border_style="cyan",
        expand=False
    )

    rich_print("\n")
    rich_print(panel)

def show_grid(data):
    rich_print("\n[bold cyan]=== TYCOON GRID ===[/bold cyan]")

    grid = data["grid"]

    for row in grid:
        rich_print(" ".join(row))

def place_machine(data):
    rich_print("\n[bold cyan]=== PLACE MACHINE ===[/bold cyan]")

    rich_print("Tu possèdes :")
    for category in ["droppers", "upgraders", "collectors", "depots", "special"]:
        for key, count in data["machines"][category].items():
            if count > 0:
                rich_print(f"- {key} x{count}")

    machine_key = input("Quelle machine veux-tu placer ? : ")

    found = False
    for category in data["machines"]:
        if machine_key in data["machines"][category] and data["machines"][category][machine_key] > 0:
            found = True
            break

    if not found:
        rich_print("[red]❌ Tu ne possèdes pas cette machine.[/red]")
        return

    try:
        x = int(input("X (0-9) : "))
        y = int(input("Y (0-9) : "))
    except:
        rich_print("[red]❌ Coordonnées invalides.[/red]")
        return

    if not (0 <= x < 10 and 0 <= y < 10):
        rich_print("[red]❌ Hors de la grille.[/red]")
        return

    if data["grid"][y][x] != ".":
        rich_print("[red]❌ Case déjà occupée.[/red]")
        return

    if machine_key in droppers:
        code = "D"
    elif machine_key in upgraders:
        code = "U"
    elif machine_key in collectors:
        code = "C"
    elif machine_key in depots:
        code = "P"
    else:
        code = "S"

    data["grid"][y][x] = code

    pos_key = f"{x},{y}"
    data["placed"][pos_key] = machine_key

    data["machines"][category][machine_key] -= 1

    rich_print(f"[green]✔ Machine placée : {machine_key} en ({x},{y})[/green]")
    save_game(data)


def remove_machine(data):
    rich_print("\n[bold cyan]=== REMOVE MACHINE ===[/bold cyan]")

    try:
        x = int(input("X (0-9) : "))
        y = int(input("Y (0-9) : "))
    except:
        rich_print("[red]❌ Coordonnées invalides.[/red]")
        return

    pos_key = f"{x},{y}"

    if pos_key not in data["placed"]:
        rich_print("[red]❌ Aucune machine ici.[/red]")
        return

    machine_key = data["placed"][pos_key]

    data["grid"][y][x] = "."
    del data["placed"][pos_key]

    for category in data["machines"]:
        if machine_key in data["machines"][category]:
            data["machines"][category][machine_key] += 1
            break

    rich_print(f"[green]✔ Machine retirée : {machine_key}[/green]")
    save_game(data)




# ============================
#   ACTIONS
# ============================

def mine_stone(data):
    data["inventory"]["stone"] += 1
    rich_print("[yellow]⛏️  +1 Stone[/yellow]")
    save_game(data)


def sell_material(data):
    rich_print("\n[bold cyan]=== SELL ===[/bold cyan]")
    rich_print("Tu peux vendre :")

    owned_materials = {k: v for k, v in data["inventory"].items() if k in materials and v > 0}

    if not owned_materials:
        rich_print("[red]❌ Tu ne possèdes aucun matériau à vendre.[/red]")
        return

    for key, amount in owned_materials.items():
        mat = materials[key]
        rich_print(f"- {mat.colored_name()} (valeur : {mat.value}$) : {amount}")

    choice = input("Quel matériau veux-tu vendre ? : ")

    if choice not in owned_materials:
        rich_print("[red]❌ Tu ne possèdes pas ce matériau.[/red]")
        return

    try:
        amount = int(input("Combien veux-tu en vendre ? : "))
    except ValueError:
        rich_print("[red]❌ Nombre invalide.[/red]")
        return

    if amount <= 0:
        rich_print("[red]❌ Nombre doit être > 0.[/red]")
        return

    if data["inventory"][choice] < amount:
        rich_print(f"[red]❌ Pas assez de {choice}[/red]")
        return

    mat = materials[choice]
    gain = amount * mat.value

    data["inventory"][choice] -= amount
    data["inventory"]["money"] += gain

    rich_print(f"[green]💰 Tu gagnes {format_money(gain)}[/green]")
    save_game(data)


def build_depot(data):
    rich_print("\n[bold cyan]=== BUILD DEPOT ===[/bold cyan]")
    for key, depot in depots.items():
        rich_print(f"- {depot.colored_name()} | {format_money(depot.cost_money)} + {depot.cost_materials}")

    choice = input("Quel depot veux-tu construire ? : ")

    if choice not in depots:
        rich_print("[red]❌ Depot inconnu.[/red]")
        return

    depot = depots[choice]

    if data["inventory"]["money"] < depot.cost_money:
        rich_print("[red]❌ Pas assez d'argent.[/red]")
        return

    for mat_key, needed in depot.cost_materials.items():
        if data["inventory"].get(mat_key, 0) < needed:
            rich_print(f"[red]❌ Pas assez de {mat_key}[/red]")
            return

    data["inventory"]["money"] -= depot.cost_money
    for mat_key, needed in depot.cost_materials.items():
        data["inventory"][mat_key] -= needed

    data["machines"]["depots"][choice] = data["machines"]["depots"].get(choice, 0) + 1

    rich_print(f"[green]🏭 Depot construit : {depot.name}[/green]")
    save_game(data)


def build_dropper(data):
    rich_print("\n[bold cyan]=== BUILD DROPPER ===[/bold cyan]")
    for key, dropper in droppers.items():
        rich_print(f"- {dropper.colored_name()} | {format_money(dropper.cost_money)} + {dropper.cost_materials}")

    choice = input("Quel dropper veux-tu construire ? : ")

    if choice not in droppers:
        rich_print("[red]❌ Dropper inconnu.[/red]")
        return

    dropper = droppers[choice]

    if data["inventory"]["money"] < dropper.cost_money:
        rich_print("[red]❌ Pas assez d'argent.[/red]")
        return

    for mat_key, needed in dropper.cost_materials.items():
        if data["inventory"].get(mat_key, 0) < needed:
            rich_print(f"[red]❌ Pas assez de {mat_key}[/red]")
            return

    data["inventory"]["money"] -= dropper.cost_money
    for mat_key, needed in dropper.cost_materials.items():
        data["inventory"][mat_key] -= needed

    data["machines"]["droppers"][choice] = data["machines"]["droppers"].get(choice, 0) + 1

    rich_print(f"[green]🏭 Dropper construit : {dropper.name}[/green]")
    save_game(data)


def build_upgrader(data):
    rich_print("\n[bold cyan]=== BUILD UPGRADER ===[/bold cyan]")
    for key, upgrader in upgraders.items():
        rich_print(f"- {upgrader.colored_name()} | {format_money(upgrader.cost_money)} + {upgrader.cost_materials}")

    choice = input("Quel upgrader veux-tu construire ? : ")

    if choice not in upgraders:
        rich_print("[red]❌ Upgrader inconnu.[/red]")
        return

    upgrader = upgraders[choice]

    if data["inventory"]["money"] < upgrader.cost_money:
        rich_print("[red]❌ Pas assez d'argent.[/red]")
        return

    for mat_key, needed in upgrader.cost_materials.items():
        if data["inventory"].get(mat_key, 0) < needed:
            rich_print(f"[red]❌ Pas assez de {mat_key}[/red]")
            return

    data["inventory"]["money"] -= upgrader.cost_money
    for mat_key, needed in upgrader.cost_materials.items():
        data["inventory"][mat_key] -= needed

    data["machines"]["upgraders"][choice] = data["machines"]["upgraders"].get(choice, 0) + 1

    rich_print(f"[green]🔧 Upgrader construit : {upgrader.name}[/green]")
    save_game(data)


def build_collector(data):
    rich_print("\n[bold cyan]=== BUILD COLLECTOR ===[/bold cyan]")

    for key, collector in collectors.items():
        mat_cost = ", ".join(
            f"[{MATERIAL_COLORS[m]}]{m}[/]: {amt}"
            for m, amt in collector.cost_materials.items()
        ) if collector.cost_materials else "Aucun matériau"

        rich_print(
            f"- {collector.colored_name()} | "
            f"{format_money(collector.cost_money)} + {mat_cost}"
        )

    choice = input("Quel collector veux-tu construire ? : ")

    if choice not in collectors:
        rich_print("[red]❌ Collector inconnu.[/red]")
        return

    collector = collectors[choice]

    # Vérification argent
    if data["inventory"]["money"] < collector.cost_money:
        rich_print("[red]❌ Pas assez d'argent.[/red]")
        return

    # Vérification matériaux
    for mat_key, needed in collector.cost_materials.items():
        if data["inventory"].get(mat_key, 0) < needed:
            rich_print(f"[red]❌ Pas assez de {mat_key}[/red]")
            return

    # Paiement
    data["inventory"]["money"] -= collector.cost_money
    for mat_key, needed in collector.cost_materials.items():
        data["inventory"][mat_key] -= needed

    # Ajout collector
    data["machines"]["collectors"][choice] = data["machines"]["collectors"].get(choice, 0) + 1

    rich_print(f"[green]🔥 Collector construit : {collector.name}[/green]")
    save_game(data)



def build_special_machine(data):
    from rich import print as rich_print

    rich_print("\n[bold cyan]=== BUILD SPECIAL MACHINE ===[/bold cyan]")

    for key, machine in machines.items():
        # Affichage du coût en matériaux
        mat_cost = ", ".join(
            f"[{MATERIAL_COLORS[m]}]{m}[/]: {amt}"
            for m, amt in machine.cost_materials.items()
        ) if hasattr(machine, "cost_materials") else "Aucun matériau"

        rich_print(
            f"- {machine.colored_name()} | "
            f"{format_money(machine.cost_money)} + {mat_cost}"
        )

    choice = input("Quelle machine veux-tu construire ? : ")

    if choice not in machines:
        rich_print("[red]❌ Machine inconnue.[/red]")
        return

    machine = machines[choice]

    # Vérification argent
    if data["inventory"]["money"] < machine.cost_money:
        rich_print("[red]❌ Pas assez d'argent.[/red]")
        return

    # Vérification matériaux
    for mat_key, needed in machine.cost_materials.items():
        if data["inventory"].get(mat_key, 0) < needed:
            rich_print(f"[red]❌ Pas assez de {mat_key}[/red]")
            return

    # Paiement
    data["inventory"]["money"] -= machine.cost_money
    for mat_key, needed in machine.cost_materials.items():
        data["inventory"][mat_key] -= needed

    # Ajout machine
    data["machines"]["special"][choice] = data["machines"]["special"].get(choice, 0) + 1

    rich_print(f"[green]⚙️ Machine construite : {machine.name}[/green]")
    save_game(data)



def build_generator(data):
    rich_print("\n[bold cyan]=== BUILD GENERATOR ===[/bold cyan]")
    for key, gen in generators.items():
        rich_print(f"- {gen.colored_name()} | {format_money(gen.cost_money)} + {gen.cost_materials} → {format_power(gen.power_output)}")

    choice = input("Quel générateur veux-tu construire ? : ")

    if choice not in generators:
        rich_print("[red]❌ Générateur inconnu.[/red]")
        return

    gen = generators[choice]

    if data["inventory"]["money"] < gen.cost_money:
        rich_print("[red]❌ Pas assez d'argent.[/red]")
        return

    for mat_key, needed in gen.cost_materials.items():
        if data["inventory"].get(mat_key, 0) < needed:
            rich_print(f"[red]❌ Pas assez de {mat_key}[/red]")
            return

    data["inventory"]["money"] -= gen.cost_money
    for mat_key, needed in gen.cost_materials.items():
        data["inventory"][mat_key] -= needed

    data["power"]["generators"][choice] = data["power"]["generators"].get(choice, 0) + gen.power_output
    data["power"]["total_power"] += gen.power_output

    rich_print(f"[green]⚡ Générateur construit : {gen.name}[/green]")
    save_game(data)


def process_one_drop(data):
    rich_print("\n[bold cyan]=== PROCESS DROP ===[/bold cyan]")

    # Vérification droppers
    if not data["machines"]["droppers"]:
        rich_print("[red]❌ Aucun dropper disponible.[/red]")
        return

    # Vérification collectors
    if not data["machines"]["collectors"]:
        rich_print("[red]❌ Aucun collector disponible.[/red]")
        return

    # ============================
    #   TROUVER LE MEILLEUR DROPPER
    # ============================

    best_dropper = None
    best_dropper_value = 0

    for key, count in data["machines"]["droppers"].items():
        dropper = droppers[key]
        if dropper.base_value > best_dropper_value:
            best_dropper_value = dropper.base_value
            best_dropper = dropper

    # ============================
    #   UPGRADERS : STACK COMPLET
    # ============================

    upgrader_list = []

    for key, count in data["machines"]["upgraders"].items():
        for _ in range(count):
            upgrader_list.append(upgraders[key])

    # ============================
    #   TROUVER LE MEILLEUR COLLECTOR
    # ============================

    best_collector = None
    best_collector_value = 1

    for key, count in data["machines"]["collectors"].items():
        collector = collectors[key]
        if collector.multiplier > best_collector_value:
            best_collector_value = collector.multiplier
            best_collector = collector

    # ============================
    #   VÉRIFIER L'ÉNERGIE TOTALE
    # ============================
    total_power = data["power"]["total_power"]
    # Calcul consommation totale
    total_consumption = 0

    # Depots
    for key, count in data["machines"]["depots"].items():
        depot = depots.get(key)
        if depot:
            total_consumption += depot.power_required * count

    # Droppers
    for key, count in data["machines"]["droppers"].items():
        dropper = droppers.get(key)
        if dropper:
            total_consumption += dropper.power_required * count

    # Upgraders
    for key, count in data["machines"]["upgraders"].items():
        upgrader = upgraders.get(key)
        if upgrader:
            total_consumption += upgrader.power_required * count

    # Collectors
    for key, count in data["machines"]["collectors"].items():
        collector = collectors.get(key)
        if collector:
            total_consumption += collector.power_required * count

    # Special machines
    for key, count in data["machines"]["special"].items():
        machine = machines.get(key)
        if machine and hasattr(machine, "power_required"):
            total_consumption += machine.power_required * count

    # Vérification surcharge
    if total_power < total_consumption:
        rich_print("[red]❌ Impossible d'utiliser votre setup : consommation d'énergie trop élevée.[/red]")
        return


    # ============================
    #   CALCUL FINAL DU DROP
    # ============================

    final_value = process_drop(best_dropper, upgrader_list, best_collector)

    data["inventory"]["money"] += final_value

    rich_print(f"[green]💎 Valeur du drop : {format_money(final_value)}[/green]")
    rich_print(f"[green]💰 Argent total : {format_money(data['inventory']['money'])}[/green]")

    save_game(data)


def use_machines(data):
    from rich import print as rich_print

    rich_print("\n[bold cyan]=== MACHINES ===[/bold cyan]")

    # Liste des machines possédées
    owned = []
    for key, count in data["machines"]["special"].items():
        if count > 0:
            owned.append(key)

    if not owned:
        rich_print("[red]❌ Tu n'as aucune machine spéciale.[/red]")
        return

    # Affichage du menu
    for i, key in enumerate(owned, 1):
        machine = machines[key]
        rich_print(f"{i}. {machine.colored_name()}")

    try:
        choice = int(input("Choisis une machine : "))
    except ValueError:
        rich_print("[red]❌ Choix invalide.[/red]")
        return

    if choice < 1 or choice > len(owned):
        rich_print("[red]❌ Choix invalide.[/red]")
        return

    selected_key = owned[choice - 1]

    # Appel de la machine correspondante
    if selected_key == "wood_sawmill":
        process_wood_sawmill(data)
    elif selected_key == "alloy_factory":
        process_alloy_factory(data)
    else:
        rich_print("[yellow]⚠ Cette machine n'a pas encore de fonction.[/yellow]")

# ============================
#   PRODUCTION AUTOMATIQUE
# ============================

def tick_production(data):
    total_power = data["power"].get("total_power", 0)
    # ============================
    #   SURCHARGE : STOP PRODUCTION
    # ============================

    # Calcul consommation totale
    total_consumption = 0

    # Depots
    for key, count in data["machines"]["depots"].items():
        depot = depots.get(key)
        if depot:
            total_consumption += depot.power_required * count

    # Droppers
    for key, count in data["machines"]["droppers"].items():
        dropper = droppers.get(key)
        if dropper:
            total_consumption += dropper.power_required * count

    # Upgraders
    for key, count in data["machines"]["upgraders"].items():
        upgrader = upgraders.get(key)
        if upgrader:
            total_consumption += upgrader.power_required * count

    # Collectors
    for key, count in data["machines"]["collectors"].items():
        collector = collectors.get(key)
        if collector:
            total_consumption += collector.power_required * count

    # Special machines
    for key, count in data["machines"]["special"].items():
        machine = machines.get(key)
        if machine and hasattr(machine, "power_required"):
            total_consumption += machine.power_required * count

    # Si surcharge → production stoppée
    if total_power < total_consumption:
        # On ne produit rien, mais on ne bloque pas le jeu
        return


    for depot_key in data["machines"]["depots"]:
        if depot_key not in data["depot_timers"]:
            data["depot_timers"][depot_key] = 0

    for depot_key, count in data["machines"]["depots"].items():
        depot = depots.get(depot_key)
        if not depot:
            continue

        required = depot.power_required * count
        if total_power < required:
            continue

        data["depot_timers"][depot_key] += 1

        if data["depot_timers"][depot_key] >= depot.production_time:
            for mat_key, amount in depot.production.items():
                data["inventory"][mat_key] = data["inventory"].get(mat_key, 0) + amount * count

            data["depot_timers"][depot_key] = 0

    save_game(data)


# ============================
#   MAIN LOOP
# ============================

def main():
    data = init_game()
    last_tick = time.time()

    while True:
        current = time.time()
        elapsed = current - last_tick

        if elapsed >= 1:
            ticks = int(elapsed)
            for _ in range(ticks):
                tick_production(data)
            last_tick = current

        print("\n=== MENU ===")
        print("1. Mine (Stone)")
        print("2. Inventory")
        print("3. Sell")
        print("4. Build Depot")
        print("5. Build Dropper")
        print("6. Build Upgrader")
        print("7. Build Collector")
        print("8. Build Special Machine")
        print("9. Base")
        print("10. Exit")
        print("11. Build Generator")
        print("12. Process Drop")
        print("13. Use Machines")
        print("14. View Tycoon")


        choice = input("Choisis une option : ")

        if choice == "1":
            mine_stone(data)
        elif choice == "2":
            show_inventory(data)
        elif choice == "3":
            sell_material(data)
        elif choice == "4":
            build_depot(data)
        elif choice == "5":
            build_dropper(data)
        elif choice == "6":
            build_upgrader(data)
        elif choice == "7":
            build_collector(data)
        elif choice == "8":
            build_special_machine(data)
        elif choice == "9":
            show_base(data)
        elif choice == "10":
            rich_print("[bold red]👋 Au revoir Esteban ![/bold red]")
            save_game(data)
            break
        elif choice == "11":
            build_generator(data)
        elif choice == "12":
            process_one_drop(data)
        elif choice == "13":
            use_machines(data)
        elif choice == "14":
            while True:
                rich_print("\n[bold cyan]=== TYCOON MENU ===[/bold cyan]")
                print("1. Show Grid")
                print("2. Place Machine")
                print("3. Remove Machine")
                print("4. Back")

                sub = input("Choisis une option : ")

                if sub == "1":
                    show_grid(data)
                elif sub == "2":
                    place_machine(data)
                elif sub == "3":
                    remove_machine(data)
                elif sub == "4":
                    break
                else:
                    rich_print("[red]❌ Option invalide.[/red]")
        else:
            rich_print("[red]❌ Option invalide.[/red]")


if __name__ == "__main__":
    main()
