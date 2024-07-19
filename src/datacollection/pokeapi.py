import pokebase as pb

# This is an import of the pokebase library, a python wrapper made by Alessandro Pezzè for the pokeapi database. Check out his github repo here at: https://github.com/PokeAPI/pokebase
# Also visit the PokeAPI website at: https://pokeapi.co/
# This file will be used to fetch all available pokemon stats, abilities, and forms from the pokeapi database, then store them in the local database for later use.


# This function will fetch some pokemon data from the pokeapi database and store it in the local database.
def fetch_pokemon_data():
    i = 1  # Start at 500 because the first 500 pokemon are already in the database
    data = [
        (
            [
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
        )
    ]  # Start up those headers
    while (
        pokemon := pb.pokemon(i)
    ) is not None:  # Basically just keep going until I have all of the pokemon. All of them.
        name = pokemon.name
        base_stats = {stat.stat.name: stat.base_stat for stat in pokemon.stats}
        abilities = [ability.ability.name for ability in pokemon.abilities]
        data.append(
            [
                i,
                name,
                types[0].type.name if (types := pokemon.types) else None,
                types[1].type.name if len(types) > 1 else None,
                base_stats["hp"],
                base_stats["attack"],
                base_stats["defense"],
                base_stats["special-attack"],
                base_stats["special-defense"],
                base_stats["speed"],
                abilities[0],
                abilities[1] if len(abilities) > 1 else None,
                abilities[2] if len(abilities) > 2 else None,
            ]
        )
        i += 1
        if i >= 1025:
            break
    return data
