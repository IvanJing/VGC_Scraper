from bs4 import BeautifulSoup
import requests

url = "https://rk9.gg/events/pokemon"

response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

rows = soup.find_all('tr')

for row in rows:
    columns = row.find_all('td')
    for column in columns:
        print(column.text.strip())

        links = column.find_all('a', string = 'VG')

        for link in links:
            print(link['href'].strip('/tournament/'))================================


