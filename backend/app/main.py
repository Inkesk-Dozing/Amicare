import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.seed_data import seed_database
from app.routers import assessment, helplines, resources, chat

# Ensure database tables exist and seed on startup
Base.metadata.create_all(bind=engine)
try:
    seed_database()
except Exception as e:
    print(f"Seed note: {e}")

app = FastAPI(
    title="AmiCare API",
    description="Non-diagnostic Stress Self-Assessment & Support Helpline Referral System API",
    version="1.0.0"
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat.router)
app.include_router(assessment.router)
app.include_router(helplines.router)
app.include_router(resources.router)

@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "AmiCare Backend",
        "version": "1.0.0"
    }
