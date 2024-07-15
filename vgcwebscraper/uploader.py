"""This module handles all database uploading."""
import os
import sqlalchemy as sqlachl
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
dbAPI = os.getenv('DATABASE_URL')

def upload_tournaments(filepath):
    """Uploads the tournament data to the PostgreSQL database."""
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filepath)
    
    # Create a connection to the PostgreSQL database
    engine = sqlachl.create_engine(dbAPI, echo=True)
    
    # Create the Tournaments table if it doesn't exist
    with engine.connect() as connection:
        connection.execute(sqlachl.text("""
            CREATE TABLE IF NOT EXISTS Tournaments (
                tournament_id VARCHAR(50) PRIMARY KEY,
                tournament_name VARCHAR(50),
                start_date DATE,
                end_date DATE,
                location VARCHAR(50),
                rk9_id VARCHAR(50),
                logo_link VARCHAR(100)
            )
        """))
    
    # Upload the data to the Tournaments table
    df.to_sql('Tournaments', engine, if_exists='append', index=False)
    connection.commit()

    

def upload_standings(filepath):
    """Uploads the standings data to the PostgreSQL database."""


    df = pd.read_csv(filepath)

    engine = sqlachl.create_engine(dbAPI, echo=True)

    with engine.connect() as connection:
        connection.execute(sqlachl.text("""
            CREATE TABLE IF NOT EXISTS Standings(
                tournament_id VARCHAR(50),
                player_id VARCHAR(50),
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                country VARCHAR(30),
                trainer_name VARCHAR(20),
                team_list VARCHAR(50),
                standing INT,
                PRIMARY KEY (tournament_id, player_id)   
                );
                                        """))

    df.to_sql('Standings', engine, if_exists='append', index=False)
    connection.commit()


def upload_teams(filepath):
    """Uploads the teams data to the PostgreSQL database."""

    df = pd.read_csv(filepath)

    engine = sqlachl.create_engine(dbAPI, echo=True)

    with engine.connect() as connection:
        connection.execute(sqlachl.text("""
        CREATE TABLE IF NOT EXISTS Team_members(
            tournament_id VARCHAR(50),
            player_id VARCHAR(50),
            icon VARCHAR(100),
            pokemon VARCHAR(50),
            form VARCHAR(50),
            tera_type VARCHAR(50),
            ability VARCHAR(50),                           
            held_item VARCHAR(50),
            move1 VARCHAR(50),
            move2 VARCHAR(50),
            move3 VARCHAR(50),
            move4 VARCHAR(50),
            PRIMARY KEY (tournament_id, player_id, pokemon)
            );                                
                                        """))
        
    df.to_sql('Team_members', engine, if_exists='append', index=False)
    connection.commit()


upload_teams('data/teams.csv')