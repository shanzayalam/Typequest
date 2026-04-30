const OPTIONS = [
  { value: 1, label: "Strongly Disagree" },
  { value: 2, label: "Disagree" },
  { value: 3, label: "Neutral" },
  { value: 4, label: "Agree" },
  { value: 5, label: "Strongly Agree" }
];

export default function LikertScale({ value, onChange }) {
  return (
    <div className="grid gap-3 sm:grid-cols-5">
      {OPTIONS.map((option) => {
        const active = value === option.value;
        return (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            className={`rounded-2xl border px-4 py-3 text-sm transition ${
              active
                ? "border-signal bg-signal/15 text-white"
                : "border-white/10 bg-white/5 text-slate-300 hover:border-ocean/50 hover:bg-white/10"
            }`}
          >
            <span className="block text-base font-semibold">{option.value}</span>
            <span className="block text-xs">{option.label}</span>
          </button>
        );
      })}
    </div>
  );
}
