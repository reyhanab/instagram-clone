"""Added Room model and updated Message model

Revision ID: 5048d0bce572
Revises: 7e6c5e90ec4b
Create Date: 2022-12-06 18:40:23.921677

"""
from alembic import op
import sqlalchemy as sa

import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")


# revision identifiers, used by Alembic.
revision = '5048d0bce572'
down_revision = '7e6c5e90ec4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room_user',
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('room_id', 'user_id')
    )
    op.add_column('messages', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('messages', sa.Column('room_id', sa.Integer(), nullable=True))
    op.drop_constraint('recipient_id', 'messages', type_='foreignkey')
    op.drop_constraint('sender_id', 'messages', type_='foreignkey')
    op.create_foreign_key('fk_messages_users', 'messages', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_messages_rooms', 'messages', 'rooms', ['room_id'], ['id'])
    op.drop_column('messages', 'recipient_id')
    op.drop_column('messages', 'sender_id')
    # ### end Alembic commands ###
    op.execute(f"ALTER TABLE rooms SET SCHEMA {SCHEMA};")



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('sender_id', sa.INTEGER(), nullable=True))
    op.add_column('messages', sa.Column('recipient_id', sa.INTEGER(), nullable=True))
    op.drop_constraint('recipient_id', 'messages', type_='foreignkey')
    op.drop_constraint('sender_id', 'messages', type_='foreignkey')
    op.create_foreign_key('fk_messages_users', 'messages', 'users', ['sender_id'], ['id'])
    op.create_foreign_key('fk_messages_rooms', 'messages', 'users', ['recipient_id'], ['id'])
    op.drop_column('messages', 'room_id')
    op.drop_column('messages', 'user_id')
    op.drop_table('room_user')
    op.drop_table('rooms')
    # ### end Alembic commands ###
