# Landing page & README anatomy (in depth)

This expands the structure in `SKILL.md`. Read it when a page needs more than the quick pass — when the value isn't landing, when a section feels flat, or when the user wants the reasoning.

The governing fact: **visitors scan, and they leave fast.** On a landing page, most people read the headline and little else before deciding to stay or go. In a README, developers skim the top, look for a quickstart, and bail if they can't tell what it does or how to try it. Everything below is in service of that reality.

## Above the fold (the part that decides everything)

### Hero headline

The most important line you will write. It must communicate the **value**, not the category or the mechanism.

- **Outcome, not mechanism.** "Deploy to your servers in seconds" beats "A Go-based deployment CLI with rolling and canary strategies."
- **Specific, not grand.** "Cut invoice entry from minutes to zero" beats "Transform your accounts payable workflow."
- **No product name as the headline.** The name means nothing to a first-time visitor; the value does.
- **Readable cold.** Someone who has never heard of the product should understand it from this line alone.

A reliable shape: *[do desirable outcome] [without painful thing]* — e.g., "Ship to production without babysitting the build."

### Subhead

One or two sentences directly under the headline. Answer three things: **who it's for**, **what it is**, and **the payoff**. This is where the audience gets named ("For on-call engineers…", "For independent bookkeepers…").

### Primary call-to-action

One action, visible above the fold. "Get started," "Install," "Try it free," "Read the docs." **One** primary CTA — every competing button splits attention and lowers the odds anyone acts. Secondary links (docs, GitHub) can exist, but visually subordinate.

## Below the fold (support the promise)

### Benefit sections (≈ three)

Each section leads with an **outcome** and uses the feature as evidence. Pattern: a benefit-led heading, one or two sentences, then the concrete capability that delivers it.

- Weak: "## Multi-currency support — handles 135 currencies."
- Strong: "## Bill anyone, anywhere — charge customers in 135 currencies without a second integration."

Three is a guideline: enough to substantiate, few enough to stay scannable. A wall of ten features reads as a spec sheet, not a pitch.

### Proof

The section builders most often skip, and the one that converts skeptics. Use whatever is true: a concrete before/after, a number ("99% accuracy in under 5 seconds"), a short testimonial, recognizable logos, or a live example. Specific and real beats vague and grand.

### Closing CTA

Repeat the single primary action at the bottom, for the reader who scrolled the whole way.

## READMEs specifically

A README is a landing page for developers, with different conventions:

1. **H1 = product name + a one-line value prop** on the same or next line. Not just the name.
2. **A 1–2 sentence what + why** immediately — what it does and who it's for.
3. **A quickstart high up** — install command + the smallest runnable example. Developers want to see it work before they read prose. Burying install under "Background," "Motivation," and "Architecture" loses them.
4. **Then** the details: configuration, features, how it works, links.
5. Badges (build, version, license) are fine at the top, but they aren't the value prop — don't let them stand in for one.

## Common mistakes

- **Leading with the mechanism.** "An AI-powered platform that leverages…" tells the visitor nothing they care about.
- **Burying the value below the fold.** If the hero is a logo and a vague tagline, the page has wasted its one shot.
- **Feature dump instead of benefits.** A list of capabilities is not a pitch; the reader can't tell which matter or why.
- **Multiple competing CTAs.** "Sign up / Book a demo / Read docs / Star on GitHub / Join Discord" all at once = decision paralysis.
- **No proof.** Claims with nothing concrete behind them read as marketing noise.
- **A README with no quickstart near the top.** The fastest way to lose a developer.
