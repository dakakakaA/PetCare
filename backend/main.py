import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base,engine,SessionLocal
from models import User,Animal
from auth import hash_password
from routers import auth_routes,animals,pets,care,admin

app=FastAPI(title="PetCare API",version="1.0.0",description="РЎРёСЃС‚РµРјР° СѓС‡С‘С‚Р° РґРѕРјР°С€РЅРёС… Р¶РёРІРѕС‚РЅС‹С…")
app.add_middleware(CORSMiddleware,allow_origins=os.getenv("CORS_ORIGINS","http://localhost:3000").split(","),allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
for r in [auth_routes.router,animals.router,pets.router,care.router,admin.router]:app.include_router(r)

def seed(db:Session):
    if not db.query(User).filter_by(username="client").first():
        db.add(User(username="client",email="client@example.com",password_hash=hash_password("client123"),role="Client"))
    if not db.query(User).filter_by(username="admin").first():
        db.add(User(username="admin",email="admin@example.com",password_hash=hash_password("admin123"),role="Admin"))
    if db.query(Animal).count()==0:
        db.add_all([
          Animal(name="РџРѕРјРµСЂР°РЅСЃРєРёР№ С€РїРёС†",species="РЎРѕР±Р°РєР°",breed="РџРѕРјРµСЂР°РЅСЃРєРёР№ С€РїРёС†",description="РќРµР±РѕР»СЊС€Р°СЏ Р°РєС‚РёРІРЅР°СЏ СЃРѕР±Р°РєР°-РєРѕРјРїР°РЅСЊРѕРЅ.",care_tips="Р РµРіСѓР»СЏСЂРЅРѕ РІС‹С‡С‘СЃС‹РІР°С‚СЊ, СЃР»РµРґРёС‚СЊ Р·Р° РІРµСЃРѕРј Рё РїР»Р°РЅРѕРІС‹РјРё РѕСЃРјРѕС‚СЂР°РјРё."),
          Animal(name="РўР°РєСЃР°",species="РЎРѕР±Р°РєР°",breed="РўР°РєСЃР°",description="Р›СЋР±РѕР·РЅР°С‚РµР»СЊРЅР°СЏ СЃРѕР±Р°РєР° СЃ РІС‹С‚СЏРЅСѓС‚С‹Рј РєРѕСЂРїСѓСЃРѕРј.",care_tips="РЎР»РµРґРёС‚СЊ Р·Р° РЅР°РіСЂСѓР·РєРѕР№ РЅР° СЃРїРёРЅСѓ Рё РёР·Р±РµРіР°С‚СЊ РїСЂС‹Р¶РєРѕРІ СЃ РІС‹СЃРѕС‚С‹."),
          Animal(name="Р‘СЂРёС‚Р°РЅСЃРєР°СЏ РєРѕСЂРѕС‚РєРѕС€С‘СЂСЃС‚РЅР°СЏ",species="РљРѕС€РєР°",breed="Р‘СЂРёС‚Р°РЅСЃРєР°СЏ РєРѕСЂРѕС‚РєРѕС€С‘СЂСЃС‚РЅР°СЏ",description="РЎРїРѕРєРѕР№РЅР°СЏ РєРѕС€РєР° СЃ РїР»РѕС‚РЅРѕР№ С€РµСЂСЃС‚СЊСЋ.",care_tips="Р’С‹С‡С‘СЃС‹РІР°РЅРёРµ, РёРіСЂС‹ Рё РєРѕРЅС‚СЂРѕР»СЊ РїРёС‚Р°РЅРёСЏ."),
          Animal(name="РњРµР№РЅ-РєСѓРЅ",species="РљРѕС€РєР°",breed="РњРµР№РЅ-РєСѓРЅ",description="РљСЂСѓРїРЅР°СЏ РґР»РёРЅРЅРѕС€С‘СЂСЃС‚РЅР°СЏ РєРѕС€РєР°.",care_tips="РЈС…РѕРґ Р·Р° С€РµСЂСЃС‚СЊСЋ, РєРѕРіС‚СЏРјРё Рё Р·СѓР±Р°РјРё."),
          Animal(name="Р’РѕР»РЅРёСЃС‚С‹Р№ РїРѕРїСѓРіР°Р№",species="РџС‚РёС†Р°",breed="Р’РѕР»РЅРёСЃС‚С‹Р№ РїРѕРїСѓРіР°Р№",description="РЎРѕС†РёР°Р»СЊРЅР°СЏ РЅРµР±РѕР»СЊС€Р°СЏ РїС‚РёС†Р°.",care_tips="Р‘РµР·РѕРїР°СЃРЅР°СЏ РєР»РµС‚РєР°, СЃРІРµР¶Р°СЏ РІРѕРґР° Рё РµР¶РµРґРЅРµРІРЅРѕРµ РІР·Р°РёРјРѕРґРµР№СЃС‚РІРёРµ."),
          Animal(name="РњРѕСЂСЃРєР°СЏ СЃРІРёРЅРєР°",species="Р“СЂС‹Р·СѓРЅ",breed="РњРѕСЂСЃРєР°СЏ СЃРІРёРЅРєР°",description="РЎРѕС†РёР°Р»СЊРЅС‹Р№ С‚СЂР°РІРѕСЏРґРЅС‹Р№ РіСЂС‹Р·СѓРЅ.",care_tips="РЎРµРЅРѕ РїРѕСЃС‚РѕСЏРЅРЅРѕ, РІРёС‚Р°РјРёРЅ C Рё РїСЂРѕСЃС‚РѕСЂРЅРѕРµ Р¶РёР»РёС‰Рµ.")])
    db.commit()
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:seed(db)
    finally:db.close()
@app.get("/api/health")
def health():return {"status":"ok","service":"petcare-api"}

