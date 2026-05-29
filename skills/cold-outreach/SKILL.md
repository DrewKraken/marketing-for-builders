---
name: cold-outreach
description: This skill should be used when the user wants to "write a cold email", "do cold outreach", "reach out to" a specific prospect or company, "email this lead", "write a sales email", "follow up on a cold email", "get my first customers", "email a government agency" or "B2G outreach", or asks "how do I reach [person] at [company]". Use it whenever someone needs a researched 1:1 outreach email to a specific person — not a mass campaign or a newsletter.
version: 0.1.0
license: Apache-2.0
---

# Cold Outreach

Write a cold email a specific person will actually reply to — and the short follow-up sequence behind it. The hard truth first: **AI made volume free, so volume is now working against you.** Anyone can blast thousands of generated emails, recipients delete them on sight, and Gmail/Yahoo increasingly *reject* them outright. Generic AI cold email gets roughly 90% lower replies than researched outreach.

So this skill does the opposite of what the flooded market does. It will **not** help you send more. It helps you send **fewer, better** — each email built on a real reason to reach this person *now*. The evidence is stark: signal/trigger-based outreach replies at **15–25%** vs **1–5%** for generic. The move that wins is the one builders are actually good at: be a real person, who did real homework, writing to one real person.

**Prerequisite — positioning.** You can't say "why you, why them" without a sharp sense of your value and audience. If that isn't clear, do it first (use the `positioning` skill).

## The method

### 1. Find the trigger first — or don't send

The single biggest lever. Before writing a word, find **why now**: a funding round, a new hire or open req, a product launch, a stack migration, an RFP, a public mission priority. **No trigger → don't send yet.** "I came across your company" is not a trigger; it's the tell of a blast.

Research it from whatever's real: the company blog/changelog, LinkedIn, news, job posts. *(If you have enrichment or intent tools — Apollo, G2, and the like — use them here to surface the trigger; they're an accelerant, not a requirement.)*

### 2. The relevance line + the one insight (the real lever)

Specificity is *the* factor that separates a reply from a delete: generic cold email replies at ~9%, a researched/context-specific email at ~18%, signal-based outreach at 15–25%. Two beats:

- **Relevance** — one sentence proving real homework: **context, not a merge token.** "Saw you just posted a platform-engineer role for the Kubernetes migration" lands; "I see you're in DevOps" does not.
- **The one insight** — a *non-obvious* observation about their situation that proves you actually understand it, not just that you found a trigger. e.g. "mid-migration is usually where deploys get scariest — the cutover is months out but you still ship every day." This is what a generic blast can't fake and a lazy AI draft never bothers with. **If you can't say one thing they'd find true and slightly under-discussed, you haven't researched enough yet — go back to step 1.**

### 3. Write the email — short and human

- **Subject:** short (aim ~36–50 characters), lowercase or sentence case, and specific — a question often works best. It should read like a note from someone who already knows them, not a campaign. **No hype, no clever wordplay (clever subjects lose ~10–15% of opens), no emoji, no spam-trigger words.** "your kubernetes migration" is too thin; "deploys during the k8s migration?" earns the open.
- **Body, ≤ ~125 words:** relevance + the insight → one sentence of *why it matters to them* (the outcome, tied to your positioning) → **one** low-friction ask. No feature dump, no superlatives, no fake warmth.
- **Close:** honest identity (who you are) and a **graceful opt-out, in your own words.** Put it **once, here in the first email only** — never paste the same opt-out line into every follow-up. That repetition is itself the template tell that gets you ignored.

### 4. Write the follow-up sequence

Most replies come *after* the first follow-up, so the sequence is half the work. **2–3 short follow-ups on a 3-7-7 cadence** (≈ day 3, then day 10, then day 17). Each one **adds a new angle or a piece of value** (a relevant example, a one-line result, a useful resource) — never "just bumping this to the top." **Don't restate the opt-out every time** — at most a light, varied out on the final breakup. Lint follow-ups with the `--followup` flag (it skips the cold-email-only checks).

### 5. B2G mode (selling to government)

A different game, and the one this skill most has to earn. You're writing to a committee, not a buyer (contracting officers, technical evaluators, program leads). What actually moves a public official:

- **Concrete credibility, not adjectives.** Name the relevant standard or framework (e.g. NENA i3 for 911), a certification, or a comparable agency you've served — specifics they recognize on sight. Hype actively backfires here.
- **Frame around their mandate/mission and the outcome**, not your product.
- **The "right person?" redirect.** Government roles are siloed; "are you the right person for this, or should I reach someone on the technical side?" shows you understand how they're organized.
- **A low-pressure ask** — a briefing or a pilot, never "a quick call."
- **A slower cadence.** Government inboxes don't move on an SDR rhythm; space follow-ups out (≈ day 0 / 7 / 21), align to the fiscal/procurement calendar, start well before any RFP, and expect long cycles.

### 6. Hygiene (what keeps you out of spam)

This skill is for **low-volume, researched, compliant** outreach. Keep volume sane, use a real identity, honor opt-outs, and skip the spam-trigger vocabulary. Sending thousands is the failure mode, not the goal.

## How to run it

1. **Start from the positioning** + the **specific target** and the **trigger**. If there's no trigger, say so and help find one before writing.
2. Draft the email (subject + body) and the follow-up sequence, per the method.
3. **Lint each email.** The cold email:
   ```bash
   python skills/cold-outreach/scripts/outreach_lint.py --text "<cold email>"
   ```
   Each follow-up (add `--followup` — a reply in a thread doesn't need a fresh opt-out or a hard ask):
   ```bash
   python skills/cold-outreach/scripts/outreach_lint.py --followup --text "<follow-up>"
   ```
   It flags spam-trigger words, mass-merge artifacts (`{first_name}`, "Hi there"), over-length, hype, link-overload, a missing ask, a missing opt-out, and shouting. Treat findings as revision prompts.
4. **Revise and present** the subject, the email, and the sequence — and name the trigger you built it on, so the user can confirm it's real.

## Output format

```
Subject: [short, lowercase, specific — often a question]

[Email 1 — the cold email, ≤ ~125 words]
- relevance + the one insight  →  why it matters to them  →  one ask
- honest sign-off + a graceful opt-out (here only — NOT repeated in the follow-ups)

Trigger used: [the real "why now"]   |   Insight: [the non-obvious observation]

Follow-up 1 (≈ day 3):  [short; a new angle or piece of value]
Follow-up 2 (≈ day 10): [short; a different angle / a relevant proof point]
Follow-up 3 (≈ day 17): [optional; a light breakup note]
```

## Principles

- **No trigger, no send.** Relevance and timing beat volume — that's the whole game.
- **An insight earns the reply.** A specific, non-obvious observation about their world (~18% reply) beats a restated trigger (~9%) beats a generic pitch (~1%). If you have nothing to say they don't already know, research more before sending.
- **Context, not tokens.** One line of real homework outperforms any amount of `{first_name}` personalization.
- **One opt-out, not a refrain.** A graceful out belongs once, in the first email. The same opt-out line on every follow-up is a template tell.
- **Short and human.** Write the email you'd actually want to receive from a stranger: brief, specific, one ask, easy to say no to.
- **The follow-up is the email.** Most replies come after it — and each one must add value, not nag.
- **Credibility over hype** — always, and doubly in B2G.
- **Fewer, better, compliant.** Low volume, real identity, graceful opt-out. The market's flooded with the opposite; that's your edge.

## Resources

- `references/playbook.md` — the thesis with the numbers (cited), B2B vs B2G in depth, the deliverability/compliance rules, and the trigger taxonomy. Read it for the reasoning or a hard case.
- `references/swipe.md` — annotated generic-AI-blast vs researched-trigger email, side by side.
- `scripts/outreach_lint.py` — the deterministic spam-tell / deliverability checker used in step 3.
