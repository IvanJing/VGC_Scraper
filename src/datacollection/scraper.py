"""Modules for scraping, parsing, fetching and cleaning data from the rk9.gg website.

The functions in this file are used to scrape information from the rk9 tournament website, parse the data, and prepare it for storage in a CSV file.
Because of the way the site formats tournaments, we need to first fill the tournaments dataset, then follow the scraped links in order
to fill the standings dataset. Similarly, team view is hidden behind more links, so we need to scrape and crawl those as well. 

"""

import concurrent.futures
from bs4 import BeautifulSoup
import requests
import hashlib
from daterangeparser import parse
import pandas as pd


def fetch_all_tournament_data(response):
    """Fetches tournament data from rk9 website.

    Retrieves the tournament data from the HTML response, parses it, and returns it in a format that can be used to create a CSV file.

    Returns:
        A nested list containing the corresponding table columns, as well as the additional 'tournament_id' column.
        Each row in the list represents a tournament, with the first row containing the column headers.
        example:

        {ef37920b3b369e1a760695ee54214f7f,
         North America Pokémon International Championships 2024,
         "New Orleans, US",
         NA02mtILnc5ycfC7jXkD,
         2024-06-07,2024-06-09,
         rk9.gg/static/images/naic_101x110.png}

    Raises:
        ValueError: If the date range cannot be parsed.
        IOError: If the HTML response is invalid.

    Typical use case example:
        response = fetch_html("https://rk9.gg/events/pokemon")
        data = fetch_all_tournament_data(response)
        create_csv(data, "data/tournaments.csv") <--- This part is for demonstration purposes. In reality, we would call the processor function to make the csv.

    """

    def parse_date(date_range):
        """Converts the date string provided by rk9 into start and end dates"""

        date_range = date_range.replace("–", "-")
        try:
            start_date, end_date = parse(date_range)

            return start_date.date(), end_date.date()

        except ValueError as e:
            print(f"Invalid date range: {date_range}")
            return None, None

    def generate_tournament_id(tournament_name, location, start_date):
        """Generates a unique ID for the tournament"""

        return hashlib.md5(
            f"{tournament_name}{location}{start_date}".encode()
        ).hexdigest()

    soup = BeautifulSoup(response, "lxml")
    rows = soup.find_all("tr")
    tournaments_data = [
        (
            [
                "tournament_id",
                "tournament_name",
                "location",
                "rk9_id",
                "start_date",
                "end_date",
                "logo_link",
            ]
        )
    ]

    for row in rows:
        columns = row.find_all("td")

        if len(columns) >= 5:
            date = columns[0].text.strip()
            tournament_name = columns[2].text.strip()
            location = columns[3].text.strip()
            start_date, end_date = parse_date(date)

            tournament_id = generate_tournament_id(
                tournament_name, location, start_date
            )

            logo_img = columns[1].find("img")
            if logo_img:
                logo_link = "rk9.gg" + logo_img["src"]

            link = columns[4].find("a", string="VG")
            if link:
                rk9_id = link["href"].replace("/tournament/", "")
            else:
                rk9_id = None

            tournaments_data.append(
                [
                    tournament_id,
                    tournament_name,
                    location,
                    rk9_id,
                    start_date,
                    end_date,
                    logo_link,
                ]
            )
        else:
            print("Row does not have enough columns")

    return tournaments_data


def fetch_standings_data(tournament_data):
    """Fetches standings data from rk9 website.

    Creates a URL using rk9_id and fetches all standings data from the website.

    Args:
        tournament_data: A pandas DataFrame containing the corresponding table columns for tournaments.

    Returns:
        A pandas DataFrame containing the corresponding table columns for standings, as well as the additional 'tournament_id' column.
        Most of the columns are self-explanatory, but the team list column will be a JSON file, which will be parsed later.

    Raises:
        IOError: If the HTML response is invalid.
    """

    def generate_player_id(player_id, first_name, last_name):
        """rk9 does not provide player_id in its entirety, so we'll generate our own."""
        return hashlib.md5(f"{player_id}{first_name}{last_name}".encode()).hexdigest()

    standings_data = []

    for _, row in tournament_data.iterrows():
        tournament_id = row["tournament_id"]
        rk9_id = row["rk9_id"]
        if rk9_id:
            standings_url = f"https://rk9.gg/roster/{rk9_id}"
            response = fetch_html(standings_url)
            soup = BeautifulSoup(response, "lxml")

            rows = soup.find_all("tr")

            for row in rows:
                columns = row.find_all("td")
                try:
                    if (
                        columns
                    ):  # Certain tournaments don't have standing links or lack country data.
                        first_name = columns[1].text.strip()
                        last_name = columns[2].text.strip()
                        country = columns[3].text.strip() if len(columns) >= 8 else None
                        division = columns[3 if country is None else 4].text.strip()
                        trainer_name = columns[4 if country is None else 5].text.strip()
                        team_list_element = columns[5 if country is None else 6].find(
                            "a"
                        )
                        team_list = (
                            team_list_element["href"].replace("/teamlist/public/", "")
                            if team_list_element
                            else "Submitted"
                        )
                        standing = columns[6 if country is None else 7].text.strip()
                        player_id = generate_player_id(
                            columns[0].text.strip(), first_name, last_name
                        )

                        standings_data.append(
                            [
                                tournament_id,
                                player_id,
                                first_name,
                                last_name,
                                country,
                                division,
                                trainer_name,
                                team_list,
                                standing,
                            ]
                        )
                except IndexError:
                    print(IndexError)
                    print(columns)

    standings_df = pd.DataFrame(
        standings_data,
        columns=[
            "tournament_id",
            "player_id",
            "first_name",
            "last_name",
            "country",
            "division",
            "trainer_name",
            "team_list",
            "standing",
        ],
    )

    return standings_df


def fetch_team_data(filepath):
    """Takes in the filepath for the standings csv and creates a new csv with team member data"""

    def fetch_team_members(url):
        """Fetch the team members using the constructed url."""

        response = fetch_html(url)
        soup = BeautifulSoup(response, "lxml")

        team_members = []

        team = soup.find_all("div", {"class": "pokemon bg-light-green-50 p-3"})

        for team_member in team[:6]:
            poke_icon = team_member.find("img")["src"]

            raw_text = team_member.get_text(separator=" ", strip=True)
            name = ""
            form = "N/A"

            if "[" in raw_text and "]" in raw_text:
                name = raw_text.split("[")[0].strip()
                form = raw_text.split("[")[1].split("]")[0].strip()
            else:
                name = raw_text.split(" ")[0]

            tera_type_tag = team_member.find("b", text="Tera Type:").next_sibling
            tera_type = tera_type_tag.strip().strip('"') if tera_type_tag else None

            ability_tag = team_member.find("b", text="Ability:").next_sibling
            ability = (
                ability_tag.strip().strip('"').replace("&nbsp;", "").strip()
                if ability_tag
                else None
            )

            held_item_tag = team_member.find("b", text="Held Item:").next_sibling
            held_item = held_item_tag.strip().strip('"') if held_item_tag else None

            moves = team_member.find_all("span", {"class": "badge"})
            move1, move2, move3, move4 = moves

            team_member_data = [
                poke_icon,
                name,
                form,
                tera_type,
                ability,
                held_item,
                move1.text,
                move2.text,
                move3.text,
                move4.text,
            ]

            team_members.append(team_member_data)
        return team_members

    df = pd.read_csv(filepath)
    team_data = [
        [
            "tournament_id",
            "player_id",
            "icon",
            "pokemon",
            "form",
            "tera_type",
            "ability",
            "held_item",
            "move1",
            "move2",
            "move3",
            "move4",
        ]
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {
            executor.submit(
                fetch_team_members, f"https://rk9.gg/teamlist/public/{row['team_list']}"
            ): row
            for index, row in df.iterrows()
        }
        for future in concurrent.futures.as_completed(future_to_url):
            row = future_to_url[future]
            try:
                members = future.result()
                for member in members:
                    team_data.append([row["tournament_id"], row["player_id"], *member])
            except Exception as e:
                print(f"An error occurred: {e}")

    return team_data


def fetch_html(url):
    response = requests.get(url)
    return response.text
