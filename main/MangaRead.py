import json
import requests
from selectolax.lexbor import LexborHTMLParser
from utils import cosine_similarity

# import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt',
          'r') as previousMangaUpdatesFile:
    mangas = json.loads(previousMangaUpdatesFile.read())

# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome()
mainUrl = "https://www.mangaread.org/"
mangaPageUrl = "https://www.mangaread.org/manga/"
mangaSearchPage = lambda mangaTitle: f"https://www.mangaread.org/?s={mangaTitle}&post_type=wp-manga"
updatesPage = "https://www.mangaread.org/"


def parseUrl(url):
    return url.split("/")[-2]


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
    driver.get(updatesPage)
    titles = driver.find_elements_by_class_name("post-title")


with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt', 'w') as file:
    file.write(json.dumps(mangas, indent=4))
