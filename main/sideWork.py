import json
import requests
from selectolax.lexbor import LexborHTMLParser

searchUrl = lambda x: f"https://www.mangaread.org/?s={x}&post_type=wp-manga"

with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt', 'r') as file:
    mangas = json.loads(file.read())
"""
for manga in mangas:
    isFavorite = input(f"is {manga} your favorite (yes/no): ")
    mangas[manga]["isFavorite"] = isFavorite
"""
for manga in mangas:
    searchPage = requests.get(searchUrl(manga))
    soup = LexborHTMLParser(searchPage.text)
    if soup.css_first('div.not-found-content'):
        mangas[manga]["image"] = ""
        continue
    mangas[manga]['image'] = soup.css('div.search-wrap')[0].css_first('img').attrs.get('data-src')

with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt', 'w') as file:
    file.write(json.dumps(mangas, indent=4))
