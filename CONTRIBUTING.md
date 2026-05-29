# Contributing to marketing-for-builders

Thanks for your interest. This project is in early development, and thoughtful contributions — especially from people who do developer marketing, DevRel, or have lived the "great product, no traction" problem — are genuinely welcome.

## Project philosophy

- **Depth over breadth.** We build one skill at a time and make it genuinely good before starting the next. A shallow skill that "sort of works" is worse than no skill.
- **Measured, not assumed.** Every skill ships with evals. If we can't demonstrate that it produces good output, it isn't done.
- **Honest scope.** This is marketing *craft* encoded as tooling — not growth hacks, not spam. Tactics we wouldn't be proud to put our name on don't belong here.

## How skills are structured

Each skill lives in `skills/<skill-name>/`:

```
skills/<skill-name>/
├── SKILL.md        # the playbook + frontmatter (name, description, version)
├── references/     # heavier material loaded on demand (frameworks, swipe files)
├── examples/       # before → after samples
└── scripts/        # deterministic helpers, if any
```

The `description` in `SKILL.md` frontmatter is load-bearing: it's how Claude decides when to use the skill. Keep it specific.

## Definition of done (per skill)

A skill is "done" when it has:

1. A focused `SKILL.md` with a precise trigger description.
2. Evals covering both triggering and output quality.
3. Tested helper scripts for any deterministic logic.
4. At least one real before → after example.

## Development workflow

1. Open an issue first to discuss the skill or change.
2. Fork and branch (`skill/<name>` or `fix/<short-description>`).
3. Make your change; add or update evals and examples.
4. Ensure CI passes.
5. Open a pull request using the template.

> The helper-script language (Python vs. TypeScript) and the eval runner are still being finalized — check the open issues before adding tooling.

## Commit & PR style

- Clear, present-tense commit messages that explain the *why*, not just the *what*.
- Keep PRs focused: one skill or fix per PR where possible.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## License

By contributing, you agree that your contributions are licensed under the [Apache License 2.0](LICENSE).
