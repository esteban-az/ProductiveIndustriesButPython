# data/packs.py

class Pack:
    def __init__(self, key, name, tier, cost_money, cost_materials,
                 guaranteed_item, pool, slot_chances, max_uses):
        self.key = key
        self.name = name
        self.tier = tier
        self.cost_money = cost_money
        self.cost_materials = cost_materials
        self.guaranteed_item = guaranteed_item
        self.pool = pool
        self.slot_chances = slot_chances
        self.max_uses = max_uses


packs = {
    "innovator_pack": Pack(
        key="innovator_pack",
        name="Innovator Pack",
        tier="Innovator",
        cost_money=5_000_000,
        cost_materials={"stone": 500_000, "iron": 100_000, "steel": 50_000},

        # Trophée garanti
        guaranteed_item="innovator_pylon",

        # Machines exclusives du pack
        pool=[
            "innovator_dropper",
            "innovator_upgrader",
            "innovator_collector",
            "innovator_generator",
            "innovator_refiner",
            "innovator_core"
        ],

        # Chances des slots (slot 1 = trophée, slot 2 = garanti)
        slot_chances=[1.0, 1.0, 0.7, 0.5, 0.25, 0.05],

        # Max par save file
        max_uses=1
    )
}
