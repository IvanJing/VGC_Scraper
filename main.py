import processor
import scraper
import pokeapi
import timeit


def make_all_tournament_csv():
    # Fetch the HTML from the rk9 website
    url = "https://rk9.gg/events/pokemon"
    response = scraper.fetch_html(url)

    # Fetch the tournament data from the HTML
    data = scraper.fetch_all_tournament_data(response)

    # Create a CSV file with the tournament data
    processor.create_csv(data, "data/tournaments.csv")

def make_pokemon_csv():
    # Fetch the pokemon data from the pokeapi
    data = pokeapi.fetch_pokemon_data()

    # Create a CSV file with the pokemon data
    processor.continue_csv(data, "data/pokemon.csv")


def main():
    make_all_tournament_csv()


print(timeit.timeit(main, number=1))
