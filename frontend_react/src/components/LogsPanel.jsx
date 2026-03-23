import { motion } from "framer-motion";

export default function LogsPanel({ copy, logs, isLoading }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="glass-card h-full p-6"
    >
      <div className="mb-5 flex items-center justify-between">
        <div>
          <p className="section-label">{copy.logsTitle}</p>
          <h2 className="font-display text-3xl text-white">{copy.logsTitle}</h2>
        </div>
        {isLoading ? (
          <span className="inline-flex items-center gap-2 rounded-full border border-glow-gold/20 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.24em] text-glow-gold">
            <span className="h-2 w-2 animate-pulse rounded-full bg-glow-gold" />
            Live
          </span>
        ) : null}
      </div>

      {!logs.length ? (
        <div className="rounded-2xl border border-dashed border-white/10 bg-white/5 p-5 text-sm leading-7 text-slate-400">
          {copy.logsEmpty}
        </div>
      ) : (
        <div className="space-y-3">
          {logs.map((log, index) => (
            <div
              key={`${log.agent}-${index}`}
              className="rounded-2xl border border-white/10 bg-white/5 p-4"
            >
              <div className="mb-2 flex items-center justify-between gap-3">
                <span className="text-sm font-semibold capitalize text-white">
                  {String(log.agent).replace(/_/g, " ")}
                </span>
                <span
                  className={`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.24em] ${
                    log.state === "warning"
                      ? "border border-glow-gold/30 bg-glow-gold/10 text-glow-gold"
                      : "border border-glow-violet/30 bg-glow-violet/10 text-slate-200"
                  }`}
                >
                  {log.state}
                </span>
              </div>
              <p className="text-sm leading-6 text-slate-300">{log.message}</p>
            </div>
          ))}
        </div>
      )}
    </motion.section>
  );
}

