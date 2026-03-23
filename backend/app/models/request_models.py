from typing import Literal

from pydantic import BaseModel, Field, field_validator


LanguageOption = Literal["en", "vi"]
ReadingMode = Literal["vedatwin", "eastern_destiny"]
GenderOption = Literal["female", "male", "non_binary", "prefer_not_to_say"]


class ImageInput(BaseModel):
    mime_type: str = Field(..., description="Image MIME type such as image/png.")
    data_base64: str = Field(..., description="Base64-encoded image payload.")
    file_name: str | None = Field(default=None, description="Original filename if available.")

    @field_validator("mime_type")
    @classmethod
    def validate_mime_type(cls, value: str) -> str:
        if not value.startswith("image/"):
            raise ValueError("Only image MIME types are supported.")
        return value


class AnalyzeRequest(BaseModel):
    name: str = Field(..., description="Display name used to personalize the reading.")
    reading_mode: ReadingMode = Field(default="vedatwin", description="Selected reading system.")
    birth_date: str = Field(..., description="Date of birth in ISO format.")
    birth_time: str | None = Field(default=None, description="Time of birth if known.")
    birth_place: str = Field(..., description="Birthplace in city, region, country format.")
    gender: GenderOption | None = Field(default=None, description="Optional gender context.")
    question: str = Field(..., description="User question for reflective guidance.")
    language: LanguageOption = Field(..., description="Output language.")
    time_focus: str | None = Field(default=None, description="Optional period focus such as 'this year'.")
    face_image: ImageInput | None = Field(default=None, description="Optional face image.")
    palm_image: ImageInput | None = Field(default=None, description="Optional palm image.")

    @field_validator("name", "birth_date", "birth_place", "question")
    @classmethod
    def validate_required_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field is required.")
        return value

    @field_validator("birth_time", "time_focus")
    @classmethod
    def normalize_optional_strings(cls, value: str | None) -> str | None:
        return value.strip() if value else None


class ExportPDFRequest(BaseModel):
    language: LanguageOption
    question: str
    report: str
    file_name: str = "vedatwin-report.pdf"

    @field_validator("file_name")
    @classmethod
    def ensure_pdf_extension(cls, value: str) -> str:
        return value if value.lower().endswith(".pdf") else f"{value}.pdf"
