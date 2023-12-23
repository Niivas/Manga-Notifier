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
    mangas = json.load(previousMangaUpdatesFile)

# Function to extract the chapter number from the chapter link
def fetchLatestChapter(latestChapterLink):
    """
    :param latestChapterLink: The link to the latest chapter.
    :return: The latest chapter number as a float.

    This function takes in a link to the latest chapter
    and extracts the chapter number from it.
    The chapter number is then returned as a float.

    Example usage:
    latest_chapter_link = "https://example.com/chapter/123"
    latest_chapter_number = fetchLatestChapter(latest_chapter_link)

    Note:
    This function assumes that the chapter number is located at the end of the URL
    and consists of consecutive digits followed by an optional decimal point.
    Any non-digit or non-decimal character before the chapter number will be considered as the end of the number.
    """
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
    """
    :param mangaName: The name of the manga to retrieve the latest chapter and link for.
    :return: A tuple containing the latest chapter number,
    the link to the latest chapter, and the latest release date of the manga.
    """
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
    """
    This method fetches information about mangas for a given mangaka.

    :param mangaka: A dictionary containing information about mangakas and their respective mangas.
    :return: A dictionary containing updated information about mangas.
    """
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
    """
    Get the latest chapter name from the given URL.

    :param url: The URL from which to extract the latest chapter name.
    :return: The latest chapter name extracted from the URL.
    """
    n = len(url)
    for i in range(n - 2, -1, -1):
        if url[i] == '/':
            return url[i + 1:n - 1]
    return ''


# Function to fetch manga information from the update page
def fetchMangasInfo(mangaka):
    """
    Fetches manga information from the MangaJuice website.

    :param mangaka: A dictionary of manga information, where each key is the manga title, and the value is a dictionary
    containing various manga details.
    :return: The updated manga information dictionary.

    """
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
    """
    retrieve a list of tasks for fetching manga data.

    :param session: the session to use for making HTTP requests.
    :type session: aiohttp.ClientSession
    :param mangaJuiceSans: The list of manga to fetch data for.
    :type mangaJuiceSans: list[str]
    :return: A list of tasks for fetching manga data.
    :rtype: list[asyncio.Task]
    """
    tasks = []
    for manga in mangaJuiceSans:
        tasks.append(asyncio.create_task(session.get(MangaJuiceBaseUrl + manga, ssl=False)))
    return tasks


def parseUrl(latestChapterLink):
    """
    :param latestChapterLink: The URL of the latest chapter.
    :return: The parsed version of the latest chapter link.

    This function takes in a URL and extracts the latest chapter number from it.
    The URL should be in the format "example.com/chapter-x", where x is the chapter number.
    The extracted chapter number is returned as a string.

    Example:
        latestChapterLink = "example.com/chapter-10"
        parseUrl(latestChapterLink) # returns "10"
    """
    return latestChapterLink.split("/")[-2].split("-")[-1]


async def fetchMangaResponses(mangas):
    """
    :param mangas: A dictionary containing manga information.
    :return: A list of manga responses.

    This method fetches manga responses for the given list of mangas
    using asynchronous HTTP requests with an aiohttp library.
    It retrieves the HTML content of each manga
    and performs parsing operations using LexborHTMLParser from selectolax.lexbor library.

    The method takes a parameter 'mangas', which is a dictionary containing manga information.
    Each manga is represented by a key-value pair in the dictionary.
    The key is the manga's name,
    and the value is another dictionary containing manga details such as mangaJuiceSan,
    latestChapter, latestChapterLink, and latestRelease.

    The method initializes an empty list 'mangaJuiceSans'
    to store the mangaJuiceSan values from the 'mangas' dictionary.
    It then creates a new dictionary 'saNToManga'
    to map each mangaJuiceSan value to its corresponding manga name.

    Inside the asynchronous context manager 'aiohttp.ClientSession()',
    the method creates a list of tasks using the 'get_tasks()' function and the mangaJuiceSans list.
    It then uses the 'await' keyword to gather the responses from all the tasks.

    For each mangaJuiceSan and its corresponding response,
    the method uses LexborHTMLParser to parse the HTML content.
    It retrieves the manga's title from the 'title' tag.
    If the title contains "Page Not Found" or "504", the manga is skipped.
    Otherwise, it finds the latest chapter information from the 'ul.chapterslist'
    tag and extracts the latest chapter link and release date.
    If the latest chapter is greater than the manga's current latestChapter value,
    the manga's details in the 'mangas' dictionary are updated with the new information.

    The method returns a list of manga responses.
    """
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
