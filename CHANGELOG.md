# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository scaffold: plugin manifest, base directory structure, license,
  contribution and code-of-conduct guidelines, issue/PR templates, and CI.
- `positioning` skill (initial): `SKILL.md` plus `references/` (Dunford framework + swipe file).
- `positioning_lint.py` — a deterministic positioning-copy linter — with unit tests.
- CI job running `ruff` + `pytest` on helper scripts (no LLM calls).
- Opt-in `--oneliner` word-budget check in the linter.
- `evals/` — evaluation cases and Round-1 results (the `positioning` skill beat the no-skill baseline on all 5 cases; methodology and honest caveats included).
- Worked before → after example: `skills/positioning/examples/invoiceparser-pro.md`.
- `landing-copy` skill: `SKILL.md` + `references/` (page structure + swipe file) + `landing_lint.py` (with tests). Turns positioning into landing-page / README copy; prerequisite is positioning.
- Worked before → after example: `skills/landing-copy/examples/deploykit-readme.md`.
- `landing_lint.py`: added a `competing-cta` check (flags two or more distinct CTA intents side by side; platform variants like App Store + Google Play are treated as one intent).
- `landing-copy` evaluation: Round 1 over 5 product shapes — the skill cleared the linter on all 5 cases while unaided copy tripped a first-impression failure on every one (modest per-case margin; clearest on READMEs). Methodology and honest caveats in `evals/RESULTS.md`.
