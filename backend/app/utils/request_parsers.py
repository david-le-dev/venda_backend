import base64

from fastapi import Request
from starlette.datastructures import UploadFile

from app.models.request_models import AnalyzeRequest, ImageInput


async def parse_analyze_request(request: Request) -> AnalyzeRequest:
    content_type = request.headers.get("content-type", "")
    if "multipart/form-data" in content_type:
        form = await request.form()
        payload = {
            "name": str(form.get("name", "")).strip(),
            "reading_mode": str(form.get("reading_mode", "vedatwin")).strip(),
            "birth_date": str(form.get("birth_date", "")).strip(),
            "birth_time": _clean_optional_string(form.get("birth_time")),
            "birth_place": str(form.get("birth_place", "")).strip(),
            "gender": _clean_optional_string(form.get("gender")),
            "question": str(form.get("question", "")).strip(),
            "language": str(form.get("language", "en")).strip(),
            "time_focus": _clean_optional_string(form.get("time_focus")),
            "face_image": await _parse_upload(form.get("face_image")),
            "palm_image": await _parse_upload(form.get("palm_image")),
        }
        return AnalyzeRequest.model_validate(payload)

    payload = await request.json()
    return AnalyzeRequest.model_validate(payload)


def _clean_optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


async def _parse_upload(value: object) -> ImageInput | None:
    if value is None or not isinstance(value, UploadFile) or not value.filename:
        return None

    raw = await value.read()
    if not raw:
        return None

    return ImageInput(
        mime_type=value.content_type or "application/octet-stream",
        data_base64=base64.b64encode(raw).decode("utf-8"),
        file_name=value.filename,
    )
