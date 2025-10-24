
from pydantic import BaseModel, Field
from typing import Literal, Annotated,Optional

class RisqueMammaire(BaseModel):
    age: Annotated[int, Field(ge=25, le=85)]                          # Âge de la femme
    imc: Annotated[float, Field(ge=0)]                                # Indice de masse corporelle
    ant_familiaux: Literal["Oui", "Non"]                  # Antécédents familiaux de cancer du sein (0/1)
    ant_personnels: Literal["Oui", "Non"]                    # Antécédents personnels de pathologies mammaires (0/1)
    age_premieres_regles: Annotated[int, Field(ge=0, le=25)]          # Âge des premières menstruations
    age_premier_enfant: Optional[Annotated[int, Field(ge=12, le=50)]]  # Âge à la naissance du premier enfant
    nb_enfants: Annotated[int, Field(ge=0)]                           # Nombre total d'enfants
    tabac:  Literal["Non-fumeur", "Ex-fumeur", "Fumeur"]                         # Fume ou non (0/1)
    alcool: Literal["Occasionnelle", "Aucune", "Modérée","Élevée"]                         # Consomme régulièrement de l'alcool ou non (0/1)
    activite_physique: Literal["Modérée", "Légère", "Sédentaire","Intense"]            # Niveau d'activité physique


    class Config:
        from_attributes = True
        


class PatientRisque(BaseModel):
    age: Annotated[int, Field(ge=0, le=120)]                            # Âge du patient en années
    antecedents_familiaux:  Literal["Oui", "Non"]                                          # Présence d'antécédents familiaux de cancer du sein (oui/non)
    antecedents_personnels: Literal["Oui", "Non"]                                          # Antécédents personnels de tumeurs bénignes ou autres cancers
    nombre_biopsies: Annotated[int, Field(ge=0)]                        # Nombre total de biopsies effectuées
    age_premieres_menstruations: Annotated[int, Field(ge=0, le=25)]     # Âge lors des premières menstruations
    age_premier_enfant: Annotated[int, Field(ge=0, le=50)]              # Âge à la naissance du premier enfant
    nombre_enfants: Annotated[int, Field(ge=0)]                         # Nombre d'enfants biologiques
    statut_er: Literal["Positif", "Négatif"]                                                         # Statut des récepteurs d'œstrogènes (Positif/Négatif)
    statut_pr: Literal["Positif", "Négatif"]                                                       # Statut des récepteurs de progestérone (Positif/Négatif)
    expression_her2: Literal["Positif","Négatif"]                                                                                           # Résultat de la mammographie (classification BI-RADS)
    densite_mammaire: str                                               # Densité du tissu mammaire (Dense/Non dense)

    mutation_genetique: str                                             # Mutation génétique identifiée (BRCA1, BRCA2, TP53, etc.)
    imc: Annotated[float, Field(ge=0)]                                  # Indice de masse corporelle
    tabagisme: str                                                      # Habitude tabagique actuelle ou passée
    consommation_alcool: str                                            # Niveau de consommation d'alcool
    activite_physique: str                                              # Niveau d'activité physique hebdomadaire
    risque_5_10_ans_pourcent: Annotated[float, Field(ge=0, le=100)]    # Risque estimé (%) de développer un cancer dans 5-10 ans
    recommandation_clinique: str                                        # Recommandation médicale basée sur le profil
    frequence_surveillance: str                                         # Fréquence de surveillance recommandée
    categorie_risque: str                                               # Catégorie globale du risque (faible/modéré/élevé)

    class Config:
        from_attributes = True
