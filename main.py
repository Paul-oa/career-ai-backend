from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from typing import Optional
from datetime import datetime
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

resumes = {}

@app.get("/")
def read_root():
    return {"message": "Career AI backend running."}

@app.post("/resume/upload")
async def upload_resume(user_id: str = Form(...), file: UploadFile = File(...)):
    upload_folder = "uploaded_files"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = f"{upload_folder}/{uuid4()}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_id = str(uuid4())
    resumes[resume_id] = {
        "user_id": user_id,
        "file_path": file_path,
        "parsed_text": f"Simulated parsing of {file.filename}",
        "created_at": str(datetime.now())
    }
    return {"resume_id": resume_id}
