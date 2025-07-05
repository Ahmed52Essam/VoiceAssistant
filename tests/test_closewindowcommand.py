import unittest
from unittest.mock import MagicMock
from core.text_to_speech import TextToSpeech
from core.recognizer import SpeechRecognizer
from commands import CloseWindowCommand

class TestCloseWindowCommand(unittest.TestCase):
    def setUp(self):
        self.tts = MagicMock(spec=TextToSpeech)
        self.recognizer = MagicMock(spec=SpeechRecognizer)
        self.command = CloseWindowCommand()

    def test_match_expected_command(self):
        self.assertTrue(self.command.match("close window"))

    def test_match_invalid_command(self):
        self.assertFalse(self.command.match("open notepad"))

    def test_execute(self):
        # For close window, the execute method expects user confirmation, so we mock recognizer
        self.recognizer.listen_for_command.return_value = "no"
        result = self.command.execute("close window", self.tts, self.recognizer)
        self.assertEqual(result, "OK")
        self.tts.speak.assert_called()

if __name__ == "__main__":
    unittest.main()
