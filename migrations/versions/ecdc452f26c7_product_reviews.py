"""product reviews

Revision ID: ecdc452f26c7
Revises: 8a0ac983e5a3
Create Date: 2024-06-20 18:16:15.854149

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ecdc452f26c7'
down_revision = '8a0ac983e5a3'
branch_labels = None
depends_on = None


create_trigger_fun = """
CREATE OR REPLACE FUNCTION update_product_reviews_history()
    RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO product_review_history(product_review_id, rating, message)
    VALUES (NEW.id, NEW.current_rating, NEW.current_message);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

create_trigger = """
CREATE TRIGGER after_update_product_reviews_history
    AFTER INSERT OR UPDATE OF current_rating, current_message ON product_reviews
    FOR EACH ROW EXECUTE FUNCTION update_product_reviews_history();
"""

drop_trigger = """
DROP TRIGGER after_update_product_reviews_history ON product_reviews;
"""

drop_trigger_fun = """
DROP FUNCTION update_product_reviews_history;
"""


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders_report',
    sa.Column('buyer_order_id', sa.Integer(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('seller_order_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['buyer_id'], ['buyers.id'], ),
    sa.ForeignKeyConstraint(['buyer_order_id'], ['buyers_orders.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['sellers.id'], ),
    sa.ForeignKeyConstraint(['seller_order_id'], ['sellers_orders.id'], ),
    sa.PrimaryKeyConstraint('buyer_order_id', 'buyer_id', 'seller_order_id', 'seller_id')
    )
    with op.batch_alter_table('orders_report', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_orders_report_buyer_id'), ['buyer_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_orders_report_buyer_order_id'), ['buyer_order_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_orders_report_seller_id'), ['seller_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_orders_report_seller_order_id'), ['seller_order_id'], unique=False)

    op.create_table('product_reviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('guid', sa.UUID(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('seller_order_id', sa.Integer(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.Column('current_rating', sa.Integer(), nullable=False),
    sa.Column('current_message', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['buyers.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['seller_order_id'], ['sellers_orders.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('guid')
    )
    with op.batch_alter_table('product_reviews', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_product_reviews_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_product_reviews_seller_order_id'), ['seller_order_id'], unique=False)

    op.create_table('product_review_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_review_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['product_review_id'], ['product_reviews.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('product_review_history', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_product_review_history_id'), ['id'], unique=False)

    op.execute(create_trigger_fun)
    op.execute(create_trigger)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(drop_trigger)
    op.execute(drop_trigger_fun)

    with op.batch_alter_table('product_review_history', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_product_review_history_id'))

    op.drop_table('product_review_history')
    with op.batch_alter_table('product_reviews', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_product_reviews_seller_order_id'))
        batch_op.drop_index(batch_op.f('ix_product_reviews_id'))

    op.drop_table('product_reviews')
    with op.batch_alter_table('orders_report', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_orders_report_seller_order_id'))
        batch_op.drop_index(batch_op.f('ix_orders_report_seller_id'))
        batch_op.drop_index(batch_op.f('ix_orders_report_buyer_order_id'))
        batch_op.drop_index(batch_op.f('ix_orders_report_buyer_id'))

    op.drop_table('orders_report')
    # ### end Alembic commands ###