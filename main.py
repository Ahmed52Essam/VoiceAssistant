from core.text_to_speech import TextToSpeech
from core.recognizer import SpeechRecognizer
from core.processor import CommandProcessor
import commands
import os

    
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

