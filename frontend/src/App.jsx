import { useEffect, useState } from "react";
import ProgressBar from "./components/ProgressBar";
import QuestionCard from "./components/QuestionCard";
import ResultDashboard from "./components/ResultDashboard";
import { adaptQuiz, getResult, startQuiz } from "./lib/api";

const MIDPOINT = 15;

function LearnModal({ open, onClose }) {
  if (!open) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/55 p-4 backdrop-blur-sm">
      <div className="glass-panel relative w-full max-w-2xl rounded-[2rem] p-8">
        <button
          type="button"
          onClick={onClose}
          className="glass-chip absolute right-5 top-5 rounded-full px-3 py-1 text-sm text-slate-200"
        >
          Close
        </button>
        <p className="text-sm uppercase tracking-[0.3em] text-ember">Learn How It Works</p>
        <h2 className="mt-4 max-w-xl text-3xl font-semibold text-mist">TypeQuest scores your cognitive functions first.</h2>
        <div className="mt-6 space-y-4 text-sm leading-7 text-slate-200">
          <p>
            Instead of jumping straight to letters like J or P, TypeQuest scores function patterns such as Ni, Ne, Ti,
            and Fe across your answers first.
          </p>
          <p>
            After the first 15 questions, the backend checks which function pair is still too close and chooses the next
            15 questions to separate those possibilities more clearly.
          </p>
          <p>
            Your 4-letter type is then derived from the best-fitting function stack. For example, the stack Ni-Te-Fi-Se
            maps to INTJ.
          </p>
        </div>
      </div>
    </div>
  );
}

function Hero() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <section className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-end">
        <div>
          <p className="text-6xl font-semibold tracking-tight text-mist sm:text-7xl lg:text-8xl">TypeQuest</p>
          <h1 className="mt-4 max-w-4xl text-3xl font-semibold leading-tight text-mist sm:text-4xl">
            Find your MBTI type by looking at how you think, decide, and notice patterns.
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
            TypeQuest scores your cognitive functions first, then turns that pattern into the best-fitting 4-letter
            type.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <button
              type="button"
              onClick={() => setOpen(true)}
              className="glass-chip rounded-full px-5 py-3 text-sm font-medium text-mist transition hover:border-neon/60 hover:bg-white/15"
            >
              Learn How It Works
            </button>
            <div className="glass-chip rounded-full px-5 py-3 text-sm text-slate-200">
              30 adaptive prompts
            </div>
            <div className="glass-chip rounded-full px-5 py-3 text-sm text-slate-200">
              Function-first scoring
            </div>
          </div>
        </div>
        <div className="glass-panel float-glow relative overflow-hidden rounded-[2rem] p-6">
          <div className="absolute -right-10 top-0 h-36 w-36 rounded-full bg-neon/30 blur-3xl" />
          <div className="absolute bottom-0 left-0 h-36 w-36 rounded-full bg-signal/25 blur-3xl" />
          <p className="text-sm uppercase tracking-[0.25em] text-slate-300">Why It Feels Different</p>
          <div className="mt-4 space-y-3 text-sm leading-7 text-slate-200">
            <p>Questions focus on how you notice patterns, make decisions, and respond to people and real-life events.</p>
            <p>Halfway through, TypeQuest shifts toward the areas that are still too close to call.</p>
            <p>The final result is written to feel clear and relatable, not overly technical.</p>
          </div>
        </div>
      </section>
      <LearnModal open={open} onClose={() => setOpen(false)} />
    </>
  );
}

export default function App() {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [index, setIndex] = useState(0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [adaptHint, setAdaptHint] = useState(null);

  useEffect(() => {
    async function boot() {
      try {
        const payload = await startQuiz();
        setQuestions(payload.questions);
      } catch (err) {
        setError(err.message || "Unable to load quiz.");
      } finally {
        setLoading(false);
      }
    }

    boot();
  }, []);

  const currentQuestion = questions[index];
  const currentAnswer = currentQuestion ? answers[currentQuestion.id] : null;

  function serializeAnswers(answerMap) {
    return Object.entries(answerMap).map(([question_id, value]) => ({
      question_id,
      value
    }));
  }

  async function handleNext() {
    if (!currentQuestion) {
      return;
    }

    const nextIndex = index + 1;

    if (nextIndex === MIDPOINT && questions.length === MIDPOINT) {
      setSubmitting(true);
      try {
        const payload = await adaptQuiz(serializeAnswers(answers));
        setAdaptHint(payload.hint);
        setQuestions((existing) => [...existing, ...payload.questions]);
        setIndex(nextIndex);
      } catch (err) {
        setError(err.message || "Unable to adapt quiz.");
      } finally {
        setSubmitting(false);
      }
      return;
    }

    if (nextIndex >= questions.length) {
      setSubmitting(true);
      try {
        const payload = await getResult(serializeAnswers(answers));
        setResult(payload);
      } catch (err) {
        setError(err.message || "Unable to score quiz.");
      } finally {
        setSubmitting(false);
      }
      return;
    }

    setIndex(nextIndex);
  }

  function handleAnswer(value) {
    setAnswers((existing) => ({
      ...existing,
      [currentQuestion.id]: value
    }));
  }

  return (
    <main className="min-h-screen px-4 py-8 text-white sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-10">
        <Hero />

        {loading ? (
          <div className="glass-panel rounded-[2rem] p-8 text-slate-200">
            Loading TypeQuest...
          </div>
        ) : error ? (
          <div className="rounded-[2rem] border border-rose-400/30 bg-rose-500/10 p-8 text-rose-100 shadow-panel">
            {error}
          </div>
        ) : result ? (
          <ResultDashboard result={result} />
        ) : (
          <section className="space-y-6">
            <ProgressBar current={index + 1} total={questions.length || 30} />
            {adaptHint ? (
              <div className="glass-panel rounded-2xl px-5 py-4 text-sm text-slate-100">
                Adaptive focus: {adaptHint.likely_axis.replace("_vs_", " vs ")}. {adaptHint.notes}
              </div>
            ) : null}
            {currentQuestion ? (
              <QuestionCard
                question={currentQuestion}
                answer={currentAnswer}
                onAnswer={handleAnswer}
                onNext={handleNext}
                questionNumber={index + 1}
                total={questions.length}
              />
            ) : null}
            {submitting ? <div className="text-sm text-slate-300">Reading your function pattern...</div> : null}
          </section>
        )}
      </div>
    </main>
  );
}
