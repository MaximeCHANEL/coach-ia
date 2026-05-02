## Description du projet

Coach IA est une API REST de coaching sportif personnalisé, construite avec FastAPI et LangGraph.

Après chaque séance, l'utilisateur soumet son sport, sa durée et son ressenti. 
Le système analyse automatiquement le ressenti via un LLM (Mistral), détecte les signaux 
faibles (douleur, fatigue excessive...) et génère un message de coaching adapté au contexte.

## Lien vers le notebook

Lien : https://github.com/MaximeCHANEL/coach-ia/blob/main/TP_Coach_IA_Notebook.ipynb

## Lien vers le PowerPoint

Lien : https://github.com/MaximeCHANEL/coach-ia/blob/main/CHANEL_Maxime_B3_CDA_coachIA_analyse_notebook.pptx

## Instructions d'installation locale

1. Cloner le dépôt
```bash
git clone https://github.com/MaximeCHANEL/coach-ia.git
cd coach-ia
```

2. Créer et activer l'environnement virtuel
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Remplir les valeurs dans le fichier .env
```

5. Lancer l'application
```bash
python -m uvicorn main:app --reload --port 8000
```

6. Accéder à l'API
- Documentation Swagger : http://localhost:8000/docs
- Health check : http://localhost:8000/health

## URL de production Render

URL : https://coach-ia-vosinitiales.onrender.com/

## Variables d'environnement nécessaires

> **Note pédagogique** : La clé API est fournie ici uniquement dans le cadre de ce TP.  
> En production, ne jamais exposer une clé dans un dépôt public.

```
MISTRAL_API_KEY=PM9orSRIT3br1XmGNupKgIctBEpC2dwW
MISTRAL_MODEL=mistral-small-latest
DB_PATH=coach.db
APP_ENV=dev
```

## Comment lancer les tests

Tous les tests :
```bash
pytest -v
```

Tests unitaires rapides (sans appel LLM) :
```bash
pytest tests/test_router.py -v
```