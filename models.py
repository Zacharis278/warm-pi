from dataclasses import dataclass

@dataclass
class Reading():
    channel: int
    timestamp: int
    value: float