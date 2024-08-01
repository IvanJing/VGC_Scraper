"""Modules for uploading data to the PostgreSQL database.

The functions in this file are used to upload data to the PostgreSQL database, either creating, updating, or straight up replacing tables in the database. 
The functions here are rarely called on their lonesome, and instead are called by foreign functions or manually by the user in main.py.
There's a chance for duplicate data to be scraped/retrieved by our data collection modules, and it isn't possible to check for duplicates here without pulling the data from the database first;
Therefore, we'll need to rely on the database to do this cleaning for us, and we'll need to make sure that the data we're uploading is clean and ready to be uploaded as much as possible to lighten the load.

"""

import os
import sqlalchemy as sqlachl
import pandas as pd
import datacollection.processor as process
from dotenv import load_dotenv


POKEMON_PATH = "src/data/pokemon.csv"
MOVES_PATH = "src/data/moves.csv"
ABILITIES_PATH = "src/data/abilities.csv"
ITEMS_PATH = "src/data/items.csv"
TORNAMENTS_PATH = "src/data/tournaments.csv"
STANDINGS_PATH = "src/data/standings.csv"
TEAMS_PATH = "src/data/teams.csv"

load_dotenv()
dbAPI = os.getenv("DATABASE_URL")


def upload_tournaments(filepath):
    """Uploads the tournament data to the PostgreSQL database."""

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filepath)

    # Create a connection to the PostgreSQL database
    engine = sqlachl.create_engine(dbAPI, echo=True)

    # Create the Tournaments table if it doesn't exist
    with engine.connect() as connection:
        connection.execute(
            sqlachl.text(
                """
            CREATE TABLE IF NOT EXISTS Tournaments (
                tournament_id VARCHAR(50) PRIMARY KEY,
                tournament_name VARCHAR(50),
                start_date DATE,
                end_date DATE,
                location VARCHAR(50),
                rk9_id VARCHAR(50),
                logo_link VARCHAR(100)
            )
        """
            )
        )

    # Upload the data to the Tournaments table
    df.to_sql("Tournaments", engine, if_exists="replace", index=False)
    connection.commit()


def upload_standings(filepath):
    """Uploads the standings data to the PostgreSQL database."""

    df = pd.read_csv(filepath)

    engine = sqlachl.create_engine(dbAPI, echo=True)

    with engine.connect() as connection:
        connection.execute(
            sqlachl.text(
                """
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
                                        """
            )
        )

    df.to_sql("Standings", engine, if_exists="replace", index=False)
    connection.commit()


def upload_teams(filepath):
    """Uploads the teams data to the PostgreSQL database."""

    df = pd.read_csv(filepath)

    engine = sqlachl.create_engine(dbAPI, echo=True)

    with engine.connect() as connection:
        connection.execute(
            sqlachl.text(
                """ 
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
                                        """
            )
        )

    df.to_sql("Team_members", engine, if_exists="replace", index=False)
    connection.commit()


def upload_pokemon(filepath):
    """Uploads the pokemon data to the PostgreSQL database."""

    df = pd.read_csv(filepath)

    engine = sqlachl.create_engine(dbAPI, echo=True)

    with engine.connect() as connection:
        connection.execute(
            sqlachl.text(
                """
        CREATE TABLE IF NOT EXISTS Pokemon(
            pokemon_id INT,
            name VARCHAR(50),
            type1 VARCHAR(50),
            type2 VARCHAR(50),
            health INT,
            attack INT,
            defense INT,
            special_attack INT,
            special_defense INT,
            speed INT,
            ability1 VARCHAR(50),
            ability2 VARCHAR(50),
            ability3 VARCHAR(50),
            PRIMARY KEY (pokemon_id)
            );                                
                                        """
            )
        )

    df.to_sql("Pokemon", engine, if_exists="replace", index=False)
    connection.commit()

def upload_moves(filepath):
    """Uploads the moves data to the PostgreSQL database."""

    df = pd.read_csv(filepath)

    engine = sqlachl.create_engine(dbAPI, echo=True)

    with engine.connect() as connection:
        connection.execute(
            sqlachl.text(
                """
        CREATE TABLE IF NOT EXISTS Moves(
            move_id INT,
            name VARCHAR(50),
            type VARCHAR(50),
            category VARCHAR(50),
            power INT,
            accuracy INT,
            long_effect VARCHAR(255),
            short_effect VARCHAR(255),
            PRIMARY KEY (move_id)
            );                                
                                        """
            )
        )

    df.to_sql("Moves", engine, if_exists="replace", index=False)
    connection.commit()

def upload_abilities(filepath):
    """Uploads the abilities data to the PostgreSQL database."""

    df = pd.read_csv(filepath)

    engine = sqlachl.create_engine(dbAPI, echo=True)

    with engine.connect() as connection:
        connection.execute(
            sqlachl.text(
                """
        CREATE TABLE IF NOT EXISTS Abilities(
            ability_id INT,
            name VARCHAR(50),
            description TEXT,
            PRIMARY KEY (ability_id)
            );                                
                                        """
            )
        )

    df.to_sql("Abilities", engine, if_exists="replace", index=False)
    connection.commit()

def upload_items(filepath):
    """Uploads the items data to the PostgreSQL database."""

    df = pd.read_csv(filepath)

    engine = sqlachl.create_engine(dbAPI, echo=True)

    with engine.connect() as connection:
        connection.execute(
            sqlachl.text(
                """
        CREATE TABLE IF NOT EXISTS Items(
            item_id INT,
            name VARCHAR(50),
            item_description VARCHAR(255),
            PRIMARY KEY (item_id)
            );                                
                                        """
            )
        )

    df.to_sql("Items", engine, if_exists="replace", index=False)
    connection.commit()

def update_tournament(filepath):
    """Updates the tournament data in the PostgreSQL database."""

    try:
        df = pd.read_csv(filepath)

        df = process.clean_tournament_data(df)

        engine = sqlachl.create_engine(dbAPI, echo=True)

        with engine.connect() as connection:
            connection.execute(
                sqlachl.text(
                    """
            CREATE TABLE IF NOT EXISTS Tournaments (
                tournament_id VARCHAR(50) PRIMARY KEY,
                tournament_name VARCHAR(50),
                start_date DATE,
                end_date DATE,
                location VARCHAR(50),
                rk9_id VARCHAR(50),
                logo_link VARCHAR(100)
            )
        """
                )
            )

        df.to_sql("Tournaments", engine, if_exists="replace", index=False)

    except Exception as e:
        print(e)


def update_standings(filepath):
    """Updates the standings data in the PostgreSQL database."""

    try:
        df = pd.read_csv(filepath)

        df = process.clean_standings_data(df)

        engine = sqlachl.create_engine(dbAPI, echo=True)

        with engine.connect() as connection:
            connection.execute(
                sqlachl.text(
                    """
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
                                        """
                )
            )

        df.to_sql("Standings", engine, if_exists="replace", index=False)

    except Exception as e:
        print(e)


def update_teams(filepath):
    """Updates the teams data in the PostgreSQL database."""

    try:
        df = pd.read_csv(filepath)

        df = process.clean_teams_data(df)

        engine = sqlachl.create_engine(dbAPI, echo=True)

        with engine.connect() as connection:
            connection.execute(
                sqlachl.text(
                    """
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
                                        """
                )
            )

        df.to_sql("Team_members", engine, if_exists="replace", index=False)

    except Exception as e:
        print(e)


def upload_all():
    """Uploads all data to the PostgreSQL database."""

    try:
        upload_tournaments(TORNAMENTS_PATH)
        upload_standings(STANDINGS_PATH)
        upload_teams(TEAMS_PATH)
        upload_pokemon(POKEMON_PATH)
        upload_moves(MOVES_PATH)
        upload_abilities(ABILITIES_PATH)
        upload_items(ITEMS_PATH)
    except Exception as e:
        print(e)

def upload_game_data():
    """Uploads all game data to the PostgreSQL database."""

    try:
        upload_pokemon(POKEMON_PATH)
        upload_moves(MOVES_PATH)
        upload_abilities(ABILITIES_PATH)
        upload_items(ITEMS_PATH)
    except Exception as e:
        print(f'Error, failed to upload game data.{e}')

def upload_official_data():
    """Uploads all official data to the PostgreSQL database."""

    try:
        upload_tournaments(TORNAMENTS_PATH)
        upload_standings(STANDINGS_PATH)
        upload_teams(TEAMS_PATH)
    except Exception as e:
        print(f'Error failed to upload official data{e}')

