from processor import create_csv, continue_csv
from scraper import fetch_tournament_data, fetch_html
from pokeapi import fetch_pokemon_data

def make_all_tournament_csv():
    # Fetch the HTML from the rk9 website
    url = "https://rk9.gg/events/pokemon"
    response = fetch_html(url)

    # Fetch the tournament data from the HTML
    data = fetch_tournament_data(response)

    # Create a CSV file with the tournament data
    create_csv(data, "data/tournaments.csv")

def make_pokemon_csv():
    # Fetch the pokemon data from the pokeapi
    data = fetch_pokemon_data()

    # Create a CSV file with the pokemon data
    continue_csv(data, "data/pokemon.csv")

def main():
    print("start!!")
    make_pokemon_csv()

main()