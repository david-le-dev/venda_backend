from fastapi import APIRouter
from fastapi.responses import Response

from app.models.request_models import ExportPDFRequest
from app.services.pdf_service import PDFService


router = APIRouter()
pdf_service = PDFService()


@router.post("/export/pdf")
async def export_pdf(request: ExportPDFRequest) -> Response:
    pdf_bytes = await pdf_service.render_pdf(request)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{request.file_name}"'},
    )
