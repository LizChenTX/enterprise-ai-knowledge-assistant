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

        heading_path: list[str] = []
        current_content: list[str] = []

        for line in text.splitlines():
            heading = self._parse_heading(line)

            if heading is not None:
                self._add_section(
                    sections=sections,
                    heading_path=heading_path,
                    content_lines=current_content,
                )

                level, title = heading

                heading_path = heading_path[: level - 1]
                heading_path.append(title)

                current_content = []

            else:
                current_content.append(line)

        self._add_section(
            sections=sections,
            heading_path=heading_path,
            content_lines=current_content,
        )

        return sections

    def _parse_heading(
        self,
        line: str,
    ) -> tuple[int, str] | None:
        stripped_line = line.strip()

        if not stripped_line.startswith("#"):
            return None

        level = len(stripped_line) - len(
            stripped_line.lstrip("#")
        )

        title = stripped_line[level:].strip()

        if not title:
            return None

        return level, title

    def _add_section(
        self,
        sections: list[Section],
        heading_path: list[str],
        content_lines: list[str],
    ) -> None:
        content = "\n".join(content_lines).strip()

        if content:
            sections.append(
                Section(
                    heading_path=heading_path.copy(),
                    content=content,
                )
            )