# Example: a project README opener

A worked before → after from the `landing-copy` skill, run on a project README. Fictional product (DeployKit), illustrative.

## Before — a typical first draft

> # deploykit
>
> ## Background
> Modern deployment is complex. Teams juggle Docker, multiple clouds, and a variety of strategies. DeployKit addresses this with a unified, extensible approach.

**Linter:** 2 findings — `weak-headline` (the H1 is just the product name) and `no-cta` (no quickstart or next step). A developer can't tell what it does or how to try it.

## After — skill applied

> # DeployKit — deploy web apps to your servers in one command
>
> Blue-green, canary, and rolling deploys from a single Go binary. For engineers tired of brittle deploy scripts — no agents, no control plane.
>
> **Quickstart**
> `brew install deploykit && deploykit deploy --config deploy.yaml`

**Linter:** clean.

## What changed

- **The H1 states the outcome**, not just the product name.
- **Value and audience up top**, then a **quickstart immediately** — developers want to run it before they read prose.
- Cut the "Background" preamble that buried the point.
