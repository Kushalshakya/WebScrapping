import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def cleaned_quotes(quote):
    return quote.text.replace('"', '').replace('“', '').replace('”', '')

def get_quotes(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    data = {
        "Quotes": [],
        "Authors": [],
        "Links": []
    }
    quotes = soup.select(".quote > span.text")
    authors = soup.select(".author")
    links = soup.select(".quote span a")

    data["Quotes"] = [cleaned_quotes(quote) for quote in quotes]
    for author in authors:
        data["Authors"].append(author.text)
    for link in links:
        data["Links"].append("https://quotes.toscrape.com" + link.get("href"))    
    return data
    
all_data = {
    "Quotes": [],
    "Authors": [],
    "Links": []
}

# This is the bad practice for explicitly execution for pagination
for x in range(1, 10):
    url = f"https://quotes.toscrape.com/page/{x}"
    
    page_data = get_quotes(url)
    all_data["Quotes"].extend(page_data["Quotes"])
    all_data["Authors"].extend(page_data["Authors"])
    all_data["Links"].extend(page_data["Links"])

df = pd.DataFrame.from_dict(all_data)
df.to_csv("quotes.csv", index=False)

print("Data saved to quotes.csv")
