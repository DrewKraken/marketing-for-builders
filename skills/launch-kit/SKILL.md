---
name: launch-kit
description: This skill should be used when the user wants to "write a Show HN", "launch on Product Hunt", "post my project to Reddit", "write a launch tweet" or "launch thread", "announce my launch on LinkedIn", "write a launch post", "I'm launching my product — what do I post", or "how do I post this to Hacker News". Use it whenever someone is announcing a product or project to a community or channel and needs the actual post — even if they don't name the channel.
version: 0.1.0
license: Apache-2.0
---

# Launch Kit

Turn a finished product into the launch announcement a builder actually posts — a Show HN, a Product Hunt launch, a Reddit post, a LinkedIn post, or an X thread. Launching is where technical founders go wrong in one of two ways: they post marketing-speak that the community flags and downvotes, or they under-sell with a bare "I made a thing" and no reason to care.

These communities are sharp and they punish promotion. The move that works is the same one builders are best at: **be a builder talking to builders** — say plainly what you made, who it's for, why you built it, and give people something to try. Honesty out-performs hype here, and every channel has rules that make this literal.

**Prerequisite — positioning.** A launch post is positioning aimed at a specific crowd. If it isn't already clear *who it's for*, *the value*, and *the alternative*, do that first (use the `positioning` skill). No launch post rescues a muddy pitch.

## The method

A launch post has two layers. Write the first once; the second is where the work is.

### 1. The launch narrative (write once)

From the positioning, draft the raw material every channel reuses:

- **What it is** — one plain line, the outcome and who it's for. Not the mechanism.
- **Why you built it** — the honest origin (the problem you hit). This is what makes a launch read as a builder, not an ad.
- **Something to try** — a link with no signup wall, or an install command. "Show, don't tell" is the whole game.
- **The ask** — invite *feedback*, never upvotes. Asking for votes is against the rules on HN and Product Hunt and gets posts penalized.

### 2. The channel adapter (the real work)

Every surface has **one dominant gate** — the element that, if weak, kills the post no matter how good the rest is. Lead with that gate and obey the channel's hard rules. (Full per-channel rules, timing, and sourcing are in `references/channels.md` — read it for the channel you're posting to.)

| Channel | The gate (get this right first) | Non-negotiable rules |
|---|---|---|
| **Show HN** | The title: `Show HN: Name – what it does`, plain, no hype; plus a link people can try without a signup | Must be something people can play with; no superlatives/CAPS/`!`; never ask for upvotes; you're around to answer in the thread |
| **Product Hunt** | The tagline: ≤60 chars, verb-led, one clear benefit; plus the maker's first comment | Launch 12:01 AM PT; clarity beats gimmicks; first comment = why + who + an ask for feedback (not votes) |
| **Reddit** | Subreddit fit + a title that reads as a builder sharing, not an ad; value first, link last | Post where self-promo is allowed (e.g. r/SideProject, "Show-and-Tell" threads); disclose "I built this"; be a participant, not a drive-by |
| **LinkedIn** | The hook: the first ~140 (mobile) / ~210 (desktop) chars before "…see more" must earn the click | Keep the hook in one paragraph (an early line break truncates it); put the link in the first comment, not the opening |
| **X / Twitter** | The hook post: a first line that stands alone, ≤280 chars | An external link in the main post cuts reach sharply — put the link in a reply; lead with the result or a demo |

## How to run it

1. **Start from the positioning** — the one-liner, audience, value, alternative. If they're missing, get them first.
2. **Pick the channel(s)** that fit the audience. If the user's buyers aren't on a channel (e.g. dental offices are not on Hacker News), say so and steer to the channel that fits — don't force a launch onto the wrong crowd.
3. **Draft the narrative once, then adapt to each channel's gate** using the templates below and `references/channels.md`.
4. **Lint the draft** for the channel:
   ```bash
   python skills/launch-kit/scripts/launch_lint.py --channel show_hn --text "<draft post>"
   ```
   `--channel` is one of `show_hn`, `producthunt`, `reddit`, `linkedin`, `x`. It flags vote-begging, hype/superlatives, and buzzwords always, plus the channel gate (title format, tagline length, the LinkedIn hook, a link in an X main post, a missing Reddit disclosure). Treat findings as revision prompts, not hard rules.
5. **Revise and present the post(s)** — and for Show HN / Product Hunt, the **author's first comment** too. It's half the launch.

## Output format

Present each channel separately. Templates:

**Show HN**
```
Title: Show HN: [Name] – [plainly what it does]
URL: [link people can try, no signup]

First comment (you, right after posting):
[2–4 short paragraphs: what it does, why you built it, how it works in a line
or two, what feedback you're after. No marketing voice.]
```

**Product Hunt**
```
Name: [Product]
Tagline: [≤60 chars, verb-led, one benefit]
First comment (maker, post immediately): [2–3 short paragraphs — why you built it,
who it's for, one ask for honest feedback. Not one dense block; it's read on mobile.]
Timing: launch 12:01 AM PT
```

**Reddit**
```
Subreddit: [r/... where self-promo is allowed] — and its rule you're following
Title: [a builder sharing, not an ad]
Body: [the story + value first; "I built this"; link at the end]
```

**LinkedIn**
```
Hook (first 1–2 lines, one paragraph — all most people see): [earns the click]
Body: [the story]
First comment: [the link]
```

**X / Twitter**
```
Post 1 (the hook, ≤280, stands alone): [result or demo, no link]
Post 2+ (optional thread): [how/why]
Reply: [the link]
```

## Principles

- **Communities smell marketing.** The voice that works is a builder being straight, not a brand being polished.
- **Show, don't tell.** A link people can try beats any adjective. Give them the thing.
- **Never ask for upvotes.** Ask for feedback. Vote-begging is against the rules and backfires.
- **Lead with the channel's gate.** A perfect post with a weak Show HN title — or a buried LinkedIn hook — is a dead post.
- **Match the channel to the audience,** not the audience to the channel. The best launch surface is the one your users already read.
- **The first comment is half the launch.** On HN and Product Hunt, the author's opening comment carries the context the title can't.

## Resources

- `references/channels.md` — the per-channel playbook in depth: each channel's gate, its hard rules (with sources), the format, timing, and the do/don't. Read the card for the channel you're posting to.
- `references/swipe.md` — annotated weak vs. strong launch posts for developer products. Read it to calibrate the voice.
- `scripts/launch_lint.py` — the deterministic, channel-aware draft checker used in step 4.
