# VGC Scraper for Discord Bot

## Overview
This is a web scraper designed to fetch and process Pokémon VGC (Video Game Championships) tournament data from the RK9 Labs website. The scraper extracts tournament standings, team details, and other relevant information, which is then intended to be utilized by a Discord bot for real-time data retrieval and interaction. For the time being, it is just a helper tool that collects in the form of csv files, then uploads the data to an intended database. For the sake of this project, this is in the form of a PostgreSQL DB.

## Current Features
- Tournament Data Scraping: Fetches detailed information about recent tournaments on rk9, including dates, locations, and player standings.
- Team Data Extraction: Extracts individual team details, including Pokémon, moves, abilities, items, and more.
- Data Storage: Stores the scraped data in a structured format suitable for integration with a PostgreSQL database.

## Requirements
- Python 3.8+
- BeautifulSoup4
- Requests
- CSV
- SQLAlchemy

## Future Features/Next Up:
-  Need to gather data on forms
-  Automate data to pull from sources weekly (for up-to-date information)
-  Enhanced cleaning of data
