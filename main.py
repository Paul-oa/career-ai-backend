from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from uuid import uuid4
from datetime import datetime
from typing import Optional

app = FastAPI()

resumes = {}
cover_letters = {}

@app.get("/")
def read_root():
    return {"message": "Career AI backend is running"}

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

@app.post("/cover-letter/generate")
async def generate_cover_letter(
    user_id: str = Form(...),
    resume_id: str = Form(...),
    job_position: str = Form(...),
    company_name: Optional[str] = Form(None)
):
    resume = resumes.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    prompt = f"Generate a cover letter for position '{job_position}' at '{company_name or 'a company'}' based on resume: {resume['parsed_text']}"
    ai_output = f"Generated cover letter for {job_position} at {company_name or 'a company'}"

    letter_id = str(uuid4())
    cover_letters[letter_id] = {
        "id": letter_id,
        "user_id": user_id,
        "resume_id": resume_id,
        "job_position": job_position,
        "company_name": company_name,
        "generated_text": ai_output,
        "created_at": datetime.now().isoformat()
    }

    return {
        "cover_letter_id": letter_id,
        "generated_text": ai_output
    }