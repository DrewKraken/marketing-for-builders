"""Unit tests for landing_lint."""

from __future__ import annotations

import json

from landing_lint import (
    check_audience,
    check_buzzwords,
    check_cta,
    check_headline,
    check_scannability,
    lint,
    main,
)


def codes(findings) -> set[str]:
    return {f.code for f in findings}


# --- headline ---------------------------------------------------------------

def test_headline_too_short():
    assert "weak-headline" in codes(check_headline("# Acme Observe"))


def test_headline_category_only():
    assert "weak-headline" in codes(check_headline("The unified observability platform"))


def test_headline_strong_outcome():
    assert check_headline("Find out why production broke in minutes, not hours") == []


def test_headline_strong_with_action():
    assert check_headline("Ship to your servers in one command without scripts") == []


# --- call-to-action ---------------------------------------------------------

def test_cta_present():
    assert check_cta("Get started today with one command.") == []


def test_cta_missing():
    assert "no-cta" in codes(check_cta("It does a lot of useful things for you."))


# --- audience ---------------------------------------------------------------

def test_audience_present():
    assert check_audience("Built for on-call engineers.") == []


def test_audience_missing():
    assert "no-audience" in codes(check_audience("A thing that does stuff well."))


# --- scannability -----------------------------------------------------------

def test_scannability_wall_of_text():
    wall = " ".join(["word"] * 130)
    assert "poor-scannability" in codes(check_scannability(wall))


def test_scannability_ok_with_headings():
    body = "# Title\n" + " ".join(["word"] * 130)
    assert check_scannability(body) == []


def test_scannability_short_text_ok():
    assert check_scannability("Short and sweet.") == []


# --- buzzwords --------------------------------------------------------------

def test_buzzwords_flagged():
    assert "buzzwords" in codes(check_buzzwords("A seamless, robust, scalable platform."))


# --- aggregate + CLI --------------------------------------------------------

def test_lint_clean_landing_copy():
    text = (
        "# Ship to your servers in one command\n"
        "For engineers tired of brittle deploy scripts. Get started in minutes.\n"
        "## How it works\nOne binary, one YAML file."
    )
    assert lint(text) == []


def test_main_json_output(capsys):
    rc = main(["--text", "The powerful platform.", "--json"])
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert any(item["code"] == "weak-headline" for item in data)


def test_main_clean_text_reports_no_issues(capsys):
    rc = main(["--text",
               "# Ship to your servers in one command\nFor engineers. Get started in minutes."])
    assert rc == 0
    assert "No issues found" in capsys.readouterr().out
