import requests
from bs4 import BeautifulSoup

# import main
MangaFetchUrl = 'https://japan-geeks.com/best-ongoing-manga/'
MangaSearchUrl = "https://mangajuice.com/?s="

BestContinuingMangas = [ 'One Piece', 'Jujutsu Kaisen', 'My Hero Academia', 'Chainsaw Man', 'Dragon Ball Super',
                         'Kaiju No. 8', 'Boruto: Naruto Next Generations', 'One-Punch Man', 'Spy × Family', 'Yotsuba&!',
                         'The Apothecary Diaries', 'Case Closed', 'Laid-Back Camp', 'Teasing Master Takagi-san',
                         'Bungo Stray Dogs', 'Kingdom', 'Berserk', 'Hunter x Hunter', 'A Certain Scientific Railgun',
                         'Vagabond' ]

searchPage = requests.get(MangaSearchUrl + " ")
SearchSoup = BeautifulSoup(searchPage.content, "lxml")
print(SearchSoup)
"""
fetchPage = requests.get(MangaFetchUrl)
fetchSoup = BeautifulSoup(fetchPage.content, 'lxml')

mangaElements = fetchSoup.find_all('strong')


def parseMangaElement(element):
    n = len(element)
    for i in range(n - 1, -1, -1):
        if element[i] == '(':
            return element[:i - 1]
    return element


for mangaElement in mangaElements:
    BestContinuingMangas.append(parseMangaElement(mangaElement.text))

print(BestContinuingMangas)
"""
