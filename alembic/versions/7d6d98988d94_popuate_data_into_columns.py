"""popuate data into columns

Revision ID: 7d6d98988d94
Revises: c9e060965917
Create Date: 2025-03-06 08:07:33.862177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7d6d98988d94'
down_revision: Union[str, None] = 'c9e060965917'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()

    # 1️⃣ Populate `care_types`
    conn.execute(
        sa.text("""
            INSERT INTO care_types (care_type) VALUES 
            ('stationary'::care_type), ('ambulatory'::care_type), ('day care'::care_type)
        """)
    )

    # 2️⃣ Populate `facilities`
    conn.execute(
        sa.text("""
            INSERT INTO facilities (facility_name, zip_code_start, zip_code_end, facility_zip_code, capacity, current_capacity)
            VALUES
            ('A', 10000, 14999, 12000, 100, 100),
            ('B', 15000, 19999, 17000, 100, 50),
            ('C', 20000, 24999, 22000, 80, 80),
            ('D', 25000, 29999, 27000, 80, 40),
            ('E', 10000, 24999, 18000, 200, 100)
        """)
    )

    # 3️⃣ Populate `facility_care_types` (mapping facilities to care types)
    conn.execute(
        sa.text("""
            INSERT INTO facility_care_types (facility_id, care_type)
            SELECT id, 'stationary'::care_type FROM facilities WHERE facility_name IN ('A', 'B', 'E')
            UNION ALL
            SELECT id, 'ambulatory'::care_type FROM facilities WHERE facility_name IN ('C', 'D', 'E')
        """)
    )

def downgrade():
    conn = op.get_bind()
    
    # Remove data in reverse order
    conn.execute(sa.text("DELETE FROM facility_care_types"))
    conn.execute(sa.text("DELETE FROM facilities"))
    conn.execute(sa.text("DELETE FROM care_types"))