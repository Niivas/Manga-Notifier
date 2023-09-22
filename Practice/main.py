import requests
from selectolax.lexbor import LexborHTMLParser
import time
import json
import os

baseUrl = "https://mangajuice.com/manga/"
MangaUpdatesUrl = 'https://mangajuice.com/updates/'


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
    soup = LexborHTMLParser(htmlPage.text)
    mangaElement = soup.css_first('a.Latest_Chapter')
    latestChapterLink = mangaElement.attrs.get('href')
    latestChapter = fetchLatestChapter(latestChapterLink)
    return latestChapter, latestChapterLink


def fetchMangasInfoRespective(mangaka):
    for manga in mangaka:
        chapter, link = getLatestChapterAndLink(mangaka[manga]['siteAcceptedName'])
        previousChapter = mangaka[manga]['latestChapter']
        mangas[manga]["latestChapter"] = chapter
        mangas[manga]["latestChapterLink"] = link
        mangas[manga]["chaptersAddedSinceYouLastRead"] = chapter - previousChapter


def getLatestChapterName(url):
    n = len(url)
    end = 0
    for i in range(n - 2, -1, -1):
        if url[i] == 'c' and end == 0:
            end = i - 1
        if url[i] == '/':
            return url[i + 1:end]
    return ''


def fetchMangasInfo(mangaka):
    MangaAcceptedNames = set()
    sanToMangaName = { }
    for manga in mangaka:
        MangaAcceptedNames.add(mangaka[manga]['siteAcceptedName'])
        sanToMangaName[mangaka[manga]['siteAcceptedName']] = manga
    updatesPage = requests.get(MangaUpdatesUrl)
    soup = LexborHTMLParser(updatesPage.text)
    mangasInfo = soup.css('a.wrap-text')
    recentlyUpdatedMangaCount = len(mangasInfo)
    for i in range(1, recentlyUpdatedMangaCount, 2):
        latestChapterUrl = mangasInfo[i].attrs.get('href', '')
        mangaTitle = mangasInfo[i - 1].attrs.get('title', "")
        name = getLatestChapterName(latestChapterUrl)
        currentChapter = fetchLatestChapter(latestChapterUrl)
        if name in MangaAcceptedNames:
            previousChapter = mangaka[sanToMangaName[name]]['latestChapter']
            mangaka[sanToMangaName[name]]['latestChapterLink'] = latestChapterUrl
            mangaka[sanToMangaName[name]]['latestChapter'] = currentChapter
            mangaka[sanToMangaName[name]]['chaptersAddedSinceYouLastRead'] = currentChapter - previousChapter
        else:
            mangaka[mangaTitle] = dict()
            mangaka[mangaTitle]['siteAcceptedName'] = name
            mangaka[mangaTitle]['latestChapter'] = currentChapter
            mangaka[mangaTitle]['latestChapterLink'] = latestChapterUrl
            mangaka[mangaTitle]['chaptersAddedSinceYouLastRead'] = 0


previousMangaUpdatesFile = open(r'C:\Users\Nivas Reddy\Desktop\Manga-Notifier\results\Latest Manga Updates.txt', 'r')
mangas = json.loads(previousMangaUpdatesFile.read())
ti = time.time()
fetchMangasInfo(mangas)
tf = time.time()
print(f"Time took for fetching updates of {len(mangas)} mangas: {tf - ti} seconds")
previousMangaUpdatesFile.close()

os.chdir(r'C:\Users\Nivas Reddy\Desktop\Manga-Notifier\results')
ti = time.time()
with open('Latest Manga Updates.txt', 'w') as file:
    file.write(json.dumps(mangas, indent=4))
tf = time.time()
print(f"Time took for writing updates of {len(mangas)} mangas to Latest Manga Updates.txt file: {tf - ti} seconds")
