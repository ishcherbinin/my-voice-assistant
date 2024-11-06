import logging
import subprocess
import threading
import webbrowser
from typing import List, Callable
from urllib.parse import quote_plus

from urllib3.util.url import parse_url, Url

_logger = logging.getLogger(__name__)

HANDLERS: List[Callable] = []

def command_handler(*args):
    HANDLERS.append(args[0])
    def wrapper(func):
        return func
    return wrapper


# Define a set of noise words to filter out
NOISE_WORDS = {
    "пожалуйста", "в", "и", "на", "для", "с", "к", "по", "из", "это",
    "как", "что", "где", "кто", "когда", "который", "то", "это", "все"
}

@command_handler
async def google_search(query: str):
    cleaned_query = ' '.join(word for word in query.split() if word.lower() not in NOISE_WORDS)
    _logger.info(f"Searching the web for: {cleaned_query}")
    if not "ok google" in cleaned_query:
        return
    cleaned_query = cleaned_query.replace("ok google", "").strip()
    def open_browser():
        try:
            search_url: Url = parse_url(f"https://www.google.com/search?q={quote_plus(cleaned_query)}")
            # Open the web browser with the search results
            _logger.info(f"Opening the web browser with the search results for: {search_url}")
            webbrowser.open(search_url.url)
        except Exception as e:
            _logger.error(f"An error occurred: {e}")
    threading.Thread(target=open_browser).start()

@command_handler
async def open_google_chrome(query: str):
    if not "открой google chrome" in query:
        return
    _logger.info("Opening Google Chrome")
    webbrowser.open("google-chrome")

@command_handler
async def run_pycharm(query: str):
    if not "запусти pycharm" in query:
        return
    _logger.info("Opening PyCharm")
    subprocess.Popen(["pycharm-community"])


@command_handler
async def exit_assistant(query: str):
    if not "завершить" in query:
        return
    _logger.info("Exiting the assistant")
    exit(0)

@command_handler
async def lock_screen(query: str):
    if not "заблокируй экран" in query:
        return
    _logger.info("Locking the screen")
    subprocess.Popen(["gnome-screensaver-command", "-l"])