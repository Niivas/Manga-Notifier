# Manga-Notifier
A website to find all your favorite Mangas recently released chapters.
Features:
1. You can select your favorite mangas from a fixed list of mangas, and you'll get notified whenever the manga publishers release a new chapter.
2. You can directly go to the respective manga page through a link provided in the website.

The project aims to automate the process of tracking and updating manga information, including the latest chapters and links, for a list of mangakas (manga creators). It accomplishes this by scraping data from different manga websites. The script performs the following key tasks:

1. Data Collection: It collects data about the latest chapters, links, and other relevant information for a list of mangakas and their respective manga titles from the specified website.

2. Data Comparison: It compares the newly fetched data with the previously stored data to determine if there have been any updates since the last fetch.

3. Statistics Generation: It generates statistics about the updates, including the number of newly added manga titles, the number of favorite manga titles that have been updated, and the total number of favorite manga titles.

4. Data Sorting: It sorts the manga titles based on the chapters added since the last read, likely for presentation purposes.

5. Data Storage: It stores the updated manga information in JSON format in a local file named "Latest Manga Updates.txt."

6. PDF Generation: It updates a PDF file with the latest manga updates.

Successful Outcomes:
The project achieves several successful outcomes:

1. Automation: The project automates the process of manga information tracking, reducing the need for manual updates.

2. Data Accuracy: By scraping data directly from the website, it ensures that the information is up-to-date and accurate.

3. Statistics Generation: The script generates statistics about manga updates, providing valuable insights to users about the changes since the last fetch.

4. Data Sorting: Manga titles are sorted based on the chapters added since the last read, making it easier for users to prioritize their reading.

5. Data Storage: The script stores manga information in a structured JSON format, making it easily accessible and reusable.

6. PDF Update: The project successfully updates a PDF file, possibly a manga catalog or reading list, with the latest manga updates, ensuring users have an organized way to track their reading progress.

