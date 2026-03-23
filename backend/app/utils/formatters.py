from app.models.request_models import ReadingMode
from app.models.response_models import AgentOutput
from app.utils.language import SECTION_TITLES


def build_final_report(
    language: str,
    reading_mode: ReadingMode,
    disclaimer: str,
    sections: list[AgentOutput],
) -> str:
    titles = SECTION_TITLES[reading_mode][language]
    lines = [titles["disclaimer"], disclaimer, ""]

    title_map = {
        "summary": titles["summary"],
        "pillars": titles.get("pillars", "pillars"),
        "elements": titles.get("elements", "elements"),
        "tendencies": titles.get("tendencies", titles.get("personality", "tendencies")),
        "interpretation": titles.get("personality", "interpretation"),
        "question_focus": titles["question"],
        "transit": titles["timing"],
        "face": titles["face"],
        "palm": titles["palm"],
        "advisor": titles["advice"],
        "reflection_questions": titles.get("reflection_questions", "Reflection Questions"),
        "encouragement": titles["encouragement"],
    }

    for section in sections:
        lines.append(title_map.get(section.agent, section.agent.replace("_", " ").title()))
        lines.append(section.content)
        lines.append("")

    return "\n".join(lines).strip()
