import random
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
from difflib import get_close_matches



DEFAULT_Rules = {
    "required_tags": ["Braten"],
    "forbidden_tags": [],
    "max_tags_counts": {
        "Vegan": 1,
        "Fisch": 1,
        "Hühnchen": 1,
        "Rind": 1,
        "Schwein": 1,
        "Schokolade":1
    },
    "unique_main": True,
}

@dataclass
class Item:
    name: str
    category: str
    tags: Set[str]
    main: str 

def satisfies_rules(Buffet: List[Item], rules: Dict): 
    required = rules.get("required_tags", [])
    forbidden = rules.get("forbidden_tags", [])
    
    unique_main = rules.get("unique_main", False)
    all_tags = set()
    for item in Buffet:
        all_tags |= item.tags
    for tag in rules["required_tags"]:
        if tag not in all_tags:
            return False

    for tag in rules["forbidden_tags"]:
        if tag in all_tags:
            return False

    Sättigung = [i.name for i in Buffet if i.category == "Sättigung"]
    if len(Sättigung) != len(set(Sättigung)):
        return False
    Beilagen = [i.name for i in Buffet if i.category == "Beilage"]
    if len(Beilagen) != len(set(Beilagen)):
        return False
    Hauptgerichte = [i.name for i in Buffet if i.category == "Hauptgericht"]
    if len(Hauptgerichte) != len(set(Hauptgerichte)):
        return False    
    return True



def generate_Buffet(required_tags: List[str], forbidden_tags: List[str], max_tries: int = 9000) -> List[Dict]:
    all_items =  Hauptgerichte + Sättigung + Beilagen + Desserts

    rules = {
        "required_tags": required_tags,
        "forbidden_tags": forbidden_tags,
        "unique_main": True,}
    for _ in range(max_tries):
        b = random_Buffet()
        if satisfies_rules(b, rules):
            return [{
                "name": item.name, "category": item.category,
                "tags": sorted(list(item.tags)), "main": item.main}
            for item in b]

        return []

Hauptgerichte = [Item("Kasslerbraten", "Hauptgericht", {"Schwein", "Braten", "Klassisch"}, "Schwein"),
                Item("Rinderroulade", "Hauptgericht", {"Rind", "Braten", "Klassisch"}, "Rind"),
                Item("Gullasch", "Hauptgericht", {"Rind", "Braten", "Klassisch"}, "Rind"),
                Item("Hähnchen-Tomate-Morzarella", "Hauptgericht", {"Hühnchen", "Tomate", "Mozzarella", "Mediterran"}, "Hühnchen"),
                Item("Lachs auf Grillgemüse", "Hauptgericht", {"Fisch", "Gemüse", "Mediterran", "Lachs", "Grillgemüse"}, "Fisch"),
                Item("Zander auf Grillgemüse", "Hauptgericht", {"Zander", "Fisch", "Gemüse"}, "Fisch"),
                Item("Blätterteig Zupfbrot", "Hauptgericht", {"Blätterteig", "Vegan", "Brot"}, "Vegan"),
                Item("Gemischte Warme Platte", "Hauptgericht", {"Schnitezl", "Bouletten", "Gnubbel", "Platte"}, "Schnitzel"),]
Sättigung = [Item("Salzartoffel", "Sättigung", {"Salzartoffel", "Kartoffel"}, "Kartoffel"),
            Item("Klöße", "Sättigung", {"Klöße", "Kartoffel"}, "Kartoffel"),
            Item("Reis", "Sättigung", {"Reis", "Asia"}, "Reis"),
            Item("Böhmische Knödel", "Sättigung", {"Böhmische Knödel", "Knödel"}, "Kartoffel"),
            Item("Pommes", "Sättigung", {"Pommes"}, "Kartoffel"),
            Item("Kartoffel-Spalten", "Sättigung", {"Kartoffel-Spalten"}, "Kartoffel"),]
Beilagen = [Item("Rotkohl", "Beilage", {"Rotkohl"}, "Kartoffel"),
            Item("Keisergemüse", "Beilage", {"Keisergemüse", "Gemüse"}, "Gemüse"),
            Item("Grillgemüse", "Beilage", {"Grillgemüse", "Gemüse"}, "Gemüse"),
            Item("Spinat", "Beilage", {"Spinat"}, "Gemüse"),]
Desserts = [Item("Schokoladenmousse", "Dessert", {"Schokoladenmousse"}, "Schokolade"),
            Item("Schockopudding", "Dessert", {"Schockopudding", "Schokolade", "Pudding"}, "Schokolade"),
            Item("Vanillepudding", "Dessert", {"Vanillepudding", "Vanille", "Pudding"}, "Vanille"),
            Item("Cheesecake", "Dessert", {"Cheesecake"}, "Frischkäse"),
            Item("Waldbeercreme", "Dessert", {"Waldbeercreme", "Waldbeere", "Frucht"}, "Waldbeere"),
            Item("Waldmeister-Götterspeise", "Dessert", {"Waldmeister-Götterspeise", "Waldmeister"}, "Waldmeister"),
            Item("Obstplatte", "Dessert", {"Obst", "Frucht"}, "Frucht"),]




def parse_csv_words(s: str) -> list[str]:
   """
   "Braten, Vegan, Fisch" -> ["Braten", "Vegan", "Fisch"]
   leere eingabe -> []
   """
   s = s.strip()
   if not s:
       return []
   return [word.strip() for word in s.split(",") if word.strip()]



def collect_all_tags(all_items: list) -> list[str]:
    tags = set()
    for it in all_items:
        tags |= it.tags
    return sorted(tags)




def ask_tag_list(prompt: str, allowed_tags: set[str]) -> list[str]:
    while True:
        raw_input = input(prompt).strip()
        tags = parse_csv_words(raw_input)
        if not tags:
            return []
        if all(tag in allowed_tags for tag in tags):
            return tags
        print("ein oder mehrere Tags sind ungültig.")
        return tags



def build_rules_from_user_input(all_items: list) -> Dict:
    all_tags = collect_all_tags(all_items)
    allowed_tags = set(all_tags)

    required_tags = ask_tag_list("Was soll das Buffet entahlten (kommagetrennt, leer für keine): ", allowed_tags)
    forbidden_tags = ask_tag_list("was soll es nicht enthalten (kommagetrennt, leer für keine): ", allowed_tags)
    
    def normalize_tags(tags: List[str], allowed_tags: List[str], forbidden_tags: List[str], cutoff: float = 0.6) -> List[str]:
        allowed_map = {t.casefold(): t for t in allowed_tags}
        normalized = []
        for row in tags:
            t = row.strp()
            key = t.casefold()

            if key in allowed_map:
                normalized.append(allowed_map[key])
                continue

            matches = get_close_matches(key, allowed_map.keys(), n=1, cutoff=cutoff)
            if matches:
                normalized.append(allowed_map[matches[0]])
            else:
                    normalized.append(t)
        return normalized

    required_tags = normalize_tags(required_tags, all_tags, allowed_tags, cutoff=0.6)
    forbidden_tags = normalize_tags(forbidden_tags, all_tags, allowed_tags, cutoff=0.6)

    rules = {
        "required_tags": required_tags,
        "forbidden_tags": forbidden_tags,
        "unique_main": True,
    }

    return rules

def random_Buffet() -> List[Item]:
    hg1, hg2 = random.sample(Hauptgerichte, 2)
    sg1, sg2 = random.sample(Sättigung, 2)
    bg1, bg2 = random.sample(Beilagen, 2)
    return [
        hg1,
        hg2,
        sg1,
        sg2,
        bg1,
        bg2,
        random.choice(Desserts),
    ]
    
def main():
    all_items =  Hauptgerichte + Hauptgerichte + Sättigung + Beilagen + Desserts
    user_rules = build_rules_from_user_input(all_items)
    required_tags = user_rules["required_tags"]
    forbidden_tags = user_rules["forbidden_tags"]
    max_tries = 1000
    for attempt in range(1, max_tries + 1):
        Buffet = random_Buffet()
        if satisfies_rules(Buffet, user_rules):
            if user_rules["unique_main"]:
                mains = [item.main for item in Buffet if item.category == "Hauptgericht"]
                if len(mains) != len(set(mains)):
                    continue
            break   


    print("Dein Buffet:")
    for Item in Buffet:
        print("-", Item.name)

if __name__ == "__main__":
    main()
    