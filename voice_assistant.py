import logging

import speech_recognition as sr
from run_command_patterns import AbstractCommandPatterns

_logger = logging.getLogger(__name__)

class VoiceAssistant:

    """Voice assistant that recognizes speech in Russian."""

    def __init__(self,
                 language: str,
                 command_patterns: AbstractCommandPatterns):
        self._language = language
        self._command_patterns = command_patterns
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

    def run_assistant(self):
        while True:
            _logger.info("Initiate assistant cycle")
            with self._microphone as source:
                _logger.info("Start listening")
                self._recognizer.adjust_for_ambient_noise(source)
                audio = self._recognizer.listen(source)
                command = self._recognize_speech(audio)
                _logger.info(f"Recognized command: {command}")
                if command.lower() == self._command_patterns.EXIT_COMMAND:
                    _logger.info("Exiting the assistant")
                    break

    def _recognize_speech(self, audio: sr.AudioData) -> str:
        """Recognize speech using Google Web Speech API"""
        text = ""
        try:
            _logger.info("Recognizing speech")
            text = self._recognizer.recognize_google(audio, language=self._language)
        except sr.UnknownValueError:
            _logger.exception("Sorry, I could not understand the audio.")
        except sr.RequestError:
            _logger.info("Sorry, there was an error with the recognition service.")
        return text
