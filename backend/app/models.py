from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from app.database import Base

class Helpline(Base):
    __tablename__ = "helplines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    number = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)  # 24/7 Crisis, Student Counseling, Peer Support, Tele-Therapy
    description = Column(Text, nullable=True)
    hours = Column(String(100), default="24/7")
    is_toll_free = Column(Boolean, default=True)
    languages = Column(String(255), default="English, Hindi")
    website = Column(String(255), nullable=True)

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # Mindfulness, Breathing, Exam Stress, Sleep
    description = Column(Text, nullable=False)
    action_type = Column(String(50), default="article")  # interactive, article, exercise
    read_time = Column(String(50), default="3 min")
    content = Column(Text, nullable=True)

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    order_num = Column(Integer, nullable=False)
    prompt = Column(Text, nullable=False)
    is_reverse_scored = Column(Boolean, default=False)
    options_json = Column(Text, nullable=False)  # JSON array of options
