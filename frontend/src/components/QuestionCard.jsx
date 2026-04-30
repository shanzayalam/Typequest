import LikertScale from "./LikertScale";

export default function QuestionCard({
  question,
  answer,
  onAnswer,
  onNext,
  questionNumber,
  total
}) {
  return (
    <section className="glass-panel rounded-[2rem] p-8">
      <div className="mb-6 flex items-center justify-between text-sm uppercase tracking-[0.25em] text-slate-300">
        <span>Question {questionNumber}</span>
        <span>{total} Total</span>
      </div>
      <h2 className="mb-8 max-w-3xl text-2xl font-semibold leading-relaxed text-mist sm:text-3xl">
        {question.prompt}
      </h2>
      <LikertScale value={answer} onChange={onAnswer} />
      <div className="mt-8 flex justify-end">
        <button
          type="button"
          onClick={onNext}
          disabled={!answer}
          className="rounded-full bg-gradient-to-r from-signal via-neon to-ocean px-6 py-3 font-semibold text-white shadow-glow transition hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Continue
        </button>
      </div>
    </section>
  );
}
