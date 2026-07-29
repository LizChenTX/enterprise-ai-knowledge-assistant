from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.enums import DocumentSource, DocumentType

class Metadata(BaseModel):
    """
    Metadata describing a document.

    Technical metadata:
        - source

    Business metadata:
        - document_type
        - service
        - owner
    """

    title: str
    source: DocumentSource = Field(
        description="Original source of the document."
    )

    document_type: DocumentType = Field(
        description="Business category of the document."
    )

    service: Optional[str] = Field(
        default=None,
        description="Related business service."
    )

    owner: Optional[str] = Field(
        default=None,
        description="Owner of this document."
    )

    tags: List[str] = Field(
        default_factory=list,
        description="Searchable tags."
    )

    version: str = Field(
        default="1.0",
        description="Document version."
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )
