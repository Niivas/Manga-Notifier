import json

with open(r'/results/Latest Manga Updates.txt', 'r') as file:
    mangas = json.loads(file.read())
"""
for manga in mangas:
    isFavorite = input(f"is {manga} your favorite (yes/no): ")
    mangas[manga]["isFavorite"] = isFavorite

def parseName(name):
    if "\u2019" in name:
        return name.split("\u2019")[0]
    if "'" in name:
        return name.split("'")[0]
    return name


for manga in mangas:
    searchPage = requests.get(searchUrl(parseName(manga)))
    soup = LexborHTMLParser(searchPage.text)
    if soup.css_first('div.not-found-content'):
        mangas[manga]["image"] = ""
        print(f"Could not find {manga}")
        continue
    mangas[manga]['image'] = soup.css('div.search-wrap')[0].css_first('img').attrs.get('data-src')
    print(f"Found {manga}")

for manga in mangas:
    mangas[manga]["mangaJuiceSan"] = mangas[manga]["siteAcceptedName"]
    del mangas[manga]["siteAcceptedName"]
"""
# with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt', 'w') as file:
#    file.write(json.dumps(mangas, indent=4))
"""
ti = time.time()
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
    for url, stats in zip(MangaUrls, MangaStats):
        print(url, stats)

except Exception as e:
    print("Could not load page")
    driver.quit()
tf = time.time()
print(f"Time took: {tf - ti} seconds")
"""
