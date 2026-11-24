# AmiCare — Team Presentation Script & Project Walkthrough
### *Structured 5-Speaker Script Covering Every Aspect & Feature of AmiCare*

---

## 🎙️ Speaker 1: Problem Statement, Social Context & SDG 3 Alignment
**Assigned Speaker:** Harsh Dev Jha *(or Speaker 1: Introduction & Mission Lead)*  
**Word Count:** ~145 words  

> "Good morning, respected mentors and evaluators. Today, our team presents **AmiCare**, a digital campus mental well-being platform designed specifically for university students. During college life, students face intense academic pressure, overlapping assignment deadlines, exam anxiety, career uncertainty, and irregular sleep schedules. Unfortunately, over seventy percent of struggling students never seek help due to fear of social stigma, peer judgment, high therapy costs, and lack of privacy. 
> 
> AmiCare bridges this critical sub-clinical gap between suffering in silence and formal clinical therapy. Guided by **United Nations Sustainable Development Goal 3 (Good Health and Well-Being)**, our platform serves as a psychological first-aid haven. It is completely free, non-diagnostic, and built with a zero-friction privacy philosophy: students do not need to register, create accounts, or provide any personal information. Anyone can open the platform in incognito mode, reflect on their mental state, and access immediate guidance safely."

---

## 🎙️ Speaker 2: Conversational AI Companion & Emotional State Inference
**Assigned Speaker:** Ishan Rawat *(or Speaker 2: Conversational AI & NLP Lead)*  
**Word Count:** ~140 words  

> "Once a student enters AmiCare, our first interactive touchpoint is the **AmiCare AI Companion**, powered by our asynchronous FastAPI backend. Rather than acting as a generic automated chatbot, our companion is engineered with multi-turn sentiment analysis and contextual memory. As the student types naturally about their day, the system continuously analyzes linguistic markers and autonomously infers their emotional state of being—classifying it into categories like *Acute Exam Anxiety*, *Academic Workload Strain*, *Sleep Deprivation*, *Emotional Distress*, or *Stable Baseline*.
> 
> The interface displays a live state-of-being banner with clear severity badges: Low, Moderate, or Elevated. Most importantly, the companion has built-in ethical safety triggers. If a student mentions severe hopelessness, crisis, or self-harm keywords, the AI immediately de-escalates the conversation and automatically surfaces emergency referral cards for national 24/7 toll-free crisis lifelines such as Tele-MANAS, ensuring student safety is always prioritized."

---

## 🎙️ Speaker 3: Affective Computer Vision & OpenCV Face Wellness Scanner
**Assigned Speaker:** Akshay Kumar *(or Speaker 3: Computer Vision & Biometrics Lead)*  
**Word Count:** ~150 words  

> "A standout engineering innovation in AmiCare is our **Face Wellness Scan**, which introduces affective computing through OpenCV and deep learning. Students experiencing cognitive overload often find it difficult to express their emotions in text. Our computer vision pipeline integrates the lightweight **YuNet ONNX deep neural network** (`face_detection_yunet.onnx`) running on a 320x320 input size to detect five-point facial landmarks with high precision.
> 
> The engine examines physiological stress markers: it measures brow furrow and forehead tension by calculating Sobel horizontal gradients and Laplacian variance over the *corrugator supercilii* muscle, computes the smile valence ratio, and checks eye alertness. Synthesizing these metrics, it classifies the student into *Happy*, *Well & Balanced*, *Sad*, or *Stressed* with an estimated stress score from zero to one hundred percent. The scanner overlays a futuristic visual Heads-Up Display (HUD) and logs anonymized diagnostic telemetry into our SQLite database, all without saving raw user photographs."

---

## 🎙️ Speaker 4: Psychometric PSS-4 Self-Assessment & Somatic Relaxation Tools
**Assigned Speaker:** Hrijul Bharadwaj *(or Speaker 4: Psychometrics & Somatic Tools Lead)*  
**Word Count:** ~140 words  

> "In addition to conversational and biometric reflection, AmiCare incorporates standardized psychometric evaluation through the **Cohen Perceived Stress Scale (PSS-4)**. This validated, four-item questionnaire measures how unpredictable and overwhelming a student finds their life over the past month. Our backend implements custom reverse-scoring logic for resilience items and computes a calibrated stress index categorized into Low, Moderate, or Elevated stress tiers in under two minutes.
> 
> To provide immediate physiological relief, AmiCare features two evidence-based somatic relaxation modules. The **Guided Box Breathing Tool** utilizes a 4-4-4-4 rhythm—inhale, hold, exhale, hold—paired with smooth, hardware-accelerated CSS pulsating circle animations to activate the parasympathetic nervous system and reduce acute panic. Complementing this is our **5-4-3-2-1 Sensory Grounding Tool**, an interactive step-by-step exercise guiding students through sight, touch, sound, smell, and taste to pull racing minds back to present reality."

---

## 🎙️ Speaker 5: Verified Referral Database, System Architecture & Impact
**Assigned Speaker:** Anvesha Saxena *(or Speaker 5: System Architecture & Community Impact Lead)*  
**Word Count:** ~155 words  

> "Completing the AmiCare care cycle is our **Verified Helpline Referral Directory**. Through an optimized SQLite database (`amicare.db`) and SQLAlchemy ORM, we provide students with instant click-to-call links and one-click clipboard copying for verified 24/7 emergency services, including Government of India's **Tele-MANAS (`14416`)**, **KIRAN (`1800-599-0019`)**, and the **Vandrevala Foundation**. A prominent crisis dialler button remains permanently pinned in our navigation header on every screen.
> 
> Architecturally, AmiCare combines a modern React 18 single-page frontend using a soothing healthcare glassmorphism design system, an asynchronous Python 3.13 FastAPI backend, and an in-memory OpenCV processing pipeline. During our field validation across forty-five campus peers at K.R. Mangalam University, the platform achieved an outstanding **System Usability Scale (SUS) score of 86.4 out of 100**, logging over thirty-six community immersion hours. AmiCare turns small moments of student distress into meaningful steps toward mental well-being. Thank you."

---

## 📋 Summary Table for Quick Reference during Q&A / Viva

| Speaker | Primary Focus Area | Key Features & Technologies Covered | Word Count |
| :---: | :--- | :--- | :---: |
| **Speaker 1** | **Social Context & Mission** | Academic pressures, help-seeking stigma, UN SDG 3, Zero-login / Anonymity policy. | ~145 |
| **Speaker 2** | **Conversational Companion** | Multi-turn NLP sentiment inference, state-of-being banner, automated crisis escalation. | ~140 |
| **Speaker 3** | **OpenCV Face Wellness Scanner** | YuNet ONNX landmark model, forehead Sobel/Laplacian tension gradients, smile ratio, HUD. | ~150 |
| **Speaker 4** | **Psychometrics & Somatic Tools** | Cohen PSS-4 reverse scoring, 4-4-4-4 Box Breathing visualizer, 5-4-3-2-1 Sensory Grounding. | ~140 |
| **Speaker 5** | **Referrals, Architecture & Impact** | Tele-MANAS (14416), KIRAN, FastAPI + React + SQLite stack, SUS score (86.4), Field testing. | ~155 |
