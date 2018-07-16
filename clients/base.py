from requests_futures.sessions import FuturesSession


class BaseClient:
    def __init__(self):
        self.session = FuturesSession(max_workers=200)
