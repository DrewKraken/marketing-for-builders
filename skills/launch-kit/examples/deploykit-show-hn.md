# Worked example — launching DeployKit on Show HN

A run of the skill on a real-shaped input, from raw blurb to posted launch. The same product, DeployKit, is the dev-tool case in the repo's eval set.

## Input (the builder's blurb)

> DeployKit — a command-line tool for deploying web apps. Go, single binary, no
> dependencies. YAML config. Docker, rolling/blue-green/canary deploys, pre/post
> hooks, AWS/GCP/Azure, built-in rollback, parallel deploys over SSH, plugin system.
> Open source (MIT). CLI-first with an optional web dashboard. Secrets via env files
> or Vault.

## Step 1 — the launch narrative (write once)

- **What it is:** a single-binary CLI that deploys web apps to your own servers in one command — for small teams who never adopted Kubernetes.
- **Why I built it:** years of hand-rolled, brittle bash deploy scripts.
- **Something to try:** `brew install deploykit`, or the MIT repo — no account needed.
- **The ask:** feedback on the config format and the rollback flow.

## Step 2 — adapt to the channel gate

DeployKit is open source, runnable, and aimed at developers — a near-perfect **Show HN** fit. The gate is the title.

### The post

```
Title: Show HN: DeployKit – deploy web apps to your own servers in one command
URL:   https://github.com/example/deploykit
```

### First comment (post immediately after submitting)

```
I built DeployKit after years of hand-rolling deploy scripts for small teams that
never moved to Kubernetes. It's a single Go binary with no dependencies: point it at
a YAML file and it does rolling, blue-green, or canary deploys over SSH, with rollback
built in.

It's MIT-licensed and runs without an account: `brew install deploykit` or grab the
binary from the releases page. There's an optional web dashboard, but the CLI is the
whole product.

I'd love feedback on two things: the YAML config format, and whether the rollback flow
makes sense for people deploying to bare metal or VMs.
```

## Step 3 — lint it

```bash
python skills/launch-kit/scripts/launch_lint.py --channel show_hn --text "$(cat post.md)"
# No issues found. The post describes the work plainly, names no votes to beg for,
# and fits its channel.
```

## A Product Hunt variant (same product, different gate)

If the same launch went to Product Hunt, the gate becomes the tagline:

```
Name:    DeployKit
Tagline: Deploy web apps to your own servers in one command   (50 chars, verb-led)
First comment (2–3 short paragraphs, not one block):
  I built DeployKit because deploying without Kubernetes still meant hand-rolling
  brittle bash scripts for every project.

  It's an open-source Go binary — rolling, blue-green, and canary deploys over SSH,
  with one-command rollback. `brew install deploykit` and you're going.

  Would love your honest feedback on the YAML config format.
Timing: launch 12:01 AM PT
```

The narrative is identical; only the lead element changes — the Show HN title becomes the Product Hunt tagline, each shaped to its own gate and character budget.
