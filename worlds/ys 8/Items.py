from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import Item, ItemClassification


class Ys8Item(Item):
    game: str = "Kingdom Hearts"


class Ys8ItemData(NamedTuple):
    category: str
    code: int
    type: str
    quantity: int = 1
    classification: ItemClassification = ItemClassification.filler
    weight: int = 1
    flags: Optional[list[bytes]] = None


def get_items_by_category(category: str) -> Dict[str, Ys8ItemData]:
    return {name: data for name, data in item_table.items() if data.category == category}

item_table: Dict[str, Ys8ItemData] = {
    "Leather Armor":                    Ys8ItemData("Armor",        code = 243, classification = ItemClassification.useful, type = "Item", quantity = 2),
    "Heal Potion":                      Ys8ItemData("Consumable",   code = 500, classification = ItemClassification.filler, type = "Item", quantity = 1),
    "Coconut":                          Ys8ItemData("Consumable",   code = 531, classification = ItemClassification.filler, type = "Item", quantity = 1),
}

#Make item categories
item_name_groups: Dict[str, Set[str]] = {}
for item in item_table.keys():
    category = item_table[item].category
    if category not in item_name_groups.keys():
        item_name_groups[category] = set()
    item_name_groups[category].add(item)