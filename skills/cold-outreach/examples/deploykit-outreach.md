# Worked example — cold outreach for DeployKit

A full run of the skill: from a real trigger to the email and the follow-up sequence. DeployKit is the dev-tool case from the repo's eval set.

## Input

- **Product (positioning):** DeployKit — ship web apps to your own servers in one command. For teams who deploy to their own servers without Kubernetes; alternative = hand-rolled deploy scripts.
- **Target:** Sarah, VP Engineering at a Series-B SaaS company.
- **Trigger (found by research):** her team just posted a *"Platform Engineer — Kubernetes migration"* role. A migration in progress = deploys are about to get risky. That's the "why now."

## Step 1–2 — trigger, relevance, and the one insight

The job post is the trigger. The relevance line writes itself: *"saw your team just posted a Platform Engineer role focused on the Kubernetes migration."* Specific, recent, real homework — not `{first_name}`.

The **insight** is the lever: *"mid-migration is usually where deploys get scary — the cutover is months out but you still ship every day."* That's a non-obvious, true observation about her situation — the thing a generic AI draft skips and a researched human includes.

## Step 3 — the email

```
Subject: deploys during the k8s migration?

Hi Sarah — saw your team just posted a Platform Engineer role focused on the
Kubernetes migration. Mid-migration is usually where deploys get scary.

I built DeployKit for teams making exactly that move: one Go binary that does
rolling and canary deploys over SSH, with one-command rollback — so a bad deploy
is a 10-second fix, not an incident. No control plane to run.

Worth a quick look before you wire up more tooling? Happy to send a 2-minute
demo, or point you at the repo.

No worries if this isn't relevant — just say so.

Drew
```

**Trigger used:** the public job posting for a Kubernetes-migration platform role.

## Step 4 — the follow-up sequence (3-7-7)

Most replies come after the first follow-up, so these matter as much as the email. Each adds a new angle — never "just bumping."

```
Follow-up 1 (~day 3): One thing I forgot to mention: DeployKit runs the migration
and the legacy boxes from the same YAML, so you can move services over one at a
time instead of a big-bang cutover. Happy to show how — worth 10 minutes?

Follow-up 2 (~day 10): Saw your eng blog post on cutting deploy time — that's
exactly the pain DeployKit removes for the teams using it (one wrote up going
from a 40-minute scripted deploy to a single command). Want the writeup?

Follow-up 3 (~day 17): I'll stop here so I'm not cluttering your inbox. If the
migration ever makes deploys painful, the repo's a good place to start — reach
out anytime. Thanks, Sarah.
```

## Step 5 — lint it

The cold email, then each follow-up with `--followup` (so it isn't told to repeat the opt-out — note the opt-out appears only in the first email above):

```bash
python skills/cold-outreach/scripts/outreach_lint.py --text "$(cat email.md)"
# No issues found. The draft reads like a researched 1:1 note: short, specific,
# one ask, and no spam tells.

python skills/cold-outreach/scripts/outreach_lint.py --followup --text "$(cat followup-1.md)"
# No issues found.
```

Contrast with what the linter does to a generic blast of the same pitch (`Revolutionizing Your Workflow 🚀 / Hi {first_name} / #1 game-changing platform / [feature dump] / 30-min call this week!!`): it trips `spam-trigger-words`, `merge-artifacts`, `hype-superlatives`, `shouting`, and `missing-optout` at once. Same product, opposite outcome — see `references/swipe.md`.
