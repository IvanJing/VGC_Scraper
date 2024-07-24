import requests
from bs4 import BeautifulSoup

def fetch_pokemon_api():
    """Directly calls the Pokeapi to fetch all pokemon data."""

    url = "https://pokeapi.co/api/v2/pokemon/"

    headers = [
        "pokemon_id",
        "name",
        "type1",
        "type2",
        "health",
        "attack",
        "defense",
        "special_attack",
        "special_defense",
        "speed",
        "ability1",
        "ability2",
        "ability3",
    ]
    pokemon_data = [headers]

    for i in range(1026):
        try:
            pokemon = requests.get(f"{url}{i}").json()
            name = pokemon["name"]
            types = [type["type"]["name"] for type in pokemon["types"]]
            base_stats = {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon["stats"]}
            abilities = [ability["ability"]["name"] for ability in pokemon["abilities"]]

            pokemon_data.append(
                [
                    i,
                    name,
                    types[0] if types else None,
                    types[1] if len(types) > 1 else None,
                    base_stats.get("hp"),
                    base_stats.get("attack"),
                    base_stats.get("defense"),
                    base_stats.get("special-attack"),
                    base_stats.get("special-defense"),
                    base_stats.get("speed"),
                    abilities[0] if abilities else None,
                    abilities[1] if len(abilities) > 1 else None,
                    abilities[2] if len(abilities) > 2 else None,
                ]
            )
            print(f"Fetched data for Pokémon index {i}")
        except Exception as e:
            print(f"Error fetching Pokémon with index {i}: {e}")

    return pokemon_data

def fetch_ability_api():
    """Directly calls the Pokeapi to fetch all ability data."""

    def get_english_effect(effects):
        for effect in effects:
            if effect["language"]["name"] == "en":
                return effect["effect"]
        return None
    
    def fetch_bulbapedia_effect(name):
        name = name.replace(" ", "_")

        url = f"https://bulbapedia.bulbagarden.net/wiki/{name}_(Ability)"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        effect = soup.find('span', {'class': 'mw-headline', 'id': 'Effect'}).parent.find_next("p").text
        return effect
    
    def capital(words):
        words = words.split(" ")
        if len(words) > 1:
            words[0] = words[0].capitalize()
            words[-1] = words[-1].capitalize()
        elif words:
            words[0] = words[0].capitalize()
        
        return ' '.join(words)

    url = "https://pokeapi.co/api/v2/ability/"

    headers = [
        "ability_id",
        "name",
        "effect",
    ]
    ability_data = [headers]
#
    for i in range(1, 308):
        try:
            ability = requests.get(f"{url}{i}").json()
            name = ability["name"].replace("-", " ")

            effect = get_english_effect(ability["effect_entries"])

            if not effect:
                effect = fetch_bulbapedia_effect(capital(name))

            ability_data.append(
                [
                    i,
                    name,
                    effect,
                ]
            )
            print(f"Fetched data for ability index {i}")
        except Exception as e:
            print(f"Error fetching ability with index {i}: {e}")

    return ability_data

def fetch_move_api():
    """Directly calls the Pokeapi to fetch all move data."""

    def get_english_effect(effects):
        for effect in effects:
            if effect["language"]["name"] == "en":
                return [effect["effect"], effect["short_effect"]]
        return None
    
    def fetch_bulbapedia_effect(name):
        name = name.replace(" ", "_")
        url = f"https://bulbapedia.bulbagarden.net/wiki/{name}_(move)"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        effect = soup.find('span', {'class': 'mw-headline', 'id': 'Effect'}).parent.find_next("p").text
        return effect

    url = "https://pokeapi.co/api/v2/move/"

    headers = [ 
        "move_id",
        "name",
        "type",
        "category",
        "power",
        "accuracy",
        "long_effect",
        "short_effect", 
    ]

    move_data = [headers]
    for i in range(1,920):
        try:
            move = requests.get(f"{url}{i}").json()
            name = move["name"].replace("-", " ").title()
            type = move["type"]["name"]
            category = move["damage_class"]["name"]
            power = move["power"]
            accuracy = move["accuracy"]

            effects = get_english_effect(move["effect_entries"])

            if not effects:
                long_effect = fetch_bulbapedia_effect(name)
                short_effect = None
            else:
                long_effect = effects if isinstance(effects, str) else effects[0]
                short_effect = effects[1] if effects[1] else None
            
            long_effect = long_effect.replace("\n", "").strip('"')
            if short_effect: 
                short_effect = short_effect.replace("\n", "")

            move_data.append(
                [
                    i,
                    name,
                    type,
                    category,
                    power,
                    accuracy,
                    f"{long_effect}",
                    f"{short_effect}",
                ]
            )
            print(f"Fetched data for move index {i}")
        except Exception as e:
            print(f"Error fetching move with index {i} {e}")
        

    return move_data

def fetch_held_item_api():
    """This function fetches all held item data from the Pokeapi."""

    def fetch_bulbapedia_effect(name):
        name = name.replace(" ", "_")
        url = f"https://bulbapedia.bulbagarden.net/wiki/{name}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        effect = soup.find('span', {'class': 'mw-headline', 'id': 'Effect'}).parent.find_next("p").text
        effect.strip('"')
        return effect
    
    def check_if_held_item(item):
        valid_categories = ["holdable-active", "holdable", "species-specific","memories"]

        if item["category"]["name"] == "held-items":
            return True
        if  item["attributes"]:
            if  item["attributes"][0]["name"] in valid_categories:
                return True
        return False

    url = "https://pokeapi.co/api/v2/item/"

    headers = [
        "item_id",
        "name",
        "effect",
    ]
    held_item_data = [headers]

    for i in range(126, 1703):
        try:
            item = requests.get(f"{url}{i}").json()
            name = item["name"].replace("-", " ")

            if(check_if_held_item(item) == False):
                print(f"Skipping item {name} as it is not a held item")
                continue
            
            if(item["effect_entries"]):
                effect = item["effect_entries"][0]["effect"]
            else:
                effect = fetch_bulbapedia_effect(name.title())

            held_item_data.append(
                [
                    i,
                    name,
                    effect,
                ]
            )
            print(f"Fetched data for held item index {i}")
        except Exception as e:
            print(f"Error fetching held item with index {i}: {e}")

    return held_item_data