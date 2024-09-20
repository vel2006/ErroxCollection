#Welcome art stuffs
print(" _____                   __        __   _     ")
print("| ____|_ __ _ __ _____  _\\ \\      / /__| |__  ")
print("|  _| | '__| '__/ _ \\ \\/ /\\ \\ /\\ / / _ \\ '_ \\ ")
print("| |___| |  | | | (_) >  <  \\ V  V /  __/ |_) |")
print("|_____|_|  |_|  \\___/_/\_\  \\_/\\_/ \\___|_.__/")
print("Version: 2.0")
print("\nProgramed by: That1EthicalHacker\nYoutube: @That1EthicalHacker\nGitHub: https://github.com/vel2006")
import sys
import requests
import threading
import os
import time
import platform
import re
#Headers to print statements, just makes it easier on me to not remember which is which
info = "[#]"
error = "[!]"
other = "[*]"
#Checking for the required pages and stuffs
if len(sys.argv) < 1:
    print(f"{error} ERROR: First argument has to be given!")
    exit()
if sys.argv[1] == "-h":
    print("ErroxWeb help page:")
    print("Little note:\n\tErroxWeb2 does not support the format of '-h' outside of this command. Treat it as you would a method.\n\tErroxWeb2 will also save the return status and found pages inside of a file within this directory, so please let it have access.")
    print("Options:")
    print("\tArgument 1 | -h for help page or website link")
    print("\tArgument 2 | file list for page search")
    print("\tArgument 3 | file extention list for page search")
    print("\tArgument 4 | directory list for directory search")
    print("\tArgument 5 | subdomain list for subdomain search")
    print("\tArgument 6 | intager for time to sleep before spawning new thread")
    print("Examples:")
    print("Windows:")
    print("\tpython ErroxWebV2.py http://site.site path\\to\\file\\list path\\to\\extention\\list path\\to\\directory\\list path\\to\\subdomain\\list 10")
    print("\tpython ErroxWebV2.py http://site.site path\\to\\file\\list path\\to\\extention\\list None path\\to\\subdomain\\list 10")
    print("\tpython ErroxWebV2.py http://site.site path\\to\\file\\list path\\to\\extention\\list path\\to\\directory\\list None 10")
    print("\tpython ErroxWebV2.py http://site.site path\\to\\file\\list path\\to\\extention\\list path\\to\\directory\\list path\\to\\subdomain\\list None")
    print("\tpython ErroxWebV2.py http://site.site path\\to\\file\\list path\\to\\extention\\list None None 10")
    print("\tpython ErroxWebV2.py http://site.site path\\to\\file\\list path\\to\\extention\\list None None None")
    print("\tpython ErroxWebV2.py -h")
    print("Linux:")
    print("\tpython3 ErroxWebV2.py http://site.site path/to/file/list path/to/extention/list path/to/directory/list path/to/subdomain/list 10")
    print("\tpython3 ErroxWebV2.py http://site.site path/to/file/list path/to/extention/list None path/to/subdomain/list 10")
    print("\tpython3 ErroxWebV2.py http://site.site path/to/file/list path/to/extention/list path/to/directory/list None 10")
    print("\tpython3 ErroxWebV2.py http://site.site path/to/file/list path/to/extention/list path/to/directory/list path/to/subdomain/list None")
    print("\tpython3 ErroxWebV2.py http://site.site path/to/file/list path/to/extention/list None None 10")
    print("\tpython3 ErroxWebV2.py http://site.site path/to/file/list path/to/extention/list")
    print("\tpython3 ErroxWebV2.py -h")
    exit()
pageList = []
extentionList = []
directoryList = []
subdomainList = []
foundPagesList = []
statusCodePattern = re.compile(r' | +[^\s]', re.IGNORECASE)
pagePattern = re.compile(r'[^\s]+ | ', re.IGNORECASE)
timeoutLength = 0
outputFile = ""
if platform.system() == "Windows":
    outputFile = os.path.join(os.getcwd() + "\\ErroxSiteV2OutputFile.txt")
else:
    outputFile = os.path.join(os.getcwd() + "/ErroxSiteV2OutputFile.txt")
with open(outputFile, "w") as file:
    pass
if len(sys.argv) >= 3:
    if os.path.isfile(sys.argv[2]) and os.path.isfile(sys.argv[3]):
        print(f"{info} Reading: {sys.argv[2]} for page list")
        with open(sys.argv[2], "r") as file:
            for line in file:
                pageList.append(line.strip())
            file.close()
        print(f"{info} Reading: {sys.argv[3]} for extention list")
        with open(sys.argv[3], "r") as file:
            for line in file:
                extentionList.append(line.strip())
            file.close()
else:
    print(f"{error} ERROR: Second and Third arguments have to be given and be files!\nUse -h as first argument to see help page.")
    exit()
try:
    if os.path.isfile(sys.argv[4]):
        print(f"{info} Reading {sys.argv[4]} for directory list")
        with open(sys.argv[4], "r") as file:
            for line in file:
                directoryList.append(line.strip())
            file.close()
except Exception:
    print(f"{info} Skipping directory due to no file input or input isnt file\n")
try:
    if os.path.isfile(sys.argv[5]):
        print(f"{info} Reading {sys.argv[5]} for subdomain list")
        with open(sys.argv[5], "r") as file:
            for line in file:
                subdomainList.append(line.strip())
except Exception:
    print(f"{info} Skipping subdomain due to no file input or input isnt file")
try:
        int(sys.argv[6])
        print(f"{info} Timeout length set to {sys.argv[6]}")
        timeoutLength = float(sys.argv[6])
except Exception as error:
        print(f"{info} Skipping timeout due to input is not int\nUse -h as first argument to see help page.")
#For scanning a file and its extention
def PageExists(targetPage, pageExtentions, outputFile, sleepyTime):
    if type(pageExtentions) == list:
        if sleepyTime == 0:
            for extention in pageExtentions:
                response = requests.get(f"{targetPage}{extention}")
                if response.status_code == 200 or response.status_code == 403:
                    with open(outputFile, "a") as file:
                        file.write(f"{targetPage}{extention} | {response.status_code}\n")
                        file.close()
        else:
            for extention in pageExtentions:
                response = requests.get(f"{targetPage}{extention}")
                if response.status_code == 200 or response.status_code == 403:
                    with open(outputFile, "a") as file:
                        file.write(f"{targetPage}{extention} | {response.status_code}\n")
                        file.close()
                    time.sleep(sleepyTime)
    else:
        response = requests.get(targetPage)
        if response.status_code == 200 or response.status_code == 403:
            with open(outputFile, "a") as file:
                file.write(f"{targetPage} | {response.status_code}\n")
                file.close()
            return True
        else:
            return False
#For scanning a directory list
def DiveIntoDirecory(targetDirectory, directoryList, fileList, extentionList, outputFile, sleepTime):
    localThreads = []
    if PageExists(targetDirectory, None, outputFile):
        if sleepTime == 0:
            for directory in directoryList:
                localThreads.append(threading.Thread(target=DiveIntoDirecory, args=(f"{targetDirectory}/{directory}", directoryList, fileList, extentionList, outputFile, None)))
            for file in fileList:
                localThreads.append(threading.Thread(target=PageExists, args=(file, extentionList, outputFile)))
            amountOfThreads = len(localThreads) - 1
            while amountOfThreads >= 0:
                localThreads[amountOfThreads].join()
                amountOfThreads -= 1
        else:
            for directory in directoryList:
                localThreads.append(threading.Thread(target=DiveIntoDirecory, args=(f"{targetDirectory}/{directory}", directoryList, fileList, extentionList, outputFile, sleepTime)))
                time.sleep(sleepTime)
            for file in fileList:
                localThreads.append(threading.Thread(target=PageExists, args=(file, extentionList, outputFile)))
                time.sleep(sleepTime)
            amountOfThreads = len(localThreads) - 1
            while amountOfThreads >= 0:
                localThreads[amountOfThreads].join()
                amountOfThreads -= 1
#For scanning a subdomain
def DiveIntoSubDomain(targetSite, directoryList, fileList, extentionList, outputFile, sleepTime):
    localThreads = []
    for directory in directoryList:
        localThreads.append(threading.Thread(target=DiveIntoDirecory, args=(f"{targetSite}/{directory}/", fileList, extentionList, outputFile, sleepTime)))
    for page in fileList:
        localThreads.append(threading.Thread(target=PageExists, args=(f"{targetSite}/{page}", extentionList)))
    amountOfThreads = len(localThreads) - 1
    while amountOfThreads >= 0:
        localThreads[amountOfThreads].join()
        amountOfThreads -= 1
#Main Logic of the script
if len(subdomainList) >= 0:
    mainThreads = []
    for domain in subdomainList:
        mainThreads.append(threading.Thread(target=DiveIntoSubDomain, args=(sys.argv[1], directoryList, pageList, extentionList, outputFile, timeoutLength)))
if len(directoryList) >= 0:
    for directory in directoryList:
        mainThreads.append(threading.Thread(target=DiveIntoDirecory, args=(f"{sys.argv[1]}/{directory}/", directoryList, pageList, extentionList, outputFile, timeoutLength)))
for page in pageList:
    mainThreads.append(threading.Thread(target=PageExists, args=(f"{sys.argv[1]}/{page}", extentionList, outputFile)))
amountOfMainThreads = len(mainThreads) - 1
while amountOfMainThreads >= 0:
    mainThreads[amountOfMainThreads].join()
    amountOfMainThreads -= 1
with open(outputFile, "r") as file:
    for line in file:
        print(f"Found page: {pagePattern.findall(line.strip())} | Returned Status: {statusCodePattern.findall(line.strip())}")
