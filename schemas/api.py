from pydantic import BaseModel, Field
from typing import List, Optional

class SeanceIn(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=64, description="Identifiant unique de l'utilisateur")
    sport: str = Field(..., min_length=1, max_length=50, description="Sport pratiqué")
    duree_min: int = Field(..., gt=0, le=600, description="Durée de la séance en minutes")
    ressenti: str = Field(..., min_length=1, max_length=500, description="Ressenti de l'utilisateur après la séance")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "user_id": "alice42",
                "sport": "tennis",
                "duree_min": 15,
                "ressenti": "trop dur"
            }]
        }
    }

class SeanceOut(BaseModel):
    message: str = Field(..., description="Message bienveillant à afficher à l'utilisateur, 2-3 phrases max")
    ton: str = Field(..., description="Ton utilisé par le coach (chaleureux, motivant, doux, alerte)")
    sentiment: str = Field(..., description="Sentiment global détecté dans le ressenti (positif, neutre, négatif)")
    signaux_faibles: List[str] = Field(..., description="Liste des signaux faibles détectés dans le ressenti")
    encouragement: Optional[str] = Field(..., description="Le point positif clé à retenir, en 1 phrase courte")
    session_count: int = Field(..., description="Nombre total de séances enregistrées pour cet utilisateur")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "message": "Bravo pour cette première séance ! C'est normal que ce soit difficile au début, l'important est d'avoir franchi le pas. N'hésite pas à réessayer bientôt, tu vas vite progresser ! 💪",
                "ton": "chaleureux",
                "sentiment": "negatif",
                "signaux_faibles": "douleur_physique, intensite_subjective_haute",
                "encouragement": "Tu as fait le plus dur en commençant, c'est déjà une victoire !",
                "session_count": 1
            }]
        }
    }