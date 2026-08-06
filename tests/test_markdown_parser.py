from app.models.section import Section
from app.parsers.markdown_parser import MarkdownParser


def test_parse_markdown_sections():

    text = (
        "# Authentication\n\n"
        "JWT token.\n\n"
        "OAuth token.\n\n"
        "# Database\n\n"
        "PostgreSQL."
    )

    parser = MarkdownParser()

    sections = parser.parse(text)

    assert len(sections) == 2

    assert sections[0] == Section(
        title="Authentication",
        content=(
            "JWT token.\n\n"
            "OAuth token."
        ),
    )

    assert sections[1] == Section(
        title="Database",
        content="PostgreSQL.",
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
        title=None,
        content=(
            "Paragraph One.\n\n"
            "Paragraph Two."
        ),
    )