from pydantic import BaseModel


class Entity(BaseModel):
    role: str
    name: str


class FinancialValue(BaseModel):
    description: str
    amount: float
    currency: str


class DocumentAnalysis(BaseModel):
    document_type: str
    summary: str
    entities: list[Entity]
    dates: list[str]
    financial_values: list[FinancialValue]
    risks: list[str]
    missing_information: list[str]