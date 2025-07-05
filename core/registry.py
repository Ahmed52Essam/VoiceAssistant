from abc import ABC, abstractmethod

class CommandRegistry():
    _registry=[]

    @staticmethod
    def register(cls):
        CommandRegistry._registry.append(cls)
        return cls

    @staticmethod
    def get_registry():
        commands=[cls for cls in CommandRegistry._registry if cls is not UnknownCommand ]
        commands.append(UnknownCommand)
        return [cls() for cls in commands]

class VoiceCommand(ABC):
    """Base Class that every dynamic command will inherit from."""
    @abstractmethod
    def match(self, text: str) -> bool:
        """Returns True if this command should handle the text."""
        pass
    
    @abstractmethod
    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        """Excutes the command logic."""
        pass

# This class is not added to CommandRegistry as it should be fallback funcion and will be last in the _registry list, it will be appended manually
class UnknownCommand(VoiceCommand):
    """
    This class will always match if no other classes are matched.
    ***    This IS MANDATED TO BE LAST CLASS TO ENHIRIT FROM THE VOICE COMMAND CLASS   ***
    This handled through the CommandRegistry class
    """
    
    def match(self,text) -> bool:
        return True

    def execute(self, text: str, tts: "TextToSpeech", recognizer: "SpeechRecognizer") ->str:
        tts.speak("Sorry, I Can't recognize this command. Can you try again ?")
        return "OK"