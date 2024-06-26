"""carts tables

Revision ID: 77f303f91ee5
Revises: b1a5fc01696d
Create Date: 2024-05-01 18:03:49.401752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77f303f91ee5'
down_revision = 'b1a5fc01696d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('guid', sa.UUID(), nullable=False),
    sa.Column('owner_buyer_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'FINALIZED', name='cartstatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner_buyer_id'], ['buyers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('guid')
    )
    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_carts_id'), ['id'], unique=False)

    op.create_table('product_reservations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('product_sequence', sa.Integer(), nullable=False),
    sa.Column('current_quantity', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['cart_id'], ['carts.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('product_reservations', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_product_reservations_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_reservations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_product_reservations_id'))

    op.drop_table('product_reservations')
    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_carts_id'))

    op.drop_table('carts')
    # ### end Alembic commands ###
