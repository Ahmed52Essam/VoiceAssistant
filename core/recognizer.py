import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

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