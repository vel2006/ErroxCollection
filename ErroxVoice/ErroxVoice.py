import platform
import sys
import os
errorIcon = "[!]"
infoIcon = "[#]"
miscIcon = "[*]"
try:
    import pyttsx3
except Exception:
    try:
        if platform.system() == "Windows":
            os.system('python -m pip install pyttsx3')
        elif platform.system() == "Linux":
            os.system("pip3 install pyttsx3")
    except Exception as error:
        print(f"{errorIcon} Well, you cant install one of the needed packages, here\'s the error:\n{error}")
#Setting up the packages and making sure they work
engine = pyttsx3.init()
#Getting the input text to speech text
match len(sys.argv):
    case 1:
        print(f"{infoIcon} No arguments given, using default setttings...")
        inputText = input("Type the wanted text to TTS\n>")
        inputSpeed = input("Type the speed you want the TTS to speed at, default is 200\n>")
        try:
            inputSpeed = int(inputSpeed)
        except Exception:
            print(f"{errorIcon} Input speed is not an int, setting to default 200")
            inputSpeed = 200
        inputGender = input("Type the gender of the voice [male, female, neutral]\n>")
        if inputGender != "male" and inputGender != "female" and inputGender != "neutral":
            print(f"{errorIcon} Input gender is unknown, using default neutral")
            inputGender = "neutral"
        print(f"{infoIcon} Writing TTS to file for filtering")
        engine.setProperty('rate', inputSpeed)
        engine.setProperty('gender', inputGender)
        engine.save_to_file(inputText, os.path.join(os.path.dirname(os.path.abspath(__file__)), "basicTTS.mp3"))
    case 2:
        print(f"{infoIcon} One argument given, checking arguments...")
        if sys.argv[1] == "help":
            print("ErroxVoice help page:")
            print("When prompted to input the text, input the text you with to be converted to TTS\nWhen prompted to input the gender, input one of the following [male, female, neutral]\nWhen prompted to input the speed, input a number above zero")
            exit()
engine.runAndWait()
