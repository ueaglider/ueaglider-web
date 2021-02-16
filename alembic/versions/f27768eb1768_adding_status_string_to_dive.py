"""adding status string to dive

Revision ID: f27768eb1768
Revises: 41b8cd9ae94f
Create Date: 2021-02-16 09:49:03.361339

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f27768eb1768'
down_revision = '41b8cd9ae94f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('DiveInfo', sa.Column('Status', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('DiveInfo', 'Status')
    # ### end Alembic commands ###