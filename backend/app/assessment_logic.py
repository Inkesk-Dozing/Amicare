from typing import List, Dict, Tuple
from app.models import Helpline
from app.schemas import AnswerInput, HelplineSchema

def evaluate_stress_level(answers: List[AnswerInput], db_helplines: List[Helpline]) -> Dict:
    """
    Evaluates stress levels non-diagnostically based on PSS-4 standard scoring (0-16 range).
    """
    total_score = sum(ans.score for ans in answers)
    max_score = 16

    if total_score <= 5:
        level = "Low Stress"
        summary = "Your stress levels appear manageable right now. You are handling current demands well."
        recommendations = [
            "Maintain your healthy daily routines and consistent sleep schedule.",
            "Try our Box Breathing exercise for quick 2-minute relaxation micro-breaks.",
            "Keep up social connections and regular physical activity."
        ]
        # Filter top peer/student helpline
        helplines_matched = [h for h in db_helplines if "Student" in h.category or "Peer" in h.category][:2]
    elif total_score <= 10:
        level = "Moderate Stress"
        summary = "You are experiencing moderate stress. It is common during exam peaks or major life transitions, but taking proactive care is key."
        recommendations = [
            "Break large academic projects into smaller 25-minute focus intervals.",
            "Use the 4-7-8 Breathing Tool to reduce physical tension when overwhelmed.",
            "Consider reaching out to a campus counselor or trusted peer mentor for support."
        ]
        helplines_matched = [h for h in db_helplines if "Counseling" in h.category or "Tele-Therapy" in h.category][:3]
    else:
        level = "Elevated Stress"
        summary = "Your stress level is currently high. You don't have to carry this alone, and reaching out for support can make a big difference."
        recommendations = [
            "Pause demanding tasks and take immediate rest.",
            "Connect directly with one of our free 24/7 confidential helplines listed below.",
            "Talk to a healthcare provider or professional campus counselor as soon as possible."
        ]
        helplines_matched = [h for h in db_helplines if "24/7 Crisis" in h.category or "National" in h.category][:4]

    # Fallback if no specific helplines match filter
    if not helplines_matched:
        helplines_matched = db_helplines[:3]

    return {
        "total_score": total_score,
        "max_score": max_score,
        "level": level,
        "summary": summary,
        "recommendations": recommendations,
        "recommended_helplines": [HelplineSchema.model_validate(h) for h in helplines_matched]
    }
