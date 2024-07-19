"""This module handles csv file creation and SQL database uploading.

The functions of this file are used to create, modify, and upload csv files to a SQL database. 
Because it's almost certain that new data will be acquired over the lifetime of this project, we include a different function to append new rows.
"""
import pandas as pd
import json


def create_csv(data, filepath, type):
    """Creates a CSV file from a list and saves it to the specified filepath. Type denotes the type of data being saved."""

    df = pd.DataFrame(data)

    if type == 'tournament':
        df = clean_tournament_data(df)
    elif type == 'standings':
        df = clean_standings_data(df)
    elif type == 'teams':
        df = clean_teams_data(df)
    df.to_csv(filepath, index = False, encoding = 'utf-8', header = False)


def continue_csv(data, filepath, type):
    """Appends new rows to an existing CSV file. Type denotes the type of data being saved."""

    df = pd.DataFrame(data)

    if type == 'tournament':
        df = clean_tournament_data(df)
    elif type == 'standings':
        df = clean_standings_data(df)

    df.to_csv(filepath, mode = 'a', index = False, header = False, encoding = 'utf-8')


def add_column_csv(column_name, column_data, filepath):
   df = pd.read_csv(filepath, encoding = 'utf-8')
   df[column_name] = column_data
   df.to_csv(filepath, index = False, encoding = 'utf-8')


def clean_tournament_data(df):
    """Cleans the tournament data by dropping duplicates, filling in missing values, and converting columns to the correct data type."""

    df = df.drop_duplicates()
    
    df['rk9_id'] = df['rk9_id'].fillna('missing_rk9_id')
    
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    df['location'] = df['location'].str.strip()
    
    return df


def clean_standings_data(df):
    """Cleans the standings data by dropping duplicates, filling in missing values, and converting columns to the correct formats."""

    df = df.drop_duplicates()
    
    df['country'] = df['country'].fillna('Unknown')
    
    df['first_name'] = df['first_name'].str.title()
    df['last_name'] = df['last_name'].str.title()
    df['trainer_name'] = df['trainer_name'].str.title()
    
    return df

def clean_pokemon_data(df):
    """Splits the list of pokemon abilities into the 3 ability columns (ability1, ability2, ability3) and fills them with the respective abilities, or NONE if they don't exist."""

    df = df.drop_duplicates()

    df['ability1'] = df['abilities'].apply(lambda x: x[0] if len(x) > 0 else 'NONE')
    df['ability2'] = df['abilities'].apply(lambda x: x[1] if len(x) > 1 else 'NONE')
    df['ability3'] = df['abilities'].apply(lambda x: x[2] if len(x) > 2 else 'NONE')

    return df

def clean_teams_data(df):
    """Cleans the teams data by dropping duplicates, checking column validity, and converting columns to the correct formats."""
            
    return df


