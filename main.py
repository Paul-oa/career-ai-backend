from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
from uuid import uuid4
import shutil
import os
import openai
from dotenv import load_dotenv

# Načítaj .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Povolenie CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pamäťová "databáza"
resumes = {}
cover_letters = {}

# === ENDPOINTY ===

@app.get("/")
def read_root():
    return {"message": "Career AI Backend is running"}

@app.post("/resume/upload")
def upload_resume(user_id: str = Form(...), file: UploadFile = File(...)):
    file_path = f"uploaded_files/{uuid4()}_{file.filename}"
    os.makedirs("uploaded_files", exist_ok=True)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_id = str(uuid4())
    parsed_text = f"Simulovaný text z {file.filename}"

    resumes[resume_id] = {
        "user_id": user_id,
        "file_url": file_path,
        "parsed_text": parsed_text,
        "created_at": datetime.now()
    }

    return {"resume_id": resume_id, "parsed_text": parsed_text}

@app.post("/cover-letter/generate")
def generate_cover_letter(
    user_id: str = Form(...),
    resume_id: str = Form(...),
    job_position: str = Form(...),
    company_name: Optional[str] = Form(None)
):
    resume = resumes.get(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    prompt = (
        f"Based on the following resume, write a professional cover letter for "
        f"the position '{job_position}' at '{company_name or 'a company'}'. Resume:\n{resume['parsed_text']}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes professional cover letters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600
        )
        generated_text = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    letter_id = str(uuid4())
    cover_letters[letter_id] = {
        "user_id": user_id,
        "resume_id": resume_id,
        "job_position": job_position,
        "company_name": company_name,
        "generated_text": generated_text,
        "created_at": datetime.now()
    }

    return {"cover_letter_id": letter_id, "generated_text": generated_text}
