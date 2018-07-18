from requests_futures.sessions import FuturesSession


class BaseClient:
    """Base client for interfacing with all code management external APIs.

    The Python futures library is utilized to make asynchronous requests for speedier returns.
    """
    def __init__(self):
        self.session = FuturesSession(max_workers=200)
