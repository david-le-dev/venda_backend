# Architecture Notes

## Design approach

The codebase favors clear module ownership over heavy abstraction. Agent logic stays thin and prompt-driven, while deterministic work such as validation, streaming, storage, and astrology calculation is isolated in services.

## Backend shape

- `routes/` exposes HTTP APIs and SSE-compatible streaming responses.
- `agents/` owns role-specific reasoning behavior.
- `services/` owns integrations: Gemini, astrology adapters, Chroma, PDF export, orchestration.
- `models/` keeps request, response, and agent contracts explicit.
- `utils/` centralizes formatting, validation, language, and logging support.

## Frontend shape

The Streamlit app keeps UI code simple: one input form, one live log panel, one report panel, and lightweight API clients. This keeps the demo easy to deploy and fast to iterate on for a solo builder.

