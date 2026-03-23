import { motion } from "framer-motion";

import { reportSectionTitles } from "../content/uiText";

export default function StreamingResult({ copy, language, mode, streamedText, result, isLoading, error }) {
  const sections = result?.sections ?? [];
  const readingMode = result?.reading_mode ?? mode;
  const titleMap = reportSectionTitles[readingMode]?.[language] ?? reportSectionTitles.vedatwin[language];
  const disclaimer = extractDisclaimer(result?.report ?? streamedText);

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.12 }}
      className="glass-card p-6 lg:p-7"
    >
      <div className="mb-5 flex items-center justify-between gap-3">
        <div>
          <p className="section-label">{copy.resultTitle}</p>
          <h2 className="font-display text-3xl text-white">{copy.resultTitle}</h2>
        </div>
        {isLoading ? (
          <span className="inline-flex items-center gap-2 rounded-full border border-glow-violet/20 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.24em] text-slate-200">
            <span className="h-2 w-2 animate-pulse rounded-full bg-glow-violet" />
            Streaming
          </span>
        ) : null}
      </div>

      {error ? (
        <div className="rounded-2xl border border-rose-400/25 bg-rose-500/10 p-4 text-sm text-rose-100">
          {copy.errorPrefix}: {error}
        </div>
      ) : null}

      {!streamedText && !result ? (
        <div className="rounded-2xl border border-dashed border-white/10 bg-white/5 p-5 text-sm leading-7 text-slate-400">
          {copy.resultEmpty}
        </div>
      ) : (
        <div className="space-y-4">
          {disclaimer ? (
            <div className="rounded-2xl border border-glow-gold/25 bg-glow-gold/10 p-5">
              <p className="section-label">{copy.importantNote}</p>
              <p className="text-sm leading-7 text-amber-50">{disclaimer}</p>
            </div>
          ) : null}

          {sections.length ? (
            sections.map((section) => (
              <div key={section.agent} className="rounded-2xl border border-white/10 bg-white/5 p-5">
                <h3 className="font-display text-2xl text-white">
                  {titleMap[section.agent] ?? section.agent.replace(/_/g, " ")}
                </h3>
                <p className="mt-3 whitespace-pre-line text-sm leading-7 text-slate-200">{section.content}</p>
              </div>
            ))
          ) : (
            <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
              <p className="whitespace-pre-line text-sm leading-7 text-slate-200">{streamedText}</p>
            </div>
          )}
        </div>
      )}
    </motion.section>
  );
}

function extractDisclaimer(text = "") {
  const parts = text.split("\n\n");
  return parts[0]?.split("\n").slice(1).join("\n") ?? "";
}
