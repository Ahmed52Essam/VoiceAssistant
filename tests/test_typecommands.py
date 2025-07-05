import unittest
from unittest.mock import MagicMock
from core.text_to_speech import TextToSpeech
from core.recognizer import SpeechRecognizer
from commands import TypeCommand

class TestTypeCommand(unittest.TestCase):
    def setUp(self):
        self.tts = MagicMock(spec=TextToSpeech)
        self.recognizer = MagicMock(spec=SpeechRecognizer)
        self.command = TypeCommand()

    def test_match_typing_command(self):
        self.assertTrue(self.command.match("type hello world"))

    def test_match_invalid_command(self):
        self.assertFalse(self.command.match("hello"))

    def test_execute_typing_command(self):
        result = self.command.execute("type hello world", self.tts, self.recognizer)
        self.tts.speak.assert_called_once()
        self.assertEqual(result, "OK")

    def test_execute_empty_command(self):
        result = self.command.execute("type", self.tts, self.recognizer)
        self.tts.speak.assert_called_with("Please say something to type!")
        self.assertEqual(result, "OK")     

if __name__ == '__main__':
    unittest.main()
