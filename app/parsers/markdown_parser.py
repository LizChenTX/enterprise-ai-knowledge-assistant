from app.models.section import Section


class MarkdownParser:
    """
    Parse markdown into logical sections.
    """

    def parse(
        self,
        text: str,
    ) -> list[Section]:
        raise NotImplementedError