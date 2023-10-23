import json

with open(r'C:\Users\Nivas Reddy\Desktop\Manga-Notifier\results\Latest Manga Updates.txt', 'r') as file:
    mangas = json.loads(file.read())

for manga in mangas:
    isFavorite = input(f"is {manga} your favorite (yes/no): ")
    mangas[manga]["isFavorite"] = isFavorite

with open(r'C:\Users\Nivas Reddy\Desktop\Manga-Notifier\results\Latest Manga Updates.txt', 'w') as file:
    file.write(json.dumps(mangas, indent=4))
