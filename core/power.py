from typing import Dict
from math import log10, floor

# Power system and formatting utilities

class PowerSystem:
    def __init__(self):
        self.total_power = 0
        self.generators: Dict[str, int] = {}

    def add_generator(self, key, amount):
        self.generators[key] = self.generators.get(key, 0) + amount
        self.calculate_power()

    def calculate_power(self):
        self.total_power = sum(self.generators.values())
        return self.total_power

    def has_power(self, required):
        return self.total_power >= required

# -------------------------
# Formatting helpers
# -------------------------
# We format numbers by groups of 1000 (thousands). For extremely large numbers,
# if we run out of named suffixes we fall back to scientific notation.

_SUFFIXES = [
    "u",    # base unit
    "ku",   # kilo
    "Mu",   # mega
    "Bu",   # billion
    "Tu",   # trillion
    "qdU",  # quadrillion
    "Qnu",  # quintillion (Qn)
    "su",   # sextillion (short)
    "spu",  # septillion
    "ocu",  # octillion
    "nu",   # nonillion
    "deu",  # decillion
    "Udu",  # undecillion
    "Ddu",  # duodecillion
    "Tdu",  # tredecillion
    "qdDu", # quattuordecillion
    "QnDu", # quindecillion
    "Vdu",  # etc...
    # ... list can be extended if you want more human-readable names
]

def _format_with_suffix(value: float, suffixes=_SUFFIXES, precision: int = 2) -> str:
    if value < 1000:
        # integer if small, else keep decimals
        if float(value).is_integer():
            return f"{int(value)}"
        return f"{value:.{precision}f}"

    idx = 0
    v = float(value)
    while v >= 1000 and idx + 1 < len(suffixes):
        v /= 1000.0
        idx += 1

    if v >= 1000 and idx + 1 >= len(suffixes):
        # too big for named suffixes: use scientific notation
        return f"{value:.2e}"

    return f"{v:.{precision}f}{suffixes[idx]}"

def format_power(u: int) -> str:
    """
    Format energy units (u) into human readable string:
    1000 -> 1.00ku, 1_000_000 -> 1.00Mu, etc.
    """
    if u is None:
        return "0u"
    # use _format_with_suffix but ensure base suffix 'u' is appended for small numbers
    if u < 1000:
        return f"{u}u"
    # _format_with_suffix returns like "1.50ku" but without trailing 'u' for base; our suffixes already include 'u'
    return _format_with_suffix(u)  # suffixes already include 'u' variants

def format_money(amount: float) -> str:
    """
    Format money with 2 decimals ALWAYS.
    Uses suffixes (k, M, B...) for large numbers.
    """
    if amount is None:
        return "0$"

    # Si < 1000 → format normal avec 2 décimales
    if amount < 1000:
        return f"{amount:.2f}$"

    # Suffixes pour grands nombres
    money_suffixes = [
        "",    # base
        "k",   # thousand
        "M",   # million
        "B",   # billion
        "T",   # trillion
        "qd",  # quadrillion
        "Qn",  # quintillion
        "s",   # sextillion
        "sp",  # septillion
        "oc",  # octillion
        "n",   # nonillion
        "d",   # decillion
        "Ud",
        "Dd",
        "Td",
        "qdD",
        "QnD",
    ]

    # On construit une liste de suffixes pour _format_with_suffix
    tmp_suffixes = [""] + money_suffixes[1:]

    formatted = _format_with_suffix(amount, suffixes=tmp_suffixes, precision=2)

    # Si notation scientifique → ajouter $
    if "e" in formatted:
        return f"{formatted}$"

    return f"{formatted}$"

def format_resource(amount: float) -> str:
    """
    Format resources (stone, wood, coal...) with suffixes (k, M, B...)
    Always 2 decimals.
    """
    if amount is None:
        return "0"

    # Si < 1000 → format normal avec 2 décimales
    if amount < 1000:
        return f"{amount:.2f}"

    # Suffixes pour grands nombres
    resource_suffixes = [
        "",    # base
        "k",   # thousand
        "M",   # million
        "B",   # billion
        "T",   # trillion
        "qd",  # quadrillion
        "Qn",  # quintillion
        "s",   # sextillion
        "sp",  # septillion
        "oc",  # octillion
        "n",   # nonillion
        "d",   # decillion
        "Ud",
        "Dd",
        "Td",
        "qdD",
        "QnD",
    ]

    tmp_suffixes = [""] + resource_suffixes[1:]
    formatted = _format_with_suffix(amount, suffixes=tmp_suffixes, precision=2)

    return formatted


