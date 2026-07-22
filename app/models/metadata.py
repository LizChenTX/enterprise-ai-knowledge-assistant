from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

class Metadata(BaseModel):
    """Business metadata describing a document.

    Metadata is used for filtering, organization,
    and retrieval optimization."""

    title: str
    source: str = Field(
        description="Document source, e.g. markdown, pdf, confluence"
    )

    document_type: str = Field(
        description="architecture, runbook, incident, api...")
    
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
