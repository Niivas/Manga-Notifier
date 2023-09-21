import requests
from selectolax.lexbor import LexborHTMLParser
import time

MangaFetchUrl = 'https://japan-geeks.com/best-ongoing-manga/'
MangaSearchUrl = "https://mangajuice.com/?s="
MangaUpdatesUrl = 'https://mangajuice.com/updates/'

BestContinuingMangas = [ 'One Piece', 'Jujutsu Kaisen', 'My Hero Academia', 'Chainsaw Man', 'Dragon Ball Super',
                         'Kaiju No. 8', 'Boruto: Naruto Next Generations', 'One-Punch Man', 'Spy × Family', 'Yotsuba&!',
                         'The Apothecary Diaries', 'Case Closed', 'Laid-Back Camp', 'Teasing Master Takagi-san',
                         'Bungo Stray Dogs', 'Kingdom', 'Berserk', 'Hunter x Hunter', 'A Certain Scientific Railgun',
                         'Vagabond' ]

siteAcceptedNames = { 'One Piece': 'one-piece', 'Jujutsu Kaisen': 'jujutsu-kaisen',
                      'My Hero Academia': 'my-hero-academia', 'Chainsaw Man': 'chainsaw-man',
                      'Dragon Ball Super': 'dragon-ball-super', 'Kaiju No. 8': 'kaiju-no',
                      'Boruto: Naruto Next Generations': 'boruto-naruto-next-generations',
                      'Spy × Family': 'spy-x-family', 'Kingdom': 'kingdom', 'Berserk': 'berserk',
                      'Hunter x Hunter': 'hunter-x-hunter', 'Vagabond': 'vagabond',
                      'Komi Cant Communicate': 'komi-san-wa-komyushou-desu', 'Rent a Girlfriend': 'rent-a-girlfriend',
                      'More Than a Married Couple But Not Lovers': 'fuufu-ijou-koibito-miman'}

"""
def parseName(name):
    name = name.lower()
    res = [ ]
    for char in name:
        if char.isalnum():
            res.append(char)
    return "".join(res)


def parseUrl(url):
    n = len(url)
    for i in range(n - 2, -1, -1):
        if url[ i ] == '/':
            return url[ i + 1:-1 ]


for manga in BestContinuingMangas:
    searchPage = requests.get(MangaSearchUrl + manga)
    searchSoup = LexborHTMLParser(searchPage.text)
    if searchSoup.css_first('h1.page-title', default=False):
        continue
    searchResults = searchSoup.css('div.Latest_chapter_update')

    for result in searchResults:
        elementA = result.css_first('a')
        title = elementA.attrs.get('title', None)
        mangaUrl = elementA.attrs.get('href', None)
        if not title or not mangaUrl:
            continue
        if parseName(title) == parseName(manga):
            # siteAcceptedNames[ manga ] = parseUrl(mangaUrl)
            print(title)
            break
"""
# print(siteAcceptedNames)

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
ti = time.time()
searchPage = requests.get(MangaUpdatesUrl)

soup = LexborHTMLParser(searchPage.text)

As = soup.css('a.wrap-text')
n = len(As)

for i in range(1,n,2):
    print(As[i].attrs.get('href',0))
tf = time.time()

print('time took for fetching latest manga updates: ', tf-ti)