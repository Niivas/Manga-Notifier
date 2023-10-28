import json
import requests
from selectolax.lexbor import LexborHTMLParser

with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt', 'r') as file:
    mangas = json.loads(file.read())
"""
for manga in mangas:
    isFavorite = input(f"is {manga} your favorite (yes/no): ")
    mangas[manga]["isFavorite"] = isFavorite
"""

"""
def parseName(name):
    if "\u2019" in name:
        return name.split("\u2019")[0]
    if "'" in name:
        return name.split("'")[0]
    return name


for manga in mangas:
    searchPage = requests.get(searchUrl(parseName(manga)))
    soup = LexborHTMLParser(searchPage.text)
    if soup.css_first('div.not-found-content'):
        mangas[manga]["image"] = ""
        print(f"Could not find {manga}")
        continue
    mangas[manga]['image'] = soup.css('div.search-wrap')[0].css_first('img').attrs.get('data-src')
    print(f"Found {manga}")
"""

for manga in mangas:
    mangas[manga]["mangaJuiceSan"] = mangas[manga]["siteAcceptedName"]
    del mangas[manga]["siteAcceptedName"]
with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt', 'w') as file:
    file.write(json.dumps(mangas, indent=4))
