import unittest
from unittest.mock import MagicMock
from core.text_to_speech import TextToSpeech
from core.recognizer import SpeechRecognizer
from commands import OpenYoutubeCommand

class TestOpenYoutubeCommand(unittest.TestCase):
    def setUp(self):
        self.tts = MagicMock(spec=TextToSpeech)
        self.recognizer = MagicMock(spec=SpeechRecognizer)
        self.command = OpenYoutubeCommand()

    def test_match_expected_command(self):
        self.assertTrue(self.command.match("open youtube"))

    def test_match_invalid_command(self):
        self.assertFalse(self.command.match("open browser"))

    def test_execute(self):
        result = self.command.execute("open youtube", self.tts, self.recognizer)
        self.assertEqual(result, "OK")
        self.tts.speak.assert_called()

if __name__ == "__main__":
    unittest.main()
