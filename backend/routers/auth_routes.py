from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate,UserLogin,UserOut,Token
from auth import hash_password,verify_password,make_token,current_user,audit
router=APIRouter(prefix="/api/auth",tags=["Авторизация"])
@router.post("/register",response_model=UserOut,status_code=201)
def register(data:UserCreate,db:Session=Depends(get_db)):
    if db.query(User).filter((User.username==data.username)|(User.email==str(data.email))).first():
        raise HTTPException(409,"Логин или email уже зарегистрирован")
    u=User(username=data.username,email=str(data.email),password_hash=hash_password(data.password),role="Client")
    db.add(u);db.flush();audit(db,u,"REGISTER","User",u.id,"Регистрация клиента");db.commit();db.refresh(u)
    return u
@router.post("/login",response_model=Token)
def login(data:UserLogin,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.username==data.username).first()
    if not u or not verify_password(data.password,u.password_hash): raise HTTPException(401,"Неверный логин или пароль")
    audit(db,u,"LOGIN","User",u.id,"Успешный вход");db.commit()
    return Token(access_token=make_token(u),user=u)
@router.get("/me",response_model=UserOut)
def me(user:User=Depends(current_user)): return user
