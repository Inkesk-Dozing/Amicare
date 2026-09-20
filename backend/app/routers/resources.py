from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Resource
from app.schemas import ResourceSchema

router = APIRouter(prefix="/api/resources", tags=["Resources"])

@router.get("", response_model=List[ResourceSchema])
def get_resources(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    query = db.query(Resource)
    if category:
        query = query.filter(Resource.category.ilike(f"%{category}%"))
    return query.all()

@router.get("/{resource_id}", response_model=ResourceSchema)
def get_resource_by_id(resource_id: int, db: Session = Depends(get_db)):
    item = db.query(Resource).filter(Resource.id == resource_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")
    return item
