"""

create_accesstokens_table

Revision ID: f9502679fea8
Creation date: 2023-08-17 17:44:18.744994

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "f9502679fea8"
down_revision = "4d8ff5bc488b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """--sql
        CREATE TABLE access_tokens(
            token UUID NOT NULL,
            user_id UUID NOT NULL,

            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(uid) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    op.execute(
        """--sql
        DROP TABLE access_tokens;
        """
    )
