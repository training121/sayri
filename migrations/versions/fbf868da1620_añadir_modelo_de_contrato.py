"""Añadir modelo de Contrato

Revision ID: fbf868da1620
Revises: 452546f6a83e
Create Date: 2025-03-22 21:36:50.955023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbf868da1620'
down_revision = '452546f6a83e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contrato',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_archivo', sa.String(length=255), nullable=False),
    sa.Column('archivo', sa.LargeBinary(), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contrato')
    # ### end Alembic commands ###
