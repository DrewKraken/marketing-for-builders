# Evaluation results

Do these skills actually produce better output than not using them? This is the evidence, run honestly — including the limits and the cases where the gap is small.

- [`positioning`](#positioning) — clear, consistent lift (beat baseline 5/5).
- [`landing-copy`](#landing-copy) — real but smaller lift; clearest on READMEs. The linter is a weak discriminator here, and we say so.

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

## Takeaway

Across five deliberately different product shapes, the skill consistently replaced mechanism-first, feature-piled, broad-audience copy with audience-specific, outcome-led positioning that named the real alternative. Consistent lift — preliminary, but the same pattern every time.

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

## Takeaway

`landing-copy` produces a measurable, consistent improvement on all five shapes, and a clear, demonstrable win on **READMEs**, where unaided copy reliably leads with the product name and a feature dump instead of the value and the audience. On polished marketing landing pages a strong model is already decent, so there the skill's contribution is discipline — one CTA, a named audience, less sprawl — more than night-and-day quality. We'd rather show that honestly than overstate it.
