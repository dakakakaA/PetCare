from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from database import get_db
from models import AuditLog,User
from schemas import AuditOut
from auth import admin_user
router=APIRouter(prefix="/api/admin",tags=["Администрирование"])
@router.get("/audit",response_model=list[AuditOut])
def list_audit(limit:int=Query(100,ge=1,le=500),db:Session=Depends(get_db),user:User=Depends(admin_user)):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
