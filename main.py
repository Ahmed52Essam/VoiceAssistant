import sounddevice as sd
import queue
import json
from vosk import Model , KaldiRecognizer
import pyttsx3
import pyautogui
import pyperclip
from time import sleep
from PIL import Image
import webbrowser
import os
from abc import ABC, abstractmethod
from typing import Optional


class TextToSpeech():
    """
    -   The Class objects will have 1 objective : ➡️ Manage all Text-to-Speech behavior.
        
        -   Initialize a pyttsx3 engine

        -   Set properties (like rate and voice)

        -   Speak any given text

        -   So your object’s job is:

        ➡️ "Manage all Text-to-Speech behavior."
    """

    def __init__(self, cp_rate = 150, cp_voice_index = 0):
        # initialize pyttsx3 and set properties
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate',cp_rate)
        self.voices=self.engine.getProperty('voices')
        # if cp_voice_index >= len(self.voices):
        #     raise ValueError("Invalid voice index")
        # else:
        self.engine.setProperty('voice',self.voices[cp_voice_index].id)

    def speak(self, text):
        # speak the given text
        print(f"Assistant: {text}")
        self.engine.say(f"{text}")
        self.engine.runAndWait()


class SpeechRecognizer():
    """
    -   It loads the Vosk model.

    -   Sets up the microphone stream.

    -   Feeds audio to a queue (BuffQ).

    -   Processes that audio using KaldiRecognizer.

    ➡️ So the object’s job is:

    "Handle microphone input and convert speech to text using Vosk."
    """

    def __init__(self,cp_model_path,cp_sample_rate,cp_device=None):
        self.model= Model(cp_model_path)
        self.device=cp_device
        self.sample_rate=cp_sample_rate
        self.block_size=8000
        self.queue=queue.Queue()
        self.recognizer=KaldiRecognizer(self.model,self.sample_rate)

    def _fill_buffer(self,cp_indata,cp_frames ,cp_time, cp_status):
        self.queue.put(bytes(cp_indata))        

    def listen_for_command(self):
        # Open the mic
        with sd.RawInputStream(samplerate=self.sample_rate , blocksize=self.block_size,
                                device=self.device,dtype='int16',
                                channels=1,callback=self._fill_buffer   
                                ):    
            print("Listening ....")
            # Wait for the user to speak
            while True:
                #  Recognize and return the spoken text command   
                data=self.queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result=json.loads(self.recognizer.Result())
                    text=result['text'].lower()
                    if text:
                        print(f"User: {text}")
                        return text
                    
class CommandProcessor():
    """
    CommandProcessor manages the interpretation and execution of user voice commands.

    It receives recognized text commands, determines the appropriate action,
    and interacts with system utilities (like Notepad, Calculator, Clipboard, Screenshot, etc.)
    through automation libraries. It also provides spoken feedback using the TextToSpeech object.

    Responsibilities:
    - Map recognized commands to specific system actions.
    - Provide user feedback via text-to-speech.
    - Handle unknown or unsupported commands gracefully.
    - Coordinate with SpeechRecognizer for confirmation when needed (e.g., closing windows).
    """
    def __init__(self,cp_tts_object,cp_speech_rec_obj):
        self.tts=cp_tts_object
        self.recognizer=cp_speech_rec_obj

        self.pattern_commands= CommandRegistry.get_registry() #UnknownCommand is Last because it is a "Fallback Mechanism" 


    def handle_command(self, text):
        # # First, check fixed command mappings
        # if text in self.commands:
        #     self.commands[text]()
        #     if text in ['exit', 'exit program', 'bye', 'close program']:
        #         return "exit"
        #     return
        # Next, check dynamic pattern commands
        for command in self.pattern_commands:
            if command.match(text):
                result = command.execute(text,self.tts,self.recognizer) 
                if result == "exit":
                    return "exit"
                return
            
        # # If no match found            
        # self._unknown_command()

class CommandRegistry():
    _registry=[]

    @staticmethod
    def register(cls):
        CommandRegistry._registry.append(cls)
        return cls

    @staticmethod
    def get_registry():
        return [cls() for cls in (CommandRegistry._registry)] + [UnknownCommand()]

class VoiceCommand(ABC):
    """Base Class that every dynamic command will inherit from."""
    @abstractmethod
    def match(self, text: str) -> bool:
        """Returns True if this command should handle the text."""
        pass
    
    @abstractmethod
    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
        """Excutes the command logic."""
        pass
@CommandRegistry.register    
class TypeCommand(VoiceCommand):
    def match(self,text) -> bool:
        return text.lower().strip().startswith("type")

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
        tts.speak(f"openning YouTube ...")
        webbrowser.open("https://www.youtube.com/")
        return "OK"
        
@CommandRegistry.register    
class WelcomeCommand(VoiceCommand):
    def match(self,text) -> bool:
        return text.strip().lower() in ("hi" , "hey" , "hello" , "welcome" , "good morning")

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
        tts.speak("Welcome, How can I help you today ?")
        return "OK"
        
@CommandRegistry.register    
class ExitCommand(VoiceCommand):
    def match(self,text) -> bool:
        return text.strip().lower() in ("exit" , "exit program" , "bye" , "close program")

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
        tts.speak("Exiting program, Bye.....")
        return "exit"
@CommandRegistry.register
class OpenNotepadCommand(VoiceCommand):
    def match(self,text) -> bool:
        retval = False
        if text == "open notepad":
            retval = True
        return retval

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
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

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
        tts.speak("Opening browser...")
        webbrowser.open("https://www.google.com")  
        
        return "OK"
    
# This class is not added to CommandRegistry as it should be fallback funcion and will be last in the _registry list, it will be appended manually
class UnknownCommand(VoiceCommand):
    """
    This class will always match if no other classes are matched.
    ***    This IS MANDATED TO BE LAST CLASS TO ENHIRIT FROM THE VOICE COMMAND CLASS   ***
    This handled through the CommandRegistry class
    """
    
    def match(self,text) -> bool:
        return True

    def execute(self, text: str, tts: TextToSpeech, recognizer: SpeechRecognizer) ->str:
        tts.speak("Sorry, I Can't recognize this command. Can you try again ?")
        return "OK"
    
class VoiceAssistant():
    """
    VoiceAssistant is the main controller class that integrates speech recognition,
    command processing, and text-to-speech functionalities to create an interactive
    voice-controlled assistant.

    Responsibilities:
    - Initialize and coordinate the TextToSpeech, SpeechRecognizer, and CommandProcessor components.
    - Continuously listen for user voice commands.
    - Interpret and execute commands through the CommandProcessor.
    - Provide spoken feedback and handle program exit gracefully.

    Usage:
    - Instantiate the class and call the run() method to start the assistant loop.
    """
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "vosk-model-small-en-us-0.15")
        self.tts= TextToSpeech(cp_rate=130, cp_voice_index=0)
        self.recognizer=SpeechRecognizer(cp_model_path=model_path,cp_sample_rate=16000,cp_device=None)
        self.commandProcessor=CommandProcessor(self.tts,self.recognizer)

    def run(self):
        self.tts.speak("Voice Assistant is now running. Please say a command.")
        while True:
            text = self.recognizer.listen_for_command()
            result=self.commandProcessor.handle_command(text)
            if result == "exit":
                break


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()

