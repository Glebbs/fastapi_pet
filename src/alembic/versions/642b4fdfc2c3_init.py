"""init

Revision ID: 642b4fdfc2c3
Revises: 
Create Date: 2022-09-13 19:38:01.270390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '642b4fdfc2c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('parentId', sa.String(), nullable=True),
    sa.Column('type', sa.Enum('FILE', 'FOLDER', name='systemitemtype'), nullable=False),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parentId'], ['items.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    # ### end Alembic commands ###
