"""Endpoints utilisés pour observer la différence public / protégé."""

from fastapi import APIRouter, Depends,HTTPException,status
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dependencies import require_roles
from app.schemas import UserResponse,RoleUpdateRequest
from app.models import User

router = APIRouter(prefix="/admin/users",tags=["Admin_users"])
 #current_user : User = Depends(get_current_user),
# response_model=list[UserResponse]
@router.get("",response_model=list[UserResponse])
def list_users( current_user : User = Depends(require_roles("manager")),db : Session=Depends(get_db)):
    query= select(User.id,User.username,User.role).order_by(User.id)
    result = db.execute(query).mappings().all()
    return result 



@router.patch("/{id}/role",response_model=UserResponse)
def change_role(id:int,role : RoleUpdateRequest, current_user : User = Depends(require_roles("manager")) , db: Session = Depends(get_db)) : 
    result = db.get(User, id)
    if not result : 
        raise HTTPException(status_code=404, detail="User absent")
    for key,value in role.model_dump().items() : 
        setattr(result, key, value)
    db.commit()
    db.refresh(result)
    return result

