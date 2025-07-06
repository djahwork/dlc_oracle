from fastapi import FastAPI
from api.routes import router as contract_router
from db.database import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(contract_router)
