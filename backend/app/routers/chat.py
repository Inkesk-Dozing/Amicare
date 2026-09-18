import re
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Helpline, Resource

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

class ChatMessageInput(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    history: Optional[List[Dict]] = []

class StateOfBeing(BaseModel):
    state_label: str       # e.g., "Acute Exam Anxiety", "Academic Burnout", "Emotional Exhaustion"
    severity: str          # "Mild", "Moderate", "Elevated"
    primary_emotion: str   # "Anxiety", "Fatigue", "Distress", "Manageable"
    confidence: str        # "High", "Medium"

class ChatResponse(BaseModel):
    reply: str
    inferred_state: StateOfBeing
    suggested_actions: List[str]
    cards: Optional[List[Dict]] = []

def analyze_user_state_of_being(full_text: str) -> StateOfBeing:
    """
    Analyzes student conversational dialogue to autonomously infer emotional state of being.
    """
    text = full_text.lower()

    # Crisis / Severe Emotional Strain
    if any(k in text for k in ["suicide", "kill myself", "want to die", "harm myself", "worthless", "hopeless", "can't go on"]):
        return StateOfBeing(
            state_label="Severe Emotional Distress",
            severity="Elevated",
            primary_emotion="Crisis",
            confidence="High"
        )

    # Acute Anxiety & Panic
    anxiety_score = sum(1 for k in ["anxious", "panic", "scared", "fear", "shaking", "heart rate", "overwhelmed", "nervous", "terrified"] if k in text)
    if anxiety_score >= 1:
        return StateOfBeing(
            state_label="Acute Exam & Performance Anxiety",
            severity="Elevated" if anxiety_score > 2 else "Moderate",
            primary_emotion="Anxiety",
            confidence="High" if anxiety_score > 1 else "Medium"
        )

    # Sleep Deprivation & Exhaustion
    sleep_score = sum(1 for k in ["sleep", "insomnia", "tired", "exhausted", "can't sleep", "awake all night", "fatigue"] if k in text)
    if sleep_score >= 1:
        return StateOfBeing(
            state_label="Sleep Deprivation & Mental Fatigue",
            severity="Moderate",
            primary_emotion="Fatigue",
            confidence="High"
        )

    # Academic Stress & Burnout
    academic_score = sum(1 for k in ["exam", "test", "study", "marks", "grades", "assignment", "deadline", "burnout", "procrastinat", "syllabus"] if k in text)
    if academic_score >= 1:
        return StateOfBeing(
            state_label="Academic Workload Strain",
            severity="Moderate" if academic_score > 1 else "Mild",
            primary_emotion="Stress",
            confidence="High"
        )

    # Low Mood / Loneliness
    sadness_score = sum(1 for k in ["sad", "depressed", "lonely", "alone", "crying", "isolated", "nobody"] if k in text)
    if sadness_score >= 1:
        return StateOfBeing(
            state_label="Social Isolation & Emotional Strain",
            severity="Moderate",
            primary_emotion="Distress",
            confidence="Medium"
        )

    # Default / Coping Well
    return StateOfBeing(
        state_label="Stable / Baseline Well-Being",
        severity="Low",
        primary_emotion="Manageable",
        confidence="Medium"
    )

@router.post("/message", response_model=ChatResponse)
def handle_chat_message(payload: ChatMessageInput, db: Session = Depends(get_db)):
    msg = payload.message.lower().strip()
    
    # Combine past history with current message to understand state evolution
    combined_context = msg
    if payload.history:
        past_user_texts = [h.get("text", "") for h in payload.history if h.get("sender") == "user"]
        combined_context = " ".join(past_user_texts[-3:]) + " " + msg

    # Infer State of Being from conversation
    state = analyze_user_state_of_being(combined_context)

    # Crisis Response
    if state.primary_emotion == "Crisis":
        helplines = db.query(Helpline).all()
        cards = [
            {"type": "helpline", "name": h.name, "number": h.number, "category": h.category, "description": h.description}
            for h in helplines[:3]
        ]
        return ChatResponse(
            reply="I hear how painful and overwhelming things feel right now. You matter, and you don't have to go through this alone. Please reach out immediately to a free, confidential 24/7 crisis helpline:",
            inferred_state=state,
            suggested_actions=["Call Tele-MANAS (14416)", "Call KIRAN (1800-599-0019)", "View All Helplines"],
            cards=cards
        )

    # Acute Anxiety Dialogue Flow
    elif state.primary_emotion == "Anxiety":
        reply = (
            "I notice signs of anxiety and physical tension in what you're sharing. "
            "When thoughts start racing before an exam, taking rhythmic breaths can help regulate your heart rate. "
            "How does your body feel right now — are you experiencing a fast heartbeat or muscle tightness?"
        )
        return ChatResponse(
            reply=reply,
            inferred_state=state,
            suggested_actions=["Guided Box Breathing", "5-4-3-2-1 Grounding Tool", "Start Stress Check"],
            cards=[]
        )

    # Sleep & Fatigue Dialogue Flow
    elif state.primary_emotion == "Fatigue":
        reply = (
            "It sounds like sleep deprivation is really draining your energy right now. "
            "When sleep is disrupted, even small tasks can feel twice as hard. "
            "Are racing thoughts keeping you awake at night, or is it late-night studying?"
        )
        return ChatResponse(
            reply=reply,
            inferred_state=state,
            suggested_actions=["Read Sleep Hygiene Guide", "Guided Box Breathing", "Start Stress Check"],
            cards=[]
        )

    # Academic Stress Flow
    elif state.primary_emotion == "Stress":
        reply = (
            "It sounds like you're carrying a significant academic workload. "
            "When deadlines pile up, breaking work into 25-minute focus intervals can restore control. "
            "What is the main assignment or exam worrying you most today?"
        )
        return ChatResponse(
            reply=reply,
            inferred_state=state,
            suggested_actions=["Start Stress Self-Check", "Guided Box Breathing", "Burnout Guide"],
            cards=[]
        )

    # Emotional Strain / Sadness Flow
    elif state.primary_emotion == "Distress":
        reply = (
            "Thank you for being open with me. It takes real courage to acknowledge when you're feeling down or lonely. "
            "Remember that what you're going through is valid, and support is always available. "
            "Would it help to talk more about what's on your mind, or connect with a peer support line?"
        )
        return ChatResponse(
            reply=reply,
            inferred_state=state,
            suggested_actions=["Find Student Helplines", "Start Stress Check", "5-4-3-2-1 Grounding Tool"],
            cards=[]
        )

    # General Warm Dialogue
    else:
        reply = (
            "I'm listening and glad you reached out today. "
            "As we chat, I continuously help reflect your stress level and mental state of being. "
            "How has your week been going overall?"
        )
        return ChatResponse(
            reply=reply,
            inferred_state=state,
            suggested_actions=["Start Stress Self-Check", "Find Emergency Helplines", "Guided Box Breathing"],
            cards=[]
        )
