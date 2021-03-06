"""empty message

Revision ID: 4556940b26f5
Revises: 
Create Date: 2022-01-09 06:34:35.776109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4556940b26f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=80), nullable=True),
    sa.Column('abbreviation', sa.String(length=80), nullable=True),
    sa.Column('nickname', sa.String(length=80), nullable=True),
    sa.Column('city', sa.String(length=80), nullable=True),
    sa.Column('logo', sa.String(length=400), nullable=True),
    sa.Column('conf_name', sa.String(length=80), nullable=True),
    sa.Column('div_name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstName', sa.String(length=80), nullable=True),
    sa.Column('lastName', sa.String(length=80), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('country', sa.String(length=80), nullable=True),
    sa.Column('college', sa.String(length=80), nullable=True),
    sa.Column('years_pro', sa.String(length=80), nullable=True),
    sa.Column('position', sa.String(length=80), nullable=True),
    sa.Column('jersey', sa.String(length=80), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player')
    op.drop_table('user')
    op.drop_table('team')
    # ### end Alembic commands ###
