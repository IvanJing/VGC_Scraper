"""This module handles csv file creation and SQL database uploading.

The functions of this file are used to create, modify, and upload csv files to a SQL database. 
Because it's almost certain that new data will be acquired over the lifetime of this project, we include a different function to append new rows.
"""
import pandas as pd
import json
import sqlalchemy

def create_csv(data, filepath):
    df = pd.DataFrame(data)
    df.to_csv(filepath, index = False, encoding = 'utf-8')


def continue_csv(data, filepath):
    df = pd.DataFrame(data)
    df.to_csv(filepath, mode = 'a', index = False, header = False, encoding = 'utf-8')


def add_column_csv(column_name, column_data, filepath):
   df = pd.read_csv(filepath, encoding = 'utf-8')
   df[column_name] = column_data
   df.to_csv(filepath, index = False, encoding = 'utf-8')


def clean_tournament_data(df):
    df = df.drop_duplicates()
    
    df['rk9_id'] = df['rk9_id'].fillna('missing_rk9_id')
    
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    df['location'] = df['location'].str.strip()
    
    return df


def clean_standings_data(df):
    df = df.drop_duplicates()
    
    df['country'] = df['country'].fillna('Unknown')
    
    df['first_name'] = df['first_name'].str.title()
    df['last_name'] = df['last_name'].str.title()
    df['trainer_name'] = df['trainer_name'].str.title()
    
    return df


def clean_teams_data(df):
    df = df.drop_duplicates()
    
    df['team_members'] = df['team_members'].apply(json.loads)

    for team in df['team_members']:
        for member in team:
            if not member['poke_icon'].startswith('https://'):
                member['poke_icon'] = 'invalid_url'
                
    return df

