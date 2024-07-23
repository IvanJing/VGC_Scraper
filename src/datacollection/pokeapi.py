import pokebase as pb
import concurrent.futures
import time

def fetch_all_pokemon_data():
    def fetch_pokemon(index):
        try:
            pokemon = pb.pokemon(index)
            if pokemon:
                name = pokemon.name
                base_stats = {stat.stat.name: stat.base_stat for stat in pokemon.stats}
                abilities = [ability.ability.name for ability in pokemon.abilities]
                types = pokemon.types

                pokemon_data = [
                    index,
                    name,
                    types[0].type.name if types else None,
                    types[1].type.name if len(types) > 1 else None,
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
                print(f"Fetched data for Pokémon index {index}")
                return pokemon_data
            else:
                print(f"Pokémon with index {index} not found.")
                return None
        except Exception as e:
            print(f"Error fetching Pokémon with index {index}: {e}")
            return None

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
    data = [headers]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_pokemon, index): index for index in range(1, 1025)}
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    data.append(result)
            except Exception as e:
                index = futures[future]
                print(f"An error occurred with index {index}: {e}")

            # Add a small delay to avoid rate limiting
            time.sleep(0.1)

    return data

# Call the function to fetch all Pokémon data
pokemon_data = fetch_all_pokemon_data()
print("Finished fetching Pokémon data")