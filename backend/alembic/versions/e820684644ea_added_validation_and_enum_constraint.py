"""added validation and enum constraint

Revision ID: e820684644ea
Revises:
Create Date: 2024-04-16 18:13:37.806674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e820684644ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charging_station_types',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.Enum('TYPE_A', 'TYPE_B', 'TYPE_C', 'TYPE_D', 'TYPE_E', name='stationtypeenum'), nullable=True),
    sa.Column('plug_count', sa.Integer(), nullable=True),
    sa.Column('efficiency', sa.Float(), nullable=True),
    sa.Column('current_type', sa.Enum('AC', 'DC', name='currenttype'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_charging_station_types_name'), 'charging_station_types', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('charging_stations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('device_id', sa.UUID(), nullable=True),
    sa.Column('ip_address', sa.String(), nullable=True),
    sa.Column('firmware_version', sa.String(), nullable=True),
    sa.Column('type_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['charging_station_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('device_id'),
    sa.UniqueConstraint('ip_address')
    )
    op.create_index(op.f('ix_charging_stations_name'), 'charging_stations', ['name'], unique=False)
    op.create_table('connectors',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('priority', sa.Boolean(), nullable=True),
    sa.Column('charging_station_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['charging_station_id'], ['charging_stations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_connectors_name'), 'connectors', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_connectors_name'), table_name='connectors')
    op.drop_table('connectors')
    op.drop_index(op.f('ix_charging_stations_name'), table_name='charging_stations')
    op.drop_table('charging_stations')
    op.drop_table('users')
    op.drop_index(op.f('ix_charging_station_types_name'), table_name='charging_station_types')
    op.drop_table('charging_station_types')
    # ### end Alembic commands ###
