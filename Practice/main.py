from bs4 import BeautifulSoup
import requests
from collections import defaultdict

continuingMangas = ["Chainsaw man", "spy X family", "More than a married couple, but not lovers", "Rent a girlfriend",
                    "Komi can't communicate"]
mangas = defaultdict()

for manga in continuingMangas:
    mangas[manga] = defaultdict()
    mangas[manga]["link"] = input(f"link for {manga}: ")
    mangas[manga]["lastReleasedChapter"] = input(f"Last released chapter of the {manga}: ")
    mangas[manga]["isFavourite"] = input(f"Is it one of your favourite manga: y/n: ")

htmlPage = requests.get("https://www.chainsawman-online.com/")

soup = BeautifulSoup(htmlPage.content, 'lxml')

match = soup.find('li', class_="widget ceo_latest_comics_widget").text.split("\n")
print(match[1][-3:])
