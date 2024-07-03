"""Modules for scraping, parsing, fetching and cleaning data from the rk9.gg website.

The functions in this file are used to scrape information from the rk9 tournament website, parse the data, and prepare it for storage in a CSV file.
Because of the way the site formats tournaments, we need to first fill the tournaments dataset, then follow the scraped links in order
to fill the standings dataset. Similarly, team view is hidden behind more links, so we need to scrape and crawl those as well. 

"""

from bs4 import BeautifulSoup
import requests
import hashlib
from datetime import datetime
from daterangeparser import parse

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
                rk9_id = link["href"].strip("/tournament/")

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
    
    Creates a url using rk9_id and fetches all standings data from the website.

    Args:
        tournament_data: A nested list containing the corresponding table columns for tournaments.

    Returns:
        A nested list containing the corresponding table columns for standings, as well as the additional 'tournament_id' column.
        Most of the columns are self-explanatory, but the team list column will be a JSON file, which will be parsed later.
    
    Raises:
        IOError: If the HTML response is invalid.
    """

    standings_data = []

    for row in tournament_data:
        tournament_id, _,_, rk9_id, _, _, _ = row

        if rk9_id:
            standings_url = f"https://rk9.gg/roster/{rk9_id}"
            response = fetch_html(standings_url)
            soup = BeautifulSoup(response, "lxml")

            rows = soup.find_all("tr")
            
    

def fetch_html(url):
    response = requests.get(url)
    return response.text
