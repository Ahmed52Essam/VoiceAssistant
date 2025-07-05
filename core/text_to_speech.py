import pyttsx3

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