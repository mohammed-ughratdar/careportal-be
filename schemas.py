from typing import Optional

from pydantic import BaseModel, Field
from app.data_types import Type_of_Care


class UserInput(BaseModel):
    user_name: str
    type_of_care: str 
    user_zip_code: Optional[int] = Field(None, description="Required unless type_of_care is 'day_care'")

class FacilityResponse(BaseModel):

    facility_name: str
    zip_code_start: int
    zip_code_end:int
    facility_zip_code: int
  
class UserOutput(BaseModel):
    message: str
    facility: Optional[FacilityResponse]
   