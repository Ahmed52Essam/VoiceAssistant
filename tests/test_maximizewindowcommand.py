import unittest
from unittest.mock import MagicMock
from core.text_to_speech import TextToSpeech
from core.recognizer import SpeechRecognizer
from commands import MaximizeWindowCommand

class TestMaximizeWindowCommand(unittest.TestCase):
    def setUp(self):
        self.tts = MagicMock(spec=TextToSpeech)
        self.recognizer = MagicMock(spec=SpeechRecognizer)
        self.command = MaximizeWindowCommand()

    def test_match_expected_command(self):
        # The valid command for MaximizeWindowCommand is "maximize window"
        self.assertTrue(self.command.match("maximize window"))

    def test_match_invalid_command(self):
        # An invalid command is any string not matching the expected phrase
        self.assertFalse(self.command.match("minimize all windows"))

    def test_execute(self):
        result = self.command.execute("maximize window", self.tts, self.recognizer)
        self.assertEqual(result, "OK")
        self.tts.speak.assert_called()

if __name__ == "__main__":
    unittest.main()
