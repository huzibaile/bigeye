"""Add email column to users table

Revision ID: ab86865c4202
Revises: 
Create Date: 2023-04-24 01:46:19.040985

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ab86865c4202'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rw_records')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rw_records',
                    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('faction_id', mysql.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('faction_name', mysql.VARCHAR(length=50), nullable=False),
                    sa.Column('enemy_faction_id', mysql.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('enemy_faction_name', mysql.VARCHAR(length=50), nullable=False),
                    sa.Column('start_time', mysql.DATETIME(), nullable=False),
                    sa.Column('end_time', mysql.DATETIME(), nullable=True),
                    sa.Column('is_ended', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_0900_ai_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB'
                    )
    # ### end Alembic commands ###
