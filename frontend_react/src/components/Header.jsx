import { motion } from "framer-motion";

export default function Header({ copy, language, onLanguageChange }) {
  return (
    <motion.header
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card relative overflow-hidden px-8 py-8"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(139,124,255,0.18),transparent_32%)]" />
      <div className="absolute inset-y-0 right-0 w-1/3 bg-[radial-gradient(circle_at_center,rgba(215,185,119,0.10),transparent_60%)]" />

      <div className="relative flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-3xl">
          <p className="section-label">{copy.badge}</p>
          <h1 className="font-display text-5xl leading-none text-white md:text-6xl">VedaTwin AI</h1>
          <p className="mt-3 text-lg text-slate-300">{copy.tagline}</p>
          <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-400">{copy.subtitle}</p>
        </div>

        <div className="flex items-center gap-3 self-start lg:self-auto">
          <span className="text-xs uppercase tracking-[0.28em] text-glow-gold/80">{copy.language}</span>
          <div className="flex rounded-full border border-white/10 bg-white/5 p-1">
            {[
              { label: "EN", value: "en" },
              { label: "VI", value: "vi" },
            ].map((item) => (
              <button
                key={item.value}
                type="button"
                onClick={() => onLanguageChange(item.value)}
                className={`rounded-full px-4 py-2 text-sm transition ${
                  language === item.value
                    ? "bg-gradient-to-r from-glow-violet to-glow-indigo text-white shadow-card"
                    : "text-slate-300 hover:text-white"
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </motion.header>
  );
}
