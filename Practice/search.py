import requests
from bs4 import BeautifulSoup

# import main
MangaSearchUrl = "https://mangajuice.com/?s="

mangaName = "One+Piece"

htmlPage = requests.get(MangaSearchUrl + mangaName)
soup = BeautifulSoup(htmlPage.content, "lxml")
print(soup)