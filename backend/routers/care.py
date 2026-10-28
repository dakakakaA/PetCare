from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import CareEntry,Pet,User
from schemas import CareCreate,CareUpdate,CareOut
from auth import current_user,audit
router=APIRouter(prefix="/api/care",tags=["Дневник ухода"])
def own_pet(db,pet_id,user_id):
    p=db.query(Pet).filter(Pet.id==pet_id,Pet.owner_id==user_id).first()
    if not p: raise HTTPException(404,"Питомец не найден или нет доступа")
    return p
@router.get("",response_model=list[CareOut])
def list_entries(pet_id:int|None=None,db:Session=Depends(get_db),user:User=Depends(current_user)):
    q=db.query(CareEntry).join(Pet).filter(Pet.owner_id==user.id)
    if pet_id is not None:q=q.filter(CareEntry.pet_id==pet_id)
    return q.order_by(CareEntry.entry_date.desc(),CareEntry.id.desc()).all()
@router.post("",response_model=CareOut,status_code=201)
def create_entry(data:CareCreate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    own_pet(db,data.pet_id,user.id);e=CareEntry(**data.model_dump());db.add(e);db.flush();audit(db,user,"CREATE","CareEntry",e.id,e.title);db.commit();db.refresh(e);return e
@router.patch("/{item_id}",response_model=CareOut)
def update_entry(item_id:int,data:CareUpdate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    e=db.query(CareEntry).join(Pet).filter(CareEntry.id==item_id,Pet.owner_id==user.id).first()
    if not e:raise HTTPException(404,"Запись не найдена")
    for k,v in data.model_dump(exclude_unset=True).items():setattr(e,k,v)
    audit(db,user,"UPDATE","CareEntry",e.id,e.title);db.commit();db.refresh(e);return e
@router.delete("/{item_id}",status_code=204)
def delete_entry(item_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    e=db.query(CareEntry).join(Pet).filter(CareEntry.id==item_id,Pet.owner_id==user.id).first()
    if not e:raise HTTPException(404,"Запись не найдена")
    audit(db,user,"DELETE","CareEntry",e.id,e.title);db.delete(e);db.commit()
