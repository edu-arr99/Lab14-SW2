from flask import Flask, request, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")

db = client['admin']

collection = db['covid']

@app.route("/covid/insert", methods=["POST"])
def new_covid():
    data = request.json
    id = data.get("id")
    country = data.get("country")
    iso_code = data.get("iso_code")
    date = data.get("date")
    total_vaccinations = data.get("total_vaccinations")
    people_vaccinated = data.get("people_vaccinated")
    people_fully_vaccinated = data.get("people_fully_vaccinated")
    new_deaths = data.get("New_deaths")
    population = data.get("population")
    ratio = data.get("ratio")

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



@app.route("/covid/report/<country>", methods=["GET"])
def country_report(country):
    query = collection.find({"country": country.capitalize()}, {"people_fully_vaccinated": 1, "new_deaths": 1}).sort("date", 1)
    results = list(query)
    serialized_results = []
    for result in results:
        serialized_result = result.copy()  

        serialized_result["_id"] = str(result["_id"]) 

        serialized_results.append(serialized_result)

    return json.dumps(serialized_results)


@app.route("/covid/report_year/<year>", methods=["GET"])
def year_report(year):
    query = collection.find({
        "date": {
            "$gte": f"{year}-01-01",
            "$lt": f"{int(year)+1}-01-01"
        }
    }, {"people_fully_vaccinated": 1, "new_deaths": 1}).sort("date", 1)

    results = list(query)

    serialized_results = []
    for result in results:
        serialized_result = result.copy()  

        serialized_result["_id"] = str(result["_id"]) 

        serialized_results.append(serialized_result)

    return json.dumps(serialized_results)


if __name__ == '__main__':
    app.run(debug=True)