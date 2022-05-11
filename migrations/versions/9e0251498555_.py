"""empty message

Revision ID: 9e0251498555
Revises: 006b561f952a
Create Date: 2022-05-10 11:48:29.798547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e0251498555'
down_revision = '006b561f952a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('administrators', sa.Column('password', sa.String(length=255), nullable=False))
    op.add_column('approvers', sa.Column('password', sa.String(length=255), nullable=False))
    op.add_column('complainers', sa.Column('password', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('complainers', 'password')
    op.drop_column('approvers', 'password')
    op.drop_column('administrators', 'password')
    # ### end Alembic commands ###