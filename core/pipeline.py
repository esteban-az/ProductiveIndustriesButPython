def process_drop(dropper, upgrader_list, collector):
    value = dropper.base_value

    # Compter combien de fois chaque upgrader apparaît
    from collections import Counter
    counts = Counter([u.key for u in upgrader_list])

    # On applique les upgraders par groupe (par type), pas un par un
    for key, count_in_base in counts.items():
        upgrader = next(u for u in upgrader_list if u.key == key)

        # Déterminer combien de fois cet upgrader peut être utilisé
        if upgrader.max_uses is None:
            uses = count_in_base
        else:
            uses = min(count_in_base, upgrader.max_uses)

        # Vérifier condition min/max value AVANT d'appliquer
        if upgrader.condition:
            if "min_value" in upgrader.condition:
                if value < upgrader.condition["min_value"]:
                    continue

            if "max_value" in upgrader.condition:
                if value > upgrader.condition["max_value"]:
                    continue

        # Appliquer l'upgrader uses fois
        for _ in range(uses):

            if upgrader.type == "add":
                value += upgrader.value

            elif upgrader.type == "mult":
                value *= upgrader.value

            elif upgrader.type == "conditional_add":
                # condition déjà vérifiée plus haut
                value += upgrader.value

            elif upgrader.type == "conditional_mult":
                # condition déjà vérifiée plus haut
                value *= upgrader.value

    # Collector final (meilleur)
    value *= collector.multiplier

    return value
