"""empty message

Revision ID: f191a88acaa8
Revises: 7c25decd9b9b
Create Date: 2023-04-24 17:35:56.637871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f191a88acaa8'
down_revision = '7c25decd9b9b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rw_records', sa.Column('score', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('respect', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('points', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('armor_cache', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('melee_cache', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('small_cache', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('medium_arms_cache', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('heavy_armor_cache', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('enemy_score', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('enemy_respect', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('enemy_points', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('enemy_armor_cache', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('enemy_melee_cache', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('enemy_small_cache', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('enemy_medium_arms_cache', sa.Integer(), nullable=False))
    op.add_column('rw_records', sa.Column('enemy_heavy_armor_cache', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rw_records', 'enemy_heavy_armor_cache')
    op.drop_column('rw_records', 'enemy_medium_arms_cache')
    op.drop_column('rw_records', 'enemy_small_cache')
    op.drop_column('rw_records', 'enemy_melee_cache')
    op.drop_column('rw_records', 'enemy_armor_cache')
    op.drop_column('rw_records', 'enemy_points')
    op.drop_column('rw_records', 'enemy_respect')
    op.drop_column('rw_records', 'enemy_score')
    op.drop_column('rw_records', 'heavy_armor_cache')
    op.drop_column('rw_records', 'medium_arms_cache')
    op.drop_column('rw_records', 'small_cache')
    op.drop_column('rw_records', 'melee_cache')
    op.drop_column('rw_records', 'armor_cache')
    op.drop_column('rw_records', 'points')
    op.drop_column('rw_records', 'respect')
    op.drop_column('rw_records', 'score')
    # ### end Alembic commands ###