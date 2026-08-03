from app.chunking.recursive_chunker import RecursiveChunker


def test_parse_markdown_sections():

    text = (
        "# Authentication\n\n"
        "JWT token.\n\n"
        "OAuth token.\n\n"
        "# Database\n\n"
        "PostgreSQL."
    )

    parser = RecursiveChunker()

    sections = parser._parse_markdown_sections(text)

    assert len(sections) == 3

    assert sections[0] == (
        "Authentication",
        "JWT token.",
    )

    assert sections[1] == (
        "Authentication",
        "OAuth token.",
    )

    assert sections[2] == (
        "Database",
        "PostgreSQL.",
    )

def test_parse_without_heading():

    text = (
        "Paragraph One.\n\n"
        "Paragraph Two."
    )

    parser = RecursiveChunker()

    sections = parser._parse_markdown_sections(text)

    assert len(sections) == 2

    assert sections[0] == (
        None,
        "Paragraph One.",
    )

    assert sections[1] == (
        None,
        "Paragraph Two.",
    )