# Launch swipe file — weak vs. strong

Annotated before/after for developer launches. The pattern is always the same: the weak version sounds like marketing and trips the channel's rules; the strong version sounds like a builder and clears the gate. Read these to calibrate the voice, not to copy the wording.

---

## Show HN title

**Weak**
> Show HN: The REVOLUTIONARY deploy tool that will change how you ship forever!!

Why it fails: superlatives ("REVOLUTIONARY"), CAPS, exclamation points — all three explicitly discouraged by HN guidelines. It says how great it is and never says what it *is*. This gets flagged and sinks.

**Strong**
> Show HN: DeployKit – deploy web apps to your own servers in one command

Why it works: plain, lowercase, no hype. A first-time reader knows exactly what it does and who'd want it. The work is left to impress on its own.

---

## Show HN first comment

**Weak**
> Hey HN! Super excited to share DeployKit 🚀🚀 Please check it out and give us an upvote if you like it! Link: [signup page]

Why it fails: vote-begging (against the rules), emoji hype, and the link is a signup wall, not something you can try.

**Strong**
> I built DeployKit after years of hand-rolling deploy scripts for small teams that
> never moved to Kubernetes. It's a single Go binary: point it at a YAML file and it
> does rolling/blue-green/canary deploys over SSH, with rollback built in.
>
> It's open source (MIT) and works without an account: `brew install deploykit` or
> grab the binary. I'd love feedback on the config format and the rollback flow —
> especially from anyone deploying to bare metal.

Why it works: honest origin, plainly what it does and how, a no-signup way to try it, and a specific ask for *feedback* (not votes).

---

## Product Hunt tagline (≤60 chars, verb-led)

| Weak | Why | Strong |
|---|---|---|
| "DeployKit – the future of deployment" (vague, no verb) | says nothing concrete | "Deploy web apps to your own servers in one command" |
| "A powerful, scalable platform for modern DevOps teams" (buzzwords, 53 chars wasted) | could be any tool | "Ship to your servers without writing deploy scripts" |
| "The #1 deploy tool for startups" (hype, ranking claim) | unprovable brag | "Roll out, roll back, and canary — from one YAML file" |

---

## LinkedIn hook (first line is all most people see)

**Weak**
> I'm excited to announce the launch of DeployKit, a new tool we've been working on…

Why it fails: "I'm excited to announce" is the most-scrolled-past opener on LinkedIn; the real point is hidden behind "…see more," so few expand it.

**Strong**
> For two years I deployed our app by SSH-ing into a box and praying. Last month I finally fixed that for good.

Why it works: a concrete, slightly vulnerable hook that creates a curiosity gap inside the ~140-char window — the reader clicks "…see more" to find out what changed.

---

## X / Twitter hook post

**Weak**
> Check out DeployKit, our new deployment tool! [link]

Why it fails: a bare link in the main post (reach penalty), no hook, no demo, reads as an ad.

**Strong**
> Post 1: I deleted 300 lines of bash deploy scripts this week and replaced them with one command. [15-sec screen recording of `deploykit deploy`]
> Reply: It's open source — repo + install here: [link]

Why it works: a result-driven hook with a native demo clip, link demoted to the reply where it isn't penalized.
