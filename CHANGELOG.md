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
- `launch-kit` skill: `SKILL.md` + `references/` (per-channel playbook with sourced rules + swipe file) + `launch_lint.py` (with tests) + a worked example. Turns a finished product into the launch post for Show HN, Product Hunt, Reddit, LinkedIn, or X — a shared launch narrative adapted to each channel's gate; prerequisite is positioning.
- `launch_lint.py`: a deterministic, channel-aware launch-post linter (`--channel show_hn|producthunt|reddit|linkedin|x`). Always-on checks: upvote-begging, hype/superlatives, buzzwords. Channel-gated checks: Show HN title + try-link, Product Hunt tagline length/verb, Reddit disclosure, LinkedIn hook window, X post length / link-in-reply.
- `launch-kit` evaluation: Round 1 over 5 product shapes (one channel each), scored two ways. A blind LLM-judge panel (3 judges/case, randomized order) preferred the skill's post in **5/5 cases (15/15 votes)** over unaided output; the deterministic linter saw a near-tie (1 baseline finding vs 0), because rule-compliance is the wrong proxy for launch quality. Both reported in `evals/RESULTS.md`, with the judge sweep as the headline and honest limits (Claude-judged, N=5).
- `evals/METHODOLOGY.md`: documents the two-instrument evaluation framework — a deterministic linter (guardrail, free in CI) plus a blind LLM-judge panel (quality benchmark, 3 judges/case, randomized A/B), with honest limits and a cross-skill summary.
- Applied the blind judge panel across **all three** skills for consistency: positioning and landing-copy were retro-judged on their Round 1 outputs. Every skill was preferred by the blind judges in 5/5 cases (15/15 votes); both instruments rank the skills the same way (positioning > landing-copy > launch-kit by gap). `RESULTS.md` updated with a judge-panel result for each skill.
- Cross-model corroboration: an independent GPT/Codex judge re-scored the same 15 pairs blind and preferred the skill in **14/15** (29/30 blind verdicts across two model families), addressing the Claude-judging-Claude limitation. Recorded in `RESULTS.md` / `METHODOLOGY.md`.
- `launch-kit` refinement (from the cross-model critique): the Product Hunt maker-comment guidance now calls for 2–3 short paragraphs rather than one dense block (SKILL.md template, channels reference, and worked example).
