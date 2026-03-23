from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from app.models.request_models import ExportPDFRequest


class PDFService:
    """Creates a simple PDF export for completed reports."""

    UNICODE_FONT_NAME = "VedaTwinUnicode"
    FONT_CANDIDATES = (
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/tahoma.ttf"),
        Path("C:/Windows/Fonts/times.ttf"),
    )

    async def render_pdf(self, request: ExportPDFRequest) -> bytes:
        font_name = self._ensure_unicode_font()
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
        )
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "VedaTwinTitle",
            parent=styles["Title"],
            fontName=font_name,
            fontSize=20,
            leading=24,
        )
        body_style = ParagraphStyle(
            "VedaTwinBody",
            parent=styles["BodyText"],
            fontName=font_name,
            fontSize=10.5,
            leading=15,
            spaceAfter=6,
        )

        title = "VedaTwin AI Report" if request.language == "en" else "Báo cáo VedaTwin AI"

        story = [
            Paragraph(escape(title), title_style),
            Spacer(1, 12),
            Paragraph(escape(f"Language: {request.language}"), body_style),
            Spacer(1, 8),
            Paragraph(escape(f"Question: {request.question}"), body_style),
            Spacer(1, 12),
        ]

        for block in request.report.split("\n\n"):
            safe_block = "<br/>".join(escape(line) for line in block.splitlines()) or "&nbsp;"
            story.append(Paragraph(safe_block, body_style))
            story.append(Spacer(1, 10))

        doc.build(story)
        return buffer.getvalue()

    def _ensure_unicode_font(self) -> str:
        try:
            pdfmetrics.getFont(self.UNICODE_FONT_NAME)
            return self.UNICODE_FONT_NAME
        except KeyError:
            pass

        for candidate in self.FONT_CANDIDATES:
            if candidate.exists():
                pdfmetrics.registerFont(TTFont(self.UNICODE_FONT_NAME, str(candidate)))
                return self.UNICODE_FONT_NAME

        return "Helvetica"
