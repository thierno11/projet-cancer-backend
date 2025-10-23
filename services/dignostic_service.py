from sqlalchemy.orm import Session
from schema.dignostic_schema import RisqueMammaire

def effectuer_dignostic(data:RisqueMammaire):
    print(data)