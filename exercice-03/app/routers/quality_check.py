"""Endpoints utilisés pour observer la différence public / protégé."""

from fastapi import APIRouter, Depends,HTTPException,status
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dependencies import require_roles
from app.schemas import UserResponse,Quality_checkCreate,Quality_checkOut
from app.models import Quality_check,User,Dataset

router = APIRouter(prefix="/quality-checks",tags=["Quality_checks"])
 #current_user : User = Depends(get_current_user),

@router.get("",response_model=list[Quality_checkOut])
def list_Quality_checks(db : Session=Depends(get_db)):
    query= select(Quality_check).order_by(Quality_check.id)
    result = db.scalars(query).all()
    return result

@router.get("/{id}", response_model=Quality_checkOut)
def select_Quality_check(id:int ,db: Session = Depends(get_db)) : 
    result = db.get(Quality_check, id)
    if result : 
        return result
    
    raise HTTPException(status_code=404, detail="Quality_check absente")

@router.post("",response_model=Quality_checkOut, status_code = 201,)
def create_Quality_check(item : Quality_checkCreate, current_user: User = Depends(
        require_roles("analyst","manager")), db: Session = Depends(get_db)) : 
    dataset_item = db.query(Dataset).filter(Dataset.id == item.dataset_id).first()
    
    if not dataset_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Échec du check : L'élément avec l'ID {item.dataset_id} n'existe pas dans les datasets."
        )
    new_item = Quality_check(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put("/{id}",response_model=Quality_checkOut)
def replace_Quality_check(id:int,item : Quality_checkCreate , current_user : User = Depends(require_roles("analyst","manager")), db: Session = Depends(get_db)) : 
    result = db.get(Quality_check, id)

    
    if not result : 
        raise HTTPException(status_code=404, detail="Quality_check absente")
    target_item = db.query(Dataset).filter(Dataset.id == item.dataset_id).first()
            
    if not target_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Échec du check : L'élément avec l'ID {item.dataset_id_id} n'existe pas dans les datasets."
        )
    for key,value in item.model_dump().items() : 
        setattr(result, key, value)
    
    db.commit()
    db.refresh(result)
    return result


@router.delete("/{id}",response_model=Quality_checkOut)
def del_Quality_check(id:int, current_user : User = Depends(require_roles("manager")), db: Session = Depends(get_db)) : 
    result = db.get(Quality_check, id)
    if not result : 
        raise HTTPException(status_code=404, detail="Quality_check absente")
    db.delete(result)
    db.commit()
    return result