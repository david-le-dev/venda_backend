import { useMemo, useState } from "react";

import Footer from "../components/Footer";
import Header from "../components/Header";
import InputForm from "../components/InputForm";
import LogsPanel from "../components/LogsPanel";
import StreamingResult from "../components/StreamingResult";
import { getText } from "../content/uiText";
import { BASE_URL } from "../services/api";
import { useStream } from "../hooks/useStream";

export default function Home() {
  const { form, logs, streamedText, result, isLoading, error, updateField, start, reset, downloadPdf } =
    useStream(BASE_URL);
  const [submitAttempted, setSubmitAttempted] = useState(false);

  const copy = useMemo(() => getText(form.language, form.readingMode), [form.language, form.readingMode]);

  const validationError = useMemo(() => {
    if (!form.name.trim()) {
      return copy.validationName;
    }
    if (!form.birthDate) {
      return copy.validationDate;
    }
    if (!form.birthPlace.trim()) {
      return copy.validationPlace;
    }
    if (!form.question.trim()) {
      return copy.validationQuestion;
    }
    return "";
  }, [copy, form.name, form.birthDate, form.birthPlace, form.question]);

  const handleSubmit = () => {
    setSubmitAttempted(true);
    if (!validationError) {
      start();
    }
  };

  const handleReset = () => {
    setSubmitAttempted(false);
    updateField("name", "");
    updateField("readingMode", "vedatwin");
    updateField("birthDate", "");
    updateField("birthTime", "");
    updateField("birthPlace", "");
    updateField("gender", "");
    updateField("question", "");
    updateField("timeFocus", "");
    updateField("faceImage", null);
    updateField("palmImage", null);
    reset();
  };

  return (
    <main className="relative min-h-screen px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <Header copy={copy} language={form.language} onLanguageChange={(value) => updateField("language", value)} />

        <div className="mt-8 grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-6">
            <InputForm
              copy={copy}
              values={form}
              isLoading={isLoading}
              onChange={updateField}
              onSubmit={handleSubmit}
              onReset={handleReset}
            />

            {submitAttempted && validationError && !isLoading ? (
              <div className="rounded-2xl border border-amber-300/20 bg-amber-500/10 px-4 py-3 text-sm text-amber-100">
                {validationError}
              </div>
            ) : null}
          </div>

          <LogsPanel copy={copy} logs={logs} isLoading={isLoading} />
        </div>

        <div className="mt-6 grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
          <StreamingResult
            copy={copy}
            language={form.language}
            mode={form.readingMode}
            streamedText={streamedText}
            result={result}
            isLoading={isLoading}
            error={error}
          />

          <section className="glass-card p-6">
            <p className="section-label">{copy.exportTitle}</p>
            <h2 className="font-display text-3xl text-white">{copy.exportTitle}</h2>
            <p className="mt-3 text-sm leading-7 text-slate-400">{copy.exportHint}</p>

            <button type="button" onClick={downloadPdf} disabled={!result?.report} className="secondary-button mt-6 w-full">
              {copy.exportButton}
            </button>
          </section>
        </div>

        <Footer copy={copy} />
      </div>
    </main>
  );
}
