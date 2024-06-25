import pokebase as pb

#This is an import of the pokebase library, a python wrapper made by Alessandro Pezzè for the pokeapi database. Check out his github repo here at: https://github.com/PokeAPI/pokebase
#Also visit the PokeAPI website at: https://pokeapi.co/
#This file will be used to fetch all available pokemon stats, abilities, and forms from the pokeapi database, then store them in the local database for later use.

#This function will fetch some pokemon data from the pokeapi database and store it in the local database.

def fetch_pokemon_data():
    #Fetch all pokemon data from the pokeapi database
    i = 1
    while (pokemon := pb.pokemon(i)) is not None:
        name = pokemon.name
        base_stats = {stat.stat.name: stat.base_stat for stat in pokemon.stats}
        abilities = [ability.ability.name for ability in pokemon.abilities]
        print(f"Name: {name}")
        print(f"Base Stats: {base_stats}")
        i += 1
        if(i > 10):
            break

def fetch_one():
    #Fetch a single pokemon's data from the pokeapi database
    bulbasaur = pb.pokemon()
    name = bulbasaur.name

    base_stats = {stat.stat.name: stat.base_stat for stat in bulbasaur.stats}
    abilities = [ability.ability.name for ability in bulbasaur.abilities]
    print(f"Name: {name}")
    print(f"Base Stats: {base_stats}")
    
fetch_pokemon_data()