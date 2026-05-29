# Cold outreach swipe file — generic blast vs. researched

Two emails to the same person. One is what the flooded market sends; one is what gets a reply. Read them side by side to calibrate the voice — then write your own, don't copy the wording.

Target for both: **Sarah, VP Engineering at a Series-B company that just posted a "Platform Engineer — Kubernetes migration" role.** Product: DeployKit.

---

## Weak — the generic AI blast

> **Subject:** Revolutionizing Your Deployment Workflow 🚀
>
> Hi {first_name},
>
> I hope this email finds you well! My name is Drew and I'm the founder of DeployKit, the #1 game-changing deployment platform that's revolutionizing how world-class engineering teams ship software.
>
> DeployKit offers rolling deploys, blue-green deploys, canary releases, Docker support, AWS/GCP/Azure integrations, built-in rollback, a plugin system, secrets management, and so much more!
>
> I'd love to hop on a quick 30-minute call this week to walk you through a demo and explore synergies. Are you free Tuesday or Thursday?
>
> Looking forward to hearing from you!
>
> Best, Drew

**Why it fails almost every way:** an unfilled `{first_name}`; opens about *you*, not her; a hype-stuffed subject and body ("#1," "game-changing," "revolutionizing," "world-class"); a feature dump instead of one outcome; a high-friction ask (30 minutes from a stranger); exclamation shouting; no real reason she's getting this *now*; no graceful out. This is exactly the email that lands in spam or the trash, and it's what `outreach_lint.py` lights up.

---

## Strong — the researched, trigger-based note

> **Subject:** your platform-engineer req
>
> Hi Sarah — saw your team just posted a Platform Engineer role focused on the Kubernetes migration. Mid-migration is usually where deploys get scary.
>
> I built DeployKit for teams making exactly that move: one Go binary that does rolling and canary deploys over SSH, with one-command rollback — so a bad deploy is a 10-second fix, not an incident. No control plane to run.
>
> Worth a quick look before you wire up more tooling? Happy to send a 2-minute demo, or point you at the repo.
>
> No worries if this isn't relevant — just say so.
>
> Drew

**Why it works:** a real trigger (the job post) stated as homework; it's about *her* situation, not the product; one concrete outcome ("a 10-second fix, not an incident") instead of a feature list; plain language, no hype; a low-friction ask with an even-lower-friction alternative; a graceful opt-out. Short enough to read in ten seconds. Lints clean.

---

## The pattern, distilled

| | Weak | Strong |
|---|---|---|
| Reason for sending | none (could go to anyone) | a specific, recent trigger |
| First line is about | you / your product | their situation |
| Tone | hype + exclamation | plain, factual |
| Body | feature dump | one outcome |
| Ask | 30-min call | "worth a look?" + an easy out |
| Personalization | `{first_name}` | a real observation |
