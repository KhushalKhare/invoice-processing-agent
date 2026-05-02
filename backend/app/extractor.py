import os
import json
import re
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

from app.prompts import BASIC_PROMPT, RETRY_PROMPT
from app.schemas import InvoiceFields

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def rule_based_extract(text: str) -> InvoiceFields:
    vendor_name = None
    invoice_number = None
    invoice_date = None
    total_amount = None
    currency = None

    # Invoice number
    invoice_match = re.search(r"Invoice number\s+([A-Z0-9\-]+)", text, re.IGNORECASE)
    if invoice_match:
        invoice_number = invoice_match.group(1).strip()

    # Invoice date
    date_match = re.search(r"Date of issue\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", text, re.IGNORECASE)
    if date_match:
        invoice_date = date_match.group(1).strip()

    # Vendor name: line before/near "Bill to"
    vendor_match = re.search(r"Date due.*?\n(.+?)\s+Bill to", text, re.IGNORECASE | re.DOTALL)
    if vendor_match:
        vendor_name = vendor_match.group(1).strip()

    # Total / Amount due
    amount_match = re.search(r"Amount due\s+€?([\d,.]+)", text, re.IGNORECASE)
    if not amount_match:
        amount_match = re.search(r"Total\s+€?([\d,.]+)", text, re.IGNORECASE)

    if amount_match:
        total_amount = float(amount_match.group(1).replace(",", ""))

    # Currency
    if "€" in text:
        currency = "EUR"
    elif "$" in text:
        currency = "USD"

    return InvoiceFields(
        vendor_name=vendor_name,
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        total_amount=total_amount,
        currency=currency
    )


def parse_json_from_output(output: str) -> dict:
    output = output.strip()

    try:
        return json.loads(output)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*?\}", output, re.DOTALL)

    if not match:
        raise ValueError(f"No JSON found: {output}")

    return json.loads(match.group())


def call_llm(prompt: str) -> InvoiceFields:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "Return only one valid JSON object. "
                    "No explanation. No repeated JSON. "
                    "Do not invent data."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=250,
        timeout=30,
    )

    output = response.choices[0].message.content

    if output is None:
        raise ValueError("Groq returned empty response")

    output = output.strip()
    print("RAW MODEL OUTPUT:", output)

    parsed = parse_json_from_output(output)
    return InvoiceFields(**parsed)


def extract_once(text: str) -> InvoiceFields:
    # First use deterministic extraction
    extracted = rule_based_extract(text)

    if (
        extracted.vendor_name
        and extracted.invoice_number
        and extracted.invoice_date
        and extracted.total_amount is not None
        and extracted.currency
    ):
        print("USING RULE-BASED EXTRACTION")
        return extracted

    # Only fallback to LLM if rule-based extraction fails
    prompt = BASIC_PROMPT.format(document_text=text)
    return call_llm(prompt)


def extract_retry(text: str) -> InvoiceFields:
    # Retry should also prefer deterministic extraction
    extracted = rule_based_extract(text)

    if (
        extracted.vendor_name
        and extracted.invoice_number
        and extracted.invoice_date
        and extracted.total_amount is not None
        and extracted.currency
    ):
        print("USING RULE-BASED RETRY EXTRACTION")
        return extracted

    prompt = RETRY_PROMPT.format(document_text=text)
    return call_llm(prompt)