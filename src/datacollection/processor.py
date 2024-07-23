"""
This module handles CSV file creation and cleaning for SQL database uploading.

The functions of this file are used to create, modify, and prepare CSV files for SQL database uploading. 
Because it's almost certain that new data will be acquired over the lifetime of this project, we include a different function to append new rows.
"""

import pandas as pd
import datacollection.scraper as scraper
import datacollection.pokeapi as pokeapi

TOURNAMENT_PATH = "datasets/tournaments.csv"
STANDINGS_PATH = "datasets/standings.csv"
TEAMS_PATH = "datasets/teams.csv"
POKEMON_PATH = "datasets/pokemon.csv"

def create_csv(data, filepath, data_type):
    """
    Creates a CSV file from a list and saves it to the specified filepath.
    
    Args:
        data: The data to be written to the CSV.
        filepath: The path where the CSV will be saved.
        data_type: The type of data being saved.
    """
    
    df = pd.DataFrame(data)
    
    if data_type == 'tournament':
        df = clean_tournament_data(df)
    elif data_type == 'standings':
        df = clean_standings_data(df)
    elif data_type == 'teams':
        df = clean_teams_data(df)
    elif data_type == 'pokemon':
        df = clean_pokemon_data(df)
    
    df.to_csv(filepath, index=False, encoding='utf-8', header=False)

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

def make_all_csv():
    """Fetches all data and creates CSV files."""

    url = "https://rk9.gg/events/pokemon"
    response = scraper.fetch_html(url)
    data = scraper.fetch_all_tournament_data(response)
    standings = scraper.fetch_standings_data(data)
    teams = scraper.fetch_team_data(standings)
    pokemon = pokeapi.fetch_all_pokemon_data()

    create_csv(data, TOURNAMENT_PATH, "tournament")
    create_csv(standings, STANDINGS_PATH, "standings")
    create_csv(teams, TEAMS_PATH, "teams")
    create_csv(pokemon, POKEMON_PATH, "pokemon")

def make_tournaments_csv():
    """Fetches tournament data and creates a CSV file."""
    url = "https://rk9.gg/events/pokemon"
    response = scraper.fetch_html(url)
    data = scraper.fetch_all_tournament_data(response)
    create_csv(data, TOURNAMENT_PATH, "tournament")

def make_standings_csv():
    """Fetches standings data and creates a CSV file."""
    df = pd.read_csv(TOURNAMENT_PATH)
    standings = scraper.fetch_standings_data(df)
    create_csv(standings, STANDINGS_PATH, "standings")

def make_teams_csv():
    """Fetches teams data and creates a CSV file."""

    teams = scraper.fetch_team_data(pd.read_csv(STANDINGS_PATH))
    create_csv(teams, TEAMS_PATH, "teams")

def make_pokemon_csv():
    """Fetches Pokémon data and creates a CSV file."""

    data = pokeapi.fetch_all_pokemon_data()
    create_csv(data, POKEMON_PATH, "pokemon")

def write_lines(row, df):
    """Writes a single row to a given pandas dataframe."""