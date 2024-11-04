import logging
import webbrowser
from urllib3.util.url import parse_url, Url

_logger = logging.getLogger(__name__)

HANDLERS = []

def command_handler(*args):
    HANDLERS.append(args[0])
    def wrapper(func):
        return func
    return wrapper


@command_handler
def google_search(query):
    if not "найди" in query:
        return
    try:
        search_url: Url = parse_url(f"https://www.google.com/search?q={query}")
        # Open the web browser with the search results
        _logger.info(f"Opening the web browser with the search results for: {search_url}")
        webbrowser.open(search_url.url)
    except Exception as e:
        print(f"An error occurred: {e}")