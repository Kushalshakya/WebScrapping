import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_soup(url):
    try:
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def clean_text(element):
    return element.text.strip()

def countries_details(url):
    data = {
        "Countries": [],
        "Country Area": [],
        "Population": []
    }
    soup = get_soup(url)

    with open("index.html", "w", encoding='utf-8') as fp:
        fp.write(soup.prettify())

    if soup:
        names = soup.find_all(class_="country-name")
        areas = soup.select("span.country-area")
        populations = soup.select("span.country-population")
        data["Countries"] = [clean_text(name) for name in names]
        data["Country Area"] = [clean_text(area) for area in areas]
        data["Population"] = [clean_text(population) for population in populations]

        df = pd.DataFrame.from_dict(data)
        df.to_csv("countries.csv", index=False)
        print(data)

countries_details("https://www.scrapethissite.com/pages/simple/")
