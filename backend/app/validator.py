from app.schemas import InvoiceFields


def validate(data: InvoiceFields, text: str) -> list[str]:
    issues = []

    if data is None:
        return ["No data extracted"]

    if not data.vendor_name:
        issues.append("Missing vendor_name")

    if not data.invoice_number:
        issues.append("Missing invoice_number")

    if not data.invoice_date:
        issues.append("Missing invoice_date")

    if data.total_amount is None:
        issues.append("Missing total_amount")

    if not data.currency:
        issues.append("Missing currency")

    if data.invoice_number and data.invoice_number not in text:
        issues.append("Invoice number not found in invoice text")

    if data.vendor_name and data.vendor_name not in text:
        issues.append("Vendor name not found in invoice text")

    if "€" in text and data.currency != "EUR":
        issues.append("Currency mismatch: invoice contains €, but extracted currency is not EUR")

    if "$" in text and data.currency != "USD":
        issues.append("Currency mismatch: invoice contains $, but extracted currency is not USD")

    return issues