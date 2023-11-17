import time
import asyncio
import aiohttp
import requests
from selectolax.lexbor import LexborHTMLParser
from utils.utils import cosine_similarity

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome()
mainUrl = "https://www.mangaread.org/"
mangaPageUrl = "https://www.mangaread.org/manga/"
mangaSearchPage = lambda mangaTitle: f"https://www.mangaread.org/?s={mangaTitle}&post_type=wp-manga"
updatesPage = "https://www.mangaread.org/"


def get_tasks(session, mangaReadSans):
    tasks = []
    for manga in mangaReadSans:
        tasks.append(asyncio.create_task(session.get(mangaPageUrl + manga, ssl=False)))
    return tasks


async def fetchMangaResponses(mangas):
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
    return url.split("/")[-2].split("-")[-1]


def fetchMangaReadRespective(mangas):
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
        mangas[manga]["mangaReadSan"] = mangas[manga]['mangaJuiceSan']
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
        MangaUrls = [element.find_element(By.CSS_SELECTOR, "a").get_attribute("href") for element in elements]
        MangaStats = [element.text.split("\n") for element in elements]
        for i in range(len(MangaUrls)):
            mangaReadSan = parseUrl(MangaUrls[i])
            if mangaReadSan in mangaReadSans:
                mangaName = sanToMangaName[mangaReadSan]
                previousChapter = float(mangas[mangaName]['latestChapter'])
                currentChapter = float(MangaStats[i][1].split(" ")[1])
                if currentChapter >= previousChapter:
                    mangas[mangaName]["latestChapter"] = str(currentChapter)
                    mangas[mangaName]["latestChapterLink"] = MangaUrls[i]
                    mangas[mangaName]["latestRelease"] = MangaStats[i][2]
    except Exception as e:
        driver.quit()
    driver.quit()
    return mangas


def fetchFromMangaRead(mangas):
    asyncio.run(fetchMangaResponses(mangas))
    return mangas
