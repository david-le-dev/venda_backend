from __future__ import annotations

import base64
import random
from typing import Any

from app.config import get_settings
from app.utils.logging import get_logger


class GeminiService:
    """Gemini text and vision wrapper with safe local fallbacks."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.logger = get_logger(__name__)
        self._configured = False
        self._genai: Any | None = None

        if self.settings.google_api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self.settings.google_api_key)
                self._genai = genai
                self._configured = True
            except Exception as exc:  # pragma: no cover
                self.logger.warning("Gemini SDK unavailable, using fallback responses: %s", exc)

    async def generate_text(self, *, system_prompt: str, user_prompt: str, temperature: float = 0.8) -> str:
        if self._configured and self._genai is not None:
            try:
                model = self._genai.GenerativeModel(
                    model_name=self.settings.gemini_model,
                    system_instruction=system_prompt,
                )
                response = model.generate_content(
                    user_prompt,
                    generation_config={"temperature": temperature},
                )
                text = getattr(response, "text", "") or ""
                if text.strip():
                    return text.strip()
            except Exception as exc:  # pragma: no cover
                self.logger.warning("Gemini text generation failed, using fallback: %s", exc)

        return self._fallback_text(user_prompt)

    async def analyze_image(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        image_base64: str,
        mime_type: str,
        temperature: float = 0.7,
    ) -> str:
        if self._configured and self._genai is not None:
            try:
                model = self._genai.GenerativeModel(
                    model_name=self.settings.gemini_vision_model,
                    system_instruction=system_prompt,
                )
                image_part = {"mime_type": mime_type, "data": base64.b64decode(image_base64)}
                response = model.generate_content(
                    [user_prompt, image_part],
                    generation_config={"temperature": temperature},
                )
                text = getattr(response, "text", "") or ""
                if text.strip():
                    return text.strip()
            except Exception as exc:  # pragma: no cover
                self.logger.warning("Gemini vision generation failed, using fallback: %s", exc)

        return self._fallback_vision_text(user_prompt)

    def _fallback_text(self, prompt: str) -> str:
        if "Language: vi" in prompt:
            openers = [
                "Mẫu hình này có thể gợi ý một giai đoạn nhìn lại bản thân.",
                "Bản đọc cân bằng này có thể nghiêng về sự trưởng thành dần dần.",
                "Tổng thể bức tranh có thể được đọc như một quá trình phát triển có suy ngẫm.",
            ]
            closers = [
                "Hãy ưu tiên lựa chọn có ý thức thay vì xem mọi điều là cố định.",
                "Bạn có thể dùng gợi ý này như một tấm gương để tự nhận thức.",
                "Tiến bộ bền vững có thể đến từ hành động kiên nhẫn và thực tế.",
            ]
        else:
            openers = [
                "This pattern may suggest a reflective phase.",
                "A balanced reading might point toward gradual growth.",
                "The overall picture can be read as thoughtful and developmental.",
            ]
            closers = [
                "Focus on intentional choices instead of fixed outcomes.",
                "Use this as a mirror for self-awareness rather than certainty.",
                "The strongest results may come from patient, grounded action.",
            ]
        return f"{random.choice(openers)} {prompt[:220]} {random.choice(closers)}"

    def _fallback_vision_text(self, prompt: str) -> str:
        if "Language: vi" in prompt:
            reflections = [
                "Ấn tượng thị giác có thể cho thấy sự điềm tĩnh và quan sát.",
                "Hình ảnh có thể tạo cảm giác tập trung nhẹ và tiết chế cảm xúc.",
                "Tổng thể hình ảnh có thể gợi lên năng lượng bình tĩnh và sâu sắc.",
            ]
        else:
            reflections = [
                "The visual impression may come across as composed and observant.",
                "There can be a gentle sense of focus and contained emotion in the presentation.",
                "The overall image may suggest calm presence and thoughtful energy.",
            ]
        return f"{random.choice(reflections)} {prompt[:180]}"
