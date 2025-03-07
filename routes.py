import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.db.database import test_database_connection
from app.service.care_portal_service import match_facility

from app.schemas import UserInput, UserOutput

from app.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
def read_root():
    logger.info("For endpoint /, Defaulting to Careportal root endpoint...!")
    return {"message": "Defaulting to Careportal root endpoint...!"}


@router.get("/health")
def health_check():
    logger.debug("Health check endpoint called.")
    try:
        db_connection_successful = test_database_connection()
        if db_connection_successful:
            return {"Database": "successfully connected"}
        else:
            return { "Database": "unsuccess" }
    except Exception as e:
        logger.exception("Unexpected error during health check.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error during health check.",
        ) from e


@router.post("/api/v1/match-facility")
async def post_match_facility(
    user_input: UserInput,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserOutput:
    logger.info(f"/match-facility:_request_body: {user_input}")
    return await match_facility(session, user_input)

       