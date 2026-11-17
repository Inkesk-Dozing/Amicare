import sys
import os

# Add backend directory to module search path for serverless runtime
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app
from app.routers import chat, assessment, helplines, resources

# Re-register routers with stripped prefix to guarantee 100% route matching
# regardless of whether the ASGI layer preserves /api or strips it on Vercel
app.include_router(chat.router, prefix="/chat")
app.include_router(assessment.router, prefix="/assessment")
app.include_router(helplines.router, prefix="/helplines")
app.include_router(resources.router, prefix="/resources")

@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
def health_status():
    return {
        "status": "healthy",
        "service": "AmiCare Serverless API",
        "version": "1.0.0"
    }
