# [FEAT]: Integrate OpenCV Facial Stress Examination Engine, YuNet ONNX Pipeline & Cloud Production Fixes

**Issue Type:** `feat` / `enhancement` / `bugfix`  
**Components Affected:** `backend/`, `frontend/`, `api/face-scan`, `deployment`  
**Milestone:** `v1.1.0 — Computer Vision & Production Readiness`  

---

## 📌 Problem Description & Background

In production cloud deployments (Render, Vercel, Railway), the live AmiCare web app failed to execute the Face Wellness Scan feature due to three critical architectural gaps between the local environment and the remote repository:

1. **Missing Backend Vision Modules on Remote:**
   The OpenCV processing pipeline (`opencv_stress_analyzer.py`), the REST router (`routers/face_scan.py`), and the pre-trained deep neural network weights (`cascades/face_detection_yunet.onnx`) were untracked locally and absent from the GitHub repository (`origin/main`). As a result, deployed instances returned `404 Not Found` when attempting to call `/api/face-scan/analyze-frame`.

2. **Headless Cloud Linux Incompatibility (`libGL.so.1`):**
   The remote `backend/requirements.txt` previously referenced full `opencv-python`, which requires X11/GUI display libraries (`libGL.so.1`, `libglib2.0-0`) that are missing in headless Linux container runtimes (e.g., Ubuntu Docker on Render/Railway), leading to startup crashes.

3. **CORS Restrictions on Deployed Domains:**
   The `main.py` CORS configuration strictly whitelisted `localhost:5173` and `localhost:8000`, blocking cross-origin HTTP traffic from deployed HTTPS frontend domains (e.g., `*.vercel.app`, `*.onrender.com`).

---

## 🚀 Proposed Solution & Implemented Changes

### 1. Computer Vision & Affective Analysis Core (`backend/app/opencv_stress_analyzer.py`)
- Integrated **OpenCV 5.0** with **YuNet ONNX** (`cv2.FaceDetectorYN`) for fast, lightweight (232 KB) deep face landmark regression (320x320 input size).
- Developed the **Forehead & Brow Furrow Tension Index** using Sobel horizontal gradients ($G_x$) and Laplacian variance ($\sigma^2_{\text{lap}}$) to quantify cranial muscle strain (*corrugator supercilii* contraction).
- Implemented **Mouth Valence & Smile Ratio Metric** ($R_{\text{smile}} = \frac{W_{\text{mouth}}}{D_{\text{eyes}}}$) and eye alertness contrast analysis.
- Multi-factor affective state classification into:
  - `Happy` (Joyful & Relaxed)
  - `Well` (Calm & Balanced Baseline)
  - `Sad` (Low Mood / Subdued Composure)
  - `Stressed` (Acute Facial Tension & Strain)
- Added an in-memory BGR $\leftrightarrow$ Base64 codec to ensure zero-disk-write processing for complete student privacy.
- Implemented real-time dynamic Heads-Up Display (HUD) rendering with futuristic corner brackets, top biometric status tags, and calibrated stress index progress bars.

### 2. REST API & Database Logging (`backend/app/routers/face_scan.py`)
- Exposed `/api/face-scan/analyze-frame` (Base64 JPEG payload ingestion).
- Exposed `/api/face-scan/upload` (Direct multipart image upload).
- Exposed `/api/face-scan/db-status` (Diagnostic healthcheck for OpenCV + SQLite connection).
- Created `FaceScanRecord` ORM table in `amicare.db` storing anonymized telemetry: stress score, forehead tension, brow furrow percentage, smile ratio, and timestamp.
- Automatic integration with the Helpline Directory: attaches verified crisis resources (Tele-MANAS `14416`, KIRAN `1800-599-0019`) whenever elevated stress or sadness is classified.

### 3. Cloud Production & Universal CORS Readiness
- Updated `backend/requirements.txt` from `opencv-python` to `opencv-python-headless>=4.8.0` for headless cloud Linux server compatibility.
- Updated `backend/app/main.py` CORS configuration to allow all origins (`allow_origins=["*"]`, `allow_credentials=False`), resolving cross-domain preflight blocks across Vercel/Render deployments.
- Added ES Module compatibility to `frontend/dev_server.js` using `import http from 'http'`.

---

## 📂 Files Included in This Feature

```
backend/
├── app/
│   ├── cascades/
│   │   ├── face_detection_yunet.onnx         # YuNet ONNX landmark model (232 KB)
│   │   ├── haarcascade_eye.xml                # Eye detection cascade
│   │   ├── haarcascade_frontalface_default.xml # Frontal face cascade
│   │   └── haarcascade_smile.xml              # Smile detection cascade
│   ├── opencv_stress_analyzer.py             # Core vision & biometric gradient engine
│   ├── routers/
│   │   └── face_scan.py                      # FastAPI endpoints for face scanning
│   ├── main.py                               # Universal CORS & face_scan router registration
│   ├── models.py                             # FaceScanRecord SQLAlchemy model
│   ├── schemas.py                            # Pydantic schemas for face scan diagnostics
│   └── database.py                           # Database session & table creation
└── requirements.txt                          # opencv-python-headless>=4.8.0

frontend/
├── index.html                                # Live webcam capture & OpenCV HUD viewports
├── dev_server.js                             # ESM reverse proxy server (port 5173 -> 8000)
└── public/                                   # Sample student wellness demonstration portraits
```

---

## ✅ Testing & Verification Checklist

- [x] Unit test verifying `cv2.FaceDetectorYN` model loading from `face_detection_yunet.onnx`.
- [x] Verified in-memory Base64 decoding and encoding without file leaks.
- [x] API test for `GET /api/face-scan/db-status` returning HTTP 200 and `"opencv_analyzer": "Active (YuNet DNN)"`.
- [x] API test for `POST /api/face-scan/analyze-frame` with authentic student portrait returning HTTP 200, 93% stress score, and active DB logging.
- [x] Tested CORS preflight `OPTIONS` request with simulated remote origin (`https://my-deployed-app.vercel.app`) returning `Access-Control-Allow-Origin: *`.
- [x] Verified local deployment on `http://localhost:5173` proxying smoothly to FastAPI on `http://127.0.0.1:8000`.

---

## 🎯 Acceptance Criteria

1. Navigating to the **Face Wellness Scan** tab in the web client successfully activates the user's camera stream over HTTPS.
2. Clicking **Capture & Analyze Photo** dispatches the Base64 frame to `/api/face-scan/analyze-frame` and renders the OpenCV HUD annotation within < 200ms.
3. Deployed cloud instances on Render/Railway build and launch without missing dependency errors (`libGL.so.1`).
4. Telemetry records are safely persisted into `amicare.db` without storing raw user photographs or Personally Identifiable Information (PII).

---

## 🔗 Related References & Closing Tags

- **Resolves:** Missing OpenCV computer vision pipeline on remote repository.
- **Fixes:** `404 Not Found` error when calling `/api/face-scan/analyze-frame` on deployed instances.
- **Fixes:** Cross-Origin Request Blocked (CORS) on remote HTTPS frontend domains.
- **Closes:** #1, #3
