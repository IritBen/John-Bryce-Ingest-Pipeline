"""create trips table

Revision ID: 529b16ef165f
Revises: 
Create Date: 2026-07-22 19:14:12.352776
"""
from __future__ import annotations

from alembic import op

revision = '529b16ef165f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE Trips
               (
               trip_id text            PRIMARY KEY, 
               station_id text         NOT NULL, 
               started_at timestamptz  NOT NULL, 
               distance_m integer      NOT NULL 
               )
               """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE Trips
               """)
