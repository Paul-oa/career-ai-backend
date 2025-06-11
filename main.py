from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from uuid import uuid4
from datetime import datetime

app = FastAPI()

# In-memory ukladanie (na testovanie, neskôr DB)
resumes = {}

@app.get("/")
def read_root():
    return {"message": "Career AI backend is running"}

@app.get("/docs-test")
def read_docs_test():
    return {"info": "Docs are at /docs"}

@app.post("/resume/upload")
async def upload_resume(user_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are allowed")

    parsed_text = f"Simulated parsed text from {file.filename}"

    resume_id = str(uuid4())
    resumes[resume_id] = {
        "id": resume_id,
        "user_id": user_id,
        "filename": file.filename,
        "parsed_text": parsed_text,
        "created_at": datetime.now().isoformat()
    }

    return {
        "resume_id": resume_id,
        "parsed_text": parsed_text
    }