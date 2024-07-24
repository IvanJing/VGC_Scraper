from imports import processor, scraper


def test_team_fetch():
    standings_path = "data/standings.csv"

    team_data = scraper.test_fetch_team_data(standings_path)

    processor.create_csv(team_data, "data/teams.csv")

def get_data():
    """
    
    Main function for data collection. Uncomment as needed. 

    Functions under this command are used to fetch data from the web and store it in CSV files.
    Use fetch_game_data() to fetch pokemon, moves, abilities, and held items data.
    Use fetch_official_data() to fetch tournament, standings, and team data.
    Use make_all_csv() to fetch all data and create CSV files.    
    
    """
    #processor.fetch_game_data()
    #processor.fetch_official_data()
    #processor.make_all_csv()

def main():
    processor.make_abilities_csv()

main()

 