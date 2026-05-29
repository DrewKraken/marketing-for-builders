"""Unit tests for outreach_lint."""

from __future__ import annotations

import json

from outreach_lint import (
    check_ask,
    check_hype,
    check_length,
    check_links,
    check_merge_artifacts,
    check_optout,
    check_shouting,
    check_spam_trigger_words,
    lint,
    main,
)


def codes(findings) -> set[str]:
    return {f.code for f in findings}


# --- spam trigger words -----------------------------------------------------

def test_spam_phrases_flagged():
    found = check_spam_trigger_words("Act now — this limited time, risk-free offer ends soon.")
    assert "spam-trigger-words" in codes(found)


def test_spam_phrases_clean():
    assert check_spam_trigger_words("Saw your team posted a platform engineer role.") == []


def test_spam_does_not_flag_legit_free():
    # bare "free" in legitimate copy should not trip (we match phrases, not words)
    assert check_spam_trigger_words("It frees your team from babysitting deploys.") == []


# --- merge artifacts --------------------------------------------------------

def test_merge_token_flagged():
    assert "merge-artifacts" in codes(check_merge_artifacts("Hi {first_name}, quick question."))


def test_merge_greeting_flagged():
    assert "merge-artifacts" in codes(check_merge_artifacts("Hi there, I wanted to reach out."))


def test_merge_real_name_clean():
    assert check_merge_artifacts("Hi Sarah, quick question about your migration.") == []


# --- length -----------------------------------------------------------------

def test_too_long_flagged():
    assert "too-long" in codes(check_length(" ".join(["word"] * 160)))


def test_length_ok():
    assert check_length("Short, specific, one ask.") == []


# --- hype -------------------------------------------------------------------

def test_hype_flagged():
    assert "hype-superlatives" in codes(check_hype("Our revolutionary, game-changing platform."))


def test_hype_clean():
    assert check_hype("A single Go binary that deploys over SSH.") == []


# --- links ------------------------------------------------------------------

def test_link_overload_flagged():
    text = "See https://a.com and https://b.com and https://c.com"
    assert "link-overload" in codes(check_links(text))


def test_links_one_ok():
    assert check_links("Repo: https://example.com/deploykit") == []


# --- ask --------------------------------------------------------------------

def test_ask_question_ok():
    assert check_ask("Worth a quick look before you build more tooling?") == []


def test_ask_phrase_ok():
    assert check_ask("Let me know if you'd like me to send a short demo.") == []


def test_ask_missing_flagged():
    assert "no-ask" in codes(check_ask("Here is what we do. We help teams deploy faster."))


# --- opt-out ----------------------------------------------------------------

def test_optout_present():
    assert check_optout("No worries if this isn't relevant — just say so.") == []


def test_optout_missing_flagged():
    assert "missing-optout" in codes(check_optout("Thanks for your time.\n\nDrew"))


# --- shouting ---------------------------------------------------------------

def test_shouting_caps_flagged():
    assert "shouting" in codes(check_shouting("Get your FREE TRIAL TODAY."))


def test_shouting_exclamations_flagged():
    assert "shouting" in codes(check_shouting("Great offer!! Don't wait!!"))


def test_shouting_acronyms_ok():
    # allow-listed / short acronyms should not trip
    assert check_shouting("We're HIPAA compliant and expose a REST API.") == []


# --- aggregate + CLI --------------------------------------------------------

def test_lint_clean_cold_email():
    text = (
        "Hi Sarah — saw your team just posted a Platform Engineer role focused on the "
        "Kubernetes migration.\n\n"
        "I built DeployKit for teams making exactly that move: one Go binary that does "
        "rolling and canary deploys over SSH, with one-command rollback. No control "
        "plane to run.\n\n"
        "Worth a quick look before you wire up more tooling?\n\n"
        "No worries if this isn't relevant — just say so.\n\nDrew"
    )
    assert lint(text) == []


def test_main_json_output(capsys):
    rc = main(["--text", "ACT NOW!! Risk-free, 100% free {first_name}!", "--json"])
    assert rc == 0
    found = {item["code"] for item in json.loads(capsys.readouterr().out)}
    assert "spam-trigger-words" in found
    assert "merge-artifacts" in found


def test_followup_skips_optout_and_ask():
    # A breakup-style follow-up has no opt-out and no ask — fine in a thread.
    text = "One more angle: multi-workspace keeps each client's data clean and separate."
    full = codes(lint(text))
    assert "no-ask" in full and "missing-optout" in full
    fu = codes(lint(text, followup=True))
    assert "no-ask" not in fu and "missing-optout" not in fu


def test_followup_still_flags_spam():
    # Follow-up mode skips opt-out/ask but still catches spam tells.
    assert "spam-trigger-words" in codes(lint("Act now — risk-free!", followup=True))


def test_main_followup_flag(capsys):
    rc = main(["--text", "Quick new angle on the migration tail.", "--followup", "--json"])
    assert rc == 0
    found = {item["code"] for item in json.loads(capsys.readouterr().out)}
    assert "missing-optout" not in found and "no-ask" not in found


def test_main_clean_reports_no_issues(capsys):
    rc = main(["--text",
               "Hi Sarah — saw the migration role you posted. Worth a quick look at "
               "DeployKit?\n\nNo worries if not relevant.\n\nDrew"])
    assert rc == 0
    assert "No issues found" in capsys.readouterr().out
