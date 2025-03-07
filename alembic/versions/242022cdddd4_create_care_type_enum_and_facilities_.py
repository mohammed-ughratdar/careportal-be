"""create care_type enum and facilities table

Revision ID: 242022cdddd4
Revises: 
Create Date: 2025-03-04 09:59:03.915237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '242022cdddd4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "facilities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("facility_name", sa.String(255), nullable=False),
        sa.Column("type_of_care", sa.Enum("stationary", "ambulatory", "day_care", name="care_type"), nullable=False),
        sa.Column("zip_code_start", sa.Integer, nullable=False),
        sa.Column("zip_code_end", sa.Integer, nullable=False),
        sa.Column("facility_zip_code", sa.Integer, nullable=False),
        sa.Column("capacity", sa.Integer, nullable=False),
        sa.Column("current_capacity", sa.Integer, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade():
    op.drop_table("facilities")
    op.execute("DROP TYPE IF EXISTS care_type CASCADE;")
