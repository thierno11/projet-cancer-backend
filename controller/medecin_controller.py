from fastapi import APIRouter, HTTPException, status
from schema.dignostic_schema import PatientRisque
import services.medecin_service as ms

medecin_router = APIRouter(prefix="/medecin", tags=["Diagnostic"])

@medecin_router.post(
    "/",
    summary="Effectuer un diagnostic de risque de cancer du sein",
    description="Analyse les données patient et calcule le risque de cancer avec recommandations personnalisées",
    response_description="Diagnostic complet avec score de risque et recommandations"
)
def effectuer_dignostic(data: PatientRisque):
    """
    Effectue un diagnostic de risque de cancer du sein basé sur :
    - Facteurs démographiques (âge, IMC)
    - Antécédents (familiaux, personnels)
    - Résultats d'examens (mammographie, échographie)
    - Biomarqueurs (ER, PR, HER2)
    - Facteurs génétiques
    - Mode de vie

    Retourne un score de risque, une catégorie et des recommandations cliniques.
    """
    try:
        return ms.effectuer_dignostic(data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur: {str(e)}"
        )