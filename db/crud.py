import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List
from app.db.models import Facility, facility_care_types
from app.schemas import FacilityResponse

logger = logging.getLogger(__name__)

async def find_facility_by_care_capacity(session: AsyncSession, type_of_care: str) -> List[FacilityResponse]:
    stmt = (
        select(Facility)
        .join(facility_care_types, facility_care_types.c.facility_id == Facility.id)  # ✅ Fix join condition
        .where(
            facility_care_types.c.care_type == type_of_care,
            Facility.current_capacity < Facility.capacity
        )
    )

    result = await session.execute(stmt)
    facilities = result.scalars().all()

    return [FacilityResponse.model_validate(facility.__dict__) for facility in facilities]