from pydantic import BaseModel, field_validator
from typing import Optional, List


class InvoiceFields(BaseModel):
    vendor_name: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None

    @field_validator("total_amount", mode="before")
    @classmethod
    def clean_total_amount(cls, value):
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            value = (
                value.replace("€", "")
                     .replace("$", "")
                     .replace(",", "")
                     .strip()
            )

            if value == "":
                return None

            return float(value)

        raise ValueError("Invalid total_amount format")

    @field_validator("currency", mode="before")
    @classmethod
    def clean_currency(cls, value):
        if value is None:
            return None

        value = str(value).strip().upper()

        if value in ["€", "EURO", "EUROS"]:
            return "EUR"

        if value in ["$", "DOLLAR", "DOLLARS", "USD"]:
            return "USD"

        return value


class AgentResult(BaseModel):
    status: str
    extracted_data: InvoiceFields
    issues: List[str] = []
    attempts: int = 1