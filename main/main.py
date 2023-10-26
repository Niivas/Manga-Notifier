import json
import time
from datetime import datetime
from selenium import webdriver
import requests
from selectolax.lexbor import LexborHTMLParser
from UpdatePdf import updatePdf  # Assuming UpdatePdf.py has a function named updatePDF

# PATH = "C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"
# driver = webdriver.Chrome(PATH)
# Base URLs for manga information
MangaJuiceBaseUrl = "https://mangajuice.com/manga/"
MangaJuiceUpdatesUrl = 'https://mangajuice.com/updates/'


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
    htmlPage = requests.get(MangaJuiceBaseUrl + mangaName)
    soup = LexborHTMLParser(htmlPage.text)
    mangaElement = soup.css_first('a.Latest_Chapter')
    latestChapterLink = mangaElement.attrs.get('href')
    latestChapter = fetchLatestChapter(latestChapterLink)
    return latestChapter, latestChapterLink


# Function to update manga information for each mangaka
def fetchMangasInfoRespective(mangaka):
    for manga in mangaka:
        chapter, link = getLatestChapterAndLink(mangaka[manga]['siteAcceptedName'])
        previousChapter = mangaka[manga]['latestChapter']
        mangas[manga]["latestChapter"] = chapter
        mangas[manga]["latestChapterLink"] = link
        mangas[manga]["chaptersAddedSinceYouLastRead"] = chapter - previousChapter


# Function to extract the chapter name from the chapter URL
def getLatestChapterName(url):
    n = len(url)
    end = 0
    for i in range(n - 2, -1, -1):
        if url[i] == 'c' and end == 0:
            end = i - 1
        if url[i] == '/':
            return url[i + 1:end]
    return ''


# Function to fetch manga information from the update page
def fetchMangasInfo(mangaka):
    MangaAcceptedNames = set()
    sanToMangaName = {}
    for manga in mangaka:
        MangaAcceptedNames.add(mangaka[manga]['siteAcceptedName'])
        sanToMangaName[mangaka[manga]['siteAcceptedName']] = manga
    updatesPage = requests.get(MangaJuiceUpdatesUrl)
    soup = LexborHTMLParser(updatesPage.text)
    mangasInfo = soup.css('a.wrap-text')
    recentlyUpdatedMangaCount = len(mangasInfo)
    for i in range(1, recentlyUpdatedMangaCount, 2):
        latestChapterUrl = mangasInfo[i].attrs.get('href', '')
        mangaTitle = mangasInfo[i - 1].attrs.get('title', "")
        name = getLatestChapterName(latestChapterUrl)
        currentChapter = fetchLatestChapter(latestChapterUrl)
        if name in MangaAcceptedNames:
            previousChapter = float(mangaka[sanToMangaName[name]]['latestChapter'])
            mangaka[sanToMangaName[name]]['latestChapterLink'] = latestChapterUrl
            mangaka[sanToMangaName[name]]['latestChapter'] = str(currentChapter)
            mangaka[sanToMangaName[name]]['chaptersAddedSinceYouLastRead'] = str(currentChapter - previousChapter)
        else:
            mangaka[mangaTitle] = dict()
            mangaka[mangaTitle]['siteAcceptedName'] = name
            mangaka[mangaTitle]['latestChapter'] = str(currentChapter)
            mangaka[mangaTitle]['latestChapterLink'] = latestChapterUrl
            mangaka[mangaTitle]['chaptersAddedSinceYouLastRead'] = "1"
            mangaka[mangaTitle]['isFavorite'] = 'no'


# Function to update the statistics file with relevant information
def updateStatsFile(prev, curr):
    favouriteMangaUpdatedInTheRecentFetch = 0
    totalFavoriteMangas = 0
    for manga in mangas:
        if mangas[manga]['isFavorite'] == 'yes':
            if mangas[manga]['chaptersAddedSinceYouLastRead'] != '0.0':
                favouriteMangaUpdatedInTheRecentFetch += 1
            totalFavoriteMangas += 1

    content = {}
    curTimeAndDate = datetime.now().strftime("%H:%M %Y-%m-%d")
    content['Mangas last fetched time'] = curTimeAndDate
    content['Mangas Added in the recent Fetch'] = str(curr - prev)
    content['Favourite mangas updated in the recent fetch'] = str(favouriteMangaUpdatedInTheRecentFetch)
    content['Total favorite mangas'] = str(totalFavoriteMangas)
    content['Current Total Mangas'] = str(curr)
    content['Additional Info'] = "Mangas whose chapters got released recently are marked in green colour in the pdf"

    with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\stats.txt', 'w') as statsFile:
        statsFile.write(json.dumps(content, indent=4))


# Load the previous manga updates from file
with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt',
          'r') as previousMangaUpdatesFile:
    mangas = json.loads(previousMangaUpdatesFile.read())

beforeFetchMangaCount = len(mangas)

# Fetch the latest manga updates
ti = time.time()
fetchMangasInfo(mangas)
tf = time.time()
# print(f"Time took for fetching updates of {len(mangas)} mangas: {tf - ti} seconds")

afterFetchMangaCount = len(mangas)

# Update the statistics file
updateStatsFile(beforeFetchMangaCount, afterFetchMangaCount)

# Sort the manga updates based on chapters added since last read
mangas = dict(sorted(mangas.items(), key=lambda item: float(item[1]['chaptersAddedSinceYouLastRead']), reverse=True))

# Write the updated manga information to the file
# ti = time.time()
with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt', 'w') as file:
    file.write(json.dumps(mangas, indent=4))
# tf = time.time()
# print(f"Time took for writing updates of {len(mangas)} mangas to Latest Manga Updates.txt file: {tf - ti} seconds")

# Update the PDF with the latest manga information
# ti = time.time()
updatePdf(mangas)
# tf = time.time()
# print(f"Time took for writing updates of {len(mangas)} mangas to Latest Manga Updates.pdf file: {tf - ti} seconds")
