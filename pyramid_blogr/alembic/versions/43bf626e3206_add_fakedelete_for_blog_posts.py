"""Add fakedelete for blog posts

Revision ID: 43bf626e3206
Revises: bfe66b7e698e
Create Date: 2016-03-08 19:08:24.069554

"""

# revision identifiers, used by Alembic.
revision = '43bf626e3206'
down_revision = 'bfe66b7e698e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entries', sa.Column('deleted', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('entries', 'deleted')
    ### end Alembic commands ###