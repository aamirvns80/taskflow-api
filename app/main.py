from fastapi import FastAPI

app = FastAPI(
    title="TaskFlow API",
    description="A task management API built with Python.",
    version="0.1.0")

@app.get("/")
def read_root():
    return {
        "message":"Welcome to TaskFlow API"
    }
    
@app.get("/health")
def health_check():
    return{
        "status":"healthy"
    }