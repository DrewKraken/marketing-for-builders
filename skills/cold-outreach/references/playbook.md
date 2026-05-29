# Cold outreach playbook (in depth)

This expands `SKILL.md`. Read it for the reasoning, the numbers, or a hard case (especially B2G). The figures below are from current (2025–26) sources, cited inline.

## Why the market is broken — and why that's the opening

Cold email used to work because sending had a cost; now AI has made volume free, so volume is *anti-signal*. The data:

- Average cold-email reply rates fell from ~8.5% (2019) to ~5% (2025) to ~3.4% (2026); the top ~10% of campaigns still hit 8–12%. ([Instantly benchmarks](https://instantly.ai/blog/cold-email-reply-rate-benchmarks/), [The Digital Bloom](https://thedigitalbloom.com/learn/cold-outbound-reply-rate-benchmarks/))
- **Signal/trigger-based outreach replies at 15–25% vs 1–5% for generic.** One documented campaign went from 7% → ~20% after switching to signals — while *cutting* volume from ~200 to ~50 emails/week. ([Built For B2B](https://www.builtforb2b.com/blog/b2b-cold-email-benchmark-2025))
- **Timeline/trigger hooks reply ~10% vs ~4.4% for problem-statement hooks** (2.3×). Personalization works when it's *context, not tokens*; recipients "smell ChatGPT." Generic AI emails see ~90% lower replies. ([SalesCaptain stats](https://www.salescaptain.io/blog/cold-email-statistics))
- Decision-makers get ~15 cold emails/week. Of the ignored ones: **71% lacked relevance, 43% failed on personalization, 36% lacked trust signals.** ([SalesCaptain stats](https://www.salescaptain.io/blog/cold-email-statistics))

The takeaway is the whole strategy: **fewer, researched, trigger-based emails.** Everyone else is racing to send more; that's the gap.

## The trigger taxonomy (your "why now")

A trigger is a real, recent, specific event that makes reaching out *now* make sense. Strong ones:

- **Funding** — a raise means new budget and new initiatives (and, for infra/payments products, new scale problems).
- **Hiring / open reqs** — a job post is a public statement of a problem they're spending to solve (e.g., a "Platform Engineer, Kubernetes" req = a migration in progress).
- **Launches / changelog** — they shipped something your product complements or strengthens.
- **Migrations / stack changes** — visible in job posts, talks, GitHub, status pages.
- **Leadership changes** — a new VP/director re-evaluates tools in their first 90 days.
- **Regulatory / mission events (B2G)** — a new mandate, an audit finding, an incident report.

"I came across your company" / "I see you're in [industry]" are **not** triggers — they're the tell of a blast. No trigger → don't send; go find one or pick a different prospect.

## The one insight (the decisive lever)

Specificity is what separates a reply from a delete. The data: generic cold email replies at ~9%; email with advanced, context-specific personalization at ~18% (2×); signal/trigger-based at 15–25%. ([Cleverly](https://www.cleverly.co/blog/cold-email-copywriting), [Instantly](https://instantly.ai/blog/cold-email-reply-rate-benchmarks/))

But "specific" doesn't mean "mentions their company name." It means an **insight** — a non-obvious observation about *their* situation that proves you understand it. "I noticed your SDR team grew from 5 to 12 in Q3" or "mid-migration is where deploys get scariest" lands; "I see you're scaling" does not. The test: would they read the line and think *"huh, that's true and most people don't say it"*? If not, it isn't an insight yet. This is the single highest-leverage thing in the email — and the thing a capable AI will happily skip, writing a competent note *without* one. That gap is exactly why a researched human still beats the blast. Make the insight non-negotiable.

## Subject lines

The subject decides whether any of the above gets read. The data ([Belkins](https://belkins.io/blog/b2b-cold-email-subject-line-statistics)):

- **Short wins** — the shorter the subject, the higher the open; ~36–50 characters is the sweet spot.
- **Lowercase / sentence case** beats Title Case by ~8–12%; it reads like an internal note, not a campaign.
- **Questions** open well (curiosity); **personalized** subjects open ~46% vs ~35% generic.
- **Avoid:** hype and urgency ("ASAP"), generic greetings, emoji (they *lower* B2B opens and raise spam flags), and *clever* wordplay (it tanks opens ~10–15%).
- Aim for something that looks "typed in two seconds by someone who knows you."

## Anatomy of the email

- **Subject:** 2–5 words, plain and specific, no hype or spam-trigger words. Often the trigger itself ("your Kubernetes migration").
- **Line 1 — relevance:** the trigger, stated as homework you did. This earns the next sentence.
- **Line 2 — why it matters to them:** the outcome (from your positioning), tied to the trigger. Not features.
- **Line 3 — one ask:** low-friction and specific ("worth a quick look?", "are you the right person for this?"). One, not three.
- **Close:** who you are + a graceful opt-out. Short signature.
- **Length:** under ~125 words. If it needs scrolling, it won't be read.

## The follow-up sequence

Follow-ups are not optional — **~60% of replies come after the first follow-up**, and a 3-7-7 cadence captures ~93% of replies by day 10. ([SalesCaptain stats](https://www.salescaptain.io/blog/cold-email-statistics))

- **Cadence:** original → ~day 3 → ~day 10 → (optional) ~day 17.
- **Each adds value:** a relevant example, a one-line result, a useful link, or a sharper angle on the trigger. Never "just bumping this" or "did you see my last email?" — that nags without giving a reason to reply.
- **The breakup:** a final, gracious "I'll stop here — reach out if it's ever useful" often gets the reply, and it leaves the door open.

## Deliverability — the rules that now reject you

As of 2024–25, Gmail/Yahoo/Microsoft enforce hard requirements; non-compliant mail is increasingly **rejected, not just spam-foldered** (Gmail tightened to outright rejection in Nov 2025). ([Redsift guide](https://redsift.com/guides/bulk-email-sender-requirements), [Proofpoint](https://www.proofpoint.com/us/blog/email-and-cloud-threats/clock-ticking-stricter-email-authentication-enforcements-google-start))

- **Authentication:** SPF, DKIM, and DMARC are mandatory; the From domain must align.
- **Spam-complaint rate:** hard ceiling **0.3%**; aim **<0.1%**. Cold blasts routinely hit 0.5–1% and get blocked. Bounce rate >2% damages your domain.
- **Bulk threshold:** 5,000+/day to personal inboxes triggers the strictest rules — another reason low-volume researched outreach is the safer *and* more effective play.
- **One-click unsubscribe** (List-Unsubscribe) is required for bulk senders.

(These are operational/infrastructure rules — the skill doesn't configure your DNS, but it keeps the *copy* clean of the spam tells that push complaint rates up.)

## Compliance (don't skip this)

- **CAN-SPAM (US):** honest sender identity, no deceptive subjects, a working opt-out honored within 10 business days, a physical mailing address. Penalties up to ~$53k *per email* (2025). ([Instantly compliance](https://instantly.ai/blog/b2b-email-list-compliance-gdpr-canspam/))
- **GDPR (EU):** B2B cold email is generally permissible under *documented legitimate interest*; B2C requires opt-in. Always offer an easy opt-out. Fines up to €20M / 4% of revenue. ([Instantly compliance](https://instantly.ai/blog/b2b-email-list-compliance-gdpr-canspam/))
- **CASL (Canada)** is stricter (consent-based); penalties up to $10M.
- Practical rule: a real identity + a graceful one-line opt-out covers the spirit of all three and is just courteous.

## B2G — selling to government

A different game (ClearComm911's world). Sources: [Bluetext](https://bluetext.com/blog/b2g-marketing-strategies-how-to-win-government-contracts-with-your-brand/), [Deltek](https://www.deltek.com/en/government-contracting/guide/b2g), [Hermix](https://hermix.com/understanding-b2g-navigating-public-sector-sales-and-government-procurement/).

- **Committees, not buyers.** Contracting officers, technical evaluators, program leads, legal — each with different concerns. Write to the role you're emailing.
- **Credibility over hype.** Clarity, mission impact, outcomes, and *past performance* (case studies, pilots, references) carry the day. Superlatives actively hurt.
- **The ask is a briefing or a pilot,** not "a quick call." Low-friction here means low-commitment and mission-relevant.
- **Timing is calendar-driven.** Align to fiscal-year and procurement cycles; start the relationship months before any RFP. Expect long timelines.
- **Registration/credibility infrastructure** (e.g., SAM.gov at the federal level) sits behind the outreach — be ready to point to it.

## Common failure modes

- **No trigger** — the email could've been sent to anyone, so it gets read by no one.
- **About you, not them** — opening with "I'm X from Y, we do Z." Open with *their* trigger.
- **Feature dump** — a cold email is not a landing page; one outcome, one ask.
- **Fake personalization** — `Hi {first_name}` or "I loved your post!" that clearly didn't happen.
- **Hype** — "revolutionary," "game-changing," "#1." Instant credibility loss; fatal in B2G.
- **No follow-up** — leaving 60% of your replies on the table.
- **Volume** — the more you send, the worse it works now. Send 10 you researched, not 1,000 you generated.
