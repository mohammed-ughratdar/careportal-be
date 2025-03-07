"""update care type enum value

Revision ID: 76c1d3c43815
Revises: 242022cdddd4
Create Date: 2025-03-06 07:40:41.479955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '76c1d3c43815'
down_revision: Union[str, None] = '242022cdddd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


old_enum = postgresql.ENUM("stationary", "ambulatory", "day_care", name="care_type")
new_enum = postgresql.ENUM("stationary", "ambulatory", "day care", name="care_type_new")  # Temporary name

def upgrade():
    bind = op.get_bind()

    # Step 1: Create the new ENUM type
    new_enum.create(bind, checkfirst=True)

    # Step 2: Alter column to use the new ENUM type
    op.execute("ALTER TABLE facilities ALTER COLUMN type_of_care TYPE care_type_new USING type_of_care::text::care_type_new")

    # Step 3: Drop the old ENUM type
    op.execute("DROP TYPE care_type")

    # Step 4: Rename new ENUM to old name
    op.execute("ALTER TYPE care_type_new RENAME TO care_type")


def downgrade():
    bind = op.get_bind()

    # Step 1: Recreate the old ENUM type
    old_enum.create(bind, checkfirst=True)

    # Step 2: Change column back to the old ENUM type
    op.execute("ALTER TABLE facilities ALTER COLUMN type_of_care TYPE care_type USING type_of_care::text::care_type")

    # Step 3: Drop the new ENUM type
    op.execute("DROP TYPE care_type")

    # Step 4: Rename old ENUM back to `care_type`
    op.execute("ALTER TYPE care_type_new RENAME TO care_type")