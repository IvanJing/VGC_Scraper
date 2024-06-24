from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Fetches tournament data from the rk9 website
def fetch_tournament_data(response):
    soup = BeautifulSoup(response, "lxml")

    rows = soup.find_all('tr')

    for row in rows:
        columns = row.find_all('td')
        
        if len(columns) >= 5:
            # Extract Date, Tournament Name, and City from specified columns.
            date = columns[0].text.strip()
            tournament_name = columns[2].text.strip()
            city = columns[3].text.strip()
            
            print(f"Date: {date}")
            print(f"Tournament Name: {tournament_name}")
            print(f"City: {city}")

            # Extract the src attribute from the logo column
            logo_img = columns[1].find('img')
            if logo_img:
                logo_link = "rk9.gg"+logo_img['src']

            # Extract the href attribute for VGC from link column
            vg_link = columns[4].find('a', string='VG')
            if vg_link:
                print(f"VG Link: {vg_link['href'].strip('/tournament/')}")
        else:
            print("Row does not have enough columns")

#Converts a date range string into a tuple of two datetime objects
def parse_date(date_range):
    month_day, year = [part.strip() for part in date_range.split(',')]
    month, days = month_day.split(' ')
    start_day, end_day = [day.strip() for day in days.split('-')]

    # Create date strings
    start_date_str = f"{year}-{month}-{start_day}"
    end_date_str = f"{year}-{month}-{end_day}"

    # Convert to datetime objects and format the dates
    start_date = datetime.strptime(start_date_str, "%Y-%B-%d").strftime("%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%B-%d").strftime("%Y-%m-%d")

    return (start_date, end_date)

def fetch_html(url):
    response = requests.get(url)
    return response.text

url = "https://rk9.gg/events/pokemon"
print(parse_date("June 7-9, 2024"))

