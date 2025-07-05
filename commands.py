import pyperclip
import pyautogui
from time import sleep
from PIL import Image
import os
import webbrowser

from core.registry import CommandRegistry , VoiceCommand

@CommandRegistry.register    
class TypeCommand(VoiceCommand):
    def match(self,text) -> bool:
        return text.lower().strip().startswith("type")

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        new_sentence = text.partition("type")[2].strip()
        if new_sentence:
            tts.speak(f"typing {new_sentence} ...")
            pyperclip.copy(f"{new_sentence}")
            pyautogui.hotkey('ctrl','v')
        else:
            tts.speak(f"Please say something to type!")

        return "OK"
    
@CommandRegistry.register    
class SearchForCommand(VoiceCommand):
    def match(self,text) -> bool:
        return text.lower().strip().startswith("search for")

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        new_sentence = text.partition("search for")[2].strip()
        if new_sentence:
            tts.speak(f"searching for {new_sentence} ...")
            pyperclip.copy(f"{new_sentence}")
            webbrowser.open("https://www.google.com")
            sleep(1)
            pyautogui.hotkey('ctrl','v')
            pyautogui.press('Enter')  
        else:
            tts.speak(f"Please say something to search for!")

        return "OK"

    
@CommandRegistry.register    
class OpenYoutubeCommand(VoiceCommand):
    def match(self,text) -> bool:

        return text.lower().strip().startswith("open youtube") or (text.lower().strip().startswith("open you tube"))

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak(f"openning YouTube ...")
        webbrowser.open("https://www.youtube.com/")
        return "OK"
        
@CommandRegistry.register    
class WelcomeCommand(VoiceCommand):
    def match(self,text) -> bool:
        return text.strip().lower() in ("hi" , "hey" , "hello" , "welcome" , "good morning")

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Welcome, How can I help you today ?")
        return "OK"
        
@CommandRegistry.register    
class ExitCommand(VoiceCommand):
    def match(self,text) -> bool:
        return text.strip().lower() in ("exit" , "exit program" , "bye" , "close program")

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Exiting program, Bye.....")
        return "exit"
@CommandRegistry.register
class OpenNotepadCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if text == "open notepad":
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Opening notepad")
        pyperclip.copy("notepad")
        pyautogui.hotkey('win','r')
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('Enter')
        sleep(1)
        pyautogui.hotkey('ctrl','n')
        
        return "OK"
@CommandRegistry.register
class TakeScreenshotCommand(VoiceCommand):
    def match(self,text) -> bool:
        return text.strip().lower() in ("take screenshot", "take a screenshot")

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Taking a screenshot...")
        screenshot=pyautogui.screenshot()
        screenshot.save('screenshot.png')
        
        return "OK"
    
@CommandRegistry.register
class OpenCalculatorCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "open calculator"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Opening calculator...")
        pyperclip.copy("calc")
        pyautogui.hotkey('win','r')
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('Enter')
        
        return "OK"
@CommandRegistry.register
class ShowImageCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "show image"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Showing Image...")
        image_path = "image.jpg"
        if not os.path.exists(image_path):
            msg = f"Image file {image_path} not found."
            print(msg)
            tts.speak(msg)
            return
        try:
            img = Image.open(image_path)
            img.show()
        except Exception as e:
            print(f"Showing image failed with error: {e}")
            tts.speak(f"Showing image failed with error: {e}")
        
        return "OK"
    
@CommandRegistry.register
class CopyCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "copy text"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Copying the predefined text...")
        pyperclip.copy("This text was predefined by python voice assitant program")
        
        return "OK"
    
@CommandRegistry.register
class PasteCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "paste clipboard"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("pasting from the clipboard...")
        pyautogui.hotkey('ctrl','v')
        
        return "OK"
    
@CommandRegistry.register
class ReadClipboardCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "read clipboard"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        clipboard_content=pyperclip.paste()
        tts.speak("Reading from the clipboard...")
        tts.speak(f"The text at the clipboard is: {clipboard_content}")
        
        return "OK"
    
@CommandRegistry.register
class CloseWindowCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "close window"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Are you sure you want to exit the active window? Please say yes or no.")
        while True:
            confirmation = recognizer.listen_for_command()
            if 'yes' in confirmation:
                tts.speak("Closing the active window...")
                pyautogui.hotkey('alt', 'f4')
                break
            elif 'no' in confirmation:
                tts.speak("Aborting closure...")
                break
            elif confirmation:
                tts.speak("Please say yes or no.")
        
        return "OK"
    
@CommandRegistry.register
class MinimizeAllCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "minimize all windows"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("minimizing window...")
        pyautogui.hotkey('win','d')   
        
        return "OK"
    
@CommandRegistry.register
class MaximizeWindowCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "maximize window"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("maximizing window...")
        pyautogui.hotkey('win','up')    
        
        return "OK"
    
@CommandRegistry.register
class SwitchWindowCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "switch window"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Switching window...")
        pyautogui.hotkey('alt','tab')    
        
        return "OK"
    
@CommandRegistry.register
class OpenBrowserCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if (text.lower() == "open browser"):
            retval = True
        return retval

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Opening browser...")
        webbrowser.open("https://www.google.com")  
        
        return "OK"
    