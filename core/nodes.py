from typing import List, Optional, TypedDict
from infra.database import historique_utilisateur
from infra.llm import get_llm
from core.prompts import prompt_analyse as PROMPT_ANALYSE
from core.schemas import AnalyseRessenti
from .prompts import prompt_generation
from infra.database import enregistrer_seance

class EtatCoach(TypedDict, total=False):
    user_id: str
    sport: str
    duree_min: int
    ressenti: str
    historique: List[dict]
    sentiment: Optional[str]
    signaux_faibles: List[str]
    ton_impose: Optional[str]
    message_final: Optional[str]
    encouragement: Optional[str]

_llm = get_llm()
_chaine_analyse = PROMPT_ANALYSE | _llm.with_structured_output(AnalyseRessenti)

def n_recuperer_historique(state: EtatCoach) -> dict:
    """Charge les séances précédentes de l'utilisateur depuis SQLite."""
    hist = historique_utilisateur(state["user_id"], limite=5)
    print(f"   [historique] {len(hist)} séance(s) trouvée(s)")
    return {"historique": hist}

def n_analyser(state: EtatCoach) -> dict:
    """Analyse le ressenti via le LLM."""
    analyse = _chaine_analyse.invoke({"ressenti": state["ressenti"]})
    print(f"   [analyse] sentiment={analyse.sentiment}, signaux={analyse.signaux_faibles}")
    return {
        "sentiment": analyse.sentiment,
        "signaux_faibles": analyse.signaux_faibles
    }

def _generer_avec_ton(state: EtatCoach, ton: str) -> dict:
    if state.get("historique"):
        resume_hist = "\n".join(
            f"- {s['sport']} {s['duree_min']}min : {s['ressenti'][:80]}"
            for s in state["historique"][:3]
        )
    else:
        resume_hist = "Aucune séance précédente — c'est la PREMIÈRE !"

    prompt = prompt_generation(ton)
    chaine = prompt | _llm
    reponse = chaine.invoke({
        "sport": state["sport"],
        "duree": state["duree_min"],
        "ressenti": state["ressenti"],
        "signaux": ", ".join(state["signaux_faibles"]),
        "historique": resume_hist
    })
    return {
        "message_final": reponse.content,
        "ton_impose": ton
    }

def n_generer_alerte(state: EtatCoach) -> dict:
    return _generer_avec_ton(state, "alerte")

def n_generer_chaleureux(state: EtatCoach) -> dict:
    return _generer_avec_ton(state, "chaleureux")

def n_generer_doux(state: EtatCoach) -> dict:
    return _generer_avec_ton(state, "doux")

def n_generer_motivant(state: EtatCoach) -> dict:
    return _generer_avec_ton(state, "motivant")


def n_sauvegarder(state: EtatCoach) -> dict:
    """Sauvegarde la séance complète en base."""
    enregistrer_seance(
        user_id=state["user_id"],
        sport=state["sport"],
        duree_min=state["duree_min"],
        ressenti=state["ressenti"],
        sentiment=state["sentiment"],
        signaux=state["signaux_faibles"],
        ton=state["ton_impose"],
        message=state["message_final"]
    )
    print(f"   [sauvegarde] séance enregistrée pour {state['user_id']}")
    return {}

def router_selon_contexte(state: EtatCoach) -> str:

    signaux = state.get("signaux_faibles", [])

    # Priorité absolue : douleur physique
    if "douleur_physique" in signaux:
        return "generer_alerte"

    # Première séance ?
    if len(state.get("historique", [])) == 0:
        return "generer_chaleureux"

    # 3 dernières séances toutes négatives ?
    historique = state.get("historique", [])
    if len(historique) >= 3:
        derniers_sentiments = [s.get("sentiment") for s in historique[:3]]
        if all(s == "negatif" for s in derniers_sentiments):
            return "generer_doux"

    # Cas par défaut : motivant
    return "generer_motivant"