from src.imports import processor, scraper, pokeapi, uploader







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
