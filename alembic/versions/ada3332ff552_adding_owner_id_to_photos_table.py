"""Adding owner_id to photos table

Revision ID: ada3332ff552
Revises: 4dd8b43fc939
Create Date: 2024-01-08 23:26:07.384626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ada3332ff552"
down_revision: Union[str, None] = "4dd8b43fc939"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("photos", sa.Column("owner_id", sa.String(), nullable=False))
    op.create_foreign_key(None, "photos", "users", ["owner_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "photos", type_="foreignkey")
    op.drop_column("photos", "owner_id")
    # ### end Alembic commands ###
