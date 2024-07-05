import processor
import scraper
import pokeapi
import timeit


def make_all_tournaments_csv():
    # Fetch the HTML from the rk9 website
    url = "https://rk9.gg/events/pokemon"
    response = scraper.fetch_html(url)

    # Fetch the tournament data from the HTML
    data = scraper.fetch_all_tournament_data(response)

    standings = scraper.fetch_standings_data(data)

    teams = scraper.fetch_team_data(standings)

    # Create a CSV file with the tournament data
    processor.create_csv(data, "data/tournaments.csv")

    processor.create_csv(standings, "data/standings.csv")

    processor.create_csv(teams, "data/teams.csv")

def make_pokemon_csv():
    # Fetch the pokemon data from the pokeapi
    data = pokeapi.fetch_pokemon_data()

    # Create a CSV file with the pokemon data
    processor.continue_csv(data, "data/pokemon.csv")

def main():
    make_all_tournaments_csv()


main()
