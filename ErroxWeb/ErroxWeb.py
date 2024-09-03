import requests
import sys
print(" _____                   __        __   _     ")
print("| ____|_ __ _ __ _____  _\\ \\      / /__| |__  ")
print("|  _| | '__| '__/ _ \\ \\/ /\\ \\ /\\ / / _ \\ '_ \\ ")
print("| |___| |  | | | (_) >  <  \\ V  V /  __/ |_) |")
print("|_____|_|  |_|  \\___/_/\_\  \\_/\\_/ \\___|_.__/")
print("\nProgramed by: That1EthicalHacker\nYoutube: @That1EthicalHacker\nGitHub: https://github.com/vel2006")
if sys.argv[1] == "-h":
    print("ERROX WEB Help page.\nErroxWeb.py works by scrapping for pages on a site passed. It only looks for publically avalable ones.")
    print("Argument 1:\n\tFile extention file, for the love of everything good in tech, have each one on their own line.")
    print("Argument 2:\n\tDirectory / File list, same thing, have them on their own lines.")
    print("Argument 3:\n\tTarget URL. (if an ip, format http:[ip]:[port] or https:[ip]:[port]) will default to port 80 / 443.")
    print("Example Usage:")
    print("\tWindows:")
    print("\t\tpython .\\ErroxSite.py extentionsFile.txt pagesFile.txt http://127.0.0.1:1234")
    print("\tLinux:")
    print("\t\tpython3 ErroxSite.py extentionsFile.txt pagesFile.txt http://127.0.0.1:1234")
    print("Contents of Files File:\n\tforum\n\tblog\n\tcourses")
    print("Contents of Extentions File:\n\t.php\n\t.phps\n\t.html\n\t.php7")
    print("Misc:\n\tErroxWeb.py will search for index.[extention] by default, don\'t have it in your list.\n\tErroxWeb.py DOES NOT EARCH FOR SUBDOMAINS! STOP ASKING!")
    exit()
if len(sys.argv) != 4:
    print("[!] Error: Incorrect amount of arguments!\n\tUse -h for help.")
    exit()
#Arrays that will be output
finalFiles = []
finalDirs = []
finalExt = []
#Getting the values that will be saved within the fileExtention and directories arrays
fileExtentions = []
fileDirectories = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        fileExtentions.append(line.strip())
    file.close()
with open(sys.argv[2], 'r') as file:
    for line in file:
        fileDirectories.append(line.strip())
    file.close()
#Seeing if the target is online
if (requests.get(sys.argv[3])).status_code == 200:
    print("[#] Target Online.")
    foundExtentions = []
    foundPages = []
    foundDirectories = []
    #Finding file extention of index page
    for ext in fileExtentions:
        if (requests.get(f"{sys.argv[3]}/index{ext}")).status_code == 200:
            foundExtentions.append(ext)
    if len(foundExtentions) != 0:
        print(f"[#] Found extention of index page: {str(foundExtentions)}")
        for dir in fileDirectories:
            for ext in fileExtentions:
                if (requests.get(f"{sys.argv[3]}/{dir}/{fileExtentions}")).status_code == 200:
                    if ext not in foundExtentions:
                        foundExtentions.append(ext)
                    foundPages.append(f"{dir}{ext}")
        for dir in fileDirectories:
            if (requests.get(f"{sys.argv[3]}/{dir}")).status_code == 200:
                foundDirectories.append(dir)
        print(f"[#] Searched directory: {'base'}")
        print(f"[*] Found directories: {foundDirectories}")
        print(f"[*] Found pages: {foundPages}")
        print(f"[*] Found extentions: {foundExtentions}")
        if len(foundDirectories) != 0:
            for dir in foundDirectories:
                disPages = []
                disDirs = []
                disExt = []
                if dir in finalDirs:
                    continue
                else:
                    for page in fileDirectories:
                        for ext in fileExtentions:
                            if (requests.get(f"{sys.argv[3]}/{dir}/{page}{ext}")).status_code == 200:
                                if ext not in disExt:
                                    disExt.append(ext)
                                if ext not in finalExt:
                                    finalExt.append(ext)
                                disPages.append(page)
                                finalFiles.append(f"{page}{ext}")
                    for page in fileDirectories:
                        if (requests.get(f"{sys.argv[3]}/{dir}/{page}")).status_code == 200:
                            disDirs.append(f"{dir}/{page}")
                            foundDirectories.append(f"{dir}/{page}")
                    finalDirs.append(dir)
                    print(f"[#] Searched Directory: {dir}")
                    print(f"[*] Found directories: {disDirs}")
                    print(f"[*] Found pages: {disPages}")
                    print(f"[*] Found extentions: {disExt}")
    else:
        print("[!] No extentions in file provided found!")
else:
    print("[!] Target Offline!")
