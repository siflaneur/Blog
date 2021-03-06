"""empty message

Revision ID: 5040227b3762
Revises: 
Create Date: 2017-09-15 15:48:24.645352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5040227b3762'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('slug', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('slug', sa.String(length=64), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('created_timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('created_timestamp', sa.DateTime(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('modified_timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('ip_address', sa.String(length=64), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('created_timestamp', sa.DateTime(), nullable=True),
    sa.Column('entry_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entry_id'], ['entries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entry_tags',
    sa.Column('tags_id', sa.Integer(), nullable=True),
    sa.Column('entries_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entries_id'], ['entries.id'], ),
    sa.ForeignKeyConstraint(['tags_id'], ['tags.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry_tags')
    op.drop_table('comments')
    op.drop_table('entries')
    op.drop_table('users')
    op.drop_table('tags')
    # ### end Alembic commands ###
