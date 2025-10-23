from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

# Définition des rôles possibles
class RoleEnum(str, enum.Enum):
    MEDECIN = "medecin"
    ADMIN = "admin"
    PATIENT = "patient"

# Schéma de base partagé
class UtilisateurSchema(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    role: Optional[str] ="medecin"  # par défaut "medecin"

# Schéma pour la création d'un utilisateur
class UtilisateurRequest(UtilisateurSchema):
    password: str

# Schéma pour la réponse API
class UtilisateurResponse(UtilisateurSchema):
    id: int

    class Config:
        from_attributes = True  # nécessaire pour convertir les objets SQLAlchemy en Pydantic

# Schéma pour la mise à jour (PATCH / PUT)
class UpdateUtilisateur(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    password: Optional[str] = None
