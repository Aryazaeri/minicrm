import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, leads, contacts, ai

app = FastAPI(title="Mini CRM API", version="1.0.0")

origins = ["http://localhost:5173", "http://localhost:3000"]
extra = os.getenv("CORS_ORIGINS", "")
if extra:
    origins.extend([o.strip() for o in extra.split(",") if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(contacts.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "Mini CRM API running"}
