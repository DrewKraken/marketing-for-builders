#!/usr/bin/env python3
"""Deterministic checker for product positioning copy.

Flags common failure modes in a one-liner or value proposition:
  - buzzwords / filler that could appear on any product's homepage
  - feature-speak with no benefit/outcome language
  - a missing target audience
  - vague qualifiers used without evidence
  - overlong sentences that bury the point
  - one-liners that exceed a tight word budget (with --oneliner)

This is advisory: it surfaces revision prompts, not hard rules. It uses only the
Python standard library, so it runs anywhere (including CI) with no dependencies.

Usage:
    python positioning_lint.py --text "your one-liner or value prop"
    python positioning_lint.py path/to/copy.txt
    echo "your copy" | python positioning_lint.py
    python positioning_lint.py --text "..." --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

# Filler that could sit on any product's homepage. Signals the writer hasn't
# decided what the product actually is.
BUZZWORDS: frozenset[str] = frozenset({
    "seamless", "seamlessly", "robust", "powerful", "cutting-edge", "next-generation",
    "next-gen", "world-class", "best-in-class", "best-of-breed", "innovative",
    "revolutionary", "state-of-the-art", "game-changing", "game-changer", "frictionless",
    "turnkey", "holistic", "disruptive", "synergy", "synergies", "bleeding-edge",
    "leverage", "leveraging", "paradigm", "unparalleled", "unrivaled", "supercharge",
    "supercharged", "enterprise-grade", "military-grade", "comprehensive", "scalable",
})

# Adjectives that *feel* like substance but make a claim without evidence.
VAGUE_QUALIFIERS: frozenset[str] = frozenset({
    "easy", "simple", "fast", "flexible", "intuitive", "modern", "smart", "efficient",
    "reliable", "secure", "advanced", "rich", "lightweight", "user-friendly", "amazing",
    "great", "awesome",
})

# Phrases that signal benefit/outcome language rather than a feature description.
# Note the bare "so you "/"so they " (verb to follow) in addition to "so you can":
# an outcome clause is usually "so you <verb>" ("so you skip the retyping"), which
# the can/your-only list used to miss — including on this skill's own example.
BENEFIT_SIGNALS: tuple[str, ...] = (
    "so you ", "so they ", "so your", "so that", "helps you", "help you",
    "lets you", "let you", "without having to", "without the", "no longer",
    "instead of", "in minutes", "in seconds", "saves", "cuts", "reduces", "avoid",
    "never again",
)

# Hints that a target audience is named. Bare "for" is intentionally excluded —
# it is too common to be meaningful.
AUDIENCE_SIGNALS: tuple[str, ...] = (
    # Heuristic, non-exhaustive vocabulary of audience cues. The right audience word
    # is domain-specific — a dev tool says "engineers", an accounting tool says
    # "bookkeepers" — so expand this list as the package is used on new domains.
    "built for", "designed for", "teams", "developers", "engineers", "founders",
    "builders", "marketers", "designers", "analysts", "managers", "startups",
    "companies", "businesses", "small businesses", "smbs", "agencies", "operators",
    "bookkeepers", "accountants", "accounting firms", "bookkeeping firms",
    "accounts payable", "ap teams", "controllers", "cpas", "finance", "anyone who",
    "people who", "those who",
)

SENTENCE_SPLIT = re.compile(r"[.!?]+")
WORD = re.compile(r"[A-Za-z][A-Za-z\-']*")
MAX_SENTENCE_WORDS = 30
MAX_ONELINER_WORDS = 20


@dataclass(frozen=True)
class Finding:
    """A single advisory note about the copy."""

    code: str
    severity: str  # "warn" | "info"
    message: str


def _words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def check_buzzwords(text: str) -> list[Finding]:
    found = sorted({w for w in _words(text) if w in BUZZWORDS})
    if not found:
        return []
    return [Finding(
        code="buzzwords",
        severity="warn",
        message=("Buzzwords/filler that could sit on any product's homepage: "
                 f"{', '.join(found)}. Replace each with a specific claim."),
    )]


def check_vague_qualifiers(text: str) -> list[Finding]:
    found = sorted({w for w in _words(text) if w in VAGUE_QUALIFIERS})
    if not found:
        return []
    return [Finding(
        code="vague-qualifiers",
        severity="info",
        message=(f"Vague qualifiers used without evidence: {', '.join(found)}. "
                 "Back each with a number, comparison, or example, or cut it."),
    )]


def check_benefit_language(text: str) -> list[Finding]:
    lowered = text.lower()
    if any(sig in lowered for sig in BENEFIT_SIGNALS):
        return []
    if len(_words(text)) < 4:  # too short to warrant a benefit clause
        return []
    return [Finding(
        code="no-benefit-language",
        severity="warn",
        message=("Reads as a description of what the product is, not what the customer "
                 "gets. State an outcome (e.g. 'so you can ...', 'cuts X from ... to ...')."),
    )]


def check_audience(text: str) -> list[Finding]:
    lowered = text.lower()
    if any(sig in lowered for sig in AUDIENCE_SIGNALS):
        return []
    return [Finding(
        code="no-audience",
        severity="warn",
        message=("No target customer is named. Say who it's for - the sharper the "
                 "segment, the clearer the value."),
    )]


def check_sentence_length(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for raw in SENTENCE_SPLIT.split(text):
        count = len(_words(raw))
        if count > MAX_SENTENCE_WORDS:
            snippet = raw.strip()
            if len(snippet) > 60:
                snippet = snippet[:57].rstrip() + "..."
            findings.append(Finding(
                code="long-sentence",
                severity="info",
                message=(f"Sentence runs {count} words (>{MAX_SENTENCE_WORDS}); the point "
                         f'gets buried. Split it: "{snippet}"'),
            ))
    return findings


def check_oneliner_length(text: str) -> list[Finding]:
    """Flag a one-liner / tagline that exceeds a tight word budget."""
    count = len(_words(text))
    if count <= MAX_ONELINER_WORDS:
        return []
    return [Finding(
        code="oneliner-too-long",
        severity="warn",
        message=(f"One-liner runs {count} words; that's long for a tagline (aim for ~15). "
                 "Tighten to one plain idea a stranger gets at a glance."),
    )]


CHECKS = (
    check_buzzwords,
    check_vague_qualifiers,
    check_benefit_language,
    check_audience,
    check_sentence_length,
)


def lint(text: str, *, oneliner: bool = False) -> list[Finding]:
    """Run all checks and return the combined findings.

    Set oneliner=True to also enforce a tight word budget - use it for one-liners
    and taglines, which must stay short.
    """
    checks = [*CHECKS]
    if oneliner:
        checks.append(check_oneliner_length)
    findings: list[Finding] = []
    for check in checks:
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
        return "No issues found. The copy is specific, names an audience, and leads with value."
    lines = [f"{len(findings)} suggestion(s):", ""]
    for finding in findings:
        marker = "!" if finding.severity == "warn" else "-"
        lines.append(f" [{marker}] {finding.code}: {finding.message}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint product positioning copy.")
    parser.add_argument("path", nargs="?", help="Path to a text file to check.")
    parser.add_argument("--text", help="Positioning copy passed directly as a string.")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON.")
    parser.add_argument("--oneliner", action="store_true",
                        help="Treat input as a one-liner and enforce a tight word budget.")
    args = parser.parse_args(argv)

    text = _read_input(args)
    if not text.strip():
        parser.error("no input: pass --text, a file path, or pipe text via stdin")

    findings = lint(text, oneliner=args.oneliner)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print(_format_human(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
