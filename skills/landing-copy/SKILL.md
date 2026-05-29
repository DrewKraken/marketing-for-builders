---
name: landing-copy
description: This skill should be used when the user wants to "write a landing page", "write my README", "fix my homepage copy", "write a hero section", "my landing page isn't converting", "what should my README say", or turn positioning into the actual page a visitor reads first. Use it whenever someone needs first-impression copy for a product — a landing page or a project README — even if they don't say "landing page".
version: 0.1.0
license: Apache-2.0
---

# Landing Copy

Turn a product's positioning into the copy a visitor reads first — a landing page or a project README. This is the first impression, and most technical products waste it: they open with the mechanism ("an AI-powered platform that…") or bury the value below the fold.

**Prerequisite — positioning.** If it isn't already clear *who it's for*, *the value*, and *the alternative*, do that first (use the `positioning` skill). Landing copy expresses positioning; it can't rescue a muddy one.

## The method

Structure the page top-to-bottom — order matters because visitors scan and bounce in seconds.

1. **Hero headline** — the value proposition in one line. Outcome-led; not the product name, not the mechanism. The single most-read line on the page; if someone reads only this, they should get it.
2. **Subhead** — one or two sentences: who it's for + what it does + the payoff. Expands the headline in plain language.
3. **Primary CTA** — one clear action, above the fold ("Get started", "Install", "Try it free"). One primary CTA — not five competing ones.
4. **How it works / benefits** — about three sections, each led by an outcome with the feature as support. Not a feature dump.
5. **Proof** — a concrete example, numbers, before/after, logos, or testimonials. Builders skip this; it's what earns trust.
6. **Closing CTA** — repeat the one action at the bottom.

**For a README specifically:** H1 = product name + a one-line value prop; immediately a 1–2 sentence what/why; a **quickstart** (install + minimal usage) high up; then details. Developers decide in seconds whether to keep reading — give them the value and a runnable example fast.

## How to run it

1. Start from the positioning — the one-liner, value prop, audience, and alternative. If they're missing, get them first.
2. Draft the page (or README) in the structure above. Lead every section with the outcome, not the feature.
3. **Lint the draft:**
   ```bash
   python skills/landing-copy/scripts/landing_lint.py --text "<draft>"
   ```
   It flags a weak headline (bare product name / mechanism), a missing call-to-action, a missing audience, poor scannability (no headings, walls of text), and buzzwords. Treat findings as revision prompts, not hard rules.
4. Revise and present the result.

## Output format

**Landing page:**
```
# [Hero headline — the value proposition, outcome-led]
[Subhead: who it's for + what it does + the payoff]
[Primary CTA]

## [Benefit 1 — outcome-led] / ## [Benefit 2] / ## [Benefit 3]
## Proof  (example, numbers, or testimonial)
[Closing CTA]
```

**README:**
```
# [Product] — [one-line value prop]
[1–2 sentence what + why]
## Quickstart  (install + minimal usage)
## [Then: how it works, features, links]
```

## Principles

- **The headline is the page.** If a visitor reads only the H1, they should understand the value.
- **Above the fold sells; below the fold supports.** Don't bury the value.
- **One primary CTA.** Competing actions kill conversion.
- **Benefit first, feature second** — in every section.
- **Developers scan.** Short paragraphs, clear headings, and a quickstart they can copy-paste.

## Resources

- `references/structure.md` — anatomy of a high-converting landing page / README for technical products, in depth.
- `references/swipe.md` — annotated weak vs. strong hero copy for developer products.
- `scripts/landing_lint.py` — the deterministic draft checker used in step 3.
