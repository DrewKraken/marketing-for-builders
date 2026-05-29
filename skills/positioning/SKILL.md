---
name: positioning
description: This skill should be used when the user wants to "position my product", "write a value proposition", "explain what my tool does", "sharpen my README/landing pitch", "figure out who this is for", "say why anyone would care", or turn a feature list into a clear message. Use it whenever someone is struggling to describe a technical product compellingly — even if they never say the word "positioning".
version: 0.1.0
license: Apache-2.0
---

# Positioning

Turn a builder's raw, feature-heavy description of a product into clear positioning — who it's for, what they'd otherwise use, the unique value, and why it matters — then express it as a tight one-liner and a short value proposition.

Positioning is upstream of all other marketing. A landing page, a launch post, a cold email — each is easy when the positioning is sharp and impossible when it isn't. Get this right before writing any other copy.

The core failure to correct: technical founders describe **what they built** (features, stack, architecture) instead of **why anyone should care** (the outcome, and for whom). The job here is to make that translation.

## The method

Work the six components below in order. Do not jump to the one-liner — the one-liner is an *output* of this analysis, not a starting point. (For the reasoning and per-component questions, read `references/framework.md`.)

1. **Competitive alternatives** — what would the customer use if this product did not exist? Often a spreadsheet, a manual process, a rival tool, or "nothing / do it by hand." Value is always relative to the alternative, so name it first.
2. **Unique attributes** — what does this product have that those alternatives lack? Capabilities, model, design. Stay concrete and factual.
3. **Value** — what does each attribute let the customer *do* or *avoid*? Translate every attribute into an outcome. This feature → benefit bridge is the step builders skip.
4. **Best-fit customers** — who has the problem so acutely that the value is obvious and urgent? Niche down to the sharpest segment, never "everyone."
5. **Market category** — what frame of reference makes the value obvious and tells the customer what to compare this to?
6. **Relevant trend** (optional) — a larger shift that makes it timely. Use only if genuinely true; skip otherwise.

## How to run it

1. **Take the raw input as-is.** A feature dump or vague paragraph is the expected "before." Only ask questions if a critical element is missing — usually just two: *who is the customer* and *what would they use instead*.
2. **Work the components briefly with the user.** Push back on feature-speak by converting each feature into the value it delivers. Resist "for everyone" — force the sharpest-fit segment and check whether the value got clearer (it usually does).
3. **Draft** the positioning statement, the one-liner, and the value proposition.
4. **Lint the drafts.** Run the value proposition through the checker, and the one-liner with `--oneliner` (which also enforces a tight word budget):
   ```bash
   python skills/positioning/scripts/positioning_lint.py --oneliner --text "<draft one-liner>"
   python skills/positioning/scripts/positioning_lint.py --text "<draft value proposition>"
   ```
   It flags buzzwords, feature-speak with no benefit language, a missing audience, vague qualifiers, overlong sentences, and (with `--oneliner`) a too-long one-liner. Treat findings as revision prompts, not hard rules.
5. **Revise and present the before → after** so the improvement is visible.

## Output format

ALWAYS present results in this structure:

```
## Positioning
**For** [target customer] **who** [situation/need], **[Product]** is a **[category]**
that **[unique value]** — unlike **[alternative]**.

## One-liner
[plain-language, benefit-forward, ~15 words or fewer, no buzzwords]

## Value proposition
[2–4 sentences: who it's for, the problem, what it does, the payoff]

## What changed
[1–2 lines naming the biggest shift from the original]
```

## Principles

- **Lead with the outcome, not the mechanism.** Builders sell the engine; buyers buy the destination.
- **Specific beats impressive.** "Cuts payroll reconciliation from 3 days to 20 minutes" beats "powerful automation platform."
- **Position against the real alternative** — usually a spreadsheet or "doing nothing," not a flashy competitor.
- **Narrow the audience until it feels uncomfortably specific,** then verify the value got sharper.
- **Cut every word that could appear in any other product's copy.** Buzzwords signal you haven't decided what you are.

## Resources

- `references/framework.md` — the method in depth: per-component questions, the feature → benefit technique, and common traps. Read it when a positioning problem is knotty or the user wants the reasoning.
- `references/swipe.md` — annotated weak vs. strong positioning for developer/technical products. Read it to calibrate what "good" looks like.
- `scripts/positioning_lint.py` — the deterministic draft checker used in step 4.
