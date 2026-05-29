#!/usr/bin/env python3
"""Deterministic checker for landing-page and README copy.

Flags common first-impression failures:
  - a weak headline (bare product name, too short, or category-only)
  - no call-to-action
  - no target audience named
  - poor scannability (a wall of text with no headings)
  - buzzwords / filler

Advisory, not hard rules. Standard library only, so it runs anywhere (including CI)
with no dependencies. (Word lists are intentionally duplicated from the positioning
skill's linter so each skill stays self-contained.)

Usage:
    python landing_lint.py --text "your landing or README copy"
    python landing_lint.py path/to/page.md
    echo "..." | python landing_lint.py
    python landing_lint.py --text "..." --json
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

AUDIENCE_SIGNALS: tuple[str, ...] = (
    "built for", "designed for", "teams", "developers", "engineers", "founders",
    "builders", "marketers", "designers", "analysts", "managers", "startups",
    "companies", "businesses", "small businesses", "smbs", "agencies", "operators",
    "bookkeepers", "accountants", "accounting firms", "finance", "anyone who",
    "people who", "those who",
)

# Phrases that indicate a call-to-action.
CTA_SIGNALS: tuple[str, ...] = (
    "get started", "sign up", "try it", "try free", "start free", "install",
    "download", "book a demo", "read the docs", "quickstart", "request access",
    "get the", "join ", "pip install", "npm install", "brew install",
)

# Category nouns that, on their own, do not communicate value.
CATEGORY_NOUNS: tuple[str, ...] = (
    "platform", "tool", "library", "solution", "framework", "api", "app",
    "software", "service", "system", "infrastructure", "suite", "engine",
)

# Outcome / benefit cues that make a headline carry value.
HEADLINE_VALUE_SIGNALS: tuple[str, ...] = (
    "without", "in seconds", "in minutes", "in one", "so you", "so your", "stop",
    "cut", "save", "ship", "deploy", "find", "build", "launch", "turn", "no more",
    "faster", "add ", "get ", "never",
)

WORD = re.compile(r"[A-Za-z][A-Za-z\-']*")
MIN_HEADLINE_WORDS = 4
SCANNABILITY_WORD_THRESHOLD = 120


@dataclass(frozen=True)
class Finding:
    """A single advisory note about the copy."""

    code: str
    severity: str  # "warn" | "info"
    message: str


def _words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def _first_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped.lstrip("#").strip()
    return ""


def check_headline(text: str) -> list[Finding]:
    headline = _first_line(text)
    if not headline:
        return []
    words = _words(headline)
    lowered = headline.lower()
    has_value = any(sig in lowered for sig in HEADLINE_VALUE_SIGNALS)
    has_category = any(noun in words for noun in CATEGORY_NOUNS)
    if len(words) < MIN_HEADLINE_WORDS:
        return [Finding(
            "weak-headline", "warn",
            "Headline is too short to carry a value proposition. Lead with the "
            "outcome a visitor gets, not the product name.")]
    if has_category and not has_value:
        return [Finding(
            "weak-headline", "warn",
            "Headline names a category ('platform', 'tool', ...) but no outcome. "
            "Say what the visitor gets, not what kind of thing it is.")]
    return []


def check_cta(text: str) -> list[Finding]:
    if any(sig in text.lower() for sig in CTA_SIGNALS):
        return []
    return [Finding(
        "no-cta", "warn",
        "No call-to-action found. Tell the reader the one next step "
        "(e.g. 'Get started', 'Install', a quickstart).")]


def check_audience(text: str) -> list[Finding]:
    if any(sig in text.lower() for sig in AUDIENCE_SIGNALS):
        return []
    return [Finding(
        "no-audience", "warn",
        "No target customer is named. Say who it's for.")]


def check_scannability(text: str) -> list[Finding]:
    if len(_words(text)) <= SCANNABILITY_WORD_THRESHOLD:
        return []
    headings = sum(1 for line in text.splitlines() if line.lstrip().startswith("#"))
    if headings == 0:
        return [Finding(
            "poor-scannability", "info",
            "Long copy with no headings reads as a wall of text. Break it into "
            "scannable sections — visitors skim before they read.")]
    return []


def check_buzzwords(text: str) -> list[Finding]:
    found = sorted({w for w in _words(text) if w in BUZZWORDS})
    if not found:
        return []
    return [Finding(
        "buzzwords", "warn",
        f"Buzzwords that could sit on any product's page: {', '.join(found)}. "
        "Replace each with a specific claim.")]


CHECKS = (
    check_headline,
    check_cta,
    check_audience,
    check_scannability,
    check_buzzwords,
)


def lint(text: str) -> list[Finding]:
    """Run all checks and return the combined findings."""
    findings: list[Finding] = []
    for check in CHECKS:
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
        return ("No issues found. The page leads with value, names an audience, "
                "and has a clear call-to-action.")
    lines = [f"{len(findings)} suggestion(s):", ""]
    for finding in findings:
        marker = "!" if finding.severity == "warn" else "-"
        lines.append(f" [{marker}] {finding.code}: {finding.message}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint landing-page / README copy.")
    parser.add_argument("path", nargs="?", help="Path to a text file to check.")
    parser.add_argument("--text", help="Copy passed directly as a string.")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON.")
    args = parser.parse_args(argv)

    text = _read_input(args)
    if not text.strip():
        parser.error("no input: pass --text, a file path, or pipe text via stdin")

    findings = lint(text)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print(_format_human(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
