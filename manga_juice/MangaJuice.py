import json

import requests
import aiohttp
import asyncio
from selectolax.lexbor import LexborHTMLParser

# Base URLs for manga information
MangaJuiceBaseUrl = "https://mangajuice.com/manga/"
MangaJuiceUpdatesUrl = "https://mangajuice.com/updates/"

with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt',
          'r') as previousMangaUpdatesFile:
    mangas = json.loads(previousMangaUpdatesFile.read())

# Function to extract the chapter number from the chapter link
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


# Function to get the latest chapter and its link for a given manga
def getLatestChapterAndLink(mangaName):
    try:
        htmlPage = requests.get(MangaJuiceBaseUrl + mangaName)
        soup = LexborHTMLParser(htmlPage.text)
        mangaElement = soup.css_first('ul.chapterslist')
        latestChapterLink = mangaElement.css_first('li').css_first('a').attrs.get('href', '')
        latestRelease = mangaElement.css_first('li').css_first('span').text()
        latestChapter = fetchLatestChapter(latestChapterLink)
        return latestChapter, latestChapterLink, latestRelease
    except AttributeError:
        print(f"Could not find {mangaName}")
        return 0, "", ""


# Function to update manga information for each manga
def fetchMangasInfoRespective(mangaka):
    mangas = mangaka.copy()
    for manga in mangaka:
        mangaName = mangaka[manga]["mangaJuiceSan"]
        print(f"Updated {manga}")
        chapter, link, latestRelease = getLatestChapterAndLink(mangaName)
        previousChapter = float(mangaka[manga]['latestChapter'])
        mangas[manga]["latestChapter"] = str(chapter) if chapter != 0 else previousChapter
        mangas[manga]["latestChapterLink"] = link if link != "" else mangas[manga]["latestChapterLink"]
        mangas[manga]["latestRelease"] = latestRelease if latestRelease != "" else mangas[manga]["latestRelease"]
    return mangas


# Function to extract the chapter name from the chapter URL
def getLatestChapterName(url):
    n = len(url)
    for i in range(n - 2, -1, -1):
        if url[i] == '/':
            return url[i + 1:n - 1]
    return ''


# Function to fetch manga information from the update page
def fetchMangasInfo(mangaka):
    MangaAcceptedNames = set()
    sanToMangaName = {}
    for manga in mangaka:
        MangaAcceptedNames.add(mangaka[manga]['mangaJuiceSan'])
        sanToMangaName[mangaka[manga]['mangaJuiceSan']] = manga
    updatesPage = requests.get(MangaJuiceUpdatesUrl)
    soup = LexborHTMLParser(updatesPage.text)
    mangaInfo = soup.css('div.Latest_chapter_update')
    for node in mangaInfo:
        latestChapterUrls = node.css("a.wrap-text")
        mangaTitle = latestChapterUrls[0].attrs.get('title', "")
        name = getLatestChapterName(latestChapterUrls[0].attrs.get('href', ""))
        currentChapter = fetchLatestChapter(latestChapterUrls[1].attrs.get('href', ""))
        if name in MangaAcceptedNames:
            previousChapter = float(mangaka[sanToMangaName[name]]['latestChapter'])
            mangaka[sanToMangaName[name]]['latestChapterLink'] = latestChapterUrls[1].attrs.get('href', "")
            mangaka[sanToMangaName[name]]['latestChapter'] = str(currentChapter)
            mangaka[sanToMangaName[name]]['chaptersAddedSinceYouLastRead'] = str(currentChapter - previousChapter)
            mangaka[sanToMangaName[name]]['latestRelease'] = node.css_first('span').text()
        else:
            mangaka[mangaTitle] = {}
            mangaka[mangaTitle]['mangaJuiceSan'] = name
            mangaka[mangaTitle]['latestChapter'] = str(currentChapter)
            mangaka[mangaTitle]['latestChapterLink'] = latestChapterUrls[1].attrs.get('href', "")
            mangaka[mangaTitle]['chaptersAddedSinceYouLastRead'] = "1"
            mangaka[mangaTitle]['isFavorite'] = 'no'
            mangaka[mangaTitle]['latestRelease'] = node.css_first('span').text()
    return mangaka


def get_tasks(session, mangaJuiceSans):
    tasks = []
    for manga in mangaJuiceSans:
        tasks.append(asyncio.create_task(session.get(MangaJuiceBaseUrl + manga, ssl=False)))
    return tasks


def parseUrl(latestChapterLink):
    return latestChapterLink.split("/")[-2].split("-")[-1]


async def fetchMangaResponses(mangas):
    mangaJuiceSans = []
    mangaResponses = []
    for manga in mangas:
        mangaJuiceSans.append(mangas[manga]["mangaJuiceSan"])
    saNToManga = {}
    for manga in mangas:
        saNToManga[mangas[manga]["mangaJuiceSan"]] = manga

    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, mangaJuiceSans)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            mangaResponses.append(await response.text())
    for manga, response in zip(mangaJuiceSans, mangaResponses):
        soup = LexborHTMLParser(response)
        title = soup.css_first("title").text()
        if "Page Not Found" in title or "504" in title:
            continue
        latestNode = soup.css_first("ul.chapterslist").css_first("li")
        if latestNode is None:
            continue
        latestChapterLink = latestNode.css_first("a").attrs.get("href")
        releaseDate = latestNode.css_first("span").text()
        latestChapter = float(parseUrl(latestChapterLink))
        if latestChapter > float(mangas[saNToManga[manga]]["latestChapter"]):
            mangas[saNToManga[manga]]["latestChapter"] = latestChapter
            mangas[saNToManga[manga]]["latestChapterLink"] = latestChapterLink
            mangas[saNToManga[manga]]["latestRelease"] = releaseDate
