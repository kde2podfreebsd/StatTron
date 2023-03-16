"""empty message

Revision ID: aa76c6771dd1
Revises: 
Create Date: 2023-02-26 19:15:42.906737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa76c6771dd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_id', sa.String(), nullable=False),
    sa.Column('api_hash', sa.String(length=128), nullable=False),
    sa.Column('phone', sa.String(length=32), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('host', sa.String(length=32), nullable=True),
    sa.Column('port', sa.String(length=32), nullable=True),
    sa.Column('public_key', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account')
    # ### end Alembic commands ###