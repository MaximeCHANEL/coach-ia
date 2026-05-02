from .nodes import (
    EtatCoach,
    n_analyser,
    n_generer_alerte,
    n_generer_chaleureux,
    n_generer_doux,
    n_generer_motivant,
    n_sauvegarder,
    router_selon_contexte,
    n_recuperer_historique
)
from langgraph.graph import StateGraph, START, END

def build_graph():
    builder2 = StateGraph(EtatCoach)

    # Nœuds réutilisés de la v1
    builder2.add_node("recuperer_historique", n_recuperer_historique)
    builder2.add_node("analyser", n_analyser)

    # Nouveaux nœuds : un par ton
    builder2.add_node("generer_alerte", n_generer_alerte)
    builder2.add_node("generer_chaleureux", n_generer_chaleureux)
    builder2.add_node("generer_doux", n_generer_doux)
    builder2.add_node("generer_motivant", n_generer_motivant)
    builder2.add_node("sauvegarder", n_sauvegarder)

    # Arêtes
    builder2.add_edge(START, "recuperer_historique")
    builder2.add_edge("recuperer_historique", "analyser")

    #  ARÊTE CONDITIONNELLE : c'est ici que le routage opère
    builder2.add_conditional_edges(
        "analyser",
        router_selon_contexte,  # la fonction de routage
        {
            "generer_alerte": "generer_alerte",
            "generer_chaleureux": "generer_chaleureux",
            "generer_doux": "generer_doux",
            "generer_motivant": "generer_motivant"
        }
    )

    # Tous les générateurs convergent vers la sauvegarde
    for nom in ["generer_alerte", "generer_chaleureux", "generer_doux", "generer_motivant"]:
        builder2.add_edge(nom, "sauvegarder")

    builder2.add_edge("sauvegarder", END)

    return builder2.compile()