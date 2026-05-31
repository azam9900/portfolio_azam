"""Initial tables

Revision ID: 001_initial
Revises:
Create Date: 2026-05-26
"""
from alembic import op
import sqlalchemy as sa

revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Users table
    op.create_table(
        'users',
        sa.Column('id',         sa.Integer(),     primary_key=True, index=True),
        sa.Column('name',       sa.String(100),   nullable=False),
        sa.Column('email',      sa.String(255),   nullable=False, unique=True, index=True),
        sa.Column('password',   sa.String(255),   nullable=False),
        sa.Column('is_active',  sa.Boolean(),     default=True),
        sa.Column('is_admin',   sa.Boolean(),     default=False),
        sa.Column('created_at', sa.DateTime(),    nullable=True),
        sa.Column('updated_at', sa.DateTime(),    nullable=True),
    )

    # Projects table
    op.create_table(
        'projects',
        sa.Column('id',          sa.Integer(),    primary_key=True, index=True),
        sa.Column('number',      sa.String(5),    nullable=True),
        sa.Column('name',        sa.String(200),  nullable=False),
        sa.Column('description', sa.Text(),       nullable=False),
        sa.Column('stack',       sa.JSON(),       nullable=True),
        sa.Column('link',        sa.String(500),  nullable=True),
        sa.Column('link_label',  sa.String(50),   nullable=True),
        sa.Column('image_url',   sa.String(500),  nullable=True),
        sa.Column('featured',    sa.Boolean(),    default=False),
        sa.Column('is_active',   sa.Boolean(),    default=True),
        sa.Column('order',       sa.Integer(),    default=0),
        sa.Column('created_at',  sa.DateTime(),   nullable=True),
        sa.Column('updated_at',  sa.DateTime(),   nullable=True),
    )

    # Blog posts table
    op.create_table(
        'blog_posts',
        sa.Column('id',          sa.Integer(),    primary_key=True, index=True),
        sa.Column('title',       sa.String(300),  nullable=False),
        sa.Column('excerpt',     sa.Text(),       nullable=False),
        sa.Column('content',     sa.Text(),       nullable=True),
        sa.Column('category',    sa.String(100),  nullable=True),
        sa.Column('read_time',   sa.String(20),   nullable=True),
        sa.Column('slug',        sa.String(300),  nullable=False, unique=True, index=True),
        sa.Column('cover_image', sa.String(500),  nullable=True),
        sa.Column('published',   sa.Boolean(),    default=False),
        sa.Column('created_at',  sa.DateTime(),   nullable=True),
        sa.Column('updated_at',  sa.DateTime(),   nullable=True),
    )

    # Contact messages table
    op.create_table(
        'contact_messages',
        sa.Column('id',         sa.Integer(),    primary_key=True, index=True),
        sa.Column('name',       sa.String(100),  nullable=False),
        sa.Column('email',      sa.String(255),  nullable=False),
        sa.Column('subject',    sa.String(300),  nullable=False),
        sa.Column('message',    sa.Text(),       nullable=False),
        sa.Column('is_read',    sa.Boolean(),    default=False),
        sa.Column('created_at', sa.DateTime(),   nullable=True),
    )


def downgrade():
    op.drop_table('contact_messages')
    op.drop_table('blog_posts')
    op.drop_table('projects')
    op.drop_table('users')
