"""setting table

Revision ID: b1553a4fb07
Revises: 1068cdc2fd76
Create Date: 2015-01-21 11:29:01.237722

"""

# revision identifiers, used by Alembic.
revision = 'b1553a4fb07'
down_revision = '1068cdc2fd76'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('setting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('value', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('setting')
    ### end Alembic commands ###
