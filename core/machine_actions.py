from rich import print as rich_print
from core.colors import MATERIAL_COLORS
from data.materials import materials
from data.machines import machines
from core.save import save_game


# ============================
#   WOOD SAWMILL
# ============================

def process_wood_sawmill(data):
    rich_print("\n[bold cyan]=== WOOD SAWMILL ===[/bold cyan]")

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

    if data["power"]["total_power"] < required_power:
        rich_print("[red]❌ Pas assez d'énergie pour utiliser le Wood Sawmill.[/red]")
        return

    planks = amount * 4

    data["inventory"]["wood"] -= amount
    data["inventory"]["wooden_planks"] = data["inventory"].get("wooden_planks", 0) + planks

    rich_print(f"[green]✔ Transformation réussie ![/green]")
    rich_print(f"[#8B4513]-{amount} Wood[/#8B4513]")
    rich_print(f"[#D2B48C]+{planks} Wooden Planks[/#D2B48C]")

    save_game(data)



# ============================
#   ALLOY FACTORY (STEEL)
# ============================

def process_alloy_factory(data):
    rich_print("\n[bold cyan]=== ALLOY FACTORY ===[/bold cyan]")

    coal = data["inventory"].get("coal", 0)
    iron = data["inventory"].get("iron", 0)

    if coal < 2 or iron < 1:
        rich_print("[red]❌ Pas assez de matériaux pour fabriquer du Steel.[/red]")
        rich_print("Il faut : 2 Coal + 1 Iron")
        return

    rich_print(f"Tu as [#202020]{coal} Coal[/#202020] et [#D8D8D8]{iron} Iron[/#D8D8D8].")
    rich_print("Ratio : [#202020]2 Coal[/#202020] + [#D8D8D8]1 Iron[/#D8D8D8] → [#C0C0C0]1 Steel[/#C0C0C0]")

    try:
        amount = int(input("Combien de Steel veux-tu fabriquer ? : "))
    except ValueError:
        rich_print("[red]❌ Nombre invalide.[/red]")
        return

    if amount <= 0:
        rich_print("[red]❌ Le nombre doit être > 0.[/red]")
        return

    required_coal = amount * 2
    required_iron = amount * 1

    if coal < required_coal or iron < required_iron:
        rich_print("[red]❌ Tu n'as pas assez de matériaux.[/red]")
        return

    factories = data["machines"]["special"]["alloy_factory"]
    machine = machines["alloy_factory"]
    required_power = machine.power_required * factories

    if data["power"]["total_power"] < required_power:
        rich_print("[red]❌ Pas assez d'énergie pour utiliser l'Alloy Factory.[/red]")
        return

    data["inventory"]["coal"] -= required_coal
    data["inventory"]["iron"] -= required_iron
    data["inventory"]["steel"] = data["inventory"].get("steel", 0) + amount

    rich_print(f"[green]✔ Alloy créé avec succès ![/green]")
    rich_print(f"[#202020]-{required_coal} Coal[/#202020]")
    rich_print(f"[#D8D8D8]-{required_iron} Iron[/#D8D8D8]")
    rich_print(f"[#C0C0C0]+{amount} Steel[/#C0C0C0]")

    save_game(data)
