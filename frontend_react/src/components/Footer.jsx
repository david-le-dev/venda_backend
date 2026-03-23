export default function Footer({ copy }) {
  return (
    <footer className="glass-card mt-8 px-6 py-5 text-sm leading-7 text-slate-400">
      <p className="section-label">Project Signature</p>
      <p>{copy.footer}</p>
    </footer>
  );
}
