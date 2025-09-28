from pydantic import BaseModel
from typing import List, Optional

class LegalDocsInput (BaseModel):
    idea: str

class LegalDocument (BaseModel):
    doc_type: str
    title: str
    summary: str
    content: str
    placeholders: List[str]
    defaults_used: dict
    pdf_url: Optional[str] = None

class LegalDocsOutput (BaseModel):
    docs: str
    pdfs: Optional[List[dict]] = None  # List of {title, pdf_url, pdf_data}