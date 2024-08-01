"""
This module handles CSV file creation and cleaning for SQL database uploading.

The functions of this file are used to create, modify, and prepare CSV files for SQL database uploading. 
Because it's almost certain that new data will be acquired over the lifetime of this project, we include a different function to append new rows.
"""

import pandas as pd
import datacollection.scraper as scraper
import datacollection.pokeapi as pokeapi
import os

TOURNAMENT_PATH = r"src\data\tournaments.csv"
STANDINGS_PATH = r"src\data\standings.csv"
TEAMS_PATH = r"src\data\teams.csv"
POKEMON_PATH = r"src\data\pokemon.csv"
ABILITIES_PATH = r"src\data\abilities.csv"
MOVES_PATH = r"src\data\moves.csv"
ITEMS_PATH = r"src\data\items.csv"
ICONS_PATH = r"src\data\icons.csv"

def create_csv(df, filepath):
    """
    Creates a CSV file from a list and saves it to the specified filepath.
    
    Args:
        data: The data to be written to the CSV.
        filepath: The path where the CSV will be saved.
        data_type: The type of data being saved.
    """

    if type(df) == list:
        df = pd.DataFrame(df)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    df.to_csv(filepath, index=False, encoding='utf-8', header=True)

def append_to_csv(data, filepath, data_type):
    """
    Appends new rows to an existing CSV file.
    
    Args:
        data: The data to be appended to the CSV.
        filepath: The path where the CSV is saved.
        data_type: The type of data being appended.
    """

    df = pd.DataFrame(data)
    
    if data_type == 'tournament':
        df = clean_tournament_data(df)
    elif data_type == 'standings':
        df = clean_standings_data(df)
    elif data_type == 'pokemon':
        df = clean_pokemon_data(df)
    
    df.to_csv(filepath, mode='a', index=False, header=False, encoding='utf-8')

def add_column_to_csv(column_name, column_data, filepath):
    """
    Adds a new column to an existing CSV file.
    
    Args:
        column_name: The name of the new column.
        column_data: The data for the new column.
        filepath: The path where the CSV is saved.
    """

    df = pd.read_csv(filepath, encoding='utf-8')
    df[column_name] = column_data
    df.to_csv(filepath, index=False, encoding='utf-8')



def make_all_csv():
    """Fetches all data and creates CSV files."""

    make_tournaments_csv()
    make_standings_csv()
    make_teams_csv()
    make_pokemon_csv()
    make_abilities_csv()
    make_moves_csv()
    make_held_items_csv()


def fetch_game_data():
    """This is just a seperate function for retrieving ONLY pokemon, moves, abilities, and items data."""
    make_pokemon_csv()
    make_moves_csv()
    make_abilities_csv()
    make_held_items_csv()

def fetch_official_data():
    """This is a seperate function for retrieving ONLY tournament, standings, and team data."""
    make_tournaments_csv()
    make_standings_csv()
    make_teams_csv()
    make_pokemon_csv()

def make_tournaments_csv():
    """Fetches tournament data and creates a CSV file."""
    url = "https://rk9.gg/events/pokemon"
    response = scraper.fetch_html(url)
    data = scraper.fetch_all_tournament_data(response)
    df = pd.DataFrame(data)
    df = clean_tournament_data(df)

    create_csv(df, TOURNAMENT_PATH)

def make_standings_csv():
    """Fetches standings data and creates a CSV file."""
    df = pd.read_csv(TOURNAMENT_PATH)
    data = scraper.fetch_standings_data(df)
    headers = data[0]
    rows = data[1:]

    df = pd.DataFrame(rows, columns=headers)
    df = clean_standings_data(df)

    create_csv(df, STANDINGS_PATH)

def make_teams_csv():
    """Fetches teams data and creates a CSV file."""

    data = scraper.fetch_team_data(pd.read_csv(STANDINGS_PATH))
    headers = data[0]
    rows = data[1:]

    df = pd.DataFrame(rows, columns=headers)
    df = clean_teams_data(df)

    create_csv(df, TEAMS_PATH)

def make_pokemon_csv():
    """Fetches Pokémon data from the Pokeapi and creates a CSV file."""

    data = pokeapi.fetch_pokemon_api()
    headers = data[0]
    rows = data[1:]

    df = pd.DataFrame(rows, columns=headers)
    df = clean_pokemon_data(df)

    create_csv(df, POKEMON_PATH)
    
def make_abilities_csv():
    """Fetches ability data from the Pokeapi and creates a CSV file."""

    data = pokeapi.fetch_ability_api()
    headers = [
        "ability_id",
        "ability_name",
        "description",
    ]
    rows = data[1:]

    df = pd.DataFrame(rows, columns=headers)
    df = clean_abilities_data(df)

    create_csv(df, ABILITIES_PATH)

def make_moves_csv():
    """Fetches move data from the Pokeapi and creates a CSV file."""

    data = pokeapi.fetch_move_api()
    headers = [ 
        "move_id",
        "move_name",
        "type",
        "category",
        "power",
        "accuracy",
        "long_effect",
        "short_effect", 
    ]
    rows = data[1:]

    df = pd.DataFrame(rows, columns=headers)
    df = clean_moves_data(df)

    create_csv(df, MOVES_PATH)

def make_held_items_csv():
    """Fetches held item data from the Pokeapi and creates a CSV file."""

    data = pokeapi.fetch_held_item_api()

    headers = [
        "item_id",
        "item_name",
        "item_description",
    ]
    rows = data[1:]

    df = pd.DataFrame(rows, columns=headers)
    df = clean_items_data(df)

    create_csv(df, ITEMS_PATH)

def make_icons_csv():
    """Fetches item icon links and creates a csv file."""

    data = scraper.fetch_icon_links()
    headers = [
        "item_name",
        "icon_link",
    ]

    df = pd.DataFrame(data, columns=headers)
    create_csv(df, ICONS_PATH)

"""

Below are functions for cleaning the data in the CSV files. Since each data type can come in many forms due to the inconsistency of their sources, each type has their own pre-defined cleaning logic. 
This allows for a more organized and efficient cleaning process.

"""

def clean_tournament_data(df):
    """
    Cleans the tournament data.
    
    Args:
        df: The DataFrame containing the tournament data.
    
    Returns:
        A cleaned DataFrame.
    """

    df = df.drop_duplicates()
    df['rk9_id'] = df['rk9_id'].fillna('missing_rk9_id')
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['location'] = df['location'].str.strip()
    
    return df

def clean_standings_data(df):
    """
    Cleans the standings data.
    
    Args:
        df: The DataFrame containing the standings data.
    
    Returns:
        A cleaned DataFrame.
    """

    df = df.drop_duplicates()
    df['country'] = df['country'].fillna('Unknown')
    df['first_name'] = df['first_name'].str.title()
    df['last_name'] = df['last_name'].str.title()
    df['trainer_name'] = df['trainer_name'].str.title()
    
    return df

def clean_pokemon_data(df):
    """
    Cleans the Pokémon data.
    
    Args:
        df: The DataFrame containing the Pokémon data.
    
    Returns:
        A cleaned DataFrame.
    """

    # Additional cleaning logic can be added here
    return df

def clean_teams_data(df):
    """
    Cleans the teams data.
    
    Args:
        df: The DataFrame containing the teams data.
    
    Returns:
        A cleaned DataFrame.
    """
    # Additional cleaning logic can be added here
    return df

def clean_abilities_data(df):
    """Cleans the abilities data."""

    df = df.drop_duplicates()

    separator = "Overworld:"
    df['description'] = df['description'].fillna('').astype(str)
    df['description'] = df['description'].str.split(separator, n=1).str[0]
    df['description'] = df['description'].str.replace('\n', '', regex=False).str.strip()

    df['description'] = df['description'].str.replace(r'\s*.\n\s*', '', regex= True)
    df['description'] = df['description'].str.replace(r'\s+', ' ', regex= True)
    df['description'] = df['description'].str.replace('"', '')

    print("cleaning done")
    return df

def clean_moves_data(df):
    """
    Cleans the moves data.
    
    Args:
        df: The DataFrame containing the moves data.
    
    Returns:
        A cleaned DataFrame.
    """

    #remove duplicates
    df = df.drop_duplicates()

    #remove new lines
    df['long_effect'] = df['long_effect'].fillna('').astype(str)
    df['long_effect'] = df['long_effect'].str.replace('\n', '')

    df['short_effect'] = df['short_effect'].fillna('').astype(str)
    df['short_effect'] = df['short_effect'].str.replace('\n', '')

    return df

def clean_items_data(df):
    """Cleans the csv for item data. """

    df = df.drop_duplicates()

    separator = "Used on a"
    df['item_description'] = df['item_description'].fillna('').astype(str)
    df['item_description'] = df['item_description'].str.split(separator, n=1).str[0]
    df['item_description'] = df['item_description'].str.replace('\n', '', regex=False).str.strip()

    df['item_description'] = df['item_description'].str.replace(r'\s*:\s*', ': ', regex= True)
    df['item_description'] = df['item_description'].str.replace(r'\s+', ' ', regex= True)
    df['item_description'] = df['item_description'].str.replace('"', '')
    
    return df