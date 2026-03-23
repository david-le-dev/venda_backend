import base64

from fastapi import HTTPException

from app.config import get_settings
from app.models.request_models import AnalyzeRequest, ImageInput


def validate_chat_request(request: AnalyzeRequest) -> list[str]:
    settings = get_settings()
    warnings: list[str] = []
    if not request.birth_time:
        warnings.append(
            "Birth time missing: chart precision is reduced, so the interpretation should stay softer."
            if request.language == "en"
            else "Chưa có giờ sinh: phần diễn giải chi tiết theo thời điểm sẽ được giữ mềm và linh hoạt hơn."
        )
    for image in [request.face_image, request.palm_image]:
        if image:
            _validate_image_size(image, settings.max_image_bytes)
    return warnings


def _validate_image_size(image: ImageInput, max_bytes: int) -> None:
    try:
        raw = base64.b64decode(image.data_base64, validate=True)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=422, detail="Invalid base64 image payload.") from exc

    if len(raw) > max_bytes:
        raise HTTPException(status_code=413, detail="Uploaded image exceeds size limit.")
