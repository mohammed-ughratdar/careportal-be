"""create care types table

Revision ID: 8ca47ab88193
Revises: 76c1d3c43815
Create Date: 2025-03-06 07:47:19.306497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8ca47ab88193'
down_revision: Union[str, None] = '76c1d3c43815'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    care_type_enum = postgresql.ENUM("stationary", "ambulatory", "day care", name="care_type", create_type=False)

    # Create care_types table
    op.create_table(
        "care_types",
        sa.Column("care_type", care_type_enum, primary_key=True),
    )

    # Create facility_care_types junction table
    op.create_table(
        "facility_care_types",
        sa.Column("facility_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("facilities.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("care_type", care_type_enum, primary_key=True),
    )


def downgrade():
    # Drop the junction table
    op.drop_table("facility_care_types")

    # Drop the care_types table
    op.drop_table("care_types")