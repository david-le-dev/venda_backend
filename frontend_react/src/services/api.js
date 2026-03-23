import axios from "axios";

import { buildAnalyzeFormData } from "./stream";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: BASE_URL,
});

export async function analyzeReport(values) {
  const response = await api.post("/analyze/report", buildAnalyzeFormData(values), {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
}

export async function exportPdf({ language, question, report }) {
  const response = await api.post(
    "/export/pdf",
    { language, question, report },
    {
      responseType: "blob",
    }
  );

  return response.data;
}

export { BASE_URL };
