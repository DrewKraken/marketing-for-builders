# Evaluation results

Does the `positioning` skill actually produce better positioning than not using it? This is the evidence, run honestly — including the limits.

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
