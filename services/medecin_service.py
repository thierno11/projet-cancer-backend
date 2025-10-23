from schema.dignostic_schema import PatientRisque
from fastapi import HTTPException
from typing import Dict, Any


def calculer_score_risque(data: PatientRisque) -> float:
    """
    Calcule le score de risque basé sur les facteurs cliniques
    Score entre 0 et 100
    """
    score = 0.0

    # Facteurs d'âge (0-20 points)
    if data.age >= 50:
        score += 15
    elif data.age >= 40:
        score += 10
    elif data.age >= 30:
        score += 5

    # Antécédents familiaux (0-20 points)
    if data.antecedents_familiaux == 1:
        score += 20

    # Antécédents personnels (0-15 points)
    if data.antecedents_personnels == 1:
        score += 15

    # Nombre de biopsies (0-10 points)
    score += min(data.nombre_biopsies * 3, 10)

    # Âge des premières menstruations (0-5 points)
    if data.age_premieres_menstruations < 12:
        score += 5

    # Âge premier enfant et nombre d'enfants (0-8 points)
    if data.age_premier_enfant is None or data.age_premier_enfant > 30:
        score += 5
    if data.nombre_enfants == 0:
        score += 3

    # Statuts hormonaux (0-12 points)
    if data.statut_er == "positif":
        score += 4
    if data.statut_pr == "positif":
        score += 4
    if data.expression_her2 == "positif":
        score += 4

    # Résultats imagerie (0-10 points)
    if data.resultat_mammographie == "anormale":
        score += 5
    if data.resultat_echographie == "anormale":
        score += 5

    # Densité mammaire (0-8 points)
    densite_scores = {"A": 0, "B": 2, "C": 5, "D": 8}
    score += densite_scores.get(data.densite_mammaire, 0)

    # Mutation génétique (0-25 points - facteur majeur)
    if data.mutation_genetique == 1:
        score += 25

    # Facteurs de style de vie (0-10 points)
    if data.imc > 30:
        score += 3
    if data.tabagisme == 1:
        score += 3
    if data.consommation_alcool == 1:
        score += 2

    style_vie_scores = {"sain": 0, "modéré": 1, "à risque": 2}
    score += style_vie_scores.get(data.activite_physique, 0)

    return min(score, 100)


def determiner_categorie(score: float) -> str:
    """Détermine la catégorie de risque"""
    if score < 25:
        return "faible"
    elif score < 50:
        return "modere"
    elif score < 75:
        return "eleve"
    else:
        return "tres eleve"


def generer_recommandations(data: PatientRisque, categorie: str) -> Dict[str, str]:
    """Génère les recommandations cliniques personnalisées"""

    recommandations = []
    frequence = ""

    if categorie == "faible":
        recommandations.append("Dépistage standard recommandé")
        recommandations.append("Maintenir un mode de vie sain")
        frequence = "Mammographie tous les 2 ans à partir de 50 ans"

    elif categorie == "modere":
        recommandations.append("Dépistage renforcé recommandé")
        if data.imc > 30:
            recommandations.append("Réduction du poids conseillée")
        if data.tabagisme == 1:
            recommandations.append("Arrêt du tabac fortement recommandé")
        frequence = "Mammographie annuelle + échographie si nécessaire"

    elif categorie == "eleve":
        recommandations.append("Consultation spécialisée en oncologie recommandée")
        recommandations.append("IRM mammaire à considérer")
        if data.mutation_genetique == 1:
            recommandations.append("Conseil génétique recommandé")
        if data.resultat_mammographie == "anormale":
            recommandations.append("Suivi immédiat de l'anomalie détectée")
        frequence = "Mammographie + IRM tous les 6 mois"

    else:  # tres eleve
        recommandations.append("Consultation oncologique URGENTE")
        recommandations.append("Biopsie à envisager")
        if data.mutation_genetique == 1:
            recommandations.append("Discussion sur chirurgie prophylactique possible")
        recommandations.append("IRM et échographie complètes")
        frequence = "Suivi tous les 3-6 mois avec imagerie complète"

    return {
        "recommandation_clinique": " | ".join(recommandations),
        "frequence_surveillance": frequence
    }


def effectuer_dignostic(data: PatientRisque) -> Dict[str, Any]:
    """
    Effectue le diagnostic de risque de cancer du sein
    """
    print(data)