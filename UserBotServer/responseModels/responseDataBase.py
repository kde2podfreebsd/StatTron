from dataclasses import dataclass

@dataclass
class DatabaseResponse:
    status: bool
    action: str
    message: str