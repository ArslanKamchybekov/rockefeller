from pydantic import BaseModel

class LegalDocsInput (BaseModel):
    idea: str

class LegalDocsOutput (BaseModel):
    docs: str