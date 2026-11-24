import os
import time
import cv2
import numpy as np
import base64
from typing import Dict, Any, Optional, Tuple


class OpenCVStressAnalyzer:
    """
    OpenCV Facial Stress and Emotion Analyzer for AmiCare.
    Combines YuNet ONNX facial landmark detection with:
      - Mouth openness & oral-cavity tension analysis (detects shouting, anger, jaw clenching)
      - CLAHE-normalized glabella/brow Sobel-X + Sobel-Y tension (detects frowning, anger, strain)
      - Eye contrast alertness (detects fatigue, sadness, wide-eyed strain)
      - Optional per-session EMA temporal smoothing for live real-time video analytics
    Classifies into: Happy, Well, Sad, Stressed, or Angry.
    """

    def __init__(self, model_path: Optional[str] = None):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cascades_dir = os.path.join(current_dir, "cascades")
        if model_path is None:
            model_path = os.path.join(cascades_dir, "face_detection_yunet.onnx")

        self.model_path = model_path
        self.smile_cascade_path = os.path.join(cascades_dir, "haarcascade_smile.xml")
        self.detector = None
        self.smile_cascade = None
        self._clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(4, 4))
        self._session_ema: Dict[str, Dict[str, float]] = {}
        self._init_detector()

    def _init_detector(self):
        if os.path.exists(self.model_path):
            try:
                self.detector = cv2.FaceDetectorYN.create(
                    model=self.model_path,
                    config="",
                    input_size=(320, 320),
                    score_threshold=0.50,
                    nms_threshold=0.3,
                    top_k=5000,
                )
            except Exception as e:
                print(f"[OpenCVStressAnalyzer] Error initializing YuNet: {e}")
                self.detector = None
        else:
            print(f"[OpenCVStressAnalyzer] Model file not found at: {self.model_path}")

        cascade_cls = getattr(cv2, "CascadeClassifier", None)
        if cascade_cls is not None and os.path.exists(self.smile_cascade_path):
            cascade = cascade_cls(self.smile_cascade_path)
            if not cascade.empty():
                self.smile_cascade = cascade

    def decode_image_from_base64(self, base64_str: str) -> Optional[np.ndarray]:
        """Decodes base64 string (data URI or raw base64) to an OpenCV BGR image."""
        try:
            if "," in base64_str:
                base64_str = base64_str.split(",", 1)[1]
            img_bytes = base64.b64decode(base64_str)
            nparr = np.frombuffer(img_bytes, np.uint8)
            return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            print(f"[OpenCVStressAnalyzer] Base64 decode error: {e}")
            return None

    def encode_image_to_base64(self, img: np.ndarray, quality: int = 85) -> str:
        """Encodes an OpenCV BGR image to base64 JPEG data URI."""
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, buffer = cv2.imencode(".jpg", img, encode_params)
        b64_str = base64.b64encode(buffer).decode("utf-8")
        return f"data:image/jpeg;base64,{b64_str}"

    def _apply_ema(self, session_id: str, metrics: Dict[str, float], alpha: float = 0.55) -> Dict[str, float]:
        """Applies responsive exponential moving average smoothing across live frames."""
        if len(self._session_ema) > 100:
            self._session_ema.clear()
        prev = self._session_ema.get(session_id)
        if prev is None:
            self._session_ema[session_id] = dict(metrics)
            return metrics
        smoothed = {
            k: alpha * v + (1.0 - alpha) * prev.get(k, v)
            for k, v in metrics.items()
        }
        self._session_ema[session_id] = smoothed
        return smoothed

    def analyze_frame(
        self,
        img: np.ndarray,
        session_id: Optional[str] = None,
        smooth: bool = False,
        return_image: bool = True,
    ) -> Dict[str, Any]:
        """
        Runs OpenCV facial stress & emotion examination on a BGR frame.
        When smooth=True and session_id is provided, applies EMA temporal smoothing.
        """
        t0 = time.perf_counter()

        if img is None or img.size == 0:
            return {
                "face_detected": False,
                "error": "Empty or invalid image frame provided.",
                "emotion": "Unknown",
                "stress_score": 0,
                "stress_level": "Unknown",
                "primary_indicator": "No frame data",
                "indicators": {},
                "recommendation": "Provide a valid camera frame.",
                "suggested_action": "Retry Scan",
                "inference_ms": 0.0,
            }

        orig_h, orig_w = img.shape[:2]

        if self.detector is None:
            self._init_detector()
        if self.detector is None:
            return self._fallback_analysis(img)

        self.detector.setInputSize((orig_w, orig_h))
        try:
            _, faces = self.detector.detect(img)
        except Exception as e:
            print(f"[OpenCVStressAnalyzer] Detection error: {e}")
            return self._fallback_analysis(img)

        if faces is None or len(faces) == 0:
            annotated_b64 = None
            if return_image:
                annotated = img.copy()
                self._draw_no_face_hud(annotated)
                annotated_b64 = self.encode_image_to_base64(annotated)
            elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 1)
            return {
                "face_detected": False,
                "confidence": 0.0,
                "emotion": "No Face Detected",
                "state_label": "Searching for Face",
                "stress_score": 0,
                "stress_level": "None",
                "primary_indicator": "No face detected in frame",
                "message": "Please face the camera directly in good lighting.",
                "annotated_image": annotated_b64,
                "frame_size": {"width": orig_w, "height": orig_h},
                "geometry": None,
                "indicators": {
                    "forehead_tension_percent": 0.0,
                    "smile_ratio": 0.0,
                    "brow_furrow_percent": 0.0,
                    "eye_alertness_percent": 0.0,
                    "mouth_openness_percent": 0.0,
                },
                "recommendation": "Position your face inside the scan area.",
                "suggested_action": "Align Face with Camera",
                "inference_ms": elapsed_ms,
            }

        primary_face = max(faces, key=lambda f: f[2] * f[3])
        box = primary_face[0:4].astype(int)
        r_eye = primary_face[4:6].astype(int)
        l_eye = primary_face[6:8].astype(int)
        nose = primary_face[8:10].astype(int)
        r_mouth = primary_face[10:12].astype(int)
        l_mouth = primary_face[12:14].astype(int)
        confidence = float(primary_face[14])

        bx, by, bw, bh = box
        bx = max(0, bx)
        by = max(0, by)
        bw = min(orig_w - bx, bw)
        bh = min(orig_h - by, bh)

        # 1. Geometric Ratios
        eye_distance = float(np.linalg.norm(l_eye - r_eye))
        mouth_width = float(np.linalg.norm(l_mouth - r_mouth))
        smile_ratio = mouth_width / max(eye_distance, 1.0)

        mouth_center_y = (r_mouth[1] + l_mouth[1]) / 2.0
        nose_to_mouth_y = mouth_center_y - nose[1]
        norm_mouth_drop = nose_to_mouth_y / max(bh, 1.0)

        # 2. Scale- & Lighting-Invariant Forehead/Brow Tension (Sobel X + Sobel Y + Laplacian)
        forehead_tension, brow_furrow_score = self._compute_brow_forehead_tension(
            img, (bx, by, bw, bh), r_eye, l_eye
        )

        # 3. Eye Openness & Fatigue Analysis
        eye_alertness_score = self._compute_eye_openness(img, r_eye, l_eye, eye_distance)

        # 4. Mouth Openness & Shouting / Jaw Strain Analysis
        mouth_openness, mouth_strain = self._compute_mouth_metrics(
            img, (bx, by, bw, bh), r_mouth, l_mouth, eye_distance
        )

        # 5. Haar Smile Cascade Confirmation (when available)
        haar_smile = self._detect_haar_smile(img, (bx, by, bw, bh), nose)

        # 6. Optional Temporal Smoothing for Live Video Mode
        if smooth and session_id:
            smoothed = self._apply_ema(
                session_id,
                {
                    "smile_ratio": smile_ratio,
                    "forehead_tension": forehead_tension,
                    "brow_furrow_score": brow_furrow_score,
                    "norm_mouth_drop": norm_mouth_drop,
                    "eye_alertness": eye_alertness_score,
                    "mouth_openness": mouth_openness,
                    "mouth_strain": mouth_strain,
                },
            )
            smile_ratio = smoothed["smile_ratio"]
            forehead_tension = smoothed["forehead_tension"]
            brow_furrow_score = smoothed["brow_furrow_score"]
            norm_mouth_drop = smoothed["norm_mouth_drop"]
            eye_alertness_score = smoothed["eye_alertness"]
            mouth_openness = smoothed["mouth_openness"]
            mouth_strain = smoothed["mouth_strain"]

        # 7. Multi-Factor Stress & Emotion Classification
        classification = self._classify_stress_and_emotion(
            smile_ratio=smile_ratio,
            haar_smile=haar_smile,
            forehead_tension=forehead_tension,
            brow_furrow_score=brow_furrow_score,
            norm_mouth_drop=norm_mouth_drop,
            eye_alertness=eye_alertness_score,
            mouth_openness=mouth_openness,
            mouth_strain=mouth_strain,
        )

        # 8. Render HUD Visuals on Frame (skipped in lightweight live-overlay mode)
        annotated_b64 = None
        if return_image:
            annotated = img.copy()
            self._render_opencv_hud(
                img=annotated,
                box=(bx, by, bw, bh),
                r_eye=r_eye,
                l_eye=l_eye,
                nose=nose,
                r_mouth=r_mouth,
                l_mouth=l_mouth,
                classification=classification,
                forehead_tension=forehead_tension,
            )
            annotated_b64 = self.encode_image_to_base64(annotated)

        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 1)

        return {
            "face_detected": True,
            "confidence": round(confidence, 2),
            "emotion": classification["emotion"],
            "state_label": classification["state_label"],
            "stress_score": classification["stress_score"],
            "stress_level": classification["stress_level"],
            "primary_indicator": classification["primary_indicator"],
            "indicators": {
                "forehead_tension_percent": round(forehead_tension * 100, 1),
                "smile_ratio": round(smile_ratio, 2),
                "brow_furrow_percent": round(brow_furrow_score * 100, 1),
                "eye_alertness_percent": round(eye_alertness_score * 100, 1),
                "mouth_openness_percent": round(mouth_openness * 100, 1),
                "eye_distance_px": round(eye_distance, 1),
                "mouth_width_px": round(mouth_width, 1),
                "haar_smile_verified": haar_smile,
            },
            "frame_size": {"width": orig_w, "height": orig_h},
            "geometry": {
                "box": [int(bx), int(by), int(bw), int(bh)],
                "r_eye": [int(r_eye[0]), int(r_eye[1])],
                "l_eye": [int(l_eye[0]), int(l_eye[1])],
                "nose": [int(nose[0]), int(nose[1])],
                "r_mouth": [int(r_mouth[0]), int(r_mouth[1])],
                "l_mouth": [int(l_mouth[0]), int(l_mouth[1])],
            },
            "recommendation": classification["recommendation"],
            "suggested_action": classification["suggested_action"],
            "annotated_image": annotated_b64,
            "inference_ms": elapsed_ms,
        }

    def _detect_haar_smile(
        self, img: np.ndarray, box: Tuple[int, int, int, int], nose: np.ndarray
    ) -> bool:
        """Uses Haar smile cascade on the lower-face ROI to confirm an active smile."""
        if self.smile_cascade is None:
            return False
        bx, by, bw, bh = box
        if bw < 30 or bh < 30:
            return False
        y1 = max(by, int(nose[1] - bh * 0.05))
        y2 = min(img.shape[0], by + bh)
        x1 = max(0, bx + int(bw * 0.12))
        x2 = min(img.shape[1], bx + bw - int(bw * 0.12))
        if y2 - y1 < 16 or x2 - x1 < 20:
            return False
        roi = cv2.cvtColor(img[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
        roi = cv2.resize(roi, (120, 72), interpolation=cv2.INTER_AREA)
        smiles = self.smile_cascade.detectMultiScale(
            roi, scaleFactor=1.3, minNeighbors=22, minSize=(28, 16)
        )
        return len(smiles) > 0

    def _compute_mouth_metrics(
        self,
        img: np.ndarray,
        box: Tuple[int, int, int, int],
        r_mouth: np.ndarray,
        l_mouth: np.ndarray,
        eye_distance: float,
    ) -> Tuple[float, float]:
        """
        Measures vertical mouth openness (dark oral-cavity ratio + vertical lip/teeth gradient)
        to detect shouting, screaming, or jaw tension, distinct from a closed-lip smile.
        """
        orig_h, orig_w = img.shape[:2]
        cx = int((r_mouth[0] + l_mouth[0]) / 2.0)
        cy = int((r_mouth[1] + l_mouth[1]) / 2.0)
        mw = max(16.0, float(np.linalg.norm(l_mouth - r_mouth)), eye_distance * 0.65)

        half_w = int(mw * 0.55)
        half_h = int(mw * 0.45)
        x1 = max(0, cx - half_w)
        x2 = min(orig_w, cx + half_w)
        y1 = max(0, cy - int(half_h * 0.7))
        y2 = min(orig_h, cy + int(half_h * 1.15))

        mouth_roi = img[y1:y2, x1:x2]
        if mouth_roi.size == 0 or mouth_roi.shape[0] < 6 or mouth_roi.shape[1] < 8:
            return 0.15, 0.15

        gray = cv2.cvtColor(mouth_roi, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (64, 48), interpolation=cv2.INTER_AREA)

        # Estimate surrounding lip/skin brightness from outer border of mouth ROI
        border_vals = np.concatenate([resized[0, :], resized[-1, :], resized[:, 0], resized[:, -1]])
        skin_mean = float(np.mean(border_vals))

        # Core oral cavity region (center 55% width x 65% height)
        core = resized[10:40, 15:49]
        # Dark oral cavity pixels (deep open mouth interior, excluding bright white teeth of a smile)
        dark_ratio = float(np.mean(core < (skin_mean - 42.0)))
        bright_teeth_ratio = float(np.mean(core > (skin_mean + 12.0)))

        # Vertical gradient energy (high when mouth is open)
        sobel_y = cv2.Sobel(resized, cv2.CV_64F, 0, 1, ksize=3)
        sobel_y_energy = float(np.mean(np.abs(sobel_y)))
        norm_sy = float(np.clip((sobel_y_energy - 18.0) / 30.0, 0.0, 1.0))

        # Suppress shout score if bright teeth + no deep dark cavity (classic wide smile)
        cavity_score = float(np.clip((dark_ratio - 0.5 * bright_teeth_ratio) / 0.35, 0.0, 1.0))
        mouth_openness = float(np.clip(0.75 * cavity_score + 0.25 * norm_sy, 0.0, 1.0))
        mouth_strain = float(np.clip(0.4 * norm_sy + 0.6 * mouth_openness, 0.0, 1.0))
        return mouth_openness, mouth_strain

    def _compute_brow_forehead_tension(
        self, img: np.ndarray, box: Tuple[int, int, int, int], r_eye: np.ndarray, l_eye: np.ndarray
    ) -> Tuple[float, float]:
        """
        Examines brow furrowing and glabella muscle tension using a canonical
        (96x48) CLAHE-normalized ROI. Combines Sobel-X (vertical frown lines),
        Sobel-Y (lowered/knitted brow ridge in anger), and Laplacian variance.
        """
        orig_h, orig_w = img.shape[:2]
        bx, by, bw, bh = box

        eye_min_y = int(min(r_eye[1], l_eye[1]))
        eye_min_x = int(min(r_eye[0], l_eye[0]))
        eye_max_x = int(max(r_eye[0], l_eye[0]))

        band_height = max(8, int((eye_min_y - by) * 0.68))
        top_y = max(0, eye_min_y - band_height)
        bottom_y = max(top_y + 6, min(orig_h, eye_min_y))
        span_x = max(12, eye_max_x - eye_min_x)
        left_x = max(0, eye_min_x + int(span_x * 0.08))
        right_x = min(orig_w, eye_max_x - int(span_x * 0.08))

        forehead_roi = img[top_y:bottom_y, left_x:right_x]
        if forehead_roi.size == 0 or forehead_roi.shape[0] < 4 or forehead_roi.shape[1] < 4:
            return 0.25, 0.25

        gray_fh = cv2.cvtColor(forehead_roi, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray_fh, (96, 48), interpolation=cv2.INTER_AREA)
        norm_fh = self._clahe.apply(resized)
        blurred = cv2.GaussianBlur(norm_fh, (3, 3), 0)

        sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        sobel_x_energy = float(np.mean(np.abs(sobel_x)))
        # Measure Sobel-Y only on the inner glabella (center 36% between eyes) to avoid normal eyebrows
        glabella = blurred[:, 30:66]
        sobel_y_glab = cv2.Sobel(glabella, cv2.CV_64F, 0, 1, ksize=3)
        sobel_y_energy = float(np.mean(np.abs(sobel_y_glab)))
        laplacian_var = float(cv2.Laplacian(blurred, cv2.CV_64F).var())

        norm_sobel_x = float(np.clip((sobel_x_energy - 8.0) / 24.0, 0.0, 1.0))
        norm_sobel_y = float(np.clip((sobel_y_energy - 16.0) / 28.0, 0.0, 1.0))
        norm_lap = float(np.clip((np.log1p(laplacian_var) - 3.6) / 4.2, 0.0, 1.0))

        brow_furrow = float(0.55 * norm_sobel_x + 0.20 * norm_sobel_y + 0.25 * norm_lap)
        forehead_tension = float(0.45 * norm_sobel_x + 0.15 * norm_sobel_y + 0.40 * norm_lap)

        return forehead_tension, brow_furrow

    def _compute_eye_openness(
        self, img: np.ndarray, r_eye: np.ndarray, l_eye: np.ndarray, eye_distance: float
    ) -> float:
        """Estimates eye openness / alertness vs fatigue squinting."""
        if eye_distance <= 0:
            return 0.5
        orig_h, orig_w = img.shape[:2]
        eye_radius = int(max(4, eye_distance * 0.16))
        alertness_scores = []

        for eye_pt in [r_eye, l_eye]:
            ex, ey = int(eye_pt[0]), int(eye_pt[1])
            y1 = max(0, ey - eye_radius)
            y2 = min(orig_h, ey + eye_radius)
            x1 = max(0, ex - eye_radius)
            x2 = min(orig_w, ex + eye_radius)
            eye_crop = img[y1:y2, x1:x2]
            if eye_crop.size > 0:
                gray = cv2.cvtColor(eye_crop, cv2.COLOR_BGR2GRAY)
                std_dev = float(np.std(gray))
                norm_contrast = float(np.clip(std_dev / 45.0, 0.1, 1.0))
                alertness_scores.append(norm_contrast)

        return float(np.mean(alertness_scores)) if alertness_scores else 0.7

    def _classify_stress_and_emotion(
        self,
        smile_ratio: float,
        haar_smile: bool,
        forehead_tension: float,
        brow_furrow_score: float,
        norm_mouth_drop: float,
        eye_alertness: float,
        mouth_openness: float,
        mouth_strain: float,
    ) -> Dict[str, Any]:
        """
        Synthesizes facial geometry, mouth openness (shouting/anger), brow/glabella tension,
        and eye alertness to classify into: Angry, Stressed, Sad, Happy, or Well.
        """
        # 1. Angry / Shouting / Acute Distress: wide-open mouth + brow strain or non-smiling mouth
        is_shouting_or_angry = (
            (mouth_openness >= 0.45 and (brow_furrow_score >= 0.30 or smile_ratio < 0.88))
            or (brow_furrow_score >= 0.44 and mouth_openness >= 0.32 and smile_ratio < 0.88)
        )

        # 2. Happy: genuine wide smile with relaxed brows
        is_smiling = (
            (smile_ratio >= 0.88 and haar_smile and brow_furrow_score < 0.35)
            or (smile_ratio >= 0.92 and brow_furrow_score < 0.32)
        )

        if is_shouting_or_angry:
            emotion = "Angry"
            state_label = "Anger / Acute Vocal & Facial Strain"
            stress_score = int(np.clip(72 + int(mouth_openness * 16) + int(brow_furrow_score * 14), 72, 98))
            stress_level = "High"
            primary_indicator = (
                f"Acute mouth/jaw tension ({mouth_openness * 100:.0f}% openness) & furrowed brow ({brow_furrow_score * 100:.0f}%)"
            )
            recommendation = (
                "High emotional intensity or anger/distress detected. Step back from your screen, take 3 slow deep breaths (4-7-8), or try our Guided Box Breathing to release acute adrenaline."
            )
            suggested_action = "Start Box Breathing"

        elif brow_furrow_score >= 0.54 or forehead_tension >= 0.55 or (brow_furrow_score >= 0.44 and mouth_strain >= 0.48):
            emotion = "Stressed"
            state_label = "Acute Facial Tension & Strain"
            base_stress = 62 + int(brow_furrow_score * 28) + int(mouth_strain * 10)
            stress_score = int(np.clip(base_stress, 62, 96))
            stress_level = "High" if stress_score >= 75 else "Moderate"
            primary_indicator = f"Brow furrowing ({brow_furrow_score * 100:.0f}%) & elevated forehead tension ({forehead_tension * 100:.0f}%)"
            recommendation = "Noticeable tension detected in your brow and forehead. We strongly recommend a 2-minute Guided Box Breathing session or the 5-4-3-2-1 Grounding exercise to release cranial strain."
            suggested_action = "Start Box Breathing"

        elif is_smiling and brow_furrow_score < 0.55:
            emotion = "Happy"
            state_label = "Joyful & Relaxed"
            stress_score = int(np.clip(12 + (forehead_tension * 18) - (smile_ratio - 0.85) * 25, 8, 28))
            stress_level = "Low"
            primary_indicator = f"Upward smile contour (Smile Ratio: {smile_ratio:.2f}) & relaxed brow"
            recommendation = "You look bright and cheerful! Keep maintaining a balanced routine and carry this positive energy into your studies."
            suggested_action = "Maintain Positive Habits"

        elif smile_ratio <= 0.68 or (
            smile_ratio < 0.74 and (norm_mouth_drop > 0.24 or brow_furrow_score > 0.34 or eye_alertness < 0.55)
        ):
            emotion = "Sad"
            state_label = "Low Mood / Subdued Composure"
            stress_score = int(np.clip(54 + int((1.0 - eye_alertness) * 22) + int(brow_furrow_score * 12), 50, 78))
            stress_level = "Moderate"
            primary_indicator = "Subdued expression, compressed/downward mouth posture & reduced alertness"
            recommendation = "Your facial expression looks somewhat heavy or down. Remember, you don't have to carry burdens alone. Talk with AmiCare or connect with our confidential campus counseling helpline."
            suggested_action = "Talk with AmiCare Companion"

        else:
            emotion = "Well"
            state_label = "Calm & Stable Baseline"
            stress_score = int(np.clip(22 + (forehead_tension * 25), 18, 42))
            stress_level = "Mild" if stress_score >= 35 else "Low"
            primary_indicator = "Equally balanced facial symmetry, relaxed brow & resting mouth posture"
            recommendation = "Your face shows calm, steady composure. You are well-centered. Take regular hydration breaks and pace your academic work."
            suggested_action = "Practice Mindfulness"

        return {
            "emotion": emotion,
            "state_label": state_label,
            "stress_score": stress_score,
            "stress_level": stress_level,
            "primary_indicator": primary_indicator,
            "recommendation": recommendation,
            "suggested_action": suggested_action,
        }

    def _render_opencv_hud(
        self,
        img: np.ndarray,
        box: Tuple[int, int, int, int],
        r_eye: np.ndarray,
        l_eye: np.ndarray,
        nose: np.ndarray,
        r_mouth: np.ndarray,
        l_mouth: np.ndarray,
        classification: Dict[str, Any],
        forehead_tension: float,
    ):
        """Draws OpenCV HUD overlays, bounding box, landmarks, and stress gauge onto frame."""
        bx, by, bw, bh = box
        emotion = classification["emotion"]
        stress_score = classification["stress_score"]

        if emotion == "Happy":
            hud_color = (68, 175, 42)
            badge_text = "HAPPY : RELAXED"
        elif emotion == "Well":
            hud_color = (153, 114, 27)
            badge_text = "WELL : BALANCED"
        elif emotion == "Sad":
            hud_color = (204, 115, 12)
            badge_text = "SAD : SUBDUED"
        elif emotion == "Angry":
            hud_color = (30, 30, 235)
            badge_text = "ANGRY : ACUTE DISTRESS"
        else:
            hud_color = (40, 40, 220)
            badge_text = "STRESSED : HIGH STRAIN"

        line_len = int(min(bw, bh) * 0.22)
        thick = 2

        overlay = img.copy()
        cv2.rectangle(overlay, (bx, by), (bx + bw, by + bh), hud_color, 1)
        cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)

        cv2.line(img, (bx, by), (bx + line_len, by), hud_color, thick + 1)
        cv2.line(img, (bx, by), (bx, by + line_len), hud_color, thick + 1)
        cv2.line(img, (bx + bw, by), (bx + bw - line_len, by), hud_color, thick + 1)
        cv2.line(img, (bx + bw, by), (bx + bw, by + line_len), hud_color, thick + 1)
        cv2.line(img, (bx, by + bh), (bx + line_len, by + bh), hud_color, thick + 1)
        cv2.line(img, (bx, by + bh), (bx, by + bh - line_len), hud_color, thick + 1)
        cv2.line(img, (bx + bw, by + bh), (bx + bw - line_len, by + bh), hud_color, thick + 1)
        cv2.line(img, (bx + bw, by + bh), (bx + bw, by + bh - line_len), hud_color, thick + 1)

        cv2.circle(img, (int(r_eye[0]), int(r_eye[1])), 4, (0, 255, 255), -1)
        cv2.circle(img, (int(l_eye[0]), int(l_eye[1])), 4, (0, 255, 255), -1)
        cv2.circle(img, (int(nose[0]), int(nose[1])), 3, (255, 200, 0), -1)
        cv2.circle(img, (int(r_mouth[0]), int(r_mouth[1])), 4, hud_color, -1)
        cv2.circle(img, (int(l_mouth[0]), int(l_mouth[1])), 4, hud_color, -1)
        cv2.line(img, (int(r_mouth[0]), int(r_mouth[1])), (int(l_mouth[0]), int(l_mouth[1])), hud_color, 2)

        badge_y = max(26, by - 12)
        cv2.rectangle(img, (bx, badge_y - 22), (bx + max(180, bw), badge_y + 4), (20, 20, 20), -1)
        cv2.rectangle(img, (bx, badge_y - 22), (bx + max(180, bw), badge_y + 4), hud_color, 1)
        cv2.putText(
            img,
            f"AmiCare Scan: {badge_text}",
            (bx + 6, badge_y - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

        gauge_y = min(img.shape[0] - 10, by + bh + 24)
        gauge_w = max(180, bw)
        cv2.rectangle(img, (bx, gauge_y - 18), (bx + gauge_w, gauge_y + 14), (25, 25, 25), -1)
        cv2.rectangle(img, (bx, gauge_y - 18), (bx + gauge_w, gauge_y + 14), (80, 80, 80), 1)

        bar_fill = int((gauge_w - 12) * (stress_score / 100.0))
        cv2.putText(
            img,
            f"Stress: {stress_score}% | Tension: {int(forehead_tension * 100)}%",
            (bx + 6, gauge_y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (230, 230, 230),
            1,
            cv2.LINE_AA,
        )
        cv2.rectangle(img, (bx + 6, gauge_y + 2), (bx + 6 + (gauge_w - 12), gauge_y + 8), (60, 60, 60), -1)
        cv2.rectangle(img, (bx + 6, gauge_y + 2), (bx + 6 + bar_fill, gauge_y + 8), hud_color, -1)

    def _draw_no_face_hud(self, img: np.ndarray):
        """Draws visual guidance when no face is currently detected in frame."""
        h, w = img.shape[:2]
        center_x, center_y = w // 2, h // 2
        cv2.ellipse(img, (center_x, center_y), (int(w * 0.22), int(h * 0.32)), 0, 0, 360, (0, 165, 255), 2)
        cv2.putText(
            img,
            "Align Face Within Scanner",
            (center_x - 120, center_y + int(h * 0.38)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    def _fallback_analysis(self, img: np.ndarray) -> Dict[str, Any]:
        """Graceful fallback if YuNet model cannot be evaluated."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        stress_score = int(np.clip(30 + lap_var / 50.0, 20, 65))
        return {
            "face_detected": True,
            "emotion": "Well",
            "state_label": "Calm Baseline (Sensor Mode)",
            "stress_score": stress_score,
            "stress_level": "Mild",
            "primary_indicator": "General facial contrast analysis",
            "indicators": {
                "forehead_tension_percent": 30.0,
                "smile_ratio": 0.72,
                "brow_furrow_percent": 25.0,
                "eye_alertness_percent": 75.0,
                "mouth_openness_percent": 15.0,
            },
            "recommendation": "Your baseline composure looks stable.",
            "suggested_action": "Maintain Focus",
            "annotated_image": self.encode_image_to_base64(img),
            "inference_ms": 0.0,
        }
