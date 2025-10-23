# services/utilisateur_service.py

from sqlalchemy.orm import Session
from schema.utilisateur_schema import UtilisateurRequest, UtilisateurResponse
from model.utilisateur_model import Utilisateur
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def creer_utilisateurs(request: UtilisateurRequest, db: Session):
    # Hacher le mot de passe
    hashed_password = get_password_hash(request.password)

    # Créer une instance ORM
    utilisateur = Utilisateur(
        nom=request.nom,
        prenom=request.prenom,
        email=request.email,
        password=hashed_password,
        role=request.role,
    )

    db.add(utilisateur)
    db.commit()
    db.refresh(utilisateur)

    return utilisateur


def recuperer_user_par_email(email: str, db: Session):
    utilisateur = db.query(Utilisateur).filter(Utilisateur.email == email).first()
    if not utilisateur:
        return None
    return utilisateur  # On peut aussi retourner UtilisateurResponse.model_validate(utilisateur)

def verifier_user(db: Session, username: str, password: str):
    user = recuperer_user_par_email(username, db)
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decoded_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return recuperer_user_par_email(username, db)
    except jwt.PyJWTError:
        return None

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

