from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session

from schema.utilisateur_schema import UtilisateurRequest, UtilisateurResponse
from services.utilisateurs_services import (
    creer_utilisateurs,
    verifier_user,
    create_access_token,
    decoded_token,
    recuperer_user_par_email
)
from databases.connection import get_db

routes = APIRouter(
    tags=["Utilisateurs"],
    prefix="/utilisateurs"
)

# Schéma d’authentification OAuth2
auth_scheme = OAuth2PasswordBearer(tokenUrl="utilisateurs/token")

# ------------------------------------------------------
# 🔐 Récupération de l'utilisateur courant depuis le token
# ------------------------------------------------------
def get_current_user(
    token: Annotated[str, Depends(auth_scheme)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = decoded_token(token=token, db=db)
    if user is None:
        raise credentials_exception
    
    return user

# ------------------------------------------------------
# 👤 Création d’un utilisateur (admin uniquement)
# ------------------------------------------------------
@routes.post("/", response_model=UtilisateurResponse)
def create_users(
    utilisateurs: UtilisateurRequest,
    db: Session = Depends(get_db),
    # current_user: Annotated[UtilisateurResponse, Depends(get_current_user)] = None
):
    
    return creer_utilisateurs(utilisateurs, db)

# ------------------------------------------------------
# 🔑 Authentification / génération de token
# ------------------------------------------------------
@routes.post("/token")
def login(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = verifier_user(db, request_form.username, request_form.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Génération du token JWT
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ------------------------------------------------------
# 📧 Récupération d'un utilisateur par email
# ------------------------------------------------------
@routes.get("/{email}", response_model=UtilisateurResponse)
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user: Annotated[UtilisateurResponse, Depends(get_current_user)] = None
):
    user = recuperer_user_par_email(email, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur avec l'email '{email}' introuvable"
        )

    return user
