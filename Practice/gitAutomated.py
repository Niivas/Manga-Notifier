import subprocess

msg = input('Type the commit message (+ ENTER):')


repo_directory = r'C:\Users\Nivas Reddy\Desktop\Manga-Notifier'

subprocess.run(["git", "add", "."], cwd=repo_directory)
# commit file
subprocess.run(["git", "commit", "-m", msg], cwd=repo_directory)
# push
subprocess.run(["git", "push"], cwd=repo_directory)
