export default function UploadSection({
  copy,
  faceImage,
  palmImage,
  onFaceChange,
  onPalmChange,
}) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
        <label className="mb-2 block text-sm font-medium text-white">{copy.faceUpload}</label>
        <input
          type="file"
          accept="image/png,image/jpeg,image/jpg"
          onChange={(event) => onFaceChange(event.target.files?.[0] ?? null)}
          className="block w-full text-sm text-slate-300 file:mr-4 file:rounded-xl file:border-0 file:bg-glow-violet/20 file:px-4 file:py-2 file:text-sm file:font-medium file:text-white"
        />
        <p className="mt-3 text-xs leading-6 text-slate-400">{copy.faceHelp}</p>
        {faceImage ? <p className="mt-2 text-xs text-glow-gold">{faceImage.name}</p> : null}
      </div>

      <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
        <label className="mb-2 block text-sm font-medium text-white">{copy.palmUpload}</label>
        <input
          type="file"
          accept="image/png,image/jpeg,image/jpg"
          onChange={(event) => onPalmChange(event.target.files?.[0] ?? null)}
          className="block w-full text-sm text-slate-300 file:mr-4 file:rounded-xl file:border-0 file:bg-glow-violet/20 file:px-4 file:py-2 file:text-sm file:font-medium file:text-white"
        />
        <p className="mt-3 text-xs leading-6 text-slate-400">{copy.palmHelp}</p>
        {palmImage ? <p className="mt-2 text-xs text-glow-gold">{palmImage.name}</p> : null}
      </div>
    </div>
  );
}

