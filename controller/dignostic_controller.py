from fastapi import APIRouter
from schema.dignostic_schema import RisqueMammaire
import services.dignostic_service as ds

dignostic_router = APIRouter(prefix="/diagnostic",tags=["Dignostic"])

@dignostic_router.post("/")
def effectuer_dignostic(data:RisqueMammaire):
    return ds.effectuer_dignostic(data)
    