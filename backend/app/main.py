import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.utils import extract_text_from_pdf
from app.agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/process")
async def process(file: UploadFile = File(...)):
    try:
        path = os.path.join(UPLOAD_DIR, file.filename)

        with open(path, "wb") as f:
            f.write(await file.read())

        text = extract_text_from_pdf(path)

        print("===== EXTRACTED PDF TEXT =====")
        print(text[:2000])
        print("===== END EXTRACTED PDF TEXT =====")

        if not text.strip():
            return {
                "status": "error",
                "message": "No readable text found in PDF. This may be a scanned PDF."
            }

        result = run_agent(text)
        return result.model_dump()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }