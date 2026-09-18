from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Helpline
from app.schemas import HelplineSchema

router = APIRouter(prefix="/api/helplines", tags=["Helplines"])

@router.get("", response_model=List[HelplineSchema])
def get_helplines(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search query in name or description"),
    db: Session = Depends(get_db)
):
    query = db.query(Helpline)
    if category:
        query = query.filter(Helpline.category.ilike(f"%{category}%"))
    if search:
        query = query.filter(
            (Helpline.name.ilike(f"%{search}%")) |
            (Helpline.description.ilike(f"%{search}%")) |
            (Helpline.languages.ilike(f"%{search}%"))
        )
    return query.all()

@router.get("/{helpline_id}", response_model=HelplineSchema)
def get_helpline_by_id(helpline_id: int, db: Session = Depends(get_db)):
    item = db.query(Helpline).filter(Helpline.id == helpline_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Helpline not found")
    return item
