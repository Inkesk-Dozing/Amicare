#!/usr/bin/env python3
"""
AmiCare — OpenCV Facial Stress & Emotion Examination Desktop Runner
Examines:
- Face detection & alignment
- Forehead & brow furrow tension (corrugator supercilii muscle strain)
- Smile ratio & mouth curvature (valence / happiness)
- Eye openness & strain
- Classifies emotional state: 'Happy', 'Well & Balanced', 'Sad', 'Stressed'
- Computes Stress Index (0% - 100%) and provides real-time AmiCare recommendations.
"""

import sys
import os
import time
import argparse
import cv2
import numpy as np

# Ensure UTF-8 output encoding for Windows command line compatibility
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Ensure backend directory is in Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(SCRIPT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.opencv_stress_analyzer import OpenCVStressAnalyzer

def print_banner():
    print("=" * 68)
    print("  [*] AmiCare - OpenCV Facial Stress & Emotion Examination System")
    print("  K.R. Mangalam University | Non-Diagnostic Student Support")
    print("=" * 68)
    print("  Controls:")
    print("    [Q] / [ESC] : Quit application")
    print("    [S]         : Save annotated snapshot")
    print("=" * 68 + "\n")

def run_image_analysis(analyzer: OpenCVStressAnalyzer, image_path: str):
    """Analyzes a single image file and saves annotated output."""
    if not os.path.exists(image_path):
        print(f"[!] File not found: {image_path}")
        return

    print(f"[*] Analyzing image: {os.path.basename(image_path)}")
    img = cv2.imread(image_path)
    if img is None:
        print("[!] Failed to decode image file.")
        return

    res = analyzer.analyze_frame(img)
    print(f"    - Face Detected     : {res['face_detected']}")
    if res['face_detected']:
        print(f"    - Emotion Status    : {res.get('emotion')} ({res.get('state_label')})")
        print(f"    - Stress Score      : {res.get('stress_score')}% [{res.get('stress_level')}]")
        print(f"    - Forehead Tension  : {res.get('indicators', {}).get('forehead_tension_percent')}%")
        print(f"    - Smile Ratio       : {res.get('indicators', {}).get('smile_ratio')}")
        print(f"    - Recommendation    : {res.get('recommendation')}")
        print(f"    - Suggested Action  : {res.get('suggested_action')}")
    else:
        print(f"    - Message           : {res.get('message', 'No face detected')}")

    if res.get("annotated_image"):
        annotated_bgr = analyzer.decode_image_from_base64(res["annotated_image"])
        out_filename = f"scan_result_{os.path.splitext(os.path.basename(image_path))[0]}.jpg"
        out_path = os.path.join(SCRIPT_DIR, out_filename)
        cv2.imwrite(out_path, annotated_bgr)
        print(f"    [+] Saved OpenCV annotated image to: {out_path}\n")

def run_demo_mode(analyzer: OpenCVStressAnalyzer):
    """Demonstrates OpenCV facial analysis on project student wellness samples."""
    print("[*] Running in Demonstration Mode with built-in student wellness samples...\n")
    sample_paths = [
        os.path.join(SCRIPT_DIR, "frontend", "authentic_student_wellness.jpg"),
        os.path.join(SCRIPT_DIR, "frontend", "hero_student_wellness.jpg")
    ]
    for sp in sample_paths:
        if os.path.exists(sp):
            run_image_analysis(analyzer, sp)
    print("[✓] Demonstration analysis complete.")

def run_webcam_mode(analyzer: OpenCVStressAnalyzer, cam_id: int = 0):
    """Runs live real-time OpenCV webcam tracker with HUD."""
    print(f"[*] Initializing camera device ID {cam_id}...")
    
    # Use DSHOW on Windows to prevent blocking
    backend = cv2.CAP_DSHOW if os.name == 'nt' else cv2.CAP_ANY
    cap = cv2.VideoCapture(cam_id, backend)

    if not cap.isOpened():
        print(f"[!] Could not open camera {cam_id}. Trying default backend...")
        cap = cv2.VideoCapture(cam_id)

    if not cap.isOpened():
        print("[!] No physical camera available or permission denied.")
        run_demo_mode(analyzer)
        return

    # Test reading 1 frame
    ret, test_frame = cap.read()
    if not ret or test_frame is None:
        print("[!] Camera did not return frames.")
        cap.release()
        run_demo_mode(analyzer)
        return

    window_name = "AmiCare - OpenCV Facial Stress & Emotion Detector"
    try:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 960, 640)
    except Exception as e:
        print(f"[!] GUI notice: {e}")

    prev_time = time.time()
    fps = 0.0
    last_log_time = 0

    print("[✓] Camera stream initialized! Examining facial stress in real-time...")

    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            curr_time = time.time()
            fps = 0.9 * fps + 0.1 * (1.0 / max(curr_time - prev_time, 1e-4))
            prev_time = curr_time

            result = analyzer.analyze_frame(frame)

            if result.get("annotated_image"):
                display_frame = analyzer.decode_image_from_base64(result["annotated_image"])
            else:
                display_frame = frame

            cv2.putText(display_frame, f"OpenCV FPS: {fps:.1f}", (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

            if curr_time - last_log_time > 3.0:
                last_log_time = curr_time
                if result.get("face_detected"):
                    print(f"[Live Scan] Emotion: {result['emotion']:<8} | Stress: {result['stress_score']:>2}% ({result['stress_level']:<6}) | Action: {result['suggested_action']}")
                else:
                    print("[Live Scan] Searching for face...")

            try:
                cv2.imshow(window_name, display_frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:
                    break
                elif key == ord('s'):
                    snap_file = os.path.join(SCRIPT_DIR, f"amicare_snap_{int(time.time())}.jpg")
                    cv2.imwrite(snap_file, display_frame)
                    print(f"[+] Saved snapshot to: {snap_file}")
            except Exception:
                pass
    finally:
        cap.release()
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass
        print("[*] Camera released.")

def main():
    parser = argparse.ArgumentParser(description="AmiCare OpenCV Facial Stress and Emotion Examination")
    parser.add_argument("--demo", action="store_true", help="Run demonstration on sample student photos")
    parser.add_argument("--image", type=str, help="Path to single image file to examine")
    parser.add_argument("--camera", type=int, default=0, help="Webcam device index (default: 0)")
    args = parser.parse_args()

    print_banner()
    analyzer = OpenCVStressAnalyzer()

    if args.demo:
        run_demo_mode(analyzer)
    elif args.image:
        run_image_analysis(analyzer, args.image)
    else:
        run_webcam_mode(analyzer, cam_id=args.camera)

if __name__ == "__main__":
    main()
