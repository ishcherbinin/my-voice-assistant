import asyncio
import logging.config
import os

from handler_resolver import HandlerResolver
from logging_conf import log_config
from ru_command_handlers import HANDLERS
from voice_assistant import VoiceAssistant

logging.config.dictConfig(log_config)
_logger = logging.getLogger(__name__)

async def main():
    language = os.getenv("LANGUAGE", "ru-RU")
    name = os.getenv("ASSISTANT_NAME", "Alice")
    _logger.info("Starting the voice assistant")
    handler_resolver = HandlerResolver(HANDLERS)
    assistant = VoiceAssistant(name=name, handler_resolver=handler_resolver,
        language=language)
    await assistant.run_assistant()

if __name__ == "__main__":
    asyncio.run(main())