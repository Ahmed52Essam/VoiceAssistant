from core.registry import CommandRegistry

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

        self.pattern_commands= CommandRegistry.get_registry()


    def handle_command(self, text):

        for command in self.pattern_commands:
            if command.match(text):
                result = command.execute(text,self.tts,self.recognizer) 
                if result == "exit":
                    return "exit"
                return
