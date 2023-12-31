"""empty message

Revision ID: a62a6c8f0fc0
Revises: ed099f3a3ff6
Create Date: 2023-06-11 20:11:43.303738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a62a6c8f0fc0'
down_revision = 'ed099f3a3ff6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planeta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('terrain', sa.String(length=250), nullable=False),
    sa.Column('climate', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planeta')
    # ### end Alembic commands ###
