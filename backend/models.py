from datetime import datetime, date
from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="Client")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")

class Animal(Base):
    __tablename__ = "animals"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    species: Mapped[str] = mapped_column(String(50), index=True)
    breed: Mapped[str] = mapped_column(String(100), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    care_tips: Mapped[str] = mapped_column(Text, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Pet(Base):
    __tablename__ = "pets"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    species: Mapped[str] = mapped_column(String(50))
    breed: Mapped[str] = mapped_column(String(100), default="")
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    weight_grams: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="pets")
    care_entries = relationship("CareEntry", back_populates="pet", cascade="all, delete-orphan")

class CareEntry(Base):
    __tablename__ = "care_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id", ondelete="CASCADE"), index=True)
    entry_type: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(150))
    details: Mapped[str] = mapped_column(Text, default="")
    entry_date: Mapped[date] = mapped_column(Date, default=date.today)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    pet = relationship("Pet", back_populates="care_entries")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actor_username: Mapped[str] = mapped_column(String(50), default="system")
    action: Mapped[str] = mapped_column(String(100))
    entity_type: Mapped[str] = mapped_column(String(80))
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
