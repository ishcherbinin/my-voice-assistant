import logging.config
import os

from handler_resolver import HandlerResolver
from ru_command_handlers import HANDLERS
from logging_conf import log_config
from command_patterns import patter_resolver
from voice_assistant import VoiceAssistant

logging.config.dictConfig(log_config)
_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    language = os.getenv("LANGUAGE", "ru-RU")
    pattern_identifier = os.getenv("COMMAND_PATTERN", "ru")
    command_pattern = patter_resolver(pattern_identifier)
    _logger.info("Starting the voice assistant")
    handler_resolver = HandlerResolver(HANDLERS)
    assistant = VoiceAssistant(handler_resolver=handler_resolver,
        language=language, command_patterns=command_pattern)
    assistant.run_assistant()