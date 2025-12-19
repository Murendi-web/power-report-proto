from fastapi import FastAPI
from scheduler import start_scheduler
from run_pipeline import run_pipeline

app = FastAPI()

@app.on_event("startup")
def startup():
    start_scheduler()

@app.get("/run")
def run_now():
    run_pipeline()
    return {"status": "Pipeline executed"}
