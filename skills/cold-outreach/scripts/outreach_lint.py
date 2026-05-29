#!/usr/bin/env python3
"""Deterministic checker for cold-outreach email drafts.

Cold email is broken by volume: generic, AI-blasted mail gets ~90% lower replies
and is increasingly rejected outright (Gmail/Yahoo enforce a 0.3% spam-complaint
ceiling). This linter flags the tells that get a cold email filtered, deleted, or
ignored — so the draft reads like a researched 1:1 note, not a mass merge.

Checks (each maps to a real deliverability or credibility rule):
  - spam-trigger-words   classic spam-filter phrases ("act now", "risk-free", ...)
  - merge-artifacts      unrendered tokens / mass-merge tells ("{first_name}", "Hi there")
  - too-long             cold emails must be short; long copy gets ignored
  - hype-superlatives    credibility killers ("revolutionary", "#1", ...)
  - link-overload        too many links hurt deliverability and read as salesy
  - no-ask               a cold email with no single clear ask is pointless
  - missing-optout       a graceful opt-out / honest identity (CAN-SPAM, and just polite)
  - shouting             ALL-CAPS runs and exclamation marks (spam tells)

Advisory, not hard rules. Standard library only, so it runs anywhere (including CI)
with no dependencies. Lint ONE email at a time (the cold email, or one follow-up).
Word lists are intentionally self-contained so the skill stands alone.

Usage:
    python outreach_lint.py --text "your cold email draft"
    python outreach_lint.py path/to/email.md
    echo "..." | python outreach_lint.py
    python outreach_lint.py --text "..." --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

# Classic spam-filter phrases. Kept as phrases (not bare words like "free") to
# avoid false positives on legitimate copy ("free up your team").
SPAM_PHRASES: tuple[str, ...] = (
    "act now", "buy now", "click here", "limited time", "limited-time", "risk-free",
    "risk free", "100% free", "100% satisfied", "no obligation", "order now",
    "money back", "money-back", "cash bonus", "extra income", "make money",
    "earn extra", "double your", "you have been selected", "you've been selected",
    "this is not spam", "guaranteed results", "special promotion", "exclusive deal",
    "don't miss out", "for a limited", "while supplies last", "lowest price",
)

# Superlative/hype vocabulary — credibility killers, doubly so in B2G.
HYPE_TERMS: tuple[str, ...] = (
    "revolutionary", "game-changing", "game changer", "world-class", "best-in-class",
    "cutting-edge", "groundbreaking", "amazing", "incredible", "insanely",
    "unbeatable", "best ever", "#1", "number one", "second to none",
    "industry-leading", "industry leading", "next-generation", "state-of-the-art",
)

# Phrases that indicate a clear ask.
ASK_SIGNALS: tuple[str, ...] = (
    "would you be open", "would you be up for", "worth a quick", "worth a look",
    "worth a chat", "can i send", "could i send", "happy to send", "want me to send",
    "do you have time", "do you have 15", "open to a", "open to chatting",
    "grab 15", "a quick call", "a short call", "set up a call", "book a",
    "are you the right person", "who owns", "mind if i", "would it help",
    "let me know if you'd like", "shall i",
)

# A graceful opt-out / honest close (CAN-SPAM + basic courtesy).
OPTOUT_SIGNALS: tuple[str, ...] = (
    "unsubscribe", "opt out", "opt-out", "reply stop", "no longer wish",
    "rather not hear", "leave you be", "leave you alone", "won't follow up",
    "happy to stop", "feel free to ignore", "just say the word", "no worries if not",
    "if this isn't relevant",
)

# Mass-merge / placeholder tokens: {first_name}, {{company}}, [First Name], [[name]].
MERGE_TOKEN = re.compile(r"\{\{?[^{}\n]{1,40}\}?\}|\[\[?[A-Za-z][^\]\n]{0,40}\]?\]")
GREETING_TELLS: tuple[str, ...] = (
    "hi there", "hello there", "dear sir", "dear madam", "dear sir or madam",
    "to whom it may concern", "dear valued customer", "dear customer",
)

URL_RE = re.compile(r"https?://\S+", re.I)
WORD = re.compile(r"[A-Za-z][A-Za-z\-']*")
CAPS_WORD = re.compile(r"\b[A-Z]{4,}\b")
CAPS_ALLOW: frozenset[str] = frozenset({
    "ASAP", "HIPAA", "PSAP", "FEMA", "CJIS", "NIST", "EULA", "SAML", "OAUTH",
    "JSON", "REST", "HTTP", "HTTPS", "SAAS", "DEMO", "FAQ", "GDPR", "CCPA",
})

MAX_WORDS = 150
LINK_LIMIT = 3


@dataclass(frozen=True)
class Finding:
    """A single advisory note about the draft."""

    code: str
    severity: str  # "warn" | "info"
    message: str


def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def check_spam_trigger_words(text: str) -> list[Finding]:
    low = _normalize(text).lower()
    found = sorted({p for p in SPAM_PHRASES if p in low})
    if not found:
        return []
    return [Finding(
        "spam-trigger-words", "warn",
        f"Phrases that trip spam filters: {', '.join(found)}. Cut them — they read "
        "as a sales blast, not a 1:1 note.")]


def check_merge_artifacts(text: str) -> list[Finding]:
    norm = _normalize(text)
    low = norm.lower()
    tokens = MERGE_TOKEN.findall(norm)
    greetings = [g for g in GREETING_TELLS if g in low]
    if not tokens and not greetings:
        return []
    bits: list[str] = []
    if tokens:
        bits.append("unfilled merge tokens (" + ", ".join(sorted(set(tokens))[:3]) + ")")
    if greetings:
        bits.append("generic greeting (" + ", ".join(greetings) + ")")
    return [Finding(
        "merge-artifacts", "warn",
        "Mass-merge tells: " + "; ".join(bits) + ". Address a real person and fill "
        "every field — a recipient spots a template instantly.")]


def check_length(text: str) -> list[Finding]:
    count = len(_words(text))
    if count <= MAX_WORDS:
        return []
    return [Finding(
        "too-long", "warn",
        f"{count} words. Cold emails get skimmed in seconds — aim for under "
        f"{MAX_WORDS}. Cut to the trigger, one proof, and one ask.")]


def check_hype(text: str) -> list[Finding]:
    low = _normalize(text).lower()
    found = sorted({t for t in HYPE_TERMS if t in low})
    if not found:
        return []
    return [Finding(
        "hype-superlatives", "warn",
        f"Hype that kills credibility cold: {', '.join(found)}. Replace each with a "
        "specific, verifiable fact.")]


def check_links(text: str) -> list[Finding]:
    n = len(URL_RE.findall(text))
    if n < LINK_LIMIT:
        return []
    return [Finding(
        "link-overload", "warn",
        f"{n} links. Multiple links hurt deliverability and read as a pitch. "
        "Keep at most one, or none on the first touch.")]


def check_ask(text: str) -> list[Finding]:
    low = _normalize(text).lower()
    if "?" in text or any(sig in low for sig in ASK_SIGNALS):
        return []
    return [Finding(
        "no-ask", "warn",
        "No clear ask. End with one specific, low-friction next step "
        "(e.g. 'worth a quick look?' or 'are you the right person for this?').")]


def check_optout(text: str) -> list[Finding]:
    low = _normalize(text).lower()
    if any(sig in low for sig in OPTOUT_SIGNALS):
        return []
    return [Finding(
        "missing-optout", "info",
        "No graceful opt-out. A one-line out ('no worries if this isn't relevant — "
        "just say so') is courteous, lowers complaints, and helps with CAN-SPAM.")]


def check_shouting(text: str) -> list[Finding]:
    norm = _normalize(text)
    caps = [w for w in CAPS_WORD.findall(norm) if w not in CAPS_ALLOW]
    reasons: list[str] = []
    if len(caps) >= 2:
        reasons.append("ALL-CAPS words (" + ", ".join(sorted(set(caps))[:4]) + ")")
    if norm.count("!") >= 2:
        reasons.append("multiple exclamation points")
    if not reasons:
        return []
    return [Finding(
        "shouting", "warn",
        "Spam tells: " + "; ".join(reasons) + ". Write it the way you'd write a "
        "note to one busy person.")]


CHECKS = (
    check_spam_trigger_words,
    check_merge_artifacts,
    check_length,
    check_hype,
    check_links,
    check_ask,
    check_optout,
    check_shouting,
)

# A follow-up is a reply in an existing thread: it does NOT need a fresh opt-out
# (the cold email already carried one), and a breakup follow-up legitimately has
# no ask. Skipping these on follow-ups is what prevents the opt-out line from
# being stamped onto every message — the template tell that reads as a blast.
FOLLOWUP_SKIP = frozenset({check_optout, check_ask})


def lint(text: str, followup: bool = False) -> list[Finding]:
    """Run all checks and return the combined findings.

    With ``followup=True``, skip the opt-out and ask checks (see FOLLOWUP_SKIP):
    those belong on the first cold email, not on every reply in the thread.
    """
    findings: list[Finding] = []
    for check in CHECKS:
        if followup and check in FOLLOWUP_SKIP:
            continue
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
        return ("No issues found. The draft reads like a researched 1:1 note: short, "
                "specific, one ask, and no spam tells.")
    lines = [f"{len(findings)} suggestion(s):", ""]
    for finding in findings:
        marker = "!" if finding.severity == "warn" else "-"
        lines.append(f" [{marker}] {finding.code}: {finding.message}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint a cold-outreach email draft.")
    parser.add_argument("path", nargs="?", help="Path to a text file to check.")
    parser.add_argument("--text", help="Copy passed directly as a string.")
    parser.add_argument(
        "--followup", action="store_true",
        help="Lint a follow-up (reply in a thread): skips the opt-out and ask checks.")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON.")
    args = parser.parse_args(argv)

    text = _read_input(args)
    if not text.strip():
        parser.error("no input: pass --text, a file path, or pipe text via stdin")

    findings = lint(text, followup=args.followup)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print(_format_human(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
