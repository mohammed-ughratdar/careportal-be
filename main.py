import logging
import sys

from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.settings import  LOG_LEVEL


logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],

)

logger = logging.getLogger(__name__)
logger.debug(f"Log level is set to {LOG_LEVEL}")
app = FastAPI(
    title="CareMates MVP",
    description="""
    CareMates Backend
    """,
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

