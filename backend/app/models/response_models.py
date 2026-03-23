from pydantic import BaseModel, Field

from app.models.request_models import ReadingMode


class PlanetPlacement(BaseModel):
    planet: str
    sign: str
    house: int


class ChartData(BaseModel):
    ascendant: str
    moon_sign: str
    sun_sign: str
    confidence_note: str
    key_planets: list[PlanetPlacement]
    houses_summary: list[str] = Field(default_factory=list)


class EasternChartData(BaseModel):
    year_pillar: str
    month_pillar: str
    day_pillar: str
    hour_pillar: str
    zodiac_animal: str
    dominant_elements: list[str]
    weaker_elements: list[str]
    symbolic_core: list[str]
    timezone_name: str | None = None
    timezone_confidence: str | None = None
    confidence_note: str


class RetrievalChunk(BaseModel):
    source_tag: str
    content: str


class AgentOutput(BaseModel):
    agent: str
    status: str
    content: str


class ReportMetadata(BaseModel):
    reading_mode: ReadingMode
    used_rag: bool
    face_analysis_used: bool
    palm_analysis_used: bool
    warnings: list[str]


class FinalReportResponse(BaseModel):
    language: str
    reading_mode: ReadingMode
    report: str
    sections: list[AgentOutput]
    metadata: ReportMetadata
