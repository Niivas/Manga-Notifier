import requests
from selectolax.lexbor import LexborHTMLParser


# Base URLs for manga information
MangaJuiceBaseUrl = "https://mangajuice.com/manga/"
MangaJuiceUpdatesUrl = "https://mangajuice.com/updates/"


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
        try:
            print(f"Updated {manga}")
            chapter, link, latestRelease = getLatestChapterAndLink(mangaName)
            previousChapter = float(mangaka[manga]['latestChapter'])
            mangas[manga]["latestChapter"] = str(chapter) if chapter != 0 else previousChapter
            mangas[manga]["latestChapterLink"] = link if link != "" else mangas[manga]["latestChapterLink"]
            mangas[manga]["chaptersAddedSinceYouLastRead"] = str(chapter - previousChapter) if chapter != 0 else 0
            mangas[manga]["latestRelease"] = latestRelease
        except KeyError:
            print(f"Could not update {manga}")
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
            mangaka[mangaTitle] = dict()
            mangaka[mangaTitle]['mangaJuiceSan'] = name
            mangaka[mangaTitle]['latestChapter'] = str(currentChapter)
            mangaka[mangaTitle]['latestChapterLink'] = latestChapterUrls[1].attrs.get('href', "")
            mangaka[mangaTitle]['chaptersAddedSinceYouLastRead'] = "1"
            mangaka[mangaTitle]['isFavorite'] = 'no'
            mangaka[mangaTitle]['latestRelease'] = node.css_first('span').text()
    return mangaka