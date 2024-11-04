import logging
import numpy as np
import speech_recognition as sr
from handler_resolver import HandlerResolver
from command_patterns import AbstractCommandPatterns

_logger = logging.getLogger(__name__)

class VoiceAssistant:

    """Voice assistant that recognizes speech in Russian."""

    def __init__(self,
                 handler_resolver: HandlerResolver,
                 language: str,
                 command_patterns: AbstractCommandPatterns):
        self._handler_resolver = handler_resolver
        self._language = language
        self._command_patterns = command_patterns
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

    @staticmethod
    def is_speech(audio_data: sr.AudioData) -> bool:
        # Convert audio data to raw audio
        audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
        amplitude = np.abs(audio_array).mean()
        threshold = 500  # Adjust this threshold based on your environment

        return amplitude > threshold

    def run_assistant(self):
        _logger.info("Initiate assistant cycle")
        with self._microphone as source:
            _logger.info("Start listening")
            while True:
                self._recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self._recognizer.listen(source)
                if self.is_speech(audio):
                    command = self._recognize_speech(audio).lower()
                    _logger.info(f"Recognized command: {command}")
                    if self._command_patterns.EXIT_COMMAND in command:
                        _logger.info("Exiting the assistant")
                        break
                    self._handler_resolver.resolve(command)

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
