import subprocess
from datetime import datetime

commit_message = f'Last Fetched: {datetime.now().strftime("%H:%M %Y-%m-%d")}'

repo_directory = r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier'


subprocess.run(["git", "add", "*"], cwd=repo_directory)
# commit file
subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_directory)
# push
subprocess.run(["git", "push", "origin"], cwd=repo_directory)
