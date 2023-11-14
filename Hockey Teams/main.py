import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

data = []

def get_soup(path):
    try:
        response = requests.get(path)
        return BeautifulSoup(response.text,"html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def cleaned_text(elem):
    return elem.text.strip()

def get_hockey_teams(url):
    soup = get_soup(url)
    teams = soup.find_all("tr", class_="team")

    for details in teams:
        team_name = cleaned_text(details.find("td", class_="name"))
        year = cleaned_text(details.find("td", class_="year"))
        wins = cleaned_text(details.find("td", class_="wins"))
        losses = cleaned_text(details.find("td", class_="losses"))
        ot_losses = cleaned_text(details.find("td", class_="ot-losses"))
        if (ot_losses == ""):
            ot_losses = 0
        win_percentage = cleaned_text(details.find("td", class_="pct"))
        goals_for = cleaned_text(details.find("td", class_="gf"))
        goals_against = cleaned_text(details.find("td", class_="ga"))
        positive_negative = cleaned_text(details.find("td", class_="diff"))
            
        data_dict = {
            "Team Name": team_name,
            "Year": year,
            "Wins": wins,
            "Losses": losses,
            "OT Losses": ot_losses,
            "Win %": win_percentage,
            "Goals For (GF)": goals_for,
            "Goals Against (GA)": goals_against,
            "+/-": positive_negative
        }
        data.append(data_dict)

for x in range(1, 7):
    get_hockey_teams(f"https://www.scrapethissite.com/pages/forms/?page_num={x}&per_page=100")
    time.sleep(1)

df = pd.DataFrame.from_dict(data)
df.to_csv("hockey.csv", index=False)

print("Successfully Created Hockey.csv")
