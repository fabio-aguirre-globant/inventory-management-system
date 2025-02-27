"""Corrección sin eliminar inventory ni movements

Revision ID: 557239522622
Revises: caee85aa0b98
Create Date: 2025-02-26 08:19:16.085494

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "557239522622"
down_revision: Union[str, None] = "caee85aa0b98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "inventory",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("store_id", sa.UUID(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("min_stock", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("inventory", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_inventory_id"), ["id"], unique=False)
        batch_op.create_index(batch_op.f("ix_inventory_product_id"), ["product_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_inventory_store_id"), ["store_id"], unique=False)

    op.create_table(
        "movements",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("source_store_id", sa.UUID(), nullable=True),
        sa.Column("target_store_id", sa.UUID(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("type", sa.Enum("IN", "OUT", "TRANSFER", name="movementtype"), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("movements", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_movements_id"), ["id"], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("movements", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_movements_id"))

    op.drop_table("movements")
    with op.batch_alter_table("inventory", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_inventory_store_id"))
        batch_op.drop_index(batch_op.f("ix_inventory_product_id"))
        batch_op.drop_index(batch_op.f("ix_inventory_id"))

    op.drop_table("inventory")
    # ### end Alembic commands ###
