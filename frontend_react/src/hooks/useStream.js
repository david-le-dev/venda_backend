import { useCallback, useState } from "react";

import { exportPdf } from "../services/api";
import { streamAnalysis } from "../services/stream";

const initialForm = {
  name: "",
  readingMode: "vedatwin",
  birthDate: "",
  birthTime: "",
  birthPlace: "",
  gender: "",
  question: "",
  language: "en",
  timeFocus: "",
  faceImage: null,
  palmImage: null,
};

export function useStream(baseUrl) {
  const [form, setForm] = useState(initialForm);
  const [logs, setLogs] = useState([]);
  const [streamedText, setStreamedText] = useState("");
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const reset = useCallback(() => {
    setLogs([]);
    setStreamedText("");
    setResult(null);
    setError("");
    setIsLoading(false);
  }, []);

  const updateField = useCallback((name, value) => {
    setForm((current) => ({ ...current, [name]: value }));
  }, []);

  const start = useCallback(async () => {
    setLogs([]);
    setStreamedText("");
    setResult(null);
    setError("");
    setIsLoading(true);

    try {
      for await (const event of streamAnalysis(form, baseUrl)) {
        if (event.event === "status") {
          setLogs((current) => [...current, event.data]);
        } else if (event.event === "chunk") {
          setStreamedText((current) => current + (event.data.text ?? ""));
        } else if (event.event === "done") {
          setResult(event.data);
        }
      }
    } catch (streamError) {
      setError(streamError.message || "Streaming failed.");
    } finally {
      setIsLoading(false);
    }
  }, [baseUrl, form]);

  const downloadPdf = useCallback(async () => {
    if (!result?.report) {
      return;
    }

    const blob = await exportPdf({
      language: form.language,
      question: form.question,
      report: result.report,
    });

    const url = window.URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${form.readingMode}-report.pdf`;
    anchor.click();
    window.URL.revokeObjectURL(url);
  }, [form.language, form.question, form.readingMode, result]);

  return {
    form,
    logs,
    streamedText,
    result,
    isLoading,
    error,
    updateField,
    start,
    reset,
    downloadPdf,
  };
}
