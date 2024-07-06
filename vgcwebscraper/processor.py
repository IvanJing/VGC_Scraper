# This file is made to process the data fetched from rk9 and pokebase.
# My intention is to create CSV files, to avoid using tons of insert statements in the database.
import csv

# This function creates a csv file with provided data.
def create_csv(data, filepath):
    with open(filepath, mode="w", newline="", encoding="utf-8") as file:
        file.truncate(0)
        writer = csv.writer(file)
        writer.writerows(data)


def continue_csv(data, filepath):
    with open(filepath, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)
