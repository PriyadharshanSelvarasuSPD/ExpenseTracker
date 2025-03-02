"""Initial Migration

Revision ID: e144f83f1b45
Revises: 
Create Date: 2024-12-14 00:13:16.135880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e144f83f1b45"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "expense",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("expenseDescription", sa.String(length=500), nullable=False),
        sa.Column("typeOfExpense", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("expense")
    # ### end Alembic commands ###
