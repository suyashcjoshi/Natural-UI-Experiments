import speech_recognition as sr
import pyttsx3
import pyautogui
import webbrowser as web


recognizer = sr.Recognizer()

def GuiControl(string):
  print(string)
  web.open('https://' + string, new = 2)

def Speak(command):
  engine = pyttsx3.init()
  engine.say(command)
  engine.runAwait()

def getMicInput():
  with sr.Microphone() as mic:
    recognizer.adjust_for_ambient_noise(mic, duration = 0.1)


    inputAudio = recognizer.listen(mic)

    try:

      recognized_text = recognizer.recognize_google(inputAudio)
      recognized_text = recognized_text.lower()

    except Exception as e:
      print("Error: " + str(e))
    GuiControl(recognized_text)

def main():
  getMicInput()

if __name__ == '__main__':
  main()