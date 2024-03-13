import time
import asyncio
import aiohttp
import requests
from selectolax.lexbor import LexborHTMLParser
from utils.utils import cosine_similarity

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

mainUrl = "https://www.mangaread.org/"
mangaPageUrl = "https://www.mangaread.org/manga/"
mangaSearchPage = (
    lambda mangaTitle: f"https://www.mangaread.org/?s={mangaTitle}&post_type=wp-manga"
)
updatesPage = "https://www.mangaread.org/"


def get_tasks(session, mangaReadSans):
    """
    creates a list of tasks for fetching manga pages asynchronously.

    :param session: the aiohttp session for making HTTP requests.
    :type session: aiohttp.ClientSession
    :param mangaReadSans: List of manga titles to fetch.
    :type mangaReadSans: list[str]
    :return: List of tasks for fetching manga pages.
    :rtype: list[asyncio.Task]
    """
    tasks = []
    for manga in mangaReadSans:
        tasks.append(asyncio.create_task(session.get(mangaPageUrl + manga, ssl=False)))
    return tasks


async def fetchMangaResponses(mangas):
    """
    :param mangas: A dictionary containing manga information.
    Each key represents a manga name and its corresponding
    value is another dictionary with the following keys: - "mangaReadSan": A unique identifier for the manga. -
    "latestChapter": The latest chapter number for the manga. - "latestChapterLink": The link to the latest chapter.
    - "latestRelease": The release date of the latest chapter.
    - "chaptersAddedSinceYouLastRead": An optional key
    that may exist if new chapters have been added since you last read the manga.
    :return: None

    This method fetches manga responses for each manga in the given dictionary using aiohttp.
    It retrieves the latest
    chapter information for each manga from the response
    and updates the corresponding values in the mangas
    dictionary.
    If new chapters have been added since you last read the manga, the "chaptersAddedSinceYouLastRead"
    key is removed from the manga's dictionary.
    """
    mangaReadSans = []
    mangaResponses = []
    for manga in mangas:
        mangaReadSans.append(mangas[manga]["mangaReadSan"])
    saNToMangaName = {}
    for manga in mangas:
        saNToMangaName[mangas[manga]["mangaReadSan"]] = manga

    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, mangaReadSans)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            mangaResponses.append(await response.text())
    for manga, response in zip(mangaReadSans, mangaResponses):
        soup = LexborHTMLParser(response)
        title = soup.css_first("title").text()
        if "Page not found" in title:
            continue
        latestNode = soup.css_first("li.wp-manga-chapter    ")
        if latestNode is None:
            continue
        latestChapterLink = latestNode.css_first("a").attrs.get("href")
        releaseDate = latestNode.css_first("i").text()
        latestChapter = float(parseUrl(latestChapterLink))
        if latestChapter > float(mangas[saNToMangaName[manga]]["latestChapter"]):
            mangas[saNToMangaName[manga]]["latestChapter"] = latestChapter
            mangas[saNToMangaName[manga]]["latestChapterLink"] = latestChapterLink
            mangas[saNToMangaName[manga]]["latestRelease"] = releaseDate
        if "chaptersAddedSinceYouLastRead" in mangas[saNToMangaName[manga]]:
            del mangas[saNToMangaName[manga]]["chaptersAddedSinceYouLastRead"]


def parseUrl(url):
    """
    Extracts the last portion of the URL after the second last occurrence
    of a forward slash ("/") and splits it using a hyphen ("-") as the delimiter.

    :param url: The URL to be parsed.
    :return: The last portion of the URL after splitting using a hyphen ("-").
    """
    return url.split("/")[-2].split("-")[-1]


def fetchMangaReadRespective(mangas):
    """
    Fetches the respective manga read details for each manga.

    :param mangas: A dictionary containing manga details.
    :return: The updated mangas dictionary with respective manga read details.
    """
    for manga in mangas:
        mangaPage = requests.get(mangaPageUrl + mangas[manga]["mangaJuiceSan"])
        soup = LexborHTMLParser(mangaPage.text)
        print(manga)
        title = soup.css_first("head").css_first("title").text()
        if "Page not found" in title:
            print(f"Could not find {manga}")
            mangas[manga]["mangaReadSan"] = ""
            del mangas[manga]["chaptersAddedSinceYouLastRead"]
            continue
        mangas[manga]["mangaReadSan"] = mangas[manga]["mangaJuiceSan"]
        print(f"Found {manga}")
        latestNode = soup.css_first("li.wp-manga-chapter    ")
        latestChapterLink = latestNode.css_first("a").attrs.get("href")
        latestChapter = float(parseUrl(latestChapterLink))
        if latestChapter > float(mangas[manga]["latestChapter"]):
            mangas[manga]["latestChapter"] = latestChapter
            mangas[manga]["latestChapterLink"] = latestChapterLink
            mangas[manga]["latestRelease"] = latestNode.css_first("i").text()
        del mangas[manga]["chaptersAddedSinceYouLastRead"]
    return mangas


def findMangaReadSans(mangas):
    """
    Find mangaReadSans for given mangas.

    :param mangas: A dictionary of mangas with their details.
    :type mangas: Dict
    :return: A dictionary of mangas with updated mangaReadSans.
    :rtype: Dict
    """
    for manga in mangas:
        if mangas[manga]["mangaReadSan"] != "":
            continue
        mangaReadSan = ""
        similarity = 0
        searchPage = requests.get(mangaSearchPage(manga))
        soup = LexborHTMLParser(searchPage.text)
        if soup.css_first("div.not-found-content"):
            mangas[manga]["mangaReadSan"] = ""
            print(f"Could not find {manga}")
            continue
        titleNodes = soup.css("div.post-title")
        for node in titleNodes:
            titles = [node.css_first("a").text()]
            titles += soup.css_first("div.summary-content").text().split(";")
            for title in titles:
                similarityFound = cosine_similarity(manga, title)
                if similarityFound > similarity:
                    similarity = similarityFound
                    mangaReadSan = parseUrl(node.css_first("a").attrs.get("href"))
        if similarity > 0.5:
            mangas[manga]["mangaReadSan"] = mangaReadSan
            print(f"Found {manga}:", mangas[manga]["mangaReadSan"])
        else:
            mangas[manga]["mangaReadSan"] = ""
            print(f"Could not find similar {manga}")
    return mangas


def fetchMangaUpdates(mangas):
    """
    :param mangas: A dictionary containing manga information.
    Each key represents a manga name, and the corresponding
    value is a dictionary containing the manga's details such as its latest chapter,
    latest chapter link, and the latest release.
    :return: The updated mangas dictionary with the latest chapter,
    chapter link, and release information
    for each manga.
    """
    mangaReadSans = set()
    for manga in mangas:
        mangaReadSans.add(mangas[manga]["mangaReadSan"])
    sanToMangaName = {}
    for manga in mangas:
        sanToMangaName[mangas[manga]["mangaReadSan"]] = manga

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.mangaread.org/")

    try:
        loadMore = driver.find_element(By.ID, "navigation-ajax")
        clicks = 0
        while clicks < 5:
            loadMore.click()
            time.sleep(5)
            clicks += 1
        elements = driver.find_elements(By.CSS_SELECTOR, "div.item-summary")
        MangaUrls = [
            element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            for element in elements
        ]
        MangaStats = [element.text.split("\n") for element in elements]
        for i, item in enumerate(MangaUrls):
            mangaReadSan = parseUrl(item)
            if mangaReadSan in mangaReadSans:
                mangaName = sanToMangaName[mangaReadSan]
                previousChapter = float(mangas[mangaName]["latestChapter"])
                currentChapter = float(MangaStats[i][1].split(" ")[1])
                if currentChapter >= previousChapter:
                    mangas[mangaName]["latestChapter"] = str(currentChapter)
                    mangas[mangaName]["latestChapterLink"] = item
                    mangas[mangaName]["latestRelease"] = MangaStats[i][2]
    except Exception():
        driver.quit()
    driver.quit() 
    return mangas


def fetchFromMangaRead(mangas):
    """
    Fetches manga responses from MangaRead website using asynchronous requests and stores them in the mangas list.

    :param mangas: A list of manga objects.

    :return: The updated mangas list with fetched responses.
    """
    asyncio.run(fetchMangaResponses(mangas))
    return mangas
