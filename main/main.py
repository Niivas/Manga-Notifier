import json
from datetime import datetime
from MangaJuice import fetchMangasInfo
from UpdatePdf import updatePdf


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
mangas = fetchMangasInfo(mangas)
# print(f"Time took for fetching updates of {len(mangas)} mangas: {tf - ti} seconds")
afterFetchMangaCount = len(mangas)

# Update the statistics file
updateStatsFile(beforeFetchMangaCount, afterFetchMangaCount)

# Sort the manga updates based on chapters added since last read
mangas = dict(sorted(mangas.items(), key=lambda item: float(item[1]['chaptersAddedSinceYouLastRead']), reverse=True))

# Write the updated manga information to the file
with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.txt', 'w') as file:
    file.write(json.dumps(mangas, indent=4))

updatePdf(mangas)
