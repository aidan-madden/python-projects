"""empty message

Revision ID: a550ab79978b
Revises: 4556940b26f5
Create Date: 2022-01-11 18:32:05.144459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a550ab79978b'
down_revision = '4556940b26f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player', sa.Column('h', sa.String(length=80), nullable=True))
    op.drop_column('player', 'height')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player', sa.Column('height', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('player', 'h')
    # ### end Alembic commands ###