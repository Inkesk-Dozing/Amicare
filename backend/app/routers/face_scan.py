import cv2
import numpy as np
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Helpline, FaceScanRecord
from app.schemas import FaceScanRecordSchema
from app.opencv_stress_analyzer import OpenCVStressAnalyzer

router = APIRouter(prefix="/api/face-scan", tags=["Facial Stress & Emotion Examination"])

analyzer = OpenCVStressAnalyzer()

class FrameAnalysisRequest(BaseModel):
    image: str # Base64 encoded image string (e.g. data:image/jpeg;base64,...)
    session_id: Optional[str] = "webcam-session"

class IndicatorsResponse(BaseModel):
    forehead_tension_percent: float
    smile_ratio: float
    brow_furrow_percent: float
    eye_alertness_percent: float
    eye_distance_px: Optional[float] = None
    mouth_width_px: Optional[float] = None

class FaceScanResponse(BaseModel):
    face_detected: bool
    confidence: Optional[float] = 0.0
    emotion: str            # "Happy", "Well", "Sad", "Stressed"
    state_label: str        # e.g., "Joyful & Relaxed", "Calm & Stable Baseline", "Acute Facial Tension & Strain"
    stress_score: int       # 0 - 100
    stress_level: str       # "Low", "Mild", "Moderate", "High"
    primary_indicator: str
    indicators: Dict[str, Any]
    recommendation: str
    suggested_action: str
    annotated_image: Optional[str] = None
    message: Optional[str] = None
    record_id: Optional[int] = None
    database_synced: Optional[bool] = False
    recommended_helplines: Optional[List[Dict[str, Any]]] = []

def _save_scan_to_db(result: Dict[str, Any], session_id: str, db: Session):
    """Saves OpenCV stress scan diagnostics directly into SQLite database."""
    try:
        record = FaceScanRecord(
            session_id=session_id or "default",
            face_detected=bool(result.get("face_detected", False)),
            emotion=str(result.get("emotion", "Unknown")),
            state_label=str(result.get("state_label", "")),
            stress_score=int(result.get("stress_score", 0)),
            stress_level=str(result.get("stress_level", "")),
            confidence=float(result.get("confidence", 0.0) or 0.0),
            forehead_tension_percent=float(result.get("indicators", {}).get("forehead_tension_percent", 0.0) or 0.0),
            brow_furrow_percent=float(result.get("indicators", {}).get("brow_furrow_percent", 0.0) or 0.0),
            smile_ratio=float(result.get("indicators", {}).get("smile_ratio", 0.0) or 0.0),
            eye_alertness_percent=float(result.get("indicators", {}).get("eye_alertness_percent", 0.0) or 0.0),
            recommendation=str(result.get("recommendation", "")),
            suggested_action=str(result.get("suggested_action", ""))
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        result["record_id"] = record.id
        result["database_synced"] = True
    except Exception as e:
        print(f"[OpenCV DB Record Note]: {e}")
        db.rollback()
        result["database_synced"] = False

    # Connect OpenCV results with referral helpline directory from database
    if result.get("emotion") in ["Stressed", "Sad"] or result.get("stress_score", 0) >= 50:
        try:
            db_helplines = db.query(Helpline).limit(3).all()
            result["recommended_helplines"] = [
                {
                    "id": h.id,
                    "name": h.name,
                    "number": h.number,
                    "category": h.category,
                    "description": h.description,
                    "hours": h.hours,
                    "is_toll_free": h.is_toll_free,
                    "languages": h.languages,
                    "website": h.website
                }
                for h in db_helplines
            ]
        except Exception as err:
            print(f"[OpenCV Helpline Fetch Note]: {err}")
            result["recommended_helplines"] = []
    else:
        result["recommended_helplines"] = []

MAX_PAYLOAD_BYTES = 10 * 1024 * 1024  # 10 MB payload boundary
ALLOWED_UPLOAD_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}

@router.post("/analyze-frame", response_model=FaceScanResponse)
def analyze_camera_frame(payload: FrameAnalysisRequest, db: Session = Depends(get_db)):
    """
    Receives base64 webcam frame or snapshot, examines facial stress using OpenCV,
    and saves diagnostic metrics into the database.
    """
    if not payload.image:
        raise HTTPException(status_code=400, detail="No image data provided.")

    # Guard against oversized payloads (DOS mitigation)
    if len(payload.image) > MAX_PAYLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Image payload exceeds maximum allowed size (10MB).")

    bgr_img = analyzer.decode_image_from_base64(payload.image)
    if bgr_img is None:
        raise HTTPException(status_code=400, detail="Invalid base64 image data.")

    result = analyzer.analyze_frame(bgr_img)
    _save_scan_to_db(result, payload.session_id or "webcam-session", db)
    return result

@router.post("/upload", response_model=FaceScanResponse)
async def upload_face_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a student photo or selfie to examine facial stress and log results into the database.
    """
    if file.content_type and file.content_type not in ALLOWED_UPLOAD_MIME_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported media format. Please upload a JPEG, PNG, or WebP photo.")

    contents = await file.read()
    if len(contents) > MAX_PAYLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File size exceeds maximum allowed limit (10MB).")

    nparr = np.frombuffer(contents, np.uint8)
    bgr_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if bgr_img is None:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

    result = analyzer.analyze_frame(bgr_img)
    _save_scan_to_db(result, "photo-upload", db)
    return result

@router.get("/db-status")
def get_face_scan_db_status(db: Session = Depends(get_db)):
    """
    Validates connection between OpenCV facial diagnostics module and the SQLite database.
    """
    try:
        total_scans = db.query(FaceScanRecord).count()
        total_helplines = db.query(Helpline).count()
        return {
            "status": "connected",
            "database": "SQLite (amicare.db)",
            "opencv_analyzer": "Active (YuNet DNN)",
            "total_face_scans_recorded": total_scans,
            "total_helplines_connected": total_helplines
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@router.get("/history", response_model=List[FaceScanRecordSchema])
def get_face_scan_history(limit: int = 15, db: Session = Depends(get_db)):
    """
    Retrieves the most recent OpenCV face scan analysis records from the database.
    """
    return db.query(FaceScanRecord).order_by(FaceScanRecord.created_at.desc()).limit(limit).all()

def generate_webcam_stream():
    """Streams live OpenCV analyzed video feed from local camera if available."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        dummy = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(dummy, "Webcam Not Accessible", (120, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        _, buf = cv2.imencode('.jpg', dummy)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            res = analyzer.analyze_frame(frame)
            if "annotated_image" in res and res["annotated_image"]:
                annotated = analyzer.decode_image_from_base64(res["annotated_image"])
            else:
                annotated = frame

            _, buffer = cv2.imencode('.jpg', annotated, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    finally:
        cap.release()

@router.get("/video_feed")
def live_video_feed():
    import os
    if os.getenv("ENABLE_SERVER_CAMERA", "false").lower() != "true":
        raise HTTPException(
            status_code=403,
            detail="Server-side hardware camera streaming is disabled for privacy and security. The web client captures frames locally."
        )
    return StreamingResponse(
        generate_webcam_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
