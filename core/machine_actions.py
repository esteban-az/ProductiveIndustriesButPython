from rich import print as rich_print
from core.colors import MATERIAL_COLORS
from data.materials import materials
from data.alloys import alloy_recipes_2m
from data.machines import machines
from core.save import save_game
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
import time


# ============================
#   WOOD SAWMILL
# ============================



def process_wood_sawmill(data):
    rich_print("\n[bold cyan]=== WOOD SAWMILL ===[/bold cyan]")

    # Vérifier surcharge globale
    if data["power"]["total_power"] < data["power"].get("last_consumption", 0):
        rich_print("[red]❌ La base est en surcharge énergétique. Machines spéciales désactivées.[/red]")
        return

    wood_amount = data["inventory"].get("wood", 0)
    if wood_amount <= 0:
        rich_print("[red]❌ Tu n'as pas de Wood.[/red]")
        return

    rich_print(f"Tu as [#8B4513]{wood_amount} Wood[/#8B4513].")
    rich_print("Ratio : [#8B4513]1 Wood[/#8B4513] → [#D2B48C]4 Wooden Planks[/#D2B48C]")

    try:
        amount = int(input("Combien de Wood veux-tu transformer ? : "))
    except ValueError:
        rich_print("[red]❌ Nombre invalide.[/red]")
        return

    if amount <= 0:
        rich_print("[red]❌ Le nombre doit être > 0.[/red]")
        return

    if amount > wood_amount:
        rich_print("[red]❌ Tu n'as pas assez de Wood.[/red]")
        return

    sawmills = data["machines"]["special"]["wood_sawmill"]
    machine = machines["wood_sawmill"]
    required_power = machine.power_required * sawmills

    # Vérifier énergie locale
    if data["power"]["total_power"] < required_power:
        rich_print("[red]❌ Pas assez d'énergie pour utiliser le Wood Sawmill.[/red]")
        return

    # Temps de process (10 secondes)
    PROCESS_TIME = 10

    rich_print("[yellow]⚙ Le Wood Sawmill commence à travailler...[/yellow]")

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("Transformation en cours...", total=PROCESS_TIME)
        for _ in range(PROCESS_TIME):
            time.sleep(1)
            progress.update(task, advance=1)

    # Transformation finale
    planks = amount * 4

    data["inventory"]["wood"] -= amount
    data["inventory"]["wooden_planks"] = data["inventory"].get("wooden_planks", 0) + planks

    rich_print(f"[green]✔ Transformation réussie ![/green]")
    rich_print(f"[#8B4513]-{amount} Wood[/#8B4513]")
    rich_print(f"[#D2B48C]+{planks} Wooden Planks[/#D2B48C]")

    save_game(data)



# ============================
#   ALLOY FACTORY (MODULAR 2 MATERIALS)
# ============================
def process_alloy_factory(data):
    rich_print("\n[bold cyan]=== ALLOY FACTORY ===[/bold cyan]")
    
    # Stop global si surcharge
    if data["power"]["total_power"] < data["power"].get("last_consumption", 0):
        rich_print("[red]❌ La base est en surcharge énergétique. Machines spéciales désactivées.[/red]")
        return

    # Liste des alliages disponibles
    rich_print("Quels alliage veux-tu fabriquer ?")
    for alloy in alloy_recipes_2m:
        rich_print(f"- {alloy}")

    choice = input("Alloy : ").lower()

    if choice not in alloy_recipes_2m:
        rich_print("[red]❌ Cet alliage n'existe pas.[/red]")
        return

    recipe = alloy_recipes_2m[choice]
    inputs = recipe["inputs"]
    output_amount = recipe["output"]
    machine_key = recipe["machine_key"]
    process_time = recipe.get("time", 10)  # fallback si pas défini

    # Vérifier que la machine existe dans la base
    machines_count = data["machines"]["special"].get(machine_key, 0)
    if machines_count <= 0:
        rich_print("[red]❌ Tu n'as pas d'Alloy Factory dans ta base.[/red]")
        return

    # Vérifier énergie locale
    machine = machines[machine_key]
    required_power = machine.power_required * machines_count

    if data["power"]["total_power"] < required_power:
        rich_print("[red]❌ Pas assez d'énergie pour utiliser l'Alloy Factory.[/red]")
        return

    # Vérifier matériaux
    for mat, amt in inputs.items():
        if data["inventory"].get(mat, 0) < amt:
            rich_print(f"[red]❌ Pas assez de {mat}.[/red]")
            return

    # Affichage du ratio
    rich_print("Ratio :")
    for mat, amt in inputs.items():
        rich_print(f"  {mat} x{amt}")

    try:
        amount = int(input(f"Combien de {choice} veux-tu fabriquer ? : "))
    except ValueError:
        rich_print("[red]❌ Nombre invalide.[/red]")
        return

    if amount <= 0:
        rich_print("[red]❌ Le nombre doit être > 0.[/red]")
        return

    # Vérifier matériaux totaux
    for mat, amt in inputs.items():
        if data["inventory"].get(mat, 0) < amt * amount:
            rich_print("[red]❌ Pas assez de matériaux.[/red]")
            return

    # Consommer matériaux
    for mat, amt in inputs.items():
        data["inventory"][mat] -= amt * amount

    # Temps de process
    rich_print(f"[yellow]⚙ Fabrication de {choice} en cours...[/yellow]")

    total_time = process_time * amount

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task(f"Création de {choice}...", total=total_time)
        for _ in range(total_time):
            time.sleep(1)
            progress.update(task, advance=1)

    # Donner l'alliage
    data["inventory"][choice] = data["inventory"].get(choice, 0) + (output_amount * amount)

    rich_print(f"[green]✔ {choice.capitalize()} créé avec succès ![/green]")

    for mat, amt in inputs.items():
        rich_print(f"[red]-{amt * amount} {mat}[/red]")

    rich_print(f"[green]+{output_amount * amount} {choice}[/green]")

    save_game(data)

