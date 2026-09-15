from pydantic import BaseModel
from typing import List, Optional

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
