import unittest
from unittest.mock import MagicMock
from core.text_to_speech import TextToSpeech
from core.recognizer import SpeechRecognizer
from commands import PasteCommand

class TestPasteCommand(unittest.TestCase):
    def setUp(self):
        self.tts = MagicMock(spec=TextToSpeech)
        self.recognizer = MagicMock(spec=SpeechRecognizer)
        self.command = PasteCommand()

    def test_match_expected_command(self):
        self.assertTrue(self.command.match("paste clipboard"))

    def test_match_invalid_command(self):
        self.assertFalse(self.command.match("copy text"))

    def test_execute(self):
        result = self.command.execute("paste clipboard", self.tts, self.recognizer)
        self.assertEqual(result, "OK")
        self.tts.speak.assert_called()

if __name__ == "__main__":
    unittest.main()
