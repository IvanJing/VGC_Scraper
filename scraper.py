from bs4 import BeautifulSoup
import requests
import hashlib
from datetime import datetime
from daterangeparser import parse

# Fetches tournament data from the rk9 website
def fetch_tournament_data(response):
    soup = BeautifulSoup(response, "lxml")

    rows = soup.find_all('tr') # Find all rows in the table
    data = [(["tournament_id", "tournament_name", "location", "rk9_id", "start_date", "end_date", "logo_link"])]
    tournament_id = 0

    for row in rows:
        columns = row.find_all('td')
        
        if len(columns) >= 5:
            tournament_id+=1 # Basic id for the tournaments, couldn't think of a simpler way to go about this.

            # Extract Date, Tournament Name, and City from specified columns.
            date = columns[0].text.strip()
            tournament_name = columns[2].text.strip()
            location = columns[3].text.strip()
            start_date, end_date = parse_date(date)
            
            logo_img = columns[1].find('img')# Extract the src attribute from the logo column
            if logo_img:
                logo_link = "rk9.gg"+logo_img['src']

            #Extract the href attribute for VGC from link column
            link = columns[4].find('a', string='VG')
            if link:
                rk9_id = link['href'].strip('/tournament/')
            
            #Compile data and add into list
            data.append([tournament_id, tournament_name, location, rk9_id,start_date, end_date, logo_link])
        else:
            print("Row does not have enough columns")

    return data

# Converts a date range string into a tuple of two datetime objects
def parse_date(date_range):
    # Website's dumb and uses en dashes at random.
    date_range = date_range.replace('–', '-')
    try:
        start_date, end_date = parse(date_range) # Yay for robintw's parse function!

        return start_date.date(), end_date.date()
    
    except ValueError as e:
        print(f"Invalid date range: {date_range}")
        return None, None

def generate_tournament_id(tournament_name, location, start_date):
    # Generate a unique ID for the tournament
    return hashlib.md5(f"{tournament_name}{location}{start_date}".encode()).hexdigest()

def fetch_html(url):
    response = requests.get(url)
    return response.text

