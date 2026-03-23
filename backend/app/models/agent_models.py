from pydantic import BaseModel


class AgentStatus(BaseModel):
    agent: str
    state: str
    message: str


class AgentContext(BaseModel):
    language: str
    birth_date: str
    birth_time: str | None
    birth_place: str
    question: str
    time_focus: str | None = None
