"""empty message

Revision ID: 14e9ec1362c7
Revises: c167c8b0b3f2
Create Date: 2019-05-18 14:39:45.898173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14e9ec1362c7'
down_revision = 'c167c8b0b3f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('username', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'username')
    # ### end Alembic commands ###