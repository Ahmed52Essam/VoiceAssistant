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

    def handle_command(self, text):
        if text in ['exit', 'exit program', 'bye', 'close program']:
            self._exit()
            return "exit"
        elif text in ['hello', 'hi', 'hey', 'welcome','goodmorning']:
            self._welcome()
        elif text == "open notepad":
            self._open_notepad()
        elif text == "take screenshot" or (text == "take a screenshot"):
            self._take_screenshot()
        elif text == 'open calculator':
            self._open_calculator()
        elif text == 'show image':
            self._show_image()
        elif text == 'copy this text':
            self._copy_text()
        elif text == 'paste clipboard':
            self._paste_text()
        elif text == 'close window':
            self._close_window()
        elif "type" in text:
            self._type(text)
        elif text == 'minimize all windows':
            self._minimize_all()
        elif text == 'maximize window':
            self._maximize_window()
        elif text == 'switch window':
            self._switch_window()
        elif text == 'open web browser':
            self._open_web_browser()
        elif "search for" in text:
            self._search(text)
        elif text == 'read clipboard':
            self._read_clipboard()
        else:
            self._unkown_command()

    def _welcome(self):
        self.tts.speak("Welcome, How can I help you today ?")

    def _unkown_command(self):
        self.tts.speak("Sorry, I Can't recognize this command can you try again ?")

    def _open_notepad(self):
        self.tts.speak("Opening notepad")
        pyperclip.copy("notepad")
        pyautogui.hotkey('win','r')
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('Enter')
        sleep(1)
        pyautogui.hotkey('ctrl','n')

    def _take_screenshot(self):
        self.tts.speak("Taking a screenshot...")
        screenshot=pyautogui.screenshot()
        screenshot.save('screenshot.png')
    def _open_calculator(self):
        self.tts.speak("Opening calculator...")
        pyperclip.copy("calc")
        pyautogui.hotkey('win','r')
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('Enter')
    def _show_image(self):
        self.tts.speak("Showing Image...")
        # Open the image
        img = Image.open("image.jpg")
        # Display the image
        img.show()
    def _copy_text(self):
        self.tts.speak("Copying the predefined text...")
        pyperclip.copy("This text was predefined by python voice assitant program")
    def _paste_text(self):
        self.tts.speak("pasting from the clipboard...")
        pyautogui.hotkey('ctrl','v')
    def _read_clipboard(self):
        clipboard_content=pyperclip.paste()
        self.tts.speak("Reading from the clipboard...")
        self.tts.speak(f"The text at the clipboard is: {clipboard_content}")

    def _close_window(self):
        self.tts.speak("Are you sure you want to exit the active window? Please say yes or no.")
        while True:
            confirmation = self.recognizer.listen_for_command()
            if 'yes' in confirmation:
                self.tts.speak("Closing the active window...")
                pyautogui.hotkey('alt', 'f4')
                break
            elif 'no' in confirmation:
                self.tts.speak("Aborting closure...")
                break
            elif confirmation:
                self.tts.speak("Please say yes or no.")
    def _exit(self):
        self.tts.speak("Exiting program, Bye.....")
    def _type(self,text):
        new_sentence = text.partition("type")[2].strip()
        if new_sentence:
            self.tts.speak(f"typing {new_sentence} ...")
            pyperclip.copy(f"{new_sentence}")
            pyautogui.hotkey('ctrl','v')
        else:
            self.tts.speak(f"Please say something to type!")
    def _minimize_all(self):
        self.tts.speak("minimizing window...")
        pyautogui.hotkey('win','d')        
    def _maximize_window(self):
        self.tts.speak("maximizing window...")
        pyautogui.hotkey('win','up')        
    def _switch_window(self):
        self.tts.speak("Switching window...")
        pyautogui.hotkey('alt','tab')    
    def _open_web_browser(self):
        self.tts.speak("Opening browser...")
        webbrowser.open("https://www.google.com")   
    def _search(self,text):
        new_sentence = text.partition("search for")[2].strip()
        self.tts.speak(f"Searching for {new_sentence} ...")
        pyperclip.copy(f"{new_sentence}")
        webbrowser.open("https://www.google.com")
        sleep(1)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('Enter')  

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
        self.tts= TextToSpeech(cp_rate=130, cp_voice_index=0)
        self.recognizer=SpeechRecognizer(cp_model_path="vosk-model-small-en-us-0.15",cp_sample_rate=16000,cp_device=None)
        self.commandProcessor=CommandProcessor(self.tts,self.recognizer)

    def run(self):
        while True:
            text = self.recognizer.listen_for_command()
            result=self.commandProcessor.handle_command(text)
            if result == "exit":
                break


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()

