import webbrowser

HANDLERS = []

def command_handler(*args):
    def wrapper(func):
        HANDLERS.append(func)
        return func
    return wrapper

@command_handler
def google_search(query):
    if not "найди" in query:
        return
    try:
        search_url = f"https://www.google.com/search?q={query}"
        # Open the web browser with the search results
        webbrowser.open(search_url)
    except Exception as e:
        print(f"An error occurred: {e}")