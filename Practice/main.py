import requests
from bs4 import BeautifulSoup

continuingMangas = ["chainsaw-man", "spy-x-family", "fuufu-ijou-koibito-miman", "rent-a-girlfriend",
                    "komi-san-wa-komyushou-desu"]
baseUrl = "https://mangajuice.com/manga/"

mangas = {}


def fetchLatestChapter(latestChapterLink):
    n = len(latestChapterLink)
    found = False
    chapterNumber = ""
    for i in range(n - 1, -1, -1):
        if found:
            if latestChapterLink[i].isdigit() or latestChapterLink[i] == '.':
                chapterNumber += latestChapterLink[i]
            else:
                break
        else:
            if latestChapterLink[i].isdigit():
                found = True
                chapterNumber += latestChapterLink[i]
    return float(chapterNumber[::-1])


def getLatestChapterAndLink(mangaName):
    htmlPage = requests.get(baseUrl + mangaName)
    soup = BeautifulSoup(htmlPage.content, 'lxml')
    latestChapterLink = soup.find('a', class_="Latest_Chapter")["href"]
    mangaName = {'latestChapter': fetchLatestChapter(latestChapterLink), 'link': latestChapterLink}
    return mangaName


def fetchMangasInfo(mangakas):
    for manga in mangakas:
        mangas[manga] = getLatestChapterAndLink(manga)


fetchMangasInfo(continuingMangas)
print(mangas)
