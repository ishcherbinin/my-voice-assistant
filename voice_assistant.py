import asyncio
import logging
import numpy as np
import speech_recognition as sr
from handler_resolver import HandlerResolver

_logger = logging.getLogger(__name__)

class VoiceAssistant:

    """Voice assistant that recognizes speech. Depends on command pattern and handlers
    Might use different languages and command patterns. Russian by default"""

    def __init__(self,
                 name: str,
                 handler_resolver: HandlerResolver,
                 language: str):
        self._name = name
        self._handler_resolver = handler_resolver
        self._language = language
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

    @staticmethod
    async def is_speech(audio_data: sr.AudioData) -> bool:
        # Convert audio data to raw audio
        audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
        amplitude = np.abs(audio_array).mean()
        threshold = 500  # Adjust this threshold based on your environment

        return amplitude > threshold

    async def _wait_for_wake_word(self, source: sr.Microphone):
        _logger.info("Waiting for the wake word")
        while True:
            _logger.info("Listening for the wake word")
            self._recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = await asyncio.to_thread(self._recognizer.listen, source,
                                            timeout=0, phrase_time_limit=10, snowboy_configuration=None)
            if await self.is_speech(audio):
                command = await self._recognize_speech(audio)
                command = command.lower()
                _logger.info(f"Recognized command: {command}")
                if self._name.lower() in command:
                    _logger.info("Wake word detected")
                    break

    async def run_assistant(self):
        _logger.info("Initiate assistant cycle")
        with self._microphone as source:
            _logger.info("Start listening")
            while True:
                await self._wait_for_wake_word(source)
                _logger.info("Listening for commands")
                self._recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = await asyncio.to_thread(self._recognizer.listen, source,
                                                timeout=0, phrase_time_limit=10, snowboy_configuration=None)
                if await self.is_speech(audio):
                    command = await self._recognize_speech(audio)
                    command = command.lower()
                    _logger.info(f"Recognized command: {command}")
                    await self._handler_resolver.resolve(command)
                    await asyncio.sleep(0.5)

    async def _recognize_speech(self, audio: sr.AudioData) -> str:
        """Recognize speech using Google Web Speech API"""
        text = ""
        try:
            _logger.info("Recognizing speech")
            text = await asyncio.to_thread(self._recognizer.recognize_google, audio,
                                           language=self._language, key=None, show_all=False)
        except sr.UnknownValueError:
            _logger.debug("Sorry, I could not understand the audio.")
        except sr.RequestError:
            _logger.debug("Sorry, there was an error with the recognition service.")
        return text
