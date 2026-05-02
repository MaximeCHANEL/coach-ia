from core.nodes import router_selon_contexte

def test_douleur_declenche_alerte():
    state = {"signaux_faibles": ["douleur_physique"], "historique": []}
    assert router_selon_contexte(state) == "generer_alerte"

def test_premiere_seance_declenche_chaleureux():
    state = {"signaux_faibles": ["aucun"], "historique": []}
    assert router_selon_contexte(state) == "generer_chaleureux"

def test_3_seances_negatives_declenche_doux():
    state = {"signaux_faibles": ["aucun"], "historique": [{"sentiment":"negatif"}]*3}
    assert router_selon_contexte(state) == "generer_doux"

def test_cas_normal_declenche_motivant():
    state = {"signaux_faibles": ["aucun"], "historique": [{"sentiment":"positif"}]*2}
    assert router_selon_contexte(state) == "generer_motivant"

def test_douleur_prioritaire_premiere_seance():
    state = {"signaux_faibles": ["douleur_physique"], "historique": []}
    assert router_selon_contexte(state) == "generer_alerte"