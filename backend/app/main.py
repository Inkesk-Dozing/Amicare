import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.database import engine, Base
from app.seed_data import seed_database
from app.routers import assessment, helplines, resources, chat, face_scan

# Ensure database tables exist and seed on startup
Base.metadata.create_all(bind=engine)
try:
    seed_database()
except Exception as e:
    print(f"Seed note: {e}")

app = FastAPI(
    title="AmiCare API",
    description="Non-diagnostic Stress Self-Assessment & Support Helpline Referral System API with OpenCV Facial Stress Examination",
    version="1.1.0"
)

# CORS middleware: Allow all origins for anonymous, zero-friction client access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security & Privacy Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(self), microphone=(), geolocation=()"
    return response

# Register routers
app.include_router(chat.router)
app.include_router(assessment.router)
app.include_router(helplines.router)
app.include_router(resources.router)
app.include_router(face_scan.router)

@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "AmiCare Backend with OpenCV Facial Wellness Examination",
        "version": "1.1.0"
    }

# Mount Frontend static files
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_dir):
    # Route for root /
    @app.get("/", include_in_schema=False)
    def serve_frontend_root():
        index_file = os.path.join(frontend_dir, "index.html")
        return FileResponse(index_file)

    # Route for static assets directly
    @app.get("/{filename:path}", include_in_schema=False)
    def serve_frontend_files(filename: str):
        # Don't intercept API routes or docs
        if filename.startswith("api/") or filename.startswith("docs") or filename == "openapi.json":
            raise HTTPException(status_code=404, detail="Not Found")
        
        file_path = os.path.join(frontend_dir, filename)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
            
        public_path = os.path.join(frontend_dir, "public", filename)
        if os.path.isfile(public_path):
            return FileResponse(public_path)
            
        # If it's a media asset file, return 404 rather than fallback to index.html
        ext = os.path.splitext(filename)[1].lower()
        if ext in [".png", ".jpg", ".jpeg", ".ico", ".svg", ".css", ".js", ".json"]:
            raise HTTPException(status_code=404, detail=f"Asset {filename} not found")

        # Fallback to index.html for client-side routing
        return FileResponse(os.path.join(frontend_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

