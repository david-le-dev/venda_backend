from dataclasses import dataclass


@dataclass(slots=True)
class BaseAgent:
    name: str
    description: str

