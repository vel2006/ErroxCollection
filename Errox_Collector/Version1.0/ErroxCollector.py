import struct
import re
import time
import uncompyle6
import os
import exifread

#Getting the file's extention
def GetFileExtention(input_file):
    name, extention = os.path.splitext(input_file)
    return extention
#Scrubbing .pyc file data
def CollectPYCMetadata(pyc_file):
    print(f"[+] Extracting {pyc_file}\'s metadata")
    try:
        with open(f"{pyc_file}_metadata.txt", "w") as file:
            print(f"[*] Writing data to {pyc_file}.txt")
            with open(pyc_file, 'rb') as pyc:
                magicNumber = pyc.read(4)
                file.write(struct.unpack('<I', magicNumber)[0])
                timestampOrHash = pyc.read(4)
                file.write(struct.unpack('<I', timestampOrHash)[0])
                if timestampOrHash != 0:
                    file.write(time.ctime(timestampOrHash))
                else:
                    file.write("[!] No timestamp, likely a hash for creating the .pyc file")
                try:
                    sourceSize = pyc.read(4)
                    file.write(struct.unpack('<I', sourceSize)[0])
                except:
                    file.write("[!] Not avalable, too old .pyc file")
                filePath = pyc.read(4)
                file.write(struct.unpack('<I', filePath)[0])
    except:
        print(f"[!] {pyc_file}_metadata.txt could not be created, data not saved.\n[*] Printing not saved data instead.")
        with open(pyc_file, 'rb') as pyc:
            magicNumber = pyc.read(4)
            print(hex(struct.unpack('<I', magicNumber)[0]))
            timestampOrHash = pyc.read(4)
            print(struct.unpack('<I', timestampOrHash)[0])
            if timestampOrHash != 0:
                print(time.ctime(timestampOrHash))
            else:
                print("[!] No timestamp, likely a hash for creating the .pyc file")
            try:
                sourceSize = pyc.read(4)
                print(struct.unpack('<I', sourceSize)[0])
            except:
                print("[!] Not avalable, too old .pyc file")
            filePath = pyc.read(4)
            print(struct.unpack('<I', filePath)[0])
#Decompiling .pyc files
def DecompilePYCFile(pyc_file):
    print(f"[+] Decompiling {pyc_file} into {pyc_file}.py")
    with open(f"{pyc_file}.py", 'w') as output:
        uncompyle6.decompile_file(pyc_file, output)
#Extracting information from a file
def EmailAndDatabaseInformation(input_file):
    print(f"[+] Extracing emails and database information from {input_file}")
    emailPatterns = [
        re.compile(r'[^\s]+@gmail.com', re.IGNORECASE),
        re.compile(r'[^\s]+@hotmail.com', re.IGNORECASE),
        re.compile(r'[^\s]+@protonmail.com', re.IGNORECASE),
        re.compile(r'[^\s]+@outlook.com', re.IGNORECASE),
        re.compile(r'[^\s]+@yahoo.com', re.IGNORECASE),
        re.compile(r'[^\s]+@myyahoo.com', re.IGNORECASE),
        re.compile(r'[^\s]+@tutanota.com', re.IGNORECASE),
        re.compile(r'[^\s]+@tutanota.de', re.IGNORECASE),
        re.compile(r'[^\s]+@tutamail.com', re.IGNORECASE),
        re.compile(r'[^\s]+@tuta.io', re.IGNORECASE),
        re.compile(r'[^\s]+@keemail.me', re.IGNORECASE),
        re.compile(r'[^\s]+@icloud.com', re.IGNORECASE),
        re.compile(r'[^\s]+@yandex.com', re.IGNORECASE),
        re.compile(r'[^\s]+@aol.com', re.IGNORECASE),
        re.compile(r'[^\s]+@aim.com', re.IGNORECASE),
        re.compile(r'[^\s]+@zohomail.com', re.IGNORECASE)
    ]
    databasePatterns = [
        re.compile(r'jdbc:[^\s]+', re.IGNORECASE),
        re.compile(r'mysql://[^\s]+', re.IGNORECASE),
        re.compile(r'postgres://[^\s]+', re.IGNORECASE),
        re.compile(r'sqlite://[^\s]+', re.IGNORECASE),
        re.compile(r'mongodb://[^\s]+', re.IGNORECASE)
    ]
    try:
        with open(f"{input_file}_data.txt", "w") as file:
            with open(input_file, 'r') as innerFile:
                content = innerFile.read()
                emailMatches = []
                databaseMatches = []
                file.write("Emails:\n")
                for pattern in emailPatterns:
                    emailMatches.append(f"\t{pattern.findall(content)}")
                file.write("emailMatches\n")
                file.write("Databases:\n")
                for pattern in databasePatterns:
                    databaseMatches.append(pattern.findall(content))
                file.write("databaseMatches\n")
            innerFile.close()
        file.close()
    except:
            print(f"[!] {input_file}_data.txt could not be created, data not saved.\n[*] Printing not saved data instead.")
            with open(input_file, 'r') as file:
                content = file.read()
                emailMatches = []
                databaseMatches = []
                for pattern in emailPatterns:
                    emailMatches.extend(pattern.findall(content))
                print(emailMatches)
                for pattern in databasePatterns:
                    databaseMatches.extend(pattern.findall(content))
                print(databaseMatches)
def CollectImageMetadata(input_file):
    try:
        with open(f"{input_file}_metadata.txt", "w") as file:
            with open(input_file, "rb") as innerFile:
                tags = exifread.process_file(innerFile)
            with open("metadata.txt", "w") as file:
                for tag in tags.keys():
                    file.write(f"{tag}: {tags[tag]}\n")
    except:
        with open(input_file, "rb") as file:
            tags = exifread.process_file(file)
        tagsList = [
            "Image Orientation",
            "Image Make",
            "Image Model",
            "Image XResolution",
            "Image YResolution",
            "Image ResolutionUnit",
            "Image YCbCrPositioning",
            "Image DateTime",
            "Image ExifOffset",
            "Thumbnail",
            "EXIF Flash"
        ]
        for tag in tags:
            if tag in tagsList:
                print(f"{tag}: {tags[tag]}")
#Main method that handles the logic of the user's input and what to run
def main():
    print(" _____                     ____      _ _           _")
    print("| ____|_ __ _ __ _____  __/ ___|___ | | | ___  ___| |_ ___  _ __")
    print("|  _| | '__| '__/ _ \\ \\/ / |   / _ \\| | |/ _ \\/ __| __/ _ \\| '__|")
    print("| |___| |  | | | (_) >  <| |__| (_) | | |  __/ (__| || (_) | |")
    print("|_____|_|  |_|  \___/_/\_\\\\____\\___/|_|_|\\___|\\___|\\__\\___/|_|")
    print("A script by That1EthicalHacker")
    print("\t- Dont be stupid and stay out of jail.")
    while True:
        print("")
        print("[+]Select mode:")
        print("Data collection:")
        print("\t[\"collect data\"] Collect Possible Email Accounts and Databases In File")
        print("-----------------")
        print(".pyc files:")
        print("\t[\"pyc decompile\"] Decompile A .pyc File")
        print("\t[\"pyc data\"] Get .pyc File\'s metadata")
        print("-----------------")
        print("Images:")
        print("\t[\"img data\"] Get an image file\'s metadata")
        print("-----------------")
        print("[\"help\"] Show A Help Page")
        print("[\"close\"] Close This Script")
        choice = str(input("> "))
        match choice:
            case "collect data":
                print("[+] Input File Name (must be in same directory as this script or full path)")
                file = str(input("> "))
                print("Extracted Email accounts and Databases:")
                EmailAndDatabaseInformation(file)
            case "pyc decompile":
                print("[+] Input File Name (must be in same directory as this script or full path)")
                file = str(input("> "))
                if GetFileExtention(file) == ".pyc":
                    DecompilePYCFile(file)
                else:
                    print("[!] Input file does not have the .pyc file extention")
            case "pyc data":
                print("[+] Input File Name (must be in same directory as this script or full path)")
                file = str(input("> "))
                if GetFileExtention(file) == ".pyc":
                    print(CollectPYCMetadata(file))
                else:
                    print("[!] Input file does not have the .pyc file extention")
            case "img data":
                print("[+] Input File Name (mus be in same directory as this script or full path)")
                file = str(input("> "))
                if GetFileExtention(file) == ".jpg" or GetFileExtention(file) == ".png":
                    CollectImageMetadata(file)
                else:
                    print("[!] Input file does not have an accepted image extention")
            case "help":
                print("[+] Help Page:\n")
                print("-----------------")
                print("[=] Any and all methods will try to create a {input_file}_{type_of_method}.{type_of_method} file using \"os\" that holds more detail than if it didnt\n")
                print("[*] Data Collection:")
                print("\t[~] Takes In: a not compiled clear text file")
                print("\t[`] Does: Extracts any mentions of an email and or database in the input file using \"re\" and created a _data.txt")
                print("[*] Pyc Decompile:")
                print("\t[~] Takes In: a compiled Python file into a .pyc. Only works with 3.0.0 and older Python bytecode versions")
                print("\t[`] Does: Decompiles the input .pyc file using \"uncompyle6\" and creates a _.py")
                print("[*]Pyc Data:")
                print("\t[~] Takes In: a compiled Python file into a .pyc. Only works with 3.0.0 and older Python bytecode versions")
                print("\t[`] Does: Extracts the metadata of the input .pyc file using \"struct\" and \"time\" and creates a _metadata.txt")
                print("[*]Image Metadata:")
                print("\t[~] Takes In:")
                print("\t[`] Does: Extracts the metadata of the input image file using \"exifread\" and created a _metadata.txt")
                time.sleep(2)
            case "close":
                print("[+] User selected 4.\nClosing script...")
                time.sleep(2)
                break
    print("[+] Thank you for using ErroxCollector.\nDeveloped by That1EthicalHacker.\n\tgithub: vel2006\n\tYoutube: @That1EthicalHacker")
#Calling main function
main()
