import json
import re
from datetime import datetime
from pathlib import Path

import petl
import requests

from .models import Collection

time_stamp = datetime.today().strftime("%Y-%m-%d")
data_path = Path(__file__).parent / ".." / "data"
headers = [
    "name",
    "height",
    "mass",
    "hair_color",
    "skin_color",
    "eye_color",
    "birth_year",
    "gender",
    "homeworld",
    "date",
]


def get_planet_id(planet_url):
    """
    This function is responsible for extracting the planet id
     from the planet URL by matching a pattern
    @param planet_url:
    @return: Planet ID
    """
    return re.findall(r"planets/(\d+)", planet_url)[0]


def fill_in_people_data(resource, planet):
    """
    This function is using the information already fetched
     form people and planets to construct the final object structure
    @param resource: People Object response from SWAPI API
    @param planet: Planet ID
    @return: reduced and enhanced people object
    """
    return {
        "name": resource["name"],
        "height": resource["height"],
        "mass": resource["mass"],
        "hair_color": resource["hair_color"],
        "skin_color": resource["skin_color"],
        "eye_color": resource["eye_color"],
        "birth_year": resource["birth_year"],
        "gender": resource["gender"],
        "homeworld": planet,
        "date": time_stamp,
    }


def crawl_planets():
    """
    This function calls the planets endpoint in the SWAPI API,
    @return: planets dictionary  with the planet ID as a key and its name as a value
    """
    planets = {}
    url = "https://swapi.dev/api/planets"
    next_planets_page = True
    while next_planets_page:
        response = requests.get(url)
        json_data = json.loads(response.content)
        for resource in json_data["results"]:
            planets[get_planet_id(resource["url"])] = resource["name"]
        if bool(json_data["next"]):
            url = json_data["next"]
        else:
            next_planets_page = False
    return planets


def crawl_people(planets):
    data = []
    url = "https://swapi.dev/api/people"
    next_people_page = True
    while next_people_page:
        response = requests.get(url)
        json_data = json.loads(response.content)
        for resource in json_data["results"]:
            data.append(
                fill_in_people_data(
                    resource, planets[get_planet_id(resource["homeworld"])]
                )
            )
        if bool(json_data["next"]):
            url = json_data["next"]
        else:
            next_people_page = False
    return data


def crawl():
    """
    This function is responsible for crawling  all the needed information from SWAPI API,
    it fetches the Planets endpoint at first, Then it fetches the People endpoint,
     Takes only specific attributes and replace the planet URL with the planet name before exporting
     The cleaned fetched information into CSV and saving the metadata (Filename and data of execution)
     in the Database

    @return: return the collection instance just created in the Database
    """
    planets = crawl_planets()
    people = crawl_people(planets)
    table = petl.fromdicts(people, header=headers)
    file_name = "{}.csv".format(datetime.today().strftime("%d%m%Y%H%M%S"))
    Path(data_path).mkdir(parents=True, exist_ok=True)
    petl.tocsv(table, data_path / file_name)
    collection_item = Collection.objects.create(file_name=file_name)
    return collection_item
