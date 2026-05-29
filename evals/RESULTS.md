# Evaluation results

Do these skills actually produce better output than not using them? This is the evidence, run honestly — including the limits and the cases where the gap is small.

Each skill is evaluated two ways: a **deterministic linter** (a guardrail, free in CI) and a **blind LLM-judge panel** (the quality benchmark — 3 judges/case, randomized A/B, judging quality not rule-compliance), with an **independent GPT/Codex judge** corroborating cross-model. See [`METHODOLOGY.md`](METHODOLOGY.md). The first three skills won their blind panels **5/5 on the first pass** (14/15 cross-model). **`cold-outreach` failed its first round 2/5, was reworked, then cleared 5/5** on held-out *and* fresh cases (confirmed 5/5 cross-model) — the eval doing exactly its job.

- [`positioning`](#positioning) — the biggest lift: beat baseline 5/5 on the linter, and 5/5 (15/15) under the judge panel with the widest quality gap (16.1 vs 8.0 / 20).
- [`landing-copy`](#landing-copy) — real lift, clearest on READMEs; the judge panel preferred it 5/5 (15/15) by a *wider* margin than the linter showed.
- [`launch-kit`](#launch-kit) — judge panel preferred it 5/5 (15/15), but the linter saw almost none of that gap — a case study in matching the metric to the skill.
- [`cold-outreach`](#cold-outreach) — the honest one: it *lost* its first round (2/5) against a frontier baseline, was reworked, then won 5/5 on held-out **and** fresh unseen cases (5/5 cross-model). Measures reply *quality*, not live reply rates — those come via the living-results plan.

**The author's read.** Full transparency: I've seen which draft is which, so this isn't a blind score — and I'm a technical founder, not a copywriter (closing that exact gap is the point of this project). Even so, across the first three skills' 15 pairs I picked the skill-assisted version over the cold, no-skill one every time, and it wasn't close. You don't need to be a marketing expert to see which one you'd actually ship. The blind cross-model panels carry the statistical weight; this is the person the skill is built for confirming the gap is just as obvious from the inside.

---

# positioning

Does the `positioning` skill actually produce better positioning than not using it?

## Method

Each product blurb in [`cases.md`](cases.md) is run two ways and compared:

- **Baseline** — a capable model asked to write positioning, **no skill**.
- **With skill** — the same model, given only the skill and the same blurb (no other context), following the skill's method and its [linter](../skills/positioning/scripts/positioning_lint.py).

**Scoring:** the repo's deterministic `positioning_lint.py` (objective — counts issues like buzzwords, missing audience, feature-speak, overlong copy; lower is better), plus a qualitative read.

**Run:** Round 1 — Claude Sonnet, skill v0.1, 5 cases, 2 arms.

## Honest limits (read these)

- **N = 5.** This is a baseline, not a large benchmark. Treat it as a directional signal.
- **The qualitative verdict is the author's judgment**, not a blind panel. Spot-check the before/after yourself below.
- **Part of the linter result is self-referential** — the skill instructs the model to run the linter and revise until clean, so "0 findings" partly reflects that the skill *uses* its own tool. The baseline never had it. The more meaningful differences are qualitative (audience, outcome, the named alternative).
- **Reproduce it:** an optional, bring-your-own-key harness is the intended way to re-run this independently. Numbers will vary run to run — that's normal for LLM evals; the *relative* lift is what should reproduce.

## Results

Lint findings per case (one-liner + value proposition; lower is better):

| Case | Shape | Baseline | With skill |
|------|-------|:--------:|:----------:|
| InvoiceParser Pro | B2B SaaS | 5 | **0** |
| DeployKit | dev tool / CLI | 5 | **0** |
| Streaktastic | consumer app | 4 | **0** |
| DentalFlow | vertical SaaS | 4 | **0** |
| PayBridge | payments API | 3 | **0** |

In all five, the baseline led with the *mechanism* ("AI-powered platform…"), piled on features, and addressed a broad "everyone" audience. With the skill, each result named a sharp audience, led with the *outcome*, and positioned against the *real alternative*.

## Before → after (the one-liners)

**InvoiceParser Pro**
- Baseline: *"Every invoice, extracted and posted in seconds."*
- With skill: *"Bookkeepers: cuts invoice entry from minutes to zero — InvoiceParser Pro posts it for you."*

**DeployKit**
- Baseline: *"Ship anywhere. One binary. Zero drama."*
- With skill: *"Ship to your servers in seconds — engineers drop the deploy scripts and ship."* (narrowed to VM / bare-metal teams who've rejected Kubernetes; alternative = hand-rolled shell scripts)

**Streaktastic**
- Baseline: *"Build habits together. Break none alone."* (it also silently renamed the product)
- With skill: *"For people who keep abandoning habit apps: streak freezes and friend leaderboards help you finally make habits stick."*

**DentalFlow**
- Baseline: *"Run your whole practice. From anywhere."*
- With skill: *"Dental office managers: cuts no-shows and speeds up insurance payments — no server, no IT vendor."* (narrowed to managers of 2+ locations; named the real rivals — legacy Dentrix / Eaglesoft)

**PayBridge**
- Baseline: *"Payments infrastructure developers actually want to build on."*
- With skill: *"The payments API that lets developers ship billing, subscriptions, and marketplace payouts without the PCI and fraud overhead."* (alternative = building it yourself on a raw processor)

## Judge panel (added 2026-05-29)

A blind 3-judge panel scored the baseline vs. skill **one-liners** (positioning's headline deliverable) for each case — A/B order randomized, judging quality, not told a skill was involved. **The skill swept 5/5 (15/15 votes)**, average **16.1/20 vs 8.0** — the widest quality gap of the three skills. Judges scored baseline one-liners as low as **1/5 on audience** ("names no one," "could be any product") — exactly the failure positioning exists to fix. This independently confirms the linter's 5/5 with a blind quality judge. Limits in [`METHODOLOGY.md`](METHODOLOGY.md): Claude-judged, rubric reflects positioning principles, N=5, judged at the one-liner level (full outputs weren't saved this round).

## Takeaway

Across five deliberately different product shapes, the skill consistently replaced mechanism-first, feature-piled, broad-audience copy with audience-specific, outcome-led positioning that named the real alternative. Consistent lift — preliminary, but the same pattern every time, and now confirmed by a blind judge panel as well as the linter.

---

# landing-copy

Does the `landing-copy` skill produce a better landing page or README than not using it? The honest answer: **yes — consistently, across every product shape — but the per-case margin is modest, and we're candid about why.** Unlike positioning (where unaided copy fails dramatically), a capable model already writes a *decent* landing page on its own. The skill's edge is consistency and discipline, and it's clearest on READMEs.

## Method

Same two-arm design as above (**baseline**, no skill, vs **with skill**, same model + only the skill and blurb), on the same 5 product shapes, each with a fixed deliverable type (landing page or README). **Run:** Round 1 — Claude Sonnet, skill v0.1, 5 cases, 2 arms.

## Results

Lint findings per case (lower is better):

| Case | Deliverable | Baseline | With skill | What the baseline tripped |
|------|-------------|:--------:|:----------:|---------------------------|
| InvoiceParser Pro | landing page | 1 | **0** | competing CTAs |
| DeployKit | README | 2 | **0** | bare-name headline, no audience |
| Streaktastic | landing page | 1 | **0** | no audience named |
| DentalFlow | landing page | 2 | **0** | competing CTAs, a buzzword |
| PayBridge | README | 1 | **0** | bare-name headline |
| **Total** | | **7** | **0** | |

Across five different shapes, unaided copy tripped at least one basic first-impression failure **every time**; the skill cleared all of them.

## The clearest win: READMEs

Both README baselines made the same canonical mistake — leading with a bare product-name H1 and a feature list:

**DeployKit (baseline → with skill)**
- `# DeployKit` → `# DeployKit — ship web apps to your own servers in one command`

**PayBridge (baseline → with skill)**
- `# PayBridge` → `# PayBridge — add payments to your app in an afternoon`

In both, the skill turned the most-read line into the value proposition, named the audience in the subhead, and moved a copy-pasteable quickstart up top — the difference between a developer bouncing and a developer trying it.

## Honest limits (read these)

- **Modest per-case margins.** The findings gap is 1–2 per case, not positioning's 3–5. Writing a competent landing page is well within a capable model's reach unprompted, so the *consistency* (5/5) is the signal here, not a large per-case delta.
- **Part of the result is the linter checking its own discipline.** The skill instructs running the linter and revising to clean, so a skill "0" partly reflects that it uses its own tool; the baseline never had it. The findings the baseline tripped (competing CTAs, bare-name headlines, missing audience) are nonetheless real failures a reader would notice.
- **The linter under-measures the qualitative gap.** It still can't see *sprawl* — baselines tended to kitchen-sink every feature into its own section, while the skill produced roughly half the length with three benefit-led sections plus proof. That restraint is real and not captured by a number.
- **Methodology note.** In a first pass, baseline agents with filesystem access discovered and applied the skill on their own, contaminating the "no-skill" arm. We caught it, discarded those runs, and re-ran all baselines sandboxed from the skill — the kind of leak that silently inflates eval numbers.
- **N = 5, Claude-judged.** Directional, not a large benchmark.

## Judge panel (added 2026-05-29)

A blind 3-judge panel scored the **full** baseline vs. skill pages — A/B order randomized, judging quality, not told a skill was involved. **The skill swept 5/5 (15/15 votes)**, average **17.7/20 vs 11.5** — a *wider* gap than the linter's 7-findings story implied. The two READMEs were blowouts (PayBridge 20 vs 10.7; DeployKit 18.7 vs 11) on the bare-name-H1 + buried-quickstart failure; on landing pages judges hit the baselines for competing CTAs and feature sprawl (the structure dimension the linter only partly sees). So the judge **confirms and enlarges** the qualitative read above — the linter under-measured the real lift. Limits in [`METHODOLOGY.md`](METHODOLOGY.md).

## Takeaway

`landing-copy` produces a measurable, consistent improvement on all five shapes, and a clear, demonstrable win on **READMEs**, where unaided copy reliably leads with the product name and a feature dump instead of the value and the audience. On polished marketing landing pages a strong model is already decent, so there the skill's contribution is discipline — one CTA, a named audience, less sprawl — which the blind judge panel rewarded more clearly than the linter did. We'd rather show that honestly than overstate it.

---

# launch-kit

Does the `launch-kit` skill produce a better launch post than not using it? **Yes — a blind judge panel preferred the skill's post in all 5 cases (15/15 votes).** This skill is also a lesson in *measurement*: our deterministic linter saw almost none of that gap, because rule-compliance is the wrong proxy for launch quality. Both results are below; the judge sweep is the headline.

## Method

Two arms, same as the other skills: **baseline** (no skill, sandboxed from the repo) vs **with skill** (same model + only the skill and blurb). The 5 product blurbs from [`cases.md`](cases.md) are each fixed to **one channel**, mapped across the surfaces to exercise each once: DeployKit → Show HN, PayBridge → Product Hunt, Streaktastic → Reddit, InvoiceParser Pro → LinkedIn, DentalFlow → X (a deliberate weak-fit, to test channel judgment). **Run:** Round 1 — Claude Sonnet, skill v0.1.0, 5 cases.

Scored two ways: (1) the channel-aware [`launch_lint.py`](../skills/launch-kit/scripts/launch_lint.py) (objective, lower = better); (2) a **blind LLM-judge panel** — 3 independent judges per case, A/B order randomized, judging post *quality* (not rule-compliance) and not told a skill was involved, scoring clarity / channel-gate / community-fit / persuasion and picking a winner.

## Result 1 — the judge panel (the real quality test)

| Case | Channel | Skill preferred? | Votes | Skill avg /20 | Baseline avg /20 |
|------|---------|:----------------:|:-----:|:-------------:|:----------------:|
| DeployKit | Show HN | yes | 3/3 | 17.3 | 13.7 |
| PayBridge | Product Hunt | yes | 3/3 | 15.7 | 13.0 |
| Streaktastic | Reddit | yes | 3/3 | 19.0 | 13.0 |
| InvoiceParser Pro | LinkedIn | yes | 3/3 | 16.7 | 12.3 |
| DentalFlow | X | yes | 3/3 | 16.0 | 11.0 |
| **Overall** | | **5/5** | **15/15** | **16.9** | **12.6** |

The skill won from **both** A and B positions, so it's content, not order bias. The gap concentrated in the **channel gate, community-fit, and persuasion**; **clarity was ~tied** — which is the skill's whole thesis: a strong model already writes *clearly*, so the skill's job is to make the post *land for the channel*. Judges repeatedly noted the skill led with the outcome and a builder's voice, while the baseline defaulted to a feature-list / press-release register. (One judge even rated the DeployKit baseline's "why not Kubernetes" reasoning *more persuasive* — but still picked the skill overall for its title and voice. The baseline isn't bad; the skill is consistently better.)

**Cross-model check:** an independent GPT/Codex judge agreed with the skill on **4 of the 5** launch cases. Its lone dissent was Product Hunt — it preferred the baseline's longer tagline for "broader payoff," but that tagline is **100 characters, over PH's real 60-char cap** (the skill's is 53). So the cross-model judge missed a platform constraint the skill respects. It did surface one fair, actionable critique — the skill's PH maker comment is a single dense paragraph — logged as a Round 1.1 tweak.

## Result 2 — the linter (and why it disagreed)

| Case | Channel | Baseline | With skill |
|------|---------|:--------:|:----------:|
| All five | — | **1** | **0** |

The linter found exactly one issue across all five baselines — PayBridge's Product Hunt tagline (a 100-char run-on; cap is 60; the skill cut it to 53). The always-on guardrail checks (upvote-begging, hype) never fired, because the Sonnet baselines were already disciplined. **That near-tie is not evidence the skill barely helps — it's evidence the linter can't see launch quality.** A title that buries the value, a press-release voice, the wrong channel: none are deterministically detectable, and all are exactly what the judges caught. The linter earns its keep as a guardrail (it bites on hype-prone drafts) and on the one gate it *can* measure (tagline length) — not as a quality score.

## Honest limits (read these)

- **Claude-judging-Claude.** Both arms are Sonnet outputs and the judges are Claude — possible house-style self-preference. Mitigated by blinding, position-randomization, and substantive channel-grounded reasons, but a human or cross-model judge would strengthen it.
- **The rubric's "gate" dimension reflects the same channel principles the skill encodes** — so this fairly tests "which post better fits what the channel rewards," not whether the gate philosophy itself is correct. The more neutral dimensions (clarity, community-fit, persuasion) also favored the skill.
- **The linter has a known try-link false-negative** (it passed the DeployKit baseline on the substring `pip install` *inside* "No pip install"). A safe-direction miss; noted, not hidden.
- **N = 5, one channel each, clean blurbs.** Directional, not a benchmark. A planned Round 2 feeds deliberately hype-laden "bad first draft" inputs (where the guardrail checks bite) and ideally adds a cross-model judge.

## Takeaway

On the question that matters — does the skill clearly beat unaided frontier launch work? — the blind panel says yes, 5/5. The more interesting story for an eval-minded reader is the **disagreement between the two metrics**: a deterministic linter rated it a near-tie while a quality judge rated it a sweep. We kept both and let the judge be the headline, because the linter was measuring etiquette and the bar is quality.

---

# cold-outreach

This is the skill that **failed its first eval — and that's why it's here.** Cold outreach is the hardest thing in the package to do better than a frontier model, because AI made volume free (so generic blasts are everywhere and get filtered) and the base model already writes a competent, personalized email unprompted. Round 1 proved it: the skill *lost*. We diagnosed why, reworked it, and it now clears the bar — confirmed on unseen cases and cross-model. The whole arc is the most honest evidence in this repo that the evals drive the work, not the reverse.

## Method

Two arms (sandboxed **baseline** vs **with skill**), 5 cases = (product → a specific target + a real trigger), spanning B2B and B2G. Both arms write a cold email + a short follow-up sequence. Scored by the channel/`outreach_lint.py` linter (deliverability + spam tells) and a **blind 3-judge panel** (relevance / credibility / ask / reply-likelihood). **Run:** Claude Sonnet.

## Round 1 — the skill lost (and the eval caught it)

| Round 1 | Result |
|---|---|
| Linter | baseline 9 findings → skill 0 (baselines left `[Name]` placeholders, ran long, no opt-out) |
| **Blind judge panel** | **skill 2/5** — won 2, **lost 2** (incl. B2G 0–3), tied 1. Average **14.8 vs 14.7 — dead even.** |

Against a frontier baseline, the skill was no better. Worse, two of our own choices *hurt*: a "graceful opt-out" rule that the model dutifully stamped onto *every* follow-up (a template tell the judges flagged), and a "subject = the trigger" rule that produced flat, low-open subjects. The B2G mode was too generic. We report this in full rather than quietly fixing it, because the failure is the point.

## The rework (structural, not judge-chasing)

We fixed root causes, not per-comment tweaks: the linter now has a `--followup` mode so the opt-out belongs **once** (the linter had *induced* the tic); added an **"one insight" requirement** (a non-obvious observation about the recipient — the ~9%→18% specificity lever); added real subject-line craft (short, lowercase, specific, often a question); and rebuilt **B2G mode** (concrete credibility signals, a "right person?" redirect, slower cadence, lower-pressure ask).

## Round 2 — cleared the bar, on held-out *and* fresh cases

To guard against overfitting to the cases we diagnosed, we re-ran the **3 cases it lost/tied** (held-out regression) **and 2 fresh cases the skill had never seen** (a B2B billing API, a B2G permitting platform):

| Case | Round 1 | Round 2 | skill vs base /20 |
|------|---------|---------|:--:|
| DeployKit (held-out) | baseline 2–1 | **skill 3–0** | 16.3 / 12.0 |
| ClearComm911 — B2G (held-out) | baseline 0–3 | **skill 3–0** | 18.7 / 10.7 |
| DentalFlow (held-out) | tie | **skill 3–0** | 15.7 / 11.3 |
| MeterFlow — B2B (**fresh**) | — | **skill 3–0** | 16.3 / 13.3 |
| PermitPilot — B2G (**fresh**) | — | **skill 2–1** | 16.0 / 15.7 |
| **Total** | skill 2/5 | **skill 5/5, 14/15 votes** | |

It wins the **fresh** cases too, so it generalizes — it isn't tuned to the diagnosis set. The B2G fix is the standout: 0–3 on the 911 case → wins B2G on both a held-out (3–0) and a fresh (2–1) scenario. **Cross-model (GPT/Codex), same 5 pairs, blind: skill 5/5** — and it preferred the skill *decisively* on the fresh B2G case that the Claude panel split 2–1.

## Honest limits (read these)

- **No live reply rates.** This measures the *leading indicators* of a reply (a real trigger/insight, relevance, brevity, not getting filtered) and spam-avoidance — **not** real-world response rates, which we can't measure without sending. Those will be tracked openly over time via the living-results plan; this is the skill where that matters most.
- **The fresh B2G case was 2–1, not a sweep.** One judge preferred the baseline's concrete operational bullets (cooperative-purchasing vehicles, a deployment timeline) over the skill's insight-led email. A real, minor gap → a v0.1.1 polish (fold concrete procurement/operational proof points into B2G output). Cross-model preferred the skill here, but the note stands.
- **LLM judges (Claude + GPT), small N, Claude-generated arms.** Same standing caveats as the other skills; a human spot-check is the cheap further leg.

## Takeaway

`cold-outreach` is the package's proof that the bar is real. A frontier model writes a fine cold email on its own, so the first version of the skill tied it — and the eval said so. The reworked skill wins decisively on held-out and unseen cases, across two model families, by doing the thing a generic draft skips: leading with a real insight, respecting each channel's rules, and (for B2G) trading hype for credibility. We'd rather show the failure and the fix than a fifth tidy sweep.
