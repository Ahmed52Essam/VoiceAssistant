import unittest
from unittest.mock import MagicMock
from core.text_to_speech import TextToSpeech
from core.recognizer import SpeechRecognizer
from commands import SwitchWindowCommand

class TestSwitchWindowCommand(unittest.TestCase):
    def setUp(self):
        self.tts = MagicMock(spec=TextToSpeech)
        self.recognizer = MagicMock(spec=SpeechRecognizer)
        self.command = SwitchWindowCommand()

    def test_match_expected_command(self):
        self.assertTrue(self.command.match("switch window"))

    def test_match_invalid_command(self):
        self.assertFalse(self.command.match("maximize window"))

    def test_execute(self):
        result = self.command.execute("switch window", self.tts, self.recognizer)
        self.assertEqual(result, "OK")
        self.tts.speak.assert_called()

if __name__ == "__main__":
    unittest.main()
