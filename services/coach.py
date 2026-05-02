from core.graph import build_graph
from typing import List, Optional, TypedDict
from infra.database import compter_seances

_graphe = build_graph()

def traiter_seance(user_id: str, sport: str, duree_min: int, ressenti: str) -> dict:
    """Traite une nouvelle séance et renvoie la réponse du coach."""
    etat_initial = {
        "user_id": user_id,
        "sport": sport,
        "duree_min": duree_min,
        "ressenti": ressenti,
        "historique": [],
        "sentiment": None,
        "signaux_faibles": [],
        "ton_impose": None,
        "message_final": None,
        "encouragement": None
    }

    result = _graphe.invoke(etat_initial)

    return {
        "message": result["message_final"],
        "ton": result["ton_impose"],
        "sentiment": result["sentiment"],
        "signaux_faibles": result["signaux_faibles"],
        "encouragement": result["encouragement"],
        "session_count": compter_seances(user_id)
    }