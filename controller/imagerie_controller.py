from fastapi import APIRouter, UploadFile, File
import services.imagerie_service as im

dignostic_router = APIRouter(prefix="/analyse",tags=["Analyse"])

@dignostic_router.post("/")
async def effectuer_analyse(image: UploadFile = File(...)):
    return await im.effectuer_analyse(image)