from enum import Enum


class DocumentSource(str, Enum):
    MARKDOWN = "markdown"
    PDF = "pdf"
    HTML = "html"
    CONFLUENCE = "confluence"
    JIRA = "jira"

class DocumentType(str, Enum):
    """Business document categories."""

    ARCHITECTURE = "architecture"
    RUNBOOK = "runbook"
    INCIDENT = "incident"
    API = "api"
    TUTORIAL = "tutorial"
    OTHER = "other"