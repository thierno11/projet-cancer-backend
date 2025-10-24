
from fastapi.middleware.cors import CORSMiddleware
from controller import utilisateur_controller,dignostic_controller,medecin_controller,imagerie_controller
from fastapi import FastAPI,Depends
from databases.connection import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(utilisateur_controller.routes)
app.include_router(dignostic_controller.dignostic_router)
app.include_router(medecin_controller.medecin_router)
app.include_router(imagerie_controller.analyse_router)




origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "https://projet-cancer-front.onrender.com"
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])