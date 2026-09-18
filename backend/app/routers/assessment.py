import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Question, Helpline
from app.schemas import QuestionSchema, EvaluationInput, EvaluationResult
from app.assessment_logic import evaluate_stress_level

router = APIRouter(prefix="/api/assessment", tags=["Assessment"])

@router.get("/questions", response_model=List[QuestionSchema])
def get_assessment_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).order_by(Question.order_num.asc()).all()
    result = []
    for q in questions:
        opts = json.loads(q.options_json)
        result.append({
            "id": q.id,
            "order_num": q.order_num,
            "prompt": q.prompt,
            "options": opts
        })
    return result

@router.post("/evaluate", response_model=EvaluationResult)
def evaluate_assessment(payload: EvaluationInput, db: Session = Depends(get_db)):
    if not payload.answers:
        raise HTTPException(status_code=400, detail="No answers provided.")
    
    all_helplines = db.query(Helpline).all()
    evaluation = evaluate_stress_level(payload.answers, all_helplines)
    return evaluation
