import logging
import webbrowser
from urllib.parse import quote_plus

from urllib3.util.url import parse_url, Url

_logger = logging.getLogger(__name__)

HANDLERS = []

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
def google_search(query):
    cleaned_query = ' '.join(word for word in query.split() if word.lower() not in NOISE_WORDS)
    _logger.info(f"Searching the web for: {cleaned_query}")
    if not "ok google" in cleaned_query:
        return
    cleaned_query = cleaned_query.replace("ok google", "").strip()
    try:
        search_url: Url = parse_url(f"https://www.google.com/search?q={quote_plus(cleaned_query)}")
        # Open the web browser with the search results
        _logger.info(f"Opening the web browser with the search results for: {search_url}")
        webbrowser.open(search_url.url)
    except Exception as e:
        print(f"An error occurred: {e}")