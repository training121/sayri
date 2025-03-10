"""actualzacion

Revision ID: ac11d977349c
Revises: 
Create Date: 2025-03-09 20:28:37.001376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac11d977349c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grupo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cliente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('apellido', sa.String(length=100), nullable=False),
    sa.Column('dni', sa.String(length=15), nullable=False),
    sa.Column('celular', sa.String(length=20), nullable=False),
    sa.Column('operadora', sa.String(length=50), nullable=True),
    sa.Column('banco', sa.String(length=50), nullable=True),
    sa.Column('numero_cuenta', sa.String(length=50), nullable=True),
    sa.Column('fecha_registro', sa.DateTime(), nullable=True),
    sa.Column('grupo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['grupo_id'], ['grupo.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dni')
    )
    op.create_table('prestamogrupal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grupo_id', sa.Integer(), nullable=False),
    sa.Column('monto_total', sa.Float(), nullable=True),
    sa.Column('fecha_desembolso', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['grupo_id'], ['grupo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prestamoindividual',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prestamo_grupal_id', sa.Integer(), nullable=False),
    sa.Column('cliente_id', sa.Integer(), nullable=False),
    sa.Column('monto', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.ForeignKeyConstraint(['prestamo_grupal_id'], ['prestamogrupal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pago',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prestamo_individual_id', sa.Integer(), nullable=False),
    sa.Column('fecha_pago', sa.DateTime(), nullable=True),
    sa.Column('monto_pagado', sa.Float(), nullable=False),
    sa.Column('estado', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['prestamo_individual_id'], ['prestamoindividual.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pago')
    op.drop_table('prestamoindividual')
    op.drop_table('prestamogrupal')
    op.drop_table('cliente')
    op.drop_table('grupo')
    # ### end Alembic commands ###
