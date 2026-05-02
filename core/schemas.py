from pydantic import BaseModel, Field
from typing import Literal, List

class AnalyseRessenti(BaseModel):
    """Analyse fine du ressenti d'une séance."""
    sentiment: Literal["positif", "neutre", "negatif"] = Field(
        description="sentiment global exprimé"
    )
    intensite_perçue: int = Field(
        description="Intensité de l'effort perçue par l'utilisateur, de 1 (très facile) à 10 (épuisant)",
        ge=1, le=10
    )
    signaux_faibles: List[Literal[
        "douleur_physique",
        "fatigue_excessive",
        "demotivation",
        "comparaison_negative",
        "intensite_subjective_haute",
        "aucun"
    ]] = Field(description="Liste des signaux faibles détectés. Mettre ['aucun'] si rien de notable.")
    mots_cles_alerte: List[str] = Field(
        description="Mots ou expressions du ressenti qui ont déclenché un signal (ex: 'mal au dos', 'je suis nul')"
    )

class ReponseCoach(BaseModel):
    """Réponse complète du coach après analyse d'une séance."""
    message: str = Field(description="Message bienveillant à afficher à l'utilisateur, 2-3 phrases max")
    ton: Literal["chaleureux", "motivant", "doux", "alerte"] = Field(description="Ton utilisé")
    encouragement_principal: str = Field(description="Le point positif clé à retenir, en 1 phrase courte")