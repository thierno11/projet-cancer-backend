from sqlalchemy import Column, Integer, String, DateTime, Boolean, func,Enum
from databases.connection import Base
from sqlalchemy.orm import Mapped, mapped_column
import enum

class RoleEnum(enum.Enum):
    MEDECIN = "medecin"
    ADMIN = "admin"
    PATIENT = "patient"

class Utilisateur(Base):
    __tablename__ = "Utilisateurs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="medecin")
    password: Mapped[str] = mapped_column(String(200), nullable=False)