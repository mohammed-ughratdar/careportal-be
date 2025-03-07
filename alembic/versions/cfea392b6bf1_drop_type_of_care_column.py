"""drop type_of_care column

Revision ID: cfea392b6bf1
Revises: 8ca47ab88193
Create Date: 2025-03-06 07:50:53.154854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cfea392b6bf1'
down_revision: Union[str, None] = '8ca47ab88193'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop type_of_care column from facilities
    op.drop_column("facilities", "type_of_care")

def downgrade():
    # Re-add type_of_care column (in case of rollback)
    care_type_enum = sa.Enum("stationary", "ambulatory", "day care", name="care_type", create_type=False)
    op.add_column("facilities", sa.Column("type_of_care", care_type_enum, nullable=False))