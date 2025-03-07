from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.db.crud import find_facility_by_care_capacity
from app.data_types import Type_of_Care
from app.schemas import UserInput, UserOutput, FacilityResponse

async def match_facility(session: AsyncSession, user_input: UserInput) -> UserOutput:

    if user_input.type_of_care == Type_of_Care.DAY_CARE:
        return UserOutput(message="Facility not available", facility=None)

    facilities = await find_facility_by_care_capacity(session, user_input.type_of_care)

    if not facilities:
        return UserOutput(message="No facility available", facility=None)

    matched_facility = find_closest_facility(facilities, user_input.user_zip_code)

    if not matched_facility:
        return UserOutput(message="No facility available within range", facility=None)

    return UserOutput(message="Facility matched successfully", facility=matched_facility)

def find_closest_facility(facilities: List[FacilityResponse], user_zip_code: int) -> Optional[FacilityResponse]:
    
    in_range_facilities = [
        facility for facility in facilities
        if facility.zip_code_start <= user_zip_code <= facility.zip_code_end
    ]

    if in_range_facilities:
        return min(in_range_facilities, key=lambda f: abs(f.facility_zip_code - user_zip_code))

    closest_facility = min(facilities, key=lambda f: abs(f.facility_zip_code - user_zip_code))

    if abs(closest_facility.facility_zip_code - user_zip_code) > 3000:
        return None

    return closest_facility