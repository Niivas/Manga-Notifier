import json
from datetime import datetime
from manga_juice.MangaJuice import fetchMangasInfo
from utils.updatePdf import updatePdf


# Function to update the statistics file with relevant information
def updateStatsFile(prev, curr):
    favouriteMangaUpdatedInTheRecentFetch = 0
    totalFavoriteMangas = 0
    for manga in mangas:
        if mangas[manga]['isFavorite'] == 'yes':
            totalFavoriteMangas += 1

    content = {}
    curTimeAndDate = datetime.now().strftime("%H:%M %Y-%m-%d")
    content['Mangas last fetched time'] = curTimeAndDate
    content['Mangas Added in the recent Fetch'] = str(curr - prev)
    content['Total favorite mangas'] = str(totalFavoriteMangas)
    content['Current Total Mangas'] = str(curr)
    content['Additional Info'] = "Mangas whose chapters got released recently are marked in green colour in the pdf"

    with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\stats.txt', 'w') as statFile:
        statFile.write(json.dumps(content, indent=4))


# Load the previous manga updates from file
with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt',
          'r') as previousMangaUpdatesFile:
    mangas = json.loads(previousMangaUpdatesFile.read())

beforeFetchMangaCount = len(mangas)

# Fetch the latest manga updates
mangas = fetchMangasInfo(mangas)
# print(f"Time took for fetching updates of {len(mangas)} mangas: {tf - ti} seconds")
afterFetchMangaCount = len(mangas)

# Update the statistics file
updateStatsFile(beforeFetchMangaCount, afterFetchMangaCount)

# Sort the manga updates based on chapters added since last read


# Write the updated manga information to the file
with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt', 'w') as file:
    file.write(json.dumps(mangas, indent=4))

updatePdf(mangas)
