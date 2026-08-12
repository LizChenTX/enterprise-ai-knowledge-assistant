from app.models.section import Section


class MarkdownParser:
    """
    Parse Markdown text into logical sections.
    """

    def parse(
        self,
        text: str,
    ) -> list[Section]:
        sections: list[Section] = []

        current_title: str | None = None
        current_content: list[str] = []

        for line in text.splitlines():
            if line.startswith("# "):
                self._add_section(
                    sections=sections,
                    title=current_title,
                    content_lines=current_content,
                )

                current_title = line[2:].strip()
                current_content = []

            else:
                current_content.append(line)

        self._add_section(
            sections=sections,
            title=current_title,
            content_lines=current_content,
        )

        return sections

    def _add_section(
        self,
        sections: list[Section],
        title: str | None,
        content_lines: list[str],
    ) -> None:
        content = "\n".join(content_lines).strip()

        if content:
            sections.append(
                Section(
                    title=title,
                    content=content,
                )
            )