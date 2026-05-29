"""Unit tests for launch_lint."""

from __future__ import annotations

import json

from launch_lint import (
    check_buzzwords,
    check_hype,
    check_linkedin_hook,
    check_ph_tagline,
    check_reddit_disclosure,
    check_reddit_value,
    check_show_hn_title,
    check_show_hn_trylink,
    check_upvote_begging,
    check_x_post,
    lint,
    main,
)


def codes(findings) -> set[str]:
    return {f.code for f in findings}


# --- always-on: upvote-begging ----------------------------------------------

def test_upvote_begging_flagged():
    assert "upvote-begging" in codes(check_upvote_begging("Please upvote us on Product Hunt"))


def test_upvote_begging_support_phrase():
    assert "upvote-begging" in codes(check_upvote_begging("Would love your support — vote for us!"))


def test_upvote_begging_clean():
    assert check_upvote_begging("I'd love your honest feedback.") == []


# --- always-on: hype --------------------------------------------------------

def test_hype_superlatives_flagged():
    assert "hype-superlatives" in codes(check_hype("This is an amazing, groundbreaking tool"))


def test_hype_exclamation_runs_flagged():
    assert "hype-superlatives" in codes(check_hype("It just works!! Try it!!"))


def test_hype_number_one_flagged():
    assert "hype-superlatives" in codes(check_hype("We hit #1 on the leaderboard"))


def test_hype_clean():
    assert check_hype("A small CLI that deploys web apps to your own servers.") == []


# --- always-on: buzzwords ---------------------------------------------------

def test_buzzwords_flagged():
    assert "buzzwords" in codes(check_buzzwords("A seamless, scalable, robust platform."))


# --- show_hn ----------------------------------------------------------------

def test_show_hn_title_good():
    title = "Show HN: DeployKit – deploy web apps to your own servers in one command"
    assert check_show_hn_title(title) == []


def test_show_hn_title_missing():
    assert "show-hn-title" in codes(check_show_hn_title("I made a deploy tool, take a look"))


def test_show_hn_title_no_colon():
    assert "show-hn-title" in codes(check_show_hn_title("Show HN DeployKit deploys your apps"))


def test_show_hn_title_name_only():
    assert "show-hn-title" in codes(check_show_hn_title("Show HN: DeployKit"))


def test_show_hn_title_exclamation():
    title = "Show HN: DeployKit – deploy apps in one command!"
    assert "show-hn-title" in codes(check_show_hn_title(title))


def test_show_hn_trylink_url_ok():
    assert check_show_hn_trylink("Try it: https://deploykit.dev") == []


def test_show_hn_trylink_install_ok():
    assert check_show_hn_trylink("Get it with `brew install deploykit`.") == []


def test_show_hn_trylink_missing():
    assert "show-hn-no-link" in codes(check_show_hn_trylink("It deploys your apps fast."))


# --- producthunt ------------------------------------------------------------

def test_ph_tagline_too_long():
    long = "Automate your entire multi-cloud deployment pipeline from one YAML file today"
    assert "ph-tagline-length" in codes(check_ph_tagline(long))


def test_ph_tagline_article_opener():
    assert "ph-tagline-verb" in codes(check_ph_tagline("The fastest way to deploy your apps"))


def test_ph_tagline_clean():
    assert check_ph_tagline("Deploy web apps in one command") == []


# --- reddit -----------------------------------------------------------------

def test_reddit_disclosure_present():
    assert check_reddit_disclosure("I built a small CLI for deploys this year.") == []


def test_reddit_disclosure_missing():
    assert "reddit-no-disclosure" in codes(check_reddit_disclosure("Check out this deploy tool."))


def test_reddit_low_value_link_dump():
    assert "reddit-low-value" in codes(check_reddit_value("Check it out: https://deploykit.dev"))


def test_reddit_value_ok_when_substantive():
    text = (
        "I built this after years of brittle deploy scripts and wanted something "
        "that just shipped my app to my own servers without Kubernetes. Here it is "
        "if it helps anyone: https://deploykit.dev"
    )
    assert check_reddit_value(text) == []


# --- linkedin ---------------------------------------------------------------

def test_linkedin_weak_hook_bare_link():
    findings = check_linkedin_hook("https://deploykit.dev\n\nMore below.")
    assert "linkedin-weak-hook" in codes(findings)


def test_linkedin_weak_hook_too_short():
    assert "linkedin-weak-hook" in codes(check_linkedin_hook("DeployKit 1.0\n\nDetails follow."))


def test_linkedin_link_in_hook():
    text = "I rebuilt how my team deploys — see it at https://deploykit.dev, here's why."
    assert "linkedin-link-in-hook" in codes(check_linkedin_hook(text))


def test_linkedin_hook_clean():
    text = (
        "I spent six months rebuilding how we ship to production, and the result "
        "surprised me.\n\nHere's the story, and a link in the comments."
    )
    assert check_linkedin_hook(text) == []


# --- x / twitter ------------------------------------------------------------

def test_x_post_too_long():
    block = " ".join(["word"] * 70)  # ~349 chars, no blank line
    assert "x-post-length" in codes(check_x_post(block))


def test_x_link_in_main_post():
    assert "x-link-in-post" in codes(check_x_post("Just shipped DeployKit https://deploykit.dev"))


def test_x_post_clean():
    text = (
        "Just shipped DeployKit after six months: it deploys web apps to your own "
        "servers in one command — no Kubernetes, no YAML sprawl. Link in the reply."
    )
    assert check_x_post(text) == []


# --- aggregate + CLI --------------------------------------------------------

def test_lint_runs_only_always_on_without_channel():
    assert codes(lint("This is amazing!!")) == {"hype-superlatives"}


def test_lint_clean_show_hn_post():
    text = (
        "Show HN: DeployKit – deploy web apps to your own servers in one command\n\n"
        "I built DeployKit for teams who never moved to Kubernetes. "
        "Try it: https://deploykit.dev"
    )
    assert lint(text, "show_hn") == []


def test_main_json_output(capsys):
    rc = main(["--text", "Please upvote us, it's amazing!!", "--channel", "show_hn", "--json"])
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    found = {item["code"] for item in data}
    assert "upvote-begging" in found
    assert "hype-superlatives" in found


def test_main_clean_text_reports_no_issues(capsys):
    rc = main([
        "--text",
        "Show HN: DeployKit – deploy web apps to your own servers\n\n"
        "Try it: https://deploykit.dev",
        "--channel", "show_hn",
    ])
    assert rc == 0
    assert "No issues found" in capsys.readouterr().out
