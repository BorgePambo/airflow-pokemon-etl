import requests
import json
import os
import csv

def extract_pokemn():
    url = "https://pokeapi.co/api/v2/pokemon"
    pokemon_list = []

    while url is not None:
        response = requests.get(url)
        data = response.json()
        url = data["next"]

        for item in data["results"]:
            name_poken = item["name"]
            url_poken = f"https://pokeapi.co/api/v2/pokemon/{name_poken}"
            response_poken = requests.get(url_poken).json()

            info_poken = {
                "id": response_poken["id"],
                "name": name_poken,
                "is_default": response_poken["is_default"],
                "location_area": response_poken["location_area_encounters"],
            }

            pokemon_list.append(info_poken)

    # Caminho atualizado dentro do container
    path = "/opt/airflow/datas"
    os.makedirs(path, exist_ok=True)

    csvfile = os.path.join(path, "pokemon.csv")
    if os.path.exists(csvfile):
        os.remove(csvfile)
        print("File deleted successfully")

    with open(csvfile, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["id", "name", "is_default", "location_area"])
        writer.writeheader()

        for pokemon in pokemon_list:
            writer.writerow(pokemon)
