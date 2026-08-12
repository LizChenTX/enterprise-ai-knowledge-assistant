from app.models.section import Section
from app.parsers.markdown_parser import MarkdownParser


def test_parse_markdown_heading_hierarchy():
    text = (
        "# Authentication\n\n"
        "Authentication overview.\n\n"
        "## JWT\n\n"
        "JWT tokens are used for authentication.\n\n"
        "### Expiration\n\n"
        "JWT tokens expire after one hour.\n\n"
        "## OAuth\n\n"
        "OAuth is another authentication protocol.\n\n"
        "# Database\n\n"
        "PostgreSQL is our primary database."
    )

    parser = MarkdownParser()

    sections = parser.parse(text)

    assert len(sections) == 5

    assert sections[0] == Section(
        heading_path=[
            "Authentication",
        ],
        content="Authentication overview.",
    )

    assert sections[1] == Section(
        heading_path=[
            "Authentication",
            "JWT",
        ],
        content="JWT tokens are used for authentication.",
    )

    assert sections[2] == Section(
        heading_path=[
            "Authentication",
            "JWT",
            "Expiration",
        ],
        content="JWT tokens expire after one hour.",
    )

    assert sections[3] == Section(
        heading_path=[
            "Authentication",
            "OAuth",
        ],
        content="OAuth is another authentication protocol.",
    )

    assert sections[4] == Section(
        heading_path=[
            "Database",
        ],
        content="PostgreSQL is our primary database.",
    )


def test_parse_without_heading():
    text = (
        "Paragraph One.\n\n"
        "Paragraph Two."
    )

    parser = MarkdownParser()

    sections = parser.parse(text)

    assert len(sections) == 1

    assert sections[0] == Section(
        heading_path=[],
        content=(
            "Paragraph One.\n\n"
            "Paragraph Two."
        ),
    )

def test_parse_heading():
    parser = MarkdownParser()

    assert parser._parse_heading(
        "# Authentication"
    ) == (1, "Authentication")

    assert parser._parse_heading(
        "## JWT"
    ) == (2, "JWT")

    assert parser._parse_heading(
        "### Expiration"
    ) == (3, "Expiration")

def test_parse_non_heading():
    parser = MarkdownParser()

    assert parser._parse_heading(
        "JWT token explanation."
    ) is None

    assert parser._parse_heading(
        ""
    ) is None