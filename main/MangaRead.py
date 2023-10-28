from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys


# PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome()
mainUrl = "https://www.mangaread.org/"
mangaPage = "https://www.mangaread.org/manga/"
mangaSearchPage = lambda manga: f"https://www.mangaread.org/?s={manga}&post_type=wp-manga"
updatesPage = "https://www.mangaread.org/manga/?m_orderby=latest"

driver.get(mainUrl)
print(driver.title)
