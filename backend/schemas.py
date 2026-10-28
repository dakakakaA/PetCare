from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

EntryType = Literal["feeding", "walk", "health", "grooming", "note", "vaccination"]

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; username: str; email: EmailStr; role: Literal["Client", "Admin"]; created_at: datetime
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
class AnimalBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    species: str = Field(min_length=1, max_length=50)
    breed: str = Field(default="", max_length=100)
    description: str = Field(default="", max_length=4000)
    care_tips: str = Field(default="", max_length=4000)
    is_active: bool = True
class AnimalCreate(AnimalBase): pass
class AnimalUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    species: str | None = Field(default=None, min_length=1, max_length=50)
    breed: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=4000)
    care_tips: str | None = Field(default=None, max_length=4000)
    is_active: bool | None = None
class AnimalOut(AnimalBase):
    model_config = ConfigDict(from_attributes=True)
    id: int; created_at: datetime
class PetBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    species: str = Field(min_length=1, max_length=50)
    breed: str = Field(default="", max_length=100)
    birth_date: date | None = None
    weight_grams: int | None = Field(default=None, ge=1, le=200000)
    notes: str = Field(default="", max_length=4000)
class PetCreate(PetBase): pass
class PetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    species: str | None = Field(default=None, min_length=1, max_length=50)
    breed: str | None = Field(default=None, max_length=100)
    birth_date: date | None = None
    weight_grams: int | None = Field(default=None, ge=1, le=200000)
    notes: str | None = Field(default=None, max_length=4000)
class PetOut(PetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int; owner_id: int; created_at: datetime
class CareBase(BaseModel):
    entry_type: EntryType
    title: str = Field(min_length=1, max_length=150)
    details: str = Field(default="", max_length=4000)
    entry_date: date
    completed: bool = False
class CareCreate(CareBase):
    pet_id: int
class CareUpdate(BaseModel):
    entry_type: EntryType | None = None
    title: str | None = Field(default=None, min_length=1, max_length=150)
    details: str | None = Field(default=None, max_length=4000)
    entry_date: date | None = None
    completed: bool | None = None
class CareOut(CareBase):
    model_config = ConfigDict(from_attributes=True)
    id: int; pet_id: int; created_at: datetime
class AuditOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; actor_id: int | None; actor_username: str; action: str; entity_type: str
    entity_id: int | None; details: str; created_at: datetime
