import vgcwebscraper.processor as processor
import vgcwebscraper.scraper as scraper
import vgcwebscraper.pokeapi as pokeapi
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

def test_team_fetch():
    standings_path = "data/standings.csv"

    team_data = scraper.test_fetch_team_data(standings_path)

    processor.create_csv(team_data, "data/teams.csv")

def make_all():
    make_all_tournaments_csv()
    make_pokemon_csv()

def main():
    make_pokemon_csv()

main()
