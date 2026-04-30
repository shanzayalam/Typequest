import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer
} from "recharts";

const FUNCTION_LABELS = {
  Ni: "Insight (Ni)",
  Ne: "Creativity (Ne)",
  Si: "Stability (Si)",
  Se: "Presence (Se)",
  Ti: "Logic (Ti)",
  Te: "Execution (Te)",
  Fi: "Values (Fi)",
  Fe: "Connection (Fe)"
};

const TYPE_FULL_NAMES = {
  INTJ: "Introverted, Intuitive, Thinking, Judging",
  INFJ: "Introverted, Intuitive, Feeling, Judging",
  ENTJ: "Extraverted, Intuitive, Thinking, Judging",
  ENFJ: "Extraverted, Intuitive, Feeling, Judging",
  INTP: "Introverted, Intuitive, Thinking, Perceiving",
  INFP: "Introverted, Intuitive, Feeling, Perceiving",
  ENTP: "Extraverted, Intuitive, Thinking, Perceiving",
  ENFP: "Extraverted, Intuitive, Feeling, Perceiving",
  ISTJ: "Introverted, Sensing, Thinking, Judging",
  ISFJ: "Introverted, Sensing, Feeling, Judging",
  ESTJ: "Extraverted, Sensing, Thinking, Judging",
  ESFJ: "Extraverted, Sensing, Feeling, Judging",
  ISTP: "Introverted, Sensing, Thinking, Perceiving",
  ISFP: "Introverted, Sensing, Feeling, Perceiving",
  ESTP: "Extraverted, Sensing, Thinking, Perceiving",
  ESFP: "Extraverted, Sensing, Feeling, Perceiving"
};

function functionData(functionStrengths) {
  return Object.entries(functionStrengths).map(([functionName, value]) => ({
    function: functionName,
    label: FUNCTION_LABELS[functionName] || functionName,
    value
  }));
}

export default function ResultDashboard({ result }) {
  const radarData = functionData(result.function_strengths);
  const primaryFullName = TYPE_FULL_NAMES[result.primary_type] || result.primary_type;
  const secondaryFullName = TYPE_FULL_NAMES[result.secondary_type] || result.secondary_type;

  return (
    <section className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
      <div className="glass-panel relative overflow-hidden rounded-[2rem] p-6">
        <div className="absolute -left-10 top-8 h-28 w-28 rounded-full bg-signal/30 blur-3xl" />
        <div className="absolute -right-8 bottom-10 h-32 w-32 rounded-full bg-neon/25 blur-3xl" />
        <div className="mb-6 flex items-end justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.25em] text-slate-300">Function Map</p>
            <h2 className="mt-2 text-3xl font-semibold text-mist">Your Personality Energy Map</h2>
          </div>
          <div className="glass-chip rounded-full px-4 py-2 text-sm text-signal">
            Fit ratio: {result.fit_ratio}%
          </div>
        </div>
        <div className="radar-pulse relative h-[360px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData}>
              <defs>
                <linearGradient id="typequestRadarFill" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#29d8ff" stopOpacity={0.72} />
                  <stop offset="55%" stopColor="#ff45c7" stopOpacity={0.48} />
                  <stop offset="100%" stopColor="#7f5cff" stopOpacity={0.6} />
                </linearGradient>
              </defs>
              <PolarGrid stroke="rgba(246, 237, 255, 0.16)" />
              <PolarAngleAxis dataKey="label" stroke="#f6edff" tick={{ fontSize: 12 }} />
              <PolarRadiusAxis angle={90} domain={[0, 100]} tick={false} axisLine={false} />
              <Radar
                dataKey="value"
                stroke="#29d8ff"
                fill="url(#typequestRadarFill)"
                fillOpacity={1}
                strokeWidth={2.5}
                animationDuration={1400}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-6">
        <div className="glass-panel rounded-[2rem] p-6">
          <p className="text-sm uppercase tracking-[0.25em] text-slate-300">Result</p>
          <div className="mt-4 flex items-end gap-4">
            <h2 className="text-5xl font-bold text-mist">{result.primary_type}</h2>
            <p className="mb-2 text-slate-200">Primary Type</p>
          </div>
          <p className="mt-2 text-sm leading-6 text-slate-200">{primaryFullName}</p>
          <p className="mt-6 text-sm text-slate-300">Runner up</p>
          <div className="glass-chip mt-2 rounded-2xl px-4 py-3">
            <div className="flex items-center justify-between gap-4">
              <span className="text-xl font-semibold text-white">{result.secondary_type}</span>
              <span className="text-sm text-ember">{result.fit_ratio}% match</span>
            </div>
            <p className="mt-2 text-sm text-slate-200">{secondaryFullName}</p>
          </div>
          <p className="mt-6 text-sm leading-7 text-slate-100">{result.summary}</p>
        </div>

        <div className="glass-panel rounded-[2rem] p-6">
          <p className="text-sm uppercase tracking-[0.25em] text-slate-300">Top Functions</p>
          <div className="mt-4 space-y-3">
            {radarData
              .sort((left, right) => right.value - left.value)
              .slice(0, 4)
              .map((item) => (
                <div key={item.function}>
                  <div className="mb-1 flex items-center justify-between text-sm">
                    <span className="font-medium text-mist">{item.label}</span>
                    <span className="text-slate-200">{item.value}%</span>
                  </div>
                  <div className="h-2 overflow-hidden rounded-full bg-white/10">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-signal via-neon to-ocean"
                      style={{ width: `${item.value}%` }}
                    />
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </section>
  );
}
