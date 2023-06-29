from pymongo import MongoClient
import csv


def add_data():
    client = MongoClient("mongodb://localhost:27017")

    db = client['admin']

    collection = db['covid']

    with open('covid-vaccination-vs-death_ratio.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            id = row["id"]
            country = row["country"]
            iso_code = row["iso_code"]
            date = row["date"]
            total_vaccinations = row["total_vaccinations"]
            people_vaccinated = row["people_vaccinated"]
            people_fully_vaccinated = row["people_fully_vaccinated"]
            new_deaths = row["New_deaths"]
            population = row["population"]
            ratio = row["ratio"]

            document = {
                "id": id,
                "country": country, 
                "iso_code": iso_code, 
                "date": date,
                "total_vaccinations": total_vaccinations,
                "people_vaccinated": people_vaccinated, 
                "people_fully_vaccinated": people_fully_vaccinated, 
                "new_deaths": new_deaths,
                "population": population, 
                "ratio": ratio
            }

            collection.insert_one(document)
    client.close()

add_data()

