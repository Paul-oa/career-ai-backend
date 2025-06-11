from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Career AI backend is running"}

@app.get("/docs-test")
def read_docs_test():
    return {"info": "Docs are at /docs"}