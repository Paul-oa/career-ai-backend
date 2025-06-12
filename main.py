from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from uuid import uuid4
from datetime import datetime
from typing import Optional
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

resumes = {}
cover_letters = {}

@app.get("/")
def read_root():
    return {"message": "Career AI API is running"}

@app.post("/resume/upload")
async def upload_resume(user_id: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    parsed_text = f"Simulovaný text z {file.filename}"
    resume_id = str(uuid4())
    resumes[resume_id] = {
        "user_id": user_id,
        "file_name": file.filename,
        "parsed_text": parsed_text,
        "uploaded_at": datetime.now().isoformat()
    }
    return {"resume_id": resume_id, "parsed_text": parsed_text}

@app.post("/cover-letter/generate")
def generate_cover_letter(user_id: str = Form(...), resume_id: str = Form(...), job_position: str = Form(...), company_name: str = Form(...)):
    if resume_id not in resumes:
        raise HTTPException(status_code=404, detail="Resume not found.")

    resume_data = resumes[resume_id]
    parsed_text = resume_data["parsed_text"]

    prompt = f"""
    Based on the following resume, write a professional cover letter for the position '{job_position}' at '{company_name}'. Resume:
    {parsed_text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        generated_letter = response.choices[0].message.content.strip()
        cover_letters[resume_id] = {
            "user_id": user_id,
            "resume_id": resume_id,
            "cover_letter": generated_letter,
            "generated_at": datetime.now().isoformat()
        }
        return {"cover_letter": generated_letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))