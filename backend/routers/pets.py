from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Pet,User
from schemas import PetCreate,PetUpdate,PetOut
from auth import current_user,audit
router=APIRouter(prefix="/api/pets",tags=["Мои питомцы"])
@router.get("",response_model=list[PetOut])
def list_pets(db:Session=Depends(get_db),user:User=Depends(current_user)):
    return db.query(Pet).filter(Pet.owner_id==user.id).order_by(Pet.created_at.desc()).all()
@router.get("/{item_id}",response_model=PetOut)
def get_pet(item_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    p=db.query(Pet).filter(Pet.id==item_id,Pet.owner_id==user.id).first()
    if not p: raise HTTPException(404,"Питомец не найден")
    return p
@router.post("",response_model=PetOut,status_code=201)
def create_pet(data:PetCreate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    p=Pet(owner_id=user.id,**data.model_dump());db.add(p);db.flush();audit(db,user,"CREATE","Pet",p.id,p.name);db.commit();db.refresh(p);return p
@router.patch("/{item_id}",response_model=PetOut)
def update_pet(item_id:int,data:PetUpdate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    p=db.query(Pet).filter(Pet.id==item_id,Pet.owner_id==user.id).first()
    if not p: raise HTTPException(404,"Питомец не найден")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(p,k,v)
    audit(db,user,"UPDATE","Pet",p.id,p.name);db.commit();db.refresh(p);return p
@router.delete("/{item_id}",status_code=204)
def delete_pet(item_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    p=db.query(Pet).filter(Pet.id==item_id,Pet.owner_id==user.id).first()
    if not p: raise HTTPException(404,"Питомец не найден")
    audit(db,user,"DELETE","Pet",p.id,p.name);db.delete(p);db.commit()
