import { motion } from "framer-motion";

import UploadSection from "./UploadSection";

const modeCards = ["vedatwin", "eastern_destiny"];

export default function InputForm({ copy, values, isLoading, onChange, onSubmit, onReset }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.05 }}
      className="glass-card p-6 lg:p-7"
    >
      <p className="section-label">{copy.inputTitle}</p>
      <p className="mb-6 max-w-2xl text-sm leading-7 text-slate-400">{copy.inputHint}</p>

      <div className="mb-6">
        <p className="mb-3 text-sm font-medium text-white">{copy.modeLabel}</p>
        <div className="grid gap-3 md:grid-cols-2">
          {modeCards.map((mode) => {
            const option = copy.modeOptions[mode];
            const active = values.readingMode === mode;
            return (
              <button
                key={mode}
                type="button"
                onClick={() => onChange("readingMode", mode)}
                className={`rounded-3xl border p-5 text-left transition ${
                  active
                    ? "border-glow-gold/50 bg-gradient-to-br from-white/10 via-white/5 to-glow-gold/10 shadow-card"
                    : "border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/8"
                }`}
              >
                <p className="section-label !mb-2">{option.title}</p>
                <h3 className="font-display text-2xl text-white">{option.title}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-300">{option.description}</p>
              </button>
            );
          })}
        </div>
      </div>

      <div className="grid gap-5 md:grid-cols-2">
        <Field
          label={copy.name}
          help={copy.nameHelp}
          placeholder={copy.placeholders.name}
          value={values.name}
          required
          onChange={(event) => onChange("name", event.target.value)}
        />
        <Field
          label={copy.birthDate}
          help={copy.birthDateHelp}
          type="date"
          value={values.birthDate}
          required
          onChange={(event) => onChange("birthDate", event.target.value)}
        />
        <Field
          label={copy.birthPlace}
          help={copy.birthPlaceHelp}
          placeholder={copy.placeholders.birthPlace}
          value={values.birthPlace}
          required
          onChange={(event) => onChange("birthPlace", event.target.value)}
        />
        <BirthTimeField
          copy={copy}
          label={copy.birthTime}
          help={copy.birthTimeHelp}
          value={values.birthTime}
          onChange={(nextValue) => onChange("birthTime", nextValue)}
        />
        <SelectField
          label={copy.gender}
          help={copy.genderHelp}
          value={values.gender}
          onChange={(event) => onChange("gender", event.target.value)}
          options={[
            { value: "", label: "--" },
            { value: "female", label: copy.genderOptions.female },
            { value: "male", label: copy.genderOptions.male },
            { value: "non_binary", label: copy.genderOptions.non_binary },
            { value: "prefer_not_to_say", label: copy.genderOptions.prefer_not_to_say },
          ]}
        />
        <Field
          label={copy.timeFocus}
          help={copy.timeFocusHelp}
          placeholder={copy.placeholders.timeFocus}
          value={values.timeFocus}
          onChange={(event) => onChange("timeFocus", event.target.value)}
        />
      </div>

      <div className="mt-5">
        <label className="mb-2 block text-sm font-medium text-white">{copy.question}</label>
        <textarea
          rows={5}
          required
          value={values.question}
          onChange={(event) => onChange("question", event.target.value)}
          placeholder={copy.placeholders.question}
          className="field-shell min-h-36 w-full resize-none"
        />
        <p className="mt-2 text-xs leading-6 text-slate-400">{copy.questionHelp}</p>
      </div>

      <div className="mt-5">
        <label className="mb-2 block text-sm font-medium text-white">{copy.reportLanguage}</label>
        <select value={values.language} onChange={(event) => onChange("language", event.target.value)} className="field-shell w-full">
          <option value="en">English</option>
          <option value="vi">Vietnamese</option>
        </select>
      </div>

      <div className="mt-6">
        <UploadSection
          copy={copy}
          faceImage={values.faceImage}
          palmImage={values.palmImage}
          onFaceChange={(file) => onChange("faceImage", file)}
          onPalmChange={(file) => onChange("palmImage", file)}
        />
      </div>

      <div className="mt-6 flex flex-col gap-3 sm:flex-row">
        <button type="button" onClick={onSubmit} disabled={isLoading} className="primary-button">
          {isLoading ? copy.analyzing : copy.analyze}
        </button>
        <button type="button" onClick={onReset} disabled={isLoading} className="secondary-button">
          {copy.reset}
        </button>
      </div>
    </motion.section>
  );
}

function Field({ label, help, placeholder, type = "text", value, onChange, required = false }) {
  return (
    <div>
      <label className="mb-2 block text-sm font-medium text-white">{label}</label>
      <input
        type={type}
        required={required}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="field-shell w-full"
      />
      <p className="mt-2 text-xs leading-6 text-slate-400">{help}</p>
    </div>
  );
}

function SelectField({ label, help, value, onChange, options }) {
  return (
    <div>
      <label className="mb-2 block text-sm font-medium text-white">{label}</label>
      <select value={value} onChange={onChange} className="field-shell w-full">
        {options.map((option) => (
          <option key={option.value || "empty"} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <p className="mt-2 text-xs leading-6 text-slate-400">{help}</p>
    </div>
  );
}

function BirthTimeField({ copy, label, help, value, onChange }) {
  const { hour12, minute, meridiem } = parseBirthTime(value);
  const minuteOptions = Array.from({ length: 12 }, (_, index) => String(index * 5).padStart(2, "0"));

  const updateTime = (nextHour12, nextMinute, nextMeridiem) => {
    if (!nextHour12) {
      onChange("");
      return;
    }

    const safeMinute = nextMinute || "00";
    const safeMeridiem = nextMeridiem || "AM";
    onChange(to24HourTime(nextHour12, safeMinute, safeMeridiem));
  };

  return (
    <div>
      <div className="mb-3 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <label className="block text-sm font-medium text-white">{label}</label>
        <button
          type="button"
          onClick={() => onChange("")}
          className="inline-flex w-fit items-center rounded-full border border-glow-gold/20 bg-white/5 px-3 py-1.5 text-xs font-medium text-glow-gold/90 transition hover:border-glow-gold/40 hover:text-glow-gold"
        >
          {copy.birthTimeLabels.unknown}
        </button>
      </div>
      <div className="grid gap-3 sm:grid-cols-3">
        <SelectFieldSimple
          label={copy.birthTimeLabels.hour}
          value={hour12}
          onChange={(event) => updateTime(event.target.value, minute, meridiem)}
          options={[{ value: "", label: "--" }, ...Array.from({ length: 12 }, (_, index) => ({ value: String(index + 1), label: String(index + 1) }))]}
        />
        <SelectFieldSimple
          label={copy.birthTimeLabels.minute}
          value={minute}
          onChange={(event) => updateTime(hour12, event.target.value, meridiem)}
          options={minuteOptions.map((item) => ({ value: item, label: item }))}
        />
        <SelectFieldSimple
          label={copy.birthTimeLabels.period}
          value={meridiem}
          onChange={(event) => updateTime(hour12, minute, event.target.value)}
          options={[
            { value: "AM", label: "AM" },
            { value: "PM", label: "PM" },
          ]}
        />
      </div>
      <p className="mt-3 text-xs leading-6 text-slate-400">{help}</p>
    </div>
  );
}

function SelectFieldSimple({ label, value, onChange, options }) {
  return (
    <div>
      <p className="mb-2 text-xs font-medium uppercase tracking-[0.18em] text-slate-400">{label}</p>
      <select value={value} onChange={onChange} className="field-shell w-full">
        {options.map((option) => (
          <option key={`${label}-${option.value || "empty"}`} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}

function parseBirthTime(value) {
  if (!value) {
    return { hour12: "", minute: "00", meridiem: "AM" };
  }

  const [hourText = "0", minuteText = "00"] = value.split(":");
  const hour24 = Number(hourText);
  const meridiem = hour24 >= 12 ? "PM" : "AM";
  const normalizedHour = hour24 % 12 || 12;

  return {
    hour12: String(normalizedHour),
    minute: minuteText.padStart(2, "0").slice(0, 2),
    meridiem,
  };
}

function to24HourTime(hour12, minute, meridiem) {
  const normalizedHour = Number(hour12);
  if (!normalizedHour) {
    return "";
  }

  let hour24 = normalizedHour % 12;
  if (meridiem === "PM") {
    hour24 += 12;
  }

  return `${String(hour24).padStart(2, "0")}:${minute}`;
}
