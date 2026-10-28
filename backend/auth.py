import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User, AuditLog

SECRET_KEY=os.getenv("SECRET_KEY","local-only-demo-secret-key-change-before-production-123456")
ALGORITHM="HS256"
TOKEN_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","720"))
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2=OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def hash_password(password:str)->str: return pwd.hash(password)
def verify_password(password:str, hashed:str)->bool: return pwd.verify(password,hashed)
def make_token(user:User)->str:
    expiry=datetime.now(timezone.utc)+timedelta(minutes=TOKEN_MINUTES)
    return jwt.encode({"sub":str(user.id),"username":user.username,"role":user.role,"exp":expiry},SECRET_KEY,algorithm=ALGORITHM)
def current_user(token:str=Depends(oauth2),db:Session=Depends(get_db))->User:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user=db.query(User).filter(User.id==int(payload["sub"])).first()
        if not user: raise ValueError()
        return user
    except (JWTError,ValueError,KeyError,TypeError):
        raise HTTPException(401,"Недействительный или истёкший токен",headers={"WWW-Authenticate":"Bearer"})
def admin_user(user:User=Depends(current_user))->User:
    if user.role!="Admin": raise HTTPException(403,"Доступ только для администратора")
    return user
def audit(db:Session,user:User|None,action:str,entity:str,entity_id:int|None=None,details:str=""):
    db.add(AuditLog(actor_id=user.id if user else None,actor_username=user.username if user else "system",
                    action=action,entity_type=entity,entity_id=entity_id,details=details[:4000]))
