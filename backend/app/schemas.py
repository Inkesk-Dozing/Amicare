from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class QuestionOption(BaseModel):
    label: str
    value: int

class QuestionSchema(BaseModel):
    id: int
    order_num: int
    prompt: str
    options: List[QuestionOption]

    class Config:
        from_attributes = True

class AnswerInput(BaseModel):
    question_id: int
    score: int  # 0 to 4

class EvaluationInput(BaseModel):
    answers: List[AnswerInput]

class HelplineSchema(BaseModel):
    id: int
    name: str
    number: str
    category: str
    description: Optional[str] = None
    hours: str
    is_toll_free: bool
    languages: str
    website: Optional[str] = None

    class Config:
        from_attributes = True

class ResourceSchema(BaseModel):
    id: int
    title: str
    category: str
    description: str
    action_type: str
    read_time: str
    content: Optional[str] = None

    class Config:
        from_attributes = True

class EvaluationResult(BaseModel):
    total_score: int
    max_score: int
    level: str  # Low, Moderate, Elevated
    summary: str
    recommendations: List[str]
    recommended_helplines: List[HelplineSchema]

class FaceScanRecordSchema(BaseModel):
    id: int
    session_id: str
    face_detected: bool
    emotion: Optional[str] = None
    state_label: Optional[str] = None
    stress_score: int
    stress_level: Optional[str] = None
    confidence: float
    forehead_tension_percent: Optional[float] = None
    brow_furrow_percent: Optional[float] = None
    smile_ratio: Optional[float] = None
    eye_alertness_percent: Optional[float] = None
    recommendation: Optional[str] = None
    suggested_action: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
