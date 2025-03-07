"""add foreign key to facilites_care_types

Revision ID: c9e060965917
Revises: cfea392b6bf1
Create Date: 2025-03-06 08:04:59.116099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c9e060965917'
down_revision: Union[str, None] = 'cfea392b6bf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add foreign key constraint to facility_care_types
    op.create_foreign_key(
        "fk_facility_care_types",
        "facility_care_types",
        "care_types",
        ["care_type"],
        ["care_type"],
    )

def downgrade():
    # Remove foreign key constraint
    op.drop_constraint("fk_facility_care_types", "facility_care_types", type_="foreignkey")