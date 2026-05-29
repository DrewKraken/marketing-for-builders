# Evaluation methodology

How this project decides whether a skill actually works. The results live in [`RESULTS.md`](RESULTS.md); this doc explains the framework that produced them.

Every skill is evaluated with **two instruments**, because they answer different questions and neither is sufficient alone.

## 1. The deterministic linter — a guardrail

Each skill ships a small, standard-library Python linter (e.g. [`positioning_lint.py`](../skills/positioning/scripts/positioning_lint.py), [`landing_lint.py`](../skills/landing-copy/scripts/landing_lint.py), [`launch_lint.py`](../skills/launch-kit/scripts/launch_lint.py)) that flags specific, known failure patterns — buzzwords, a missing audience, a bare-name headline, competing CTAs, upvote-begging, a tagline over the platform limit.

- **Role:** a *floor*, not a quality score. It catches specific regressions, runs free in CI on every commit, is perfectly reproducible, and is auditable (you can read every rule).
- **Limit:** it only sees what it was told to look for. It cannot judge whether a headline is *compelling*, a voice is *right for the channel*, or a launch is aimed at the *wrong audience*. For skills whose value is judgment rather than rule-compliance, a strong base model already passes the checks — so a thin linter gap means the instrument is blind, **not** that the skill is weak. (Launch-kit is the cautionary case: a near-tie on the linter, a clean sweep under the judge.)

## 2. The blind LLM-judge panel — the quality benchmark

For the question that actually matters — *does the skill produce better output than not using it?* — we run a blind head-to-head:

- Each test case is produced two ways: a **baseline** arm (a capable model, **no skill**, sandboxed so it can't read the skill from the repo — confirmed `tool_uses: 0`) and a **with-skill** arm (same model, given only the skill + the same input).
- A **panel of 3 independent judges** scores each case. The two outputs are labelled **A/B with the order randomized per case**, the judges are told to score *quality* (not rule-compliance), and they are **not told that a skill was involved**.
- Each judge scores both drafts 1–5 on task-specific dimensions and picks an overall winner. We report the majority verdict, the vote count, and average scores.

- **Role:** measures the real bar; generalizes across skills with one rubric.
- **Run on demand**, not in CI — it costs tokens and is non-deterministic, so it's a benchmark you run per round, not a per-PR gate.

## Why both

| | Linter | Judge panel |
|---|---|---|
| Question | "does it break a known rule?" | "is it actually better?" |
| Determinism | perfect | noisy (panel + randomization needed) |
| Cost | free, every commit (CI) | tokens, on demand |
| Role | regression guardrail / floor | quality benchmark / headline |

Think unit-tests-and-lint vs. an integration benchmark. A serious eval stack wants the cheap deterministic floor *and* the quality benchmark.

## Honest limits (they apply to every judge result here)

- **Claude-judging-Claude — addressed with a cross-model judge.** Both arms and the primary judges are Claude, which carries a self-preference risk (mitigated by blinding, per-case A/B randomization, substantive reasons, and the skill winning from *both* positions). To remove the objection, an **independent model family (GPT/Codex)** re-judged the same 15 pairs blind: it preferred the skill in **14/15** (the lone exception is discussed in the launch-kit results). Across both panels that's **29/30 blind verdicts favoring the skill, from two independent model families** — the conclusion does not depend on Claude judging Claude. The project's author also reviewed all 15 pairs and picked the skill-assisted version every time (a non-blind read — see the note in [`RESULTS.md`](RESULTS.md)); a *blind* human pass on fresh material is the one remaining hardening step.
- **The rubric reflects the skill's own principles.** Each rubric's "gate" dimension encodes what the channel/medium rewards — the same thing the skill teaches. So the panel fairly tests "which output better fits what works," not whether that philosophy is correct in the abstract. The more neutral dimensions (clarity, persuasion) also favor the skill.
- **Small N, Claude-judged, directional.** N=5 per skill, one round. These are honest directional signals, not a large benchmark.
- **Score absolutes are noisy; trust the relative result.** LLM judges compare far more reliably than they grade. We target a robust *relative* win over baseline, not an absolute score — chasing "18/20" would just overfit the judge.

## Cross-skill summary (Round 1, Claude Sonnet, blind 3-judge panels)

| Skill | Linter findings (baseline → skill) | Judge verdict | Judge avg (skill vs baseline /20) |
|---|:--:|:--:|:--:|
| [positioning](RESULTS.md#positioning) | 21 → 0 | 5/5 (15/15) | 16.1 vs 8.0 |
| [landing-copy](RESULTS.md#landing-copy) | 7 → 0 | 5/5 (15/15) | 17.7 vs 11.5 |
| [launch-kit](RESULTS.md#launch-kit) | 1 → 0 | 5/5 (15/15) | 16.9 vs 12.6 |

Both instruments **rank the three skills the same way** (positioning > landing-copy > launch-kit by gap size) even though they disagree on launch-kit's absolute verdict — independent corroboration that the ordering is real, and a concrete illustration of why the linter alone would have undersold launch-kit.

**Cross-model check:** an independent GPT/Codex judge, blind, re-judged all 15 pairs and agreed with the Claude panel on **14** of them (the one exception: it preferred the baseline's longer Product Hunt tagline, which actually violates PH's 60-char limit — a judge missing a platform constraint, not the skill losing on merit). **29/30 blind verdicts across two model families favor the skill.**
