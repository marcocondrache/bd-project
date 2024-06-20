"""shipment history

Revision ID: f2be23abfab2
Revises: 58b09be75b2d
Create Date: 2024-06-15 16:11:59.907009

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f2be23abfab2'
down_revision = '58b09be75b2d'
branch_labels = None
depends_on = None

create_trigger_fun = """
CREATE OR REPLACE FUNCTION update_shipment_history()
    RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO shipment_history(shipment_id, status)
    VALUES (NEW.id, NEW.current_status);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

create_trigger = """
CREATE TRIGGER after_update_shipment_history
    AFTER INSERT OR UPDATE OF current_status ON shipments
    FOR EACH ROW EXECUTE FUNCTION update_shipment_history();
"""

drop_trigger = """
DROP TRIGGER after_update_shipment_history ON shipments;
"""

drop_trigger_fun = """
DROP FUNCTION update_shipment_history;
"""


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shipment_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('shipment_id', sa.Integer(), nullable=False),
    sa.Column('status', postgresql.ENUM(name='shipmentstatus', create_type=False), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['shipment_id'], ['shipments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.execute(create_trigger_fun)
    op.execute(create_trigger)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(drop_trigger)
    op.execute(drop_trigger_fun)

    op.drop_table('shipment_history')
    # ### end Alembic commands ###