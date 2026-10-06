"""Endpoints utilisés pour observer la différence public / protégé."""

from fastapi import APIRouter, Depends,HTTPException
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.models import User,Observation
from app.schemas import UserResponse,ObservationCreate,ObservationOut

router = APIRouter(prefix="/observations",tags=["Observations"])
 #current_user : User = Depends(get_current_user),

@router.get("",response_model=list[ObservationOut])
def list_observations(db : Session=Depends(get_db)):
    query= select(Observation).order_by(Observation.id)
    result = db.scalars(query).all()
    return result

@router.get("/{id}", response_model=ObservationOut)
def select_observation(id:int ,db: Session = Depends(get_db)) : 
    result = db.get(Observation, id)
    if result : 
        return result
    raise HTTPException(status_code=404, detail="Observation absente")

@router.post("",response_model=ObservationOut, status_code = 201)
def create_observation(item : ObservationCreate, current_user : User = Depends(get_current_user), db: Session = Depends(get_db)) : 
    new_item = Observation(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put("/{id}",response_model=ObservationOut)
def replace_observation(id:int,item : ObservationCreate , current_user : User = Depends(get_current_user), db: Session = Depends(get_db)) : 
    result = db.get(Observation, id)
    if not result : 
        raise HTTPException(status_code=404, detail="Observation absente")
    for key,value in item.model_dump().items() : 
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result


@router.delete("/{id}",response_model=ObservationOut)
def del_observation(id:int, current_user : User = Depends(get_current_user), db: Session = Depends(get_db)) : 
    result = db.get(Observation, id)
    if not result : 
        raise HTTPException(status_code=404, detail="Livre absent")
    db.delete(result)
    db.commit()
    return result