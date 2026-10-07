"""Endpoints utilisés pour observer la différence public / protégé."""

from fastapi import APIRouter, Depends,HTTPException,status
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dependencies import require_roles
from app.schemas import UserResponse,DatasetCreate,DatasetOut
from app.models import Dataset,User

router = APIRouter(prefix="/Datasets",tags=["Datasets"])
 #current_user : User = Depends(get_current_user),

@router.get("",response_model=list[DatasetOut])
def list_Datasets(db : Session=Depends(get_db)):
    query= select(Dataset).order_by(Dataset.id).where(Dataset.is_public == True)
    result = db.scalars(query).all()
    return result

@router.get("/{id}", response_model=DatasetOut)
def select_Dataset(id:int ,db: Session = Depends(get_db)) : 
    result = db.get(Dataset, id)

    if result.is_public : 
        return result
    elif not result.is_public    :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Cette donnée n'est pas publique")
    
    raise HTTPException(status_code=404, detail="Dataset absente")

@router.post("",response_model=DatasetOut, status_code = 201,)
def create_Dataset(item : DatasetCreate, current_user: User = Depends(
        require_roles("manager")), db: Session = Depends(get_db)) : 
    new_item = Dataset(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put("/{id}",response_model=DatasetOut)
def replace_Dataset(id:int,item : DatasetCreate , current_user : User = Depends(require_roles("manager")), db: Session = Depends(get_db)) : 
    result = db.get(Dataset, id)
    if not result : 
        raise HTTPException(status_code=404, detail="Dataset absente")
    for key,value in item.model_dump().items() : 
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result


@router.delete("/{id}",response_model=DatasetOut)
def del_Dataset(id:int, current_user : User = Depends(require_roles("manager")), db: Session = Depends(get_db)) : 
    result = db.get(Dataset, id)
    if not result : 
        raise HTTPException(status_code=404, detail="Dataset absente")
    db.delete(result)
    db.commit()
    return result