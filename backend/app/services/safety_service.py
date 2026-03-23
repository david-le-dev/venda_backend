import re

from app.models.request_models import ReadingMode
from app.models.response_models import AgentOutput
from app.prompts.global_prompts import DISCLAIMER_TEXT
from app.prompts.safety_prompts import BANNED_PHRASES


class SafetyService:
    """Applies lightweight policy checks to the assembled report."""

    def review_sections(
        self,
        *,
        language: str,
        reading_mode: ReadingMode,
        sections: list[AgentOutput],
    ) -> tuple[list[AgentOutput], list[str]]:
        warnings: list[str] = []
        cleaned_sections: list[AgentOutput] = []

        for section in sections:
            content = section.content.strip()
            lowered = content.lower()
            for phrase in BANNED_PHRASES:
                if phrase in lowered:
                    warnings.append(f"Unsafe phrase adjusted in {section.agent}: {phrase}")
                    content = re.sub(re.escape(phrase), "may indicate a sensitive theme", content, flags=re.IGNORECASE)

            if "medical advice" in lowered or "legal advice" in lowered or "financial advice" in lowered:
                warnings.append(f"Advice boundary reinforced in {section.agent}.")
                if language == "vi":
                    content += " Đây chỉ là nội dung chiêm nghiệm và không thay thế tư vấn chuyên môn."
                else:
                    content += " This is reflective content only and should not replace professional advice."

            cleaned_sections.append(AgentOutput(agent=section.agent, status=section.status, content=content))

        disclaimer = DISCLAIMER_TEXT[reading_mode][language]
        if not disclaimer.strip():
            warnings.append("Missing disclaimer template.")

        return cleaned_sections, warnings
