from app.services.match_validation import is_valid_source_quote


def test_valid_source_quote():
    description = (
        "You will work closely with senior "
        "accountants and auditors."
    )

    assert is_valid_source_quote(
        "work closely with senior accountants",
        description,
    )


def test_invented_source_quote():
    description = "Assist with bookkeeping."

    assert not is_valid_source_quote(
        "Five years of Python experience",
        description,
    )


def test_truncated_source_quote():
    description = (
        "Assist with bookkeeping and financial rep…"
    )

    assert not is_valid_source_quote(
        "financial rep…",
        description,
    )