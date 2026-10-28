from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
from models import Animal,User
from schemas import AnimalCreate,AnimalUpdate,AnimalOut
from auth import current_user,admin_user,audit
router=APIRouter(prefix="/api/animals",tags=["Каталог"])
@router.get("",response_model=list[AnimalOut])
def list_animals(q:str=Query("",max_length=100),species:str="",db:Session=Depends(get_db),user:User=Depends(current_user)):
    query=db.query(Animal).filter(Animal.is_active.is_(True))
    if q:
        like=f"%{q}%";query=query.filter((Animal.name.ilike(like))|(Animal.breed.ilike(like))|(Animal.description.ilike(like)))
    if species: query=query.filter(Animal.species.ilike(species))
    return query.order_by(Animal.name).all()
@router.get("/{item_id}",response_model=AnimalOut)
def get_animal(item_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    a=db.query(Animal).filter(Animal.id==item_id,Animal.is_active.is_(True)).first()
    if not a: raise HTTPException(404,"Животное не найдено")
    return a
@router.post("",response_model=AnimalOut,status_code=201)
def create_animal(data:AnimalCreate,db:Session=Depends(get_db),user:User=Depends(admin_user)):
    a=Animal(**data.model_dump());db.add(a);db.flush();audit(db,user,"CREATE","Animal",a.id,a.name);db.commit();db.refresh(a);return a
@router.patch("/{item_id}",response_model=AnimalOut)
def update_animal(item_id:int,data:AnimalUpdate,db:Session=Depends(get_db),user:User=Depends(admin_user)):
    a=db.query(Animal).filter(Animal.id==item_id).first()
    if not a: raise HTTPException(404,"Животное не найдено")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(a,k,v)
    audit(db,user,"UPDATE","Animal",a.id,a.name);db.commit();db.refresh(a);return a
@router.delete("/{item_id}",status_code=204)
def delete_animal(item_id:int,db:Session=Depends(get_db),user:User=Depends(admin_user)):
    a=db.query(Animal).filter(Animal.id==item_id).first()
    if not a: raise HTTPException(404,"Животное не найдено")
    audit(db,user,"DELETE","Animal",a.id,a.name);db.delete(a);db.commit()
