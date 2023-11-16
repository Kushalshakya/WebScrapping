import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# For Extracting the links from the webpage
pages = []
def bs4Module():
    def get_soup(path):
        try:
            response = requests.get(path, headers)
            return BeautifulSoup(response.text, "html.parser")
        except request.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def fetchData(url):
        soup = get_soup(url)
        get_links = soup.select(".year-link")
        for link in get_links:
            pages.append(link.get("id"))

    fetchData("https://www.scrapethissite.com/pages/ajax-javascript/")

bs4Module()
driver = webdriver.Chrome()
driver.get(r"https://www.scrapethissite.com/pages/ajax-javascript/")

data = []

for pageLink in pages:
    driver.find_element(By.ID,pageLink).click()
    time.sleep(5)
    dynamicTable = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table"))
    )
    film_title = dynamicTable.find_elements(By.CLASS_NAME, "film-title")
    film_nominations = dynamicTable.find_elements(By.CLASS_NAME, "film-nominations")
    film_awards = dynamicTable.find_elements(By.CLASS_NAME, "film-awards")
    
    for title, nominations, awards in zip(film_title, film_nominations, film_awards):
        data_dict = {
            "Year": pageLink,
            "Film Title": title.text,
            "Film Nominations": nominations.text,
            "Film Awards": awards.text
        }
        data.append(data_dict)

# print(data)

df = pd.DataFrame.from_dict(data)
df.to_csv("data.csv", index=False)
print("Successfully created data.csv")
toJSON = pd.read_csv("data.csv")
toJSON.to_json("data.json", orient='records')
print("Successfully created data.json")
driver.close()
