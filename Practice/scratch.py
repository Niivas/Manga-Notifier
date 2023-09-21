import os
import json

file = open(r'C:\Users\Nivas Reddy\Desktop\Manga-Notifier\results\Latest Manga Updates.txt', 'r')

d = json.loads(file.read())
print(type(d))