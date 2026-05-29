# marketing-for-builders

**Marketing skills for people who can ship but can't sell.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
![Status: early development](https://img.shields.io/badge/status-early%20development-orange)
![Built with Claude](https://img.shields.io/badge/Built_with-Claude-D97757?logo=claude&logoColor=white)

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skills package that encodes go-to-market craft — positioning, copy, launch — so technical founders can turn what they built into something people actually understand and want.

> **Status:** early, but live. Two skills work today — [`positioning`](skills/positioning/) and [`landing-copy`](skills/landing-copy/). `positioning` has a published [evaluation](evals/RESULTS.md) (it beat no-skill 5/5); `landing-copy` ships linter-validated, with its baseline evaluation landing next.

## Why this exists

The hard part of marketing isn't the writing — it's the thinking. Most developer tools and indie products get described by *what they do* and never *why anyone should care*. This package encodes the thinking a good marketer would bring, so the person running it doesn't have to already be one.

It's built by a technical founder with exactly that gap, for people who share it.

## What's inside

Each capability is a focused, model-invoked **skill** — a tested playbook, not a vague prompt. Where judgment alone isn't enough, skills lean on deterministic helper scripts, and every skill is checked by an **evaluation harness** so quality is measured rather than assumed.

| Skill | Status | What it does |
|-------|--------|--------------|
| [`positioning`](skills/positioning/) | available | Turns a raw feature list into a sharp "who it's for + why it matters" value proposition. |
| [`landing-copy`](skills/landing-copy/) | available | Turns positioning into the page a visitor reads first — a landing page or a project README. |

_Skills are added one at a time, each held to the same bar: a clear playbook, evals that prove it works, and a real before → after example._

**Does it work?** See [`evals/RESULTS.md`](evals/RESULTS.md) — in the first evaluation the `positioning` skill beat the no-skill baseline on all 5 test cases, with the methodology and honest caveats shown.

## Repository layout

```
marketing-for-builders/
├── .claude-plugin/plugin.json   # plugin manifest
├── skills/                      # one directory per skill (SKILL.md + references + examples + scripts)
├── evals/                       # evaluation cases + results (cases.md, RESULTS.md)
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

## Install

This is a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin. To try it locally:

```bash
git clone https://github.com/DrewKraken/marketing-for-builders
claude --plugin-dir ./marketing-for-builders
```

Then paste a product description and ask Claude to position it — the `positioning` skill triggers on requests like "position my product," "write a value prop," or "who is this for." The Python linter needs Python 3.10+.

## Contributing

Early contributors are welcome — especially people who work in developer marketing or DevRel, or who've lived the "great product, no traction" problem. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). The quickest way in is to open an issue.

## Built with AI assistance

Developed in collaboration with Claude (Anthropic), with all direction and final judgment by the author.

## License

[Apache License 2.0](LICENSE).

## Author

Drew Swanigan — [drewswanigan.dev](https://drewswanigan.dev) · drew.swanigan@gmail.com
