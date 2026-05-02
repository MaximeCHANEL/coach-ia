from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import *
from infra.database import *
from services.coach import *
from schemas.api import *
import logging
from infra.llm import get_llm

_llm = get_llm()
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("coach-api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Démarrage...")
    init_db()      # créer la table si pas encore là
    log.info("Base prête")
    yield
    log.info("Arrêt...")

app = FastAPI(
    title="Coach IA — API",
    description="API d'un coach sportif IA bienveillant.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en prod
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/seance", response_model=SeanceOut, tags=["coach"])
def poster_seance(seance: SeanceIn):
    try:
        result = traiter_seance(seance.user_id, seance.sport, seance.duree_min, seance.ressenti)
        logger.info(f"Séance traitée : user={seance.user_id}, sport={seance.sport}, duree={seance.duree_min}min")
        return result
    except Exception as e:
        logger.error(f"Erreur pour user={seance.user_id} : {e}")
        raise HTTPException(status_code=500, detail="Le coach est momentanément indisponible.")
    
@app.get("/health/llm")
def health_llm():
    try:
        result = _llm.invoke("ping")
        return {"status": "ok", "response": result.content}
    except Exception as e:
        logger.error(f"LLM indisponible : {e}")
        raise HTTPException(status_code=503, detail="LLM indisponible.")