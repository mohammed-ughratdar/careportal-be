import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid

care_type_enum = ENUM("stationary", "ambulatory", "day care", name="care_type", create_type=True)

facility_care_types = sa.Table(
    "facility_care_types",
    Base.metadata,
    sa.Column("facility_id", sa.UUID(as_uuid=True), sa.ForeignKey("facilities.id", ondelete="CASCADE"), primary_key=True),
    sa.Column("care_type", care_type_enum, sa.ForeignKey("care_types.care_type"), primary_key=True),
)

class Facility(Base):
    __tablename__ = "facilities"

    id = sa.Column(sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    facility_name = sa.Column(sa.String(255), nullable=False)
    zip_code_start = sa.Column(sa.Integer, nullable=False)
    zip_code_end = sa.Column(sa.Integer, nullable=False)
    facility_zip_code = sa.Column(sa.Integer, nullable=False)
    capacity = sa.Column(sa.Integer, nullable=False)
    current_capacity = sa.Column(sa.Integer, nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, server_default=sa.func.now())

    care_types = relationship(
        "CareType",
        secondary=facility_care_types,
        back_populates="facilities",
    )

class CareType(Base):
    __tablename__ = "care_types"

    care_type = sa.Column(care_type_enum, primary_key=True)
    facilities = relationship("Facility", secondary=facility_care_types, back_populates="care_types")
