"""Add Settings to Debt models

Revision ID: 72c20159d072
Revises: 635f9e72f61b
Create Date: 2024-09-24 13:56:40.098584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '72c20159d072'
down_revision: Union[str, None] = '635f9e72f61b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_debts_id', table_name='debts')
    op.drop_table('debts')
    op.drop_index('ix_settings_id', table_name='settings')
    op.drop_index('ix_settings_key', table_name='settings')
    op.drop_table('settings')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('settings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('key', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='settings_pkey')
    )
    op.create_index('ix_settings_key', 'settings', ['key'], unique=True)
    op.create_index('ix_settings_id', 'settings', ['id'], unique=False)
    op.create_table('debts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('debt_type', postgresql.ENUM('owed_to', 'owed_by', name='debttype'), autoincrement=False, nullable=False),
    sa.Column('person_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('due_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='debts_pkey')
    )
    op.create_index('ix_debts_id', 'debts', ['id'], unique=False)
    # ### end Alembic commands ###
