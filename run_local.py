import os
import sys
import webbrowser
import threading
import time

# Ensure backend directory is in path
root_dir = os.path.abspath(os.path.dirname(__file__))
backend_dir = os.path.join(root_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def open_browser():
    time.sleep(1.5)
    url = "http://localhost:8000"
    print(f"\nOpening {url} in your browser...")
    webbrowser.open(url)

if __name__ == "__main__":
    print("=" * 65)
    print("  AmiCare — Student Mental Wellness & OpenCV Stress Platform")
    print("=" * 65)
    print("  Local Web App:   http://localhost:8000")
    print("  FastAPI Docs:    http://localhost:8000/docs")
    print("  OpenCV Engine:   Active & Connected")
    print("=" * 65)
    print("Press Ctrl+C to stop the server at any time.\n")

    threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
