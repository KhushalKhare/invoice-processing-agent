Use this cleaner, stronger `README.md`. Less “student project,” more “I understand production AI systems.” Humanity may recover.

````md
# Invoice Processing Agent

A full-stack invoice extraction system that converts PDF invoices into structured JSON using a hybrid extraction pipeline.

The project combines deterministic rule-based parsing with an optional LLM fallback, validation logic, and a simple frontend interface.

---

## Why This Project Matters

Many AI demos rely only on prompts and fail when inputs become messy.

This project focuses on a more realistic approach:

- Extract readable text from invoices
- Use deterministic parsing for reliable fields
- Use LLMs only as fallback
- Validate extracted results
- Return structured, machine-readable output

The main goal is not just to use an LLM, but to build a more reliable AI-assisted document processing system.

---

## Features

- PDF invoice upload
- Text extraction from PDF files
- Rule-based extraction for common invoice fields
- LLM fallback for difficult formats
- Validation layer for extracted data
- FastAPI backend
- HTML/CSS/JavaScript frontend
- Docker support
- JSON API response

---

## Extracted Fields

The system extracts:

- Vendor name
- Invoice number
- Invoice date
- Total amount
- Currency

Example output:

```json
{
  "status": "success",
  "extracted_data": {
    "vendor_name": "Germany Living 2 GmbH",
    "invoice_number": "600CDD09165982",
    "invoice_date": "May 1, 2026",
    "total_amount": 91.49,
    "currency": "EUR"
  },
  "issues": [],
  "attempts": 1
}
````

---

## Architecture

```text
Frontend
   |
   v
FastAPI Backend
   |
   v
PDF Text Extraction
   |
   v
Rule-Based Extraction
   |
   v
LLM Fallback
   |
   v
Validation Layer
   |
   v
Structured JSON Response
```

---

## Tech Stack

| Layer          | Technology            |
| -------------- | --------------------- |
| Backend        | FastAPI, Python       |
| PDF Processing | pdfplumber            |
| AI/LLM         | Groq API, LLaMA       |
| Workflow       | LangGraph             |
| Frontend       | HTML, CSS, JavaScript |
| Deployment     | Docker                |

---

## Project Structure

```text
invoice-processing-agent/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── agent.py
│   │   ├── extractor.py
│   │   ├── validator.py
│   │   ├── schemas.py
│   │   ├── prompts.py
│   │   └── utils.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/KhushalKhare/invoice-processing-agent.git
cd invoice-processing-agent
```

### 2. Create virtual environment

Windows:

```bash
python -m venv .venv
.\\.venv\\Scripts\\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

## Run Locally

### Start backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### Start frontend

Open a second terminal:

```bash
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

Frontend runs at:

```text
http://127.0.0.1:5500/index.html
```

---

## Run with Docker

### Build image

```bash
docker build -t invoice-processing-agent .
```

### Run container

```bash
docker run -p 8000:8000 --env-file .env invoice-processing-agent
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoint

### `POST /process`

Uploads an invoice PDF and returns extracted invoice data.

Request:

```text
multipart/form-data
file: invoice.pdf
```

Response:

<img width="1628" height="954" alt="image" src="https://github.com/user-attachments/assets/651fc27d-3240-43a2-ac46-fc37848977e5" />


## Key Engineering Decisions

### Rule-based extraction first

Common invoice fields such as total amount, currency, invoice number, and dates are often better extracted deterministically.

This avoids unnecessary LLM hallucinations.

### LLM fallback second

The LLM is used only when deterministic extraction cannot confidently extract all fields.

This keeps the system more reliable and cheaper to run.

### Validation layer

Extracted values are checked for missing fields, currency mismatches, and inconsistent outputs.

LLM output is treated as untrusted until validated.

---

## Current Limitations

* Works best on text-based PDFs
* Scanned invoices may require OCR
* Regex rules may need expansion for diverse invoice layouts
* PDF extraction can sometimes lose formatting, such as hyphens in invoice numbers
* No database persistence yet

---

## Future Improvements

* Add OCR support for scanned PDFs
* Add confidence scoring
* Support multilingual invoices
* Store processed invoices in a database
* Add authentication
* Add CSV/Excel export
* Improve layout-aware extraction
* Add tests for multiple invoice formats

---

## Learning Outcomes

This project demonstrates:

* Full-stack AI application development
* FastAPI backend design
* PDF processing
* LLM integration
* Hybrid extraction strategy
* Validation-driven AI engineering
* Dockerized deployment
* Practical debugging of LLM hallucinations

---

## License

This project is intended for portfolio and educational use.


C:\Users\khush\Invoice Reader\README.md
````
