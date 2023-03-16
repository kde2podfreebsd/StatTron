from typing import Optional


class UserAgentException(Exception):
    def __init__(self, err: Optional[Exception | ValueError] = Exception):
        self.error = err

    def __str__(self):
        return f"UserAgent Exception: {self.error}"