const DEFAULT_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function* streamAnalysis(values, baseUrl = DEFAULT_BASE_URL) {
  const response = await fetch(`${baseUrl}/analyze/stream`, {
    method: "POST",
    body: buildAnalyzeFormData(values),
  });

  if (!response.ok || !response.body) {
    const message = await response.text();
    throw new Error(message || "Streaming request failed.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }

    buffer += decoder.decode(value, { stream: true });
    const chunks = buffer.split(/\r?\n\r?\n/);
    buffer = chunks.pop() ?? "";

    for (const chunk of chunks) {
      const parsed = parseSseChunk(chunk);
      if (parsed) {
        yield parsed;
      }
    }
  }

  if (buffer.trim()) {
    const parsed = parseSseChunk(buffer);
    if (parsed) {
      yield parsed;
    }
  }
}

export function buildAnalyzeFormData(values) {
  const formData = new FormData();
  if (values.name?.trim()) {
    formData.append("name", values.name.trim());
  }
  formData.append("reading_mode", values.readingMode);
  formData.append("birth_date", values.birthDate);
  formData.append("birth_place", values.birthPlace);
  formData.append("question", values.question);
  formData.append("language", values.language);

  if (values.birthTime) {
    formData.append("birth_time", values.birthTime);
  }
  if (values.timeFocus) {
    formData.append("time_focus", values.timeFocus);
  }
  if (values.gender) {
    formData.append("gender", values.gender);
  }
  if (values.faceImage) {
    formData.append("face_image", values.faceImage);
  }
  if (values.palmImage) {
    formData.append("palm_image", values.palmImage);
  }

  return formData;
}

function parseSseChunk(chunk) {
  const lines = chunk.split(/\r?\n/);
  let event = "message";
  const dataLines = [];

  for (const line of lines) {
    if (line.startsWith("event:")) {
      event = line.slice(6).trim();
    } else if (line.startsWith("data:")) {
      dataLines.push(line.slice(5).trim());
    }
  }

  if (!dataLines.length) {
    return null;
  }

  return {
    event,
    data: JSON.parse(dataLines.join("\n")),
  };
}
