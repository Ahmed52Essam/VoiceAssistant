import unittest
from unittest.mock import MagicMock
from commands import ExitCommand
from core.text_to_speech import TextToSpeech
from core.recognizer import SpeechRecognizer

class TestExitCommand(unittest.TestCase):
    def setUp(self):
        self.tts = MagicMock(spec=TextToSpeech)
        self.recognizer = MagicMock(spec=SpeechRecognizer)
        self.command = ExitCommand()

    def test_match_exit(self):
        self.assertTrue(self.command.match("exit"))
        self.assertTrue(self.command.match("bye"))

    def test_match_invalid(self):
        self.assertFalse(self.command.match("hello"))

    def test_execute(self):
        result = self.command.execute("exit", self.tts, self.recognizer)
        self.tts.speak.assert_called_with("Exiting program, Bye.....")
        self.assertEqual(result, "exit")