# AmiCare — Student Stress Self-Assessment & Support Referral Platform

![AmiCare Web App](https://img.shields.io/badge/AmiCare-v1.0.0-0D9488?style=flat-square)
![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square)
![SDG](https://img.shields.io/badge/SDG_3-Good_Health_%26_Well--Being-4C9F38?style=flat-square)
![Institution](https://img.shields.io/badge/K.R._Mangalam_University-Red?style=flat-square)

**AmiCare** is a non-diagnostic digital student support platform built to encourage early self-assessment of stress, reduce hesitation in seeking help, and seamlessly connect students with reliable support resources and emergency crisis helplines.

> *"AmiCare does not provide medical support, but mental awareness and early guidance."*

---

## 👥 Project Team & Academic Credits

- **Institution**: K.R. Mangalam University (School of Engineering & Technology)
- **Faculty Mentor**: Dr. Pinky Kumari
- **Project Team Members**:
  - Harsh Dev Jha (Roll: 2501010168)
  - Ishan Rawat (Roll: 2501010153)
  - Hrijul Bharadwaj (Roll: 2501010096)
  - Akshay Kumar (Roll: 2501010033)
  - Anvesha Saxena (Roll: 2501010144)

---

## 📌 Problem Statement & Community Context

Students frequently face academic workload, examination anxiety, career uncertainty, and social pressure. When stress goes unnoticed, it can escalate from **Stress ➔ Anxiety ➔ Burnout ➔ Reduced Well-Being**.

### Key Barriers to Help-Seeking:
1. **Fear of Judgment & Stigma**: Hesitation to speak openly about mental strain.
2. **Lack of Awareness**: Unfamiliarity with available student counseling and crisis helplines.
3. **Difficulty Expressing Concerns**: Struggling to articulate emotional pressure.
4. **Delayed Support**: Accessing counseling only when issues become critical.

---

## 🎯 Objectives & SDG 3 Alignment

Aligned with **UN Sustainable Development Goal 3: Good Health & Well-Being**:

1. **Early Detection**: Identify signs of stress through simple self-assessment before escalation.
2. **Accessible Digital Support**: 24/7 student-friendly web application with non-judgmental interactions.
3. **Personalized Guidance**: Offer evidence-based coping strategies (Box Breathing, Grounding, Sleep Hygiene).
4. **Professional Helpline Referrals**: Connect high-risk cases directly to verified national and campus helplines (Tele-MANAS 14416, KIRAN 1800-599-0019, Vandrevala Foundation).

---

## 🔬 Assessment Frameworks Supported

AmiCare integrates standard non-diagnostic self-assessment frameworks:
- **PSS (Perceived Stress Scale)**: Evaluates academic and personal stress levels.
- **GAD-7 (Anxiety Screening Context)**: Evaluates nervousness and tension indicators.
- **PHQ-9 (Depression Screening Context)**: Evaluates low mood and energy trends.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Custom AmiCare Soothing CSS (Soft Teal `#0D9488`, Mint `#14B8A6`, Glassmorphism, Micro-animations)
- **Backend**: Python 3.13 / FastAPI, Virtual Environment (`.venv`), SQLite Database (`amicare.db`), SQLAlchemy ORM, Pydantic
- **Data Layer**: SQLite referral database featuring verified 24/7 national helplines and campus counseling lines


---

## 🚀 Execution Instructions

### Backend (Python Virtual Environment & FastAPI)
```powershell
# Navigate to backend
cd backend

# Virtual environment setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Seed SQLite database
python -m app.seed_data

# Launch FastAPI server
uvicorn app.main:app --reload --port 8000
```

### Frontend (React & Vite)
```powershell
# Navigate to frontend
cd frontend

# Start development server
npm run dev
```

Visit: `http://localhost:5173` | API Swagger Docs: `http://127.0.0.1:8000/docs`

---

## 📜 License
Licensed under Apache 2.0. See [LICENSE](file:///C:/Users/USER/Desktop/Extras/Amicare/LICENSE) for details.