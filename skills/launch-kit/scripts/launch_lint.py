#!/usr/bin/env python3
"""Deterministic checker for product-launch posts.

Launch communities reward a builder describing plainly what they made and
punish marketing. This linter flags the failures that get launch posts
penalized, removed, or ignored:

Always-on (any launch copy):
  - upvote-begging   asking for votes (banned on Hacker News AND Product Hunt)
  - hype-superlatives  superlatives / exclamation runs HN guidelines forbid
  - buzzwords          filler that could sit on any product's page

Channel-gated (pass --channel) — each surface has one dominant "gate":
  - show_hn       title format ("Show HN: Name - what it does") + a try-link
  - producthunt   tagline <=60 chars, verb-led
  - reddit        an "I built this" disclosure; not a drop-and-run link
  - linkedin      a hook that survives the "...see more" truncation; link in comments
  - x             first post <=280 chars; link in a reply, not the main post

Advisory, not hard rules. Standard library only, so it runs anywhere (including
CI) with no dependencies. (The buzzword list is intentionally duplicated from the
other skills' linters so each skill stays self-contained.)

Usage:
    python launch_lint.py --text "your launch post" --channel show_hn
    python launch_lint.py path/to/post.md --channel producthunt
    echo "..." | python launch_lint.py --channel reddit
    python launch_lint.py --text "..." --channel x --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

BUZZWORDS: frozenset[str] = frozenset({
    "seamless", "seamlessly", "robust", "powerful", "cutting-edge", "next-generation",
    "next-gen", "world-class", "best-in-class", "best-of-breed", "innovative",
    "revolutionary", "state-of-the-art", "game-changing", "game-changer", "frictionless",
    "turnkey", "holistic", "disruptive", "synergy", "synergies", "bleeding-edge",
    "leverage", "leveraging", "paradigm", "unparalleled", "unrivaled", "supercharge",
    "supercharged", "enterprise-grade", "military-grade", "comprehensive", "scalable",
})

# Soliciting votes. Banned by HN ("Please don't ask friends to upvote") and
# penalized by Product Hunt. The signature check of this skill.
UPVOTE_SIGNALS: tuple[str, ...] = (
    "upvote", "up vote", "up-vote", "please support", "support us", "vote for us",
    "vote for me", "hunt us", "give us a like", "smash the", "smash that",
    "show some love", "your support means", "drop an upvote", "appreciate the support",
    "appreciate your support", "give us an upvote",
)

# Hype HN guidelines explicitly discourage ("don't say how great an article is").
# Kept distinct from BUZZWORDS to avoid double-flagging the same word.
HYPE_TERMS: tuple[str, ...] = (
    "amazing", "insanely", "insane", "mind-blowing", "mind blowing", "jaw-dropping",
    "jaw dropping", "groundbreaking", "ground-breaking", "unbelievable", "blazingly",
    "blazing fast", "revolutioniz", "world's first", "worlds first", "first-ever",
    "first ever", "number one", "#1", "best ever",
)

URL_RE = re.compile(r"https?://\S+", re.I)
INSTALL_RE = re.compile(
    r"\b(pip install|pipx install|npm install|npm i |npx |yarn add|pnpm add|"
    r"brew install|docker run|docker pull|git clone|cargo install|go install|"
    r"go get|gem install|apt install|curl -)",
    re.I,
)
SHOW_HN_RE = re.compile(r"show\s*hn", re.I)
DISCLOSURE_RE = re.compile(
    r"\b(i built|i made|i created|i developed|i've been building|"
    r"i have been building|i'm the (maker|creator|developer|founder)|"
    r"i am the (maker|creator|developer|founder)|full disclosure|disclosure:|"
    r"my (own )?(project|app|tool|side project))\b",
    re.I,
)
WORD = re.compile(r"[A-Za-z][A-Za-z\-']*")

ARTICLE_OPENERS: frozenset[str] = frozenset({"the", "a", "an", "your", "our", "my"})

PH_TAGLINE_MAX = 60
X_POST_MAX = 280
LINKEDIN_SNIPPET = 210  # desktop "...see more" cutoff (mobile ~140)
MIN_HOOK_WORDS = 4

CHANNELS: tuple[str, ...] = ("show_hn", "producthunt", "reddit", "linkedin", "x")


@dataclass(frozen=True)
class Finding:
    """A single advisory note about the copy."""

    code: str
    severity: str  # "warn" | "info"
    message: str


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def _first_line(text: str) -> str:
    for line in _normalize(text).splitlines():
        stripped = line.strip()
        if stripped:
            return stripped.lstrip("#").strip()
    return ""


def _first_block(text: str) -> str:
    """The text up to the first blank line — i.e. the first post / paragraph."""
    stripped = _normalize(text).strip("\n")
    idx = stripped.find("\n\n")
    block = stripped if idx == -1 else stripped[:idx]
    return block.strip()


# --- always-on --------------------------------------------------------------

def check_upvote_begging(text: str) -> list[Finding]:
    low = _normalize(text).lower()
    if any(sig in low for sig in UPVOTE_SIGNALS):
        return [Finding(
            "upvote-begging", "warn",
            "Asking for votes/support. Hacker News and Product Hunt both forbid "
            "soliciting upvotes — it gets posts penalized or removed. Ask for "
            "feedback instead.")]
    return []


def check_hype(text: str) -> list[Finding]:
    low = _normalize(text).lower()
    reasons: list[str] = []
    matched = sorted({t for t in HYPE_TERMS if t in low})
    if matched:
        reasons.append("superlatives (" + ", ".join(matched) + ")")
    if low.count("!") >= 2:
        reasons.append("multiple exclamation points")
    if not reasons:
        return []
    return [Finding(
        "hype-superlatives", "warn",
        "Hype that communities (especially HN) penalize: " + "; ".join(reasons)
        + ". Describe plainly what it does and let the work impress.")]


def check_buzzwords(text: str) -> list[Finding]:
    found = sorted({w for w in _words(text) if w in BUZZWORDS})
    if not found:
        return []
    return [Finding(
        "buzzwords", "warn",
        f"Buzzwords that could sit on any product's post: {', '.join(found)}. "
        "Replace each with a specific claim.")]


# --- show_hn ----------------------------------------------------------------

def check_show_hn_title(text: str) -> list[Finding]:
    title = None
    for line in _normalize(text).splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped and SHOW_HN_RE.search(stripped):
            title = stripped
            break
    if title is None:
        return [Finding(
            "show-hn-title", "warn",
            "No 'Show HN:' title. Lead with the HN format: "
            "'Show HN: Name - what it does'.")]
    findings: list[Finding] = []
    if not re.match(r"show\s*hn\s*:", title, re.I):
        findings.append(Finding(
            "show-hn-title", "warn",
            "Use the exact prefix 'Show HN:' (with a colon)."))
    if "!" in title:
        findings.append(Finding(
            "show-hn-title", "warn",
            "Drop the exclamation point — HN titles read plainly, they don't shout."))
    remainder = re.sub(r"^show\s*hn\s*:?\s*", "", title, flags=re.I)
    parts = re.split(r"\s[–—-]\s", remainder, maxsplit=1)
    description = parts[1] if len(parts) == 2 else remainder
    if len(_words(description)) < 3:
        findings.append(Finding(
            "show-hn-title", "warn",
            "Title names the project but not what it does. Add a plain "
            "description: 'Show HN: Name - does X for Y'."))
    return findings


def check_show_hn_trylink(text: str) -> list[Finding]:
    if URL_RE.search(text) or INSTALL_RE.search(text):
        return []
    return [Finding(
        "show-hn-no-link", "warn",
        "Show HN must let people try it. Include a link (ideally with no signup) "
        "or an install command.")]


# --- producthunt ------------------------------------------------------------

def check_ph_tagline(text: str) -> list[Finding]:
    tagline = _first_line(text)
    findings: list[Finding] = []
    if len(tagline) > PH_TAGLINE_MAX:
        findings.append(Finding(
            "ph-tagline-length", "warn",
            f"Tagline is {len(tagline)} characters; Product Hunt caps taglines at "
            f"{PH_TAGLINE_MAX}. Tighten it to one clear benefit."))
    first_word = (_words(tagline)[:1] or [""])[0]
    if first_word in ARTICLE_OPENERS:
        findings.append(Finding(
            "ph-tagline-verb", "info",
            f"Product Hunt taglines land hardest verb-led; yours opens with "
            f"'{first_word}'. Try starting with the action."))
    return findings


# --- reddit -----------------------------------------------------------------

def check_reddit_disclosure(text: str) -> list[Finding]:
    if DISCLOSURE_RE.search(_normalize(text)):
        return []
    return [Finding(
        "reddit-no-disclosure", "warn",
        "Say that you built it ('I built this...'). Reddit expects transparency; "
        "undisclosed self-promotion gets removed.")]


def check_reddit_value(text: str) -> list[Finding]:
    if URL_RE.search(text) and len(_words(text)) < 25:
        return [Finding(
            "reddit-low-value", "info",
            "Reads as a drop-and-run link. Lead with what you made and why it "
            "helps; share the link after the value.")]
    return []


# --- linkedin ---------------------------------------------------------------

def check_linkedin_hook(text: str) -> list[Finding]:
    norm = _normalize(text).strip()
    first_line = norm.split("\n", 1)[0].strip()
    findings: list[Finding] = []
    weak = URL_RE.match(first_line) or (
        len(_words(first_line)) < MIN_HOOK_WORDS
        and not first_line.endswith(("?", ":"))
    )
    if weak:
        findings.append(Finding(
            "linkedin-weak-hook", "info",
            "Your first line is the hook — it's all most people see before "
            "'...see more'. Open with a line that earns the click, not a title "
            "or a bare link."))
    if URL_RE.search(norm[:LINKEDIN_SNIPPET]):
        findings.append(Finding(
            "linkedin-link-in-hook", "info",
            "A link in the opening competes with your hook and can dampen reach. "
            "Many builders put it in the first comment instead."))
    return findings


# --- x / twitter ------------------------------------------------------------

def check_x_post(text: str) -> list[Finding]:
    block = _first_block(text)
    findings: list[Finding] = []
    length = len(block)
    if length > X_POST_MAX:
        findings.append(Finding(
            "x-post-length", "warn",
            f"The first post is {length} characters; X caps posts at {X_POST_MAX}. "
            "Tighten the hook or split it into a thread."))
    if URL_RE.search(block):
        findings.append(Finding(
            "x-link-in-post", "warn",
            "An external link in the main post can cut reach sharply on X. Put "
            "the link in a reply and keep the hook native."))
    return findings


ALWAYS_ON = (check_upvote_begging, check_hype, check_buzzwords)

CHANNEL_CHECKS: dict[str, tuple] = {
    "show_hn": (check_show_hn_title, check_show_hn_trylink),
    "producthunt": (check_ph_tagline,),
    "reddit": (check_reddit_disclosure, check_reddit_value),
    "linkedin": (check_linkedin_hook,),
    "x": (check_x_post,),
}


def lint(text: str, channel: str | None = None) -> list[Finding]:
    """Run the always-on checks plus any checks for the given channel."""
    findings: list[Finding] = []
    for check in ALWAYS_ON:
        findings.extend(check(text))
    for check in CHANNEL_CHECKS.get(channel or "", ()):
        findings.extend(check(text))
    return findings


def _read_input(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    if args.path is not None:
        with open(args.path, encoding="utf-8") as handle:
            return handle.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def _format_human(findings: list[Finding]) -> str:
    if not findings:
        return ("No issues found. The post describes the work plainly, names no "
                "votes to beg for, and fits its channel.")
    lines = [f"{len(findings)} suggestion(s):", ""]
    for finding in findings:
        marker = "!" if finding.severity == "warn" else "-"
        lines.append(f" [{marker}] {finding.code}: {finding.message}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint a product-launch post.")
    parser.add_argument("path", nargs="?", help="Path to a text file to check.")
    parser.add_argument("--text", help="Copy passed directly as a string.")
    parser.add_argument(
        "--channel", choices=CHANNELS,
        help="Apply the channel-specific gate checks for this surface.")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON.")
    args = parser.parse_args(argv)

    text = _read_input(args)
    if not text.strip():
        parser.error("no input: pass --text, a file path, or pipe text via stdin")

    findings = lint(text, args.channel)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print(_format_human(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
