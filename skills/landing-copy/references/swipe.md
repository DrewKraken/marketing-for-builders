# Swipe file: weak vs. strong landing/README copy (technical products)

Calibration examples for hero sections and README openings. Use them to judge whether a draft actually lands — not to copy the wording. Illustrative, not real companies' copy.

---

## 1. Landing hero — observability tool

**Before**
> # Acme Observe
> The unified, AI-powered observability platform.
> [Sign up] [Book a demo] [Docs] [GitHub]

**After**
> # Find out why production broke — in minutes, not hours
> For on-call engineers: trace any user-facing error back to the exact log line and deploy that caused it.
> [Start free]

**Why:** the before leads with the product name + a category cliché and offers four competing CTAs. The after leads with the outcome at 3 a.m. the engineer actually cares about, names the user, and gives one action.

---

## 2. Landing hero — payments API

**Before**
> # The complete payments infrastructure for modern businesses.
> Powerful, scalable, developer-friendly.

**After**
> # Add payments to your app in an afternoon
> One API for cards, subscriptions, and marketplace payouts — PCI compliance and fraud handled for you.
> [Read the quickstart]

**Why:** "powerful, scalable, developer-friendly" are buzzwords that say nothing. The after promises a concrete, time-bound outcome and names what you *don't* have to deal with (PCI, fraud).

---

## 3. README opening — CLI tool

**Before**
> # deploykit
>
> ## Background
> Modern deployment is complex. Teams juggle Docker, multiple clouds, and a variety of strategies. DeployKit was created to address these challenges with a unified, extensible approach…

**After**
> # DeployKit — deploy web apps to your servers in one command
>
> Blue-green, canary, and rolling deploys from a single Go binary. No agents, no control plane.
>
> ## Quickstart
> ```bash
> brew install deploykit
> deploykit deploy --config deploy.yaml
> ```

**Why:** the before opens with a "Background" essay; a developer can't tell what it does or try it. The after states the value on line one, then hands over a copy-pasteable quickstart — the two things a developer needs first.

---

## 4. README opening — library

**Before**
> # fastparse
> [![build](...)](...) [![npm](...)](...) [![license](...)](...)
>
> A library for parsing.

**After**
> # fastparse — parse messy CSVs that break other parsers
> [badges]
>
> Handles ragged rows, weird encodings, and 100 MB files without loading them into memory.
>
> ## Install
> `npm install fastparse`

**Why:** "A library for parsing" + badges is not a value prop. The after says what makes it worth choosing (the hard cases it handles) and gets to install immediately.

---

## Patterns across the strong versions

- **The headline states the outcome**, readable by someone who's never heard of the product.
- **One action**, not a row of competing buttons.
- **READMEs get to "what it does" and a runnable quickstart fast** — no preamble.
- **Concrete beats grand** — "100 MB files without loading them into memory" over "powerful and scalable."
- **Buzzwords are gone.** If a line could headline any competitor, it's cut.
