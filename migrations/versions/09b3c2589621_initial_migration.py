"""initial migration

Revision ID: 09b3c2589621
Revises: None
Create Date: 2016-09-26 16:40:03.940226

"""

# revision identifiers, used by Alembic.
revision = '09b3c2589621'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bed',
    sa.Column('file_location', sa.Text(length=64), nullable=False),
    sa.Column('label', sa.String(length=64), nullable=True),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.Column('user', sa.String(length=32), nullable=True),
    sa.Column('md5', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('file_location'),
    sa.UniqueConstraint('date'),
    sa.UniqueConstraint('label'),
    sa.UniqueConstraint('md5')
    )
    op.create_table('colocalization',
    sa.Column('file_location1', sa.String(length=64), nullable=False),
    sa.Column('file_location2', sa.String(length=64), nullable=False),
    sa.Column('method', sa.String(length=64), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['file_location1'], ['bed.file_location'], ),
    sa.ForeignKeyConstraint(['file_location2'], ['bed.file_location'], ),
    sa.PrimaryKeyConstraint('file_location1', 'file_location2', 'method')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('colocalization')
    op.drop_table('bed')
    ### end Alembic commands ###
