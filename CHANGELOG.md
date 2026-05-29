# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- `positioning_lint.py`: `BENEFIT_SIGNALS` now recognizes the bare outcome clause
  `so you <verb>` / `so they <verb>` (e.g. "so you skip the retyping"), not only
  `so you can`. This was a false-positive `no-benefit-language` on the skill's own
  canonical example (`examples/invoiceparser-pro.md`), whose value proposition the
  example claims "passed the linter clean" but did not. Added a regression test that
  lints the example's one-liner + value proposition directly so it can't drift again.
- `positioning_lint.py`: `AUDIENCE_SIGNALS` recognizes more AP/finance roles
  (`accounts payable`, `ap teams`, `controllers`, `cpas`, `bookkeeping firms`).

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
- `cold-outreach` skill: `SKILL.md` + `references/` (research-grounded playbook with sourced principles + swipe file) + `outreach_lint.py` (with tests) + a worked example. Turns a product + a specific target into a researched, trigger-based cold email and short follow-up sequence (B2B + B2G); prerequisite is positioning. Built around the verified finding that signal/trigger-based outreach replies at 15–25% vs 1–5% generic.
- `outreach_lint.py`: a deterministic spam-tell / deliverability linter — spam-trigger words, mass-merge artifacts (`{first_name}`), over-length, hype, link-overload, missing ask, missing opt-out, shouting — plus a `--followup` mode that skips the cold-email-only checks (opt-out, ask) on thread replies.
- `cold-outreach` evaluation — the round that caught a failure and fixed it. **Round 1: the skill lost** (blind judge panel skill 2/5, dead even with the frontier baseline, including a 0–3 loss on the B2G case). Diagnosed structural defects (an opt-out the linter induced into a template tic, flat subjects, thin B2G), reworked the skill (an "insight" requirement, subject-line craft, opt-out-once via the new `--followup` mode, rebuilt B2G mode), and **Round 2: it cleared the bar** — skill 5/5 (14/15 votes) on the 3 held-out failures **and** 2 fresh unseen cases, confirmed **5/5 cross-model** (GPT/Codex). Reported in full in `evals/RESULTS.md` with the R1→R2 arc and the honest limit that this measures reply *quality*, not live reply rates.
