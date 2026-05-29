"""Unit tests for positioning_lint."""

from __future__ import annotations

import json

from positioning_lint import (
    check_audience,
    check_benefit_language,
    check_buzzwords,
    check_sentence_length,
    check_vague_qualifiers,
    lint,
    main,
)


def codes(findings) -> set[str]:
    return {f.code for f in findings}


# --- buzzwords --------------------------------------------------------------

def test_buzzwords_flagged():
    findings = check_buzzwords("A seamless, robust, next-generation platform.")
    assert "buzzwords" in codes(findings)
    assert "seamless" in findings[0].message
    assert "next-generation" in findings[0].message


def test_leverage_and_synergies_are_buzzwords():
    findings = check_buzzwords("Leverage synergies across teams.")
    assert "buzzwords" in codes(findings)


def test_buzzwords_clean():
    assert check_buzzwords("Cuts invoice reconciliation from 3 days to 20 minutes.") == []


# --- vague qualifiers -------------------------------------------------------

def test_vague_qualifiers_flagged():
    findings = check_vague_qualifiers("It is easy, fast, and intuitive.")
    assert "vague-qualifiers" in codes(findings)
    msg = findings[0].message
    assert "easy" in msg and "fast" in msg


def test_vague_qualifiers_clean():
    assert check_vague_qualifiers("Imports directly from QuickBooks.") == []


# --- benefit language -------------------------------------------------------

def test_benefit_language_missing():
    findings = check_benefit_language("A datastore with tunable consistency and a query layer.")
    assert "no-benefit-language" in codes(findings)


def test_benefit_language_present():
    assert check_benefit_language("Ship code so you can spend time on features.") == []


def test_benefit_language_skips_very_short_text():
    assert check_benefit_language("Fast database") == []


# --- audience ---------------------------------------------------------------

def test_audience_missing():
    findings = check_audience("A platform for managing data.")
    assert "no-audience" in codes(findings)


def test_audience_present():
    assert check_audience("For on-call engineers, find the cause fast.") == []


def test_audience_recognizes_non_dev_roles():
    # Surfaced by dogfooding on InvoiceParser Pro (audience = bookkeepers).
    assert check_audience("For independent bookkeepers and small businesses.") == []


def test_audience_recognizes_ap_finance_roles():
    # AP/finance variants beyond the base bookkeeper/accountant terms.
    assert check_audience("For accounts payable teams and controllers at growing firms.") == []
    assert check_audience("Built for CPAs and bookkeeping firms.") == []


def test_benefit_language_recognizes_so_you_verb():
    # Regression: an outcome clause is usually "so you <verb>", not only
    # "so you can". The bare verb form used to trip no-benefit-language —
    # including on this skill's own canonical example (see
    # examples/invoiceparser-pro.md, "...so you skip the retyping").
    assert check_benefit_language(
        "InvoiceParser Pro posts each invoice for you, so you skip the retyping."
    ) == []
    assert check_benefit_language(
        "It runs in CI, so they ship without babysitting the pipeline."
    ) == []


# --- sentence length --------------------------------------------------------

def test_long_sentence_flagged():
    sentence = " ".join(["word"] * 35) + "."
    findings = check_sentence_length(sentence)
    assert "long-sentence" in codes(findings)


def test_short_sentence_ok():
    assert check_sentence_length("Find the cause fast.") == []


# --- one-liner length (opt-in) ----------------------------------------------

def test_oneliner_length_flagged():
    long_oneliner = " ".join(["word"] * 22)
    assert "oneliner-too-long" in codes(lint(long_oneliner, oneliner=True))


def test_oneliner_length_ok_for_tight_copy():
    tight = "Bookkeepers: turn vendor invoices into clean QuickBooks and Xero entries in seconds."
    assert "oneliner-too-long" not in codes(lint(tight, oneliner=True))


def test_oneliner_check_off_by_default():
    assert "oneliner-too-long" not in codes(lint(" ".join(["word"] * 22)))


# --- aggregate lint() -------------------------------------------------------

def test_lint_clean_copy_has_no_findings():
    text = "Find out why production broke in minutes, not hours, for on-call engineers."
    assert lint(text) == []


def test_lint_aggregates_multiple_findings():
    found = codes(lint("A powerful platform for managing data."))
    assert {"buzzwords", "no-benefit-language", "no-audience"} <= found


# --- canonical example self-consistency -------------------------------------

def _example_field(label: str) -> str:
    """Pull a `> **Label:** ...` line from the InvoiceParser Pro example."""
    import re
    from pathlib import Path

    example = (
        Path(__file__).resolve().parent.parent / "examples" / "invoiceparser-pro.md"
    ).read_text(encoding="utf-8")
    m = re.search(rf"^>\s*\*\*{re.escape(label)}:\*\*\s*(.+)$", example, re.MULTILINE)
    assert m, f"{label} not found in example"
    # Strip markdown emphasis + surrounding quotes the way rendered copy reads.
    return m.group(1).replace("*", "").strip().strip('"')


def test_example_one_liner_lints_clean():
    # examples/invoiceparser-pro.md claims "the linter passed both the one-liner
    # and the value proposition clean." Pin that claim so the example can't drift
    # from its own tool (the BENEFIT_SIGNALS gap used to make this false).
    assert lint(_example_field("One-liner"), oneliner=True) == []


def test_example_value_proposition_lints_clean():
    assert lint(_example_field("Value proposition")) == []


# --- CLI --------------------------------------------------------------------

def test_main_json_output(capsys):
    rc = main(["--text", "A seamless platform.", "--json"])
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    assert any(item["code"] == "buzzwords" for item in data)


def test_main_clean_text_reports_no_issues(capsys):
    rc = main(["--text", "Cuts invoice prep from days to minutes for finance teams."])
    assert rc == 0
    assert "No issues found" in capsys.readouterr().out
