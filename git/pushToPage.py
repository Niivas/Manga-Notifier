import subprocess
from datetime import datetime


def push():
    """
    Pushes the changes to a Git repository.

    :return: None
    """
    commit_message = f'Last Fetched: {datetime.now().strftime("%H:%M %Y-%m-%d")}'
    repo_directory = r'C:\Users\Nivas Reddy\Desktop\Manga-Notifier.github.io'

    subprocess.run(["git", "pull"], cwd=repo_directory)
    subprocess.run(["git", "add", "*"], cwd=repo_directory)
    # commit file
    subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_directory)
    # push
    subprocess.run(["git", "push"], cwd=repo_directory)
