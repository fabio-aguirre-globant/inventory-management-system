"""Recreating tables

Revision ID: e8fa6c1e6cc8
Revises: 6dfebb9d8078
Create Date: 2025-03-06 17:05:04.022111

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e8fa6c1e6cc8"
down_revision: Union[str, None] = "6dfebb9d8078"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "products",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("sku", sa.String(), nullable=False),
        sa.CheckConstraint("price > 0", name="check_price_positive"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sku"),
    )
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_products_id"), ["id"], unique=False)
        batch_op.create_index(batch_op.f("ix_products_name"), ["name"], unique=False)

    op.create_table(
        "inventory",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("store_id", sa.UUID(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("min_stock", sa.Integer(), nullable=False),
        sa.CheckConstraint("min_stock >= 0", name="check_min_stock_positive"),
        sa.CheckConstraint("quantity >= 0", name="check_quantity_positive"),
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
        sa.Column("timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("type", sa.Enum("IN", "OUT", "TRANSFER", name="movementtype"), nullable=False),
        sa.CheckConstraint("quantity > 0", name="check_quantity_positive"),
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
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_products_name"))
        batch_op.drop_index(batch_op.f("ix_products_id"))

    op.drop_table("products")
    # ### end Alembic commands ###
